import csv
from pathlib import Path

path = Path('/home/ubuntu/universe-sent-me-growth-os/Operations/Research/Affiliate_Metrics_Snapshots.csv')
with path.open(newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    fields = reader.fieldnames
    excluded = {
        'MANUAL-20260820-7D-AGG',
        'MANUAL-20260818-DATE',
        'MANUAL-20260820-7D-REEL',
        'MANUAL-20260820-7D-AFF07',
    }
    rows = [row for row in reader if row['Snapshot_ID'] not in excluded]

rows.extend([
    {
        'Snapshot_ID': 'MANUAL-20260820-7D-AGG',
        'Capture_At_Local': '2026-08-20 20:51',
        'Cutoff_Start_Local': 'Últimos 7 días',
        'Campaign_ID': 'USM-HIST-FB-202608',
        'Link_ID': 'ML-FB-2026-08-04_18',
        'ML_Tag': 'Links de facebook - universesentme',
        'Platform': 'Facebook',
        'Surface': 'FACEBOOK_AGGREGATE_HISTORICAL',
        'Clicks': '1',
        'Units_Sold': '0',
        'Conversion_Rate': '0%',
        'Sales_Status': 'Sin ventas visibles',
        'Data_Quality': 'Manual_Screenshot',
        'Status': 'Recorded',
        'Source': 'Fernando screenshot',
        'Notes': 'Panel Métricas > Últimos 7 días; datos actualizados a las 20:51; etiqueta visible en tabla de seguimiento.',
    },
    {
        'Snapshot_ID': 'MANUAL-20260818-DATE',
        'Capture_At_Local': '2026-08-20',
        'Cutoff_Start_Local': '2026-08-18',
        'Cutoff_End_Local': '2026-08-18',
        'Campaign_ID': 'USM-AFF-FB20260818-30-P01',
        'ML_Tag': 'All visible tracking tags',
        'Platform': 'Facebook',
        'Surface': 'FACEBOOK_NATIVE_PRODUCT',
        'Clicks': '2',
        'Units_Sold': '0',
        'Conversion_Rate': '0%',
        'Sales_Status': 'Sin ventas visibles',
        'Data_Quality': 'Manual_Screenshot_Date_Tab',
        'Status': 'Recorded',
        'Source': 'Fernando screenshot',
        'Notes': 'Pestaña Fecha; 18/ago; 2 clics, 0 unidades, 0% conversión y $0 aumento estimado. Confirma el resumen de Últimos 7 días.',
    },
    {
        'Snapshot_ID': 'MANUAL-20260820-7D-REEL',
        'Capture_At_Local': '2026-08-20 20:51',
        'Cutoff_Start_Local': 'Últimos 7 días',
        'Campaign_ID': 'EXP-202608-REALUNIVERSE-01',
        'Link_ID': 'ML-FB-REALUNIVERSE-20260819-2210896633022235',
        'ML_Tag': 'usmfb20260819p01',
        'Platform': 'Facebook',
        'Surface': 'FACEBOOK_NATIVE_PRODUCT',
        'Content_ID': 'CON-2026-08-19-DobleCheck-Universe',
        'Meta_Post_ID': '1036844829507460_122153090559072582',
        'Reel_ID': '2210896633022235',
        'Sales_Status': 'No visible in table',
        'Data_Quality': 'Manual_Screenshot_Tag_Not_Visible',
        'Status': 'Not_Visible_No_Inference',
        'Source': 'Fernando screenshot',
        'Notes': 'La tabla visible solo muestra la etiqueta histórica y AFF-07; no se infiere que la etiqueta del Reel tenga 0 clics porque el panel puede ocultar filas sin actividad.',
    },
    {
        'Snapshot_ID': 'MANUAL-20260820-7D-AFF07',
        'Capture_At_Local': '2026-08-20 20:51',
        'Cutoff_Start_Local': 'Últimos 7 días',
        'Campaign_ID': 'USM-AFF-FB20260818-30-P01',
        'Link_ID': 'ML-FB-AFF07-260540',
        'ML_Tag': 'usmfb2605400826',
        'Platform': 'Facebook',
        'Surface': 'FACEBOOK_NATIVE_PRODUCT',
        'Content_ID': '260540',
        'Clicks': '1',
        'Units_Sold': '0',
        'Conversion_Rate': '0%',
        'Sales_Status': 'Sin ventas visibles',
        'Data_Quality': 'Manual_Screenshot',
        'Status': 'Recorded',
        'Source': 'Fernando screenshot',
        'Notes': 'AFF-07 / Elara / lámpara LED de lectura; panel Métricas > Últimos 7 días; datos actualizados a las 20:51.',
    },
])
with path.open('w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fields, lineterminator='\n')
    writer.writeheader()
    writer.writerows(rows)
print(f'rows={len(rows)}')
