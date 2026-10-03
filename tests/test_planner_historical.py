"""
Tests for the historical evidence integration in the planner.
"""
import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path
from growth.planner import build_schedule, ScheduleItem


class TestPlannerHistorical(unittest.TestCase):
    def setUp(self):
        # Sample dryrun slot for universe tenant
        self.universe_slot = {
            "slot_id": "universe-20260907-morning-01",
            "slot_type": "media",
            "date_local": "2026-09-07",
            "time_local": "08:30",
            "datetime_utc": "2026-09-07T13:30:00+00:00",
            "description": "Test post - Kael - Something",
            "source_filename": "123456 - Kael - Test.png",
            "asset_ref": "123456",
            "whatsapp_e164": None,
        }
        # Sample dryrun slot for another tenant
        self.other_slot = {
            "slot_id": "other-20260907-morning-01",
            "slot_type": "media",
            "date_local": "2026-09-07",
            "time_local": "08:30",
            "datetime_utc": "2026-09-07T13:30:00+00:00",
            "description": "Test post",
            "source_filename": "123456 - Other - Test.png",
            "asset_ref": "123456",
            "whatsapp_e164": None,
        }

    @patch('growth.planner.historical_baseline')
    def test_universe_tenant_gets_historical_evidence(self, mock_baseline):
        # Mock the historical_baseline functions to return known values
        mock_baseline.get_performance_by_personaje.return_value = [
            {"personaje": "Kael", "evidence_level": "confirmed_descriptive"}
        ]
        mock_baseline.get_signals_by_formato.return_value = [
            {"formato": "Kael (Lore/Identidad)", "evidence_level": "probable"}
        ]
        mock_baseline.load_horario_performance.return_value = [
            {"hour": 8, "posts": 2, "evidence_level": "confirmed_descriptive"}
        ]

        # Create a temporary dryrun file with the universe slot
        dryrun_path = Path("test_dryrun.json")
        dryrun_path.write_text('{"schedule": [%s]}' % self._slot_to_json(self.universe_slot))

        try:
            items = build_schedule(tenant_id="universe", source="dryrun", dryrun_path=dryrun_path)
            self.assertEqual(len(items), 1)
            item = items[0]
            self.assertIsInstance(item, ScheduleItem)
            self.assertIn('historical_evidence', item._meta)
            evidence = item._meta['historical_evidence']
            self.assertEqual(evidence['personaje'], "confirmed_descriptive")
            self.assertEqual(evidence['formato'], "probable")
            self.assertEqual(evidence['horario'], "confirmed_descriptive")
        finally:
            dryrun_path.unlink(missing_ok=True)

    @patch('growth.planner.historical_baseline')
    def test_other_tenant_gets_uncertain_evidence(self, mock_baseline):
        # Mock the historical_baseline functions to return known values (though they shouldn't be called for other tenants)
        mock_baseline.get_performance_by_personaje.return_value = []
        mock_baseline.get_signals_by_formato.return_value = []
        mock_baseline.load_horario_performance.return_value = []

        # Create a temporary dryrun file with the other slot
        dryrun_path = Path("test_dryrun.json")
        dryrun_path.write_text('{"schedule": [%s]}' % self._slot_to_json(self.other_slot))

        try:
            items = build_schedule(tenant_id="other", source="dryrun", dryrun_path=dryrun_path)
            self.assertEqual(len(items), 1)
            item = items[0]
            self.assertIsInstance(item, ScheduleItem)
            self.assertIn('historical_evidence', item._meta)
            evidence = item._meta['historical_evidence']
            # For non-universe tenants, we set everything to uncertain
            self.assertEqual(evidence['personaje'], "uncertain")
            self.assertEqual(evidence['formato'], "uncertain")
            self.assertEqual(evidence['horario'], "uncertain")
        finally:
            dryrun_path.unlink(missing_ok=True)

    def _slot_to_json(self, slot):
        # Convert a slot dict to a JSON string representation
        import json
        return json.dumps(slot)


if __name__ == '__main__':
    unittest.main()
