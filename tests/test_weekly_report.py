"""Tests del reporte semanal de cliente."""

from datetime import date

from modules.intelligence import weekly_report


def _conversation(day, contact="…1234", depth=3, ad_id="ad1", from_ad=True):
    return {
        "first_at": f"{day}T12:00:00Z",
        "contact": contact,
        "depth": depth,
        "from_ad": from_ad,
        "ad_id": ad_id,
    }


def _provider(items):
    def provide(tenant_id, limit=1000):
        return {"tenant_id": tenant_id, "conversations": items}

    return provide


def _meta_metrics():
    return {
        "channels": {
            "facebook_organic": {
                "reach": None,
                "impressions": None,
                "interactions": 430,
                "clicks": 19,
                "status": "partial",
                "note": "Alcance e impresiones no disponibles en Graph v26.",
            },
            "facebook_paid": {
                "reach": 3376,
                "impressions": 5045,
                "clicks": 354,
                "spend": 116.85,
                "conversations": 20,
                "cost_per_conversation": 5.84,
                "status": "ok",
            },
            "instagram_organic": {
                "reach": None,
                "impressions": None,
                "interactions": 0,
                "status": "partial",
            },
            "instagram_paid": {
                "reach": 17,
                "impressions": 25,
                "clicks": 0,
                "spend": 0.69,
                "conversations": 0,
                "cost_per_conversation": None,
                "status": "ok",
            },
        }
    }


class TestWeekBounds:
    def test_returns_last_closed_sunday_to_saturday(self):
        start, end = weekly_report.week_bounds(date(2026, 11, 3))
        assert start == date(2026, 10, 25)
        assert end == date(2026, 10, 31)

    def test_monday_reference_still_returns_previous_week(self):
        start, end = weekly_report.week_bounds(date(2026, 11, 2))
        assert start == date(2026, 10, 25)
        assert end == date(2026, 10, 31)


class TestBuildWeekly:
    def test_counts_window_and_delta(self, tmp_path):
        provider = _provider(
            [
                _conversation("2026-10-25", contact="…1111"),
                _conversation("2026-10-28", contact="…2222"),
                _conversation("2026-10-31", contact="…3333", depth=1),
                _conversation("2026-10-20", contact="…4444"),
            ]
        )
        data = weekly_report.build_weekly(
            "flexi", date(2026, 11, 3), base_path=tmp_path, provider=provider
        )

        assert data["conversations"]["total"] == 3
        assert data["previous"]["total"] == 1
        assert data["delta"] == 2
        assert data["conversations"]["depth"]["1"] == 1

    def test_reads_publications_from_logs(self, tmp_path):
        tenant = tmp_path / "tenants" / "flexi"
        tenant.mkdir(parents=True)
        (tenant / "publication_log_week2.csv").write_text(
            "date,time,platform,piece,asset_filename,status,publication_id,published_at,reach,interactions,DMs,leads\n"
            "2026-10-29,10:00,Instagram,Post uno,a.jpg,published,1,,,,\n"
            "2026-11-02,10:00,Facebook,Post dos,b.jpg,scheduled,2,,,,\n",
            encoding="utf-8",
        )
        data = weekly_report.build_weekly(
            "flexi", date(2026, 11, 3), base_path=tmp_path, provider=_provider([])
        )

        assert [item["piece"] for item in data["publications"]] == ["Post uno"]

    def test_recommendations_capped_at_three(self, tmp_path):
        provider = _provider([_conversation("2026-10-28", contact="…9999", depth=1)])
        data = weekly_report.build_weekly(
            "flexi", date(2026, 11, 3), base_path=tmp_path, provider=provider
        )
        notes = weekly_report._recommendations(data, {"ad1": "Izadora"})

        assert len(notes) <= 3
        assert any("Izadora" in note for note in notes)

    def test_includes_channel_metrics_and_clean_piece_titles(self, tmp_path):
        tenant = tmp_path / "tenants" / "flexi"
        tenant.mkdir(parents=True)
        (tenant / "publication_log_week2.csv").write_text(
            "date,time,platform,piece,asset_filename,status,publication_id,published_at,reach,interactions,DMs,leads\n"
            '2026-10-28,10:00,Instagram,"Hay días que piden caminar sin prisa. 👟\nISAURA: una silueta limpia",a.jpg,published,1,,,,\n',
            encoding="utf-8",
        )
        data = weekly_report.build_weekly(
            "flexi",
            date(2026, 11, 3),
            base_path=tmp_path,
            provider=_provider([]),
            meta_metrics=_meta_metrics(),
        )
        report = weekly_report.render_weekly_md(data, {"ad1": "Izadora"})

        assert "| Facebook pauta | 3,376 | 5,045 | — | 354 | $116.85 | 20 | $5.84 |" in report
        assert "Hay días que piden caminar sin prisa. 👟" in report
        assert "ISAURA: una silueta limpia" not in report

    def test_recommendations_use_paid_platform_split(self, tmp_path):
        data = weekly_report.build_weekly(
            "flexi",
            date(2026, 11, 3),
            base_path=tmp_path,
            provider=_provider([]),
            meta_metrics=_meta_metrics(),
        )
        notes = weekly_report._recommendations(data, {"ad1": "Izadora"})

        assert any("Concentrar la pauta en Facebook" in note for note in notes)


class TestWrite:
    def test_writes_md_and_html(self, tmp_path):
        provider = _provider([_conversation("2026-10-28", contact="…1111")])
        data = weekly_report.build_weekly(
            "flexi", date(2026, 11, 3), base_path=tmp_path, provider=provider
        )
        md_path, html_path = weekly_report.write_weekly(data, tmp_path)

        assert md_path.name == "reporte_semanal_2026-10-25_2026-10-31.md"
        assert html_path.is_file()
        html = html_path.read_text(encoding="utf-8")
        assert "personas escribieron" in html
        assert "Recomendaciones" in html
        assert "Resultados por canal" in html
        assert "Facebook orgánico" in html
        assert "Instagram pauta" in html
