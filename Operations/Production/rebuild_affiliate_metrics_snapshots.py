import csv
from pathlib import Path

path = Path('/home/ubuntu/universe-sent-me-growth-os/Operations/Research/Affiliate_Metrics_Snapshots.csv')
fields = [
    'Snapshot_ID', 'Capture_At_Local', 'Cutoff_Start_Local', 'Cutoff_End_Local',
    'Campaign_ID', 'Link_ID', 'ML_Tag', 'Platform', 'Surface', 'Content_ID',
    'Meta_Post_ID', 'Reel_ID', 'Clicks', 'Gross_Sales', 'Approved_Sales',
    'Units_Sold', 'Revenue_MXN', 'Commission_MXN', 'Confirmed_Commission_MXN',
    'Conversion_Rate', 'Sales_Status', 'Data_Quality', 'Status', 'Source', 'Notes'
]
rows = [
    {
        'Snapshot_ID': 'HIST-20260804-18-001',
        'Capture_At_Local': '2026-08-19',
        'Cutoff_Start_Local': '2026-08-04',
        'Cutoff_End_Local': '2026-08-18',
        'Campaign_ID': 'USM-HIST-FB-202608',
        'Link_ID': 'ML-FB-2026-08-04_18',
        'ML_Tag': 'Links de facebook - universesentme',
        'Platform': 'Facebook',
        'Surface': 'FACEBOOK_AGGREGATE_HISTORICAL',
        'Clicks': '3', 'Gross_Sales': '2', 'Units_Sold': '2',
        'Revenue_MXN': '322.65', 'Commission_MXN': '28.84',
        'Conversion_Rate': '66.67%', 'Sales_Status': 'En revisión',
        'Data_Quality': 'Historical_Aggregate_No_Link_Granularity',
        'Status': 'Recorded', 'Source': 'Mercado Libre Metrics',
        'Notes': 'Aggregate historical signal; not attributable to a specific Facebook post or product; sales in review',
    },
    {
        'Snapshot_ID': 'EXP-202608-REALUNIVERSE-01',
        'Capture_At_Local': '2026-08-20',
        'Campaign_ID': 'EXP-202608-REALUNIVERSE-01',
        'Link_ID': 'ML-FB-REALUNIVERSE-20260819-2210896633022235',
        'ML_Tag': 'usmfb20260819p01',
        'Platform': 'Facebook',
        'Surface': 'FACEBOOK_NATIVE_PRODUCT',
        'Content_ID': 'CON-2026-08-19-DobleCheck-Universe',
        'Meta_Post_ID': '1036844829507460_122153090559072582',
        'Reel_ID': '2210896633022235',
        'Sales_Status': 'No capturado',
        'Data_Quality': 'Access_Blocked_MyBrowser_NotConnected',
        'Status': 'Capture_Blocked_MyBrowser_NotConnected',
        'Source': 'My Browser / session audit',
        'Notes': 'Panel not readable; isolated-browser login shown; no credentials entered or content modified',
    },
]
with path.open('w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fields, lineterminator='\n')
    writer.writeheader()
    writer.writerows(rows)
print(f'rows={len(rows)} columns={len(fields)}')
