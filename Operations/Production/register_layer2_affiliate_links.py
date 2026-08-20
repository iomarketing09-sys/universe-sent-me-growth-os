#!/usr/bin/env python3
from pathlib import Path
import csv

LEDGER = Path('/home/ubuntu/universe-sent-me-growth-os/Operations/Research/Affiliate_Link_Ledger.csv')

rows_to_add = [
    {
        'Campaign_ID': 'USM-AFF-FB-WINNERS-202608',
        'Link_ID': 'ML-FB-WIN-2608029-XHP360',
        'ML_Link_or_ID': 'https://meli.la/1bpVmJQ',
        'ML_Tag': 'usmwin2608029w0820',
        'Platform': 'Facebook',
        'Surface': 'FACEBOOK_NATIVE_PRODUCT',
        'Content_ID': '2608029',
        'Meta_Post_ID': '',
        'Reel_ID': '',
        'Character': 'Wilfred',
        'Product_Key': 'camp_lamp_xhp360_mlmu474178210',
        'Product_ID': 'MLMU474178210',
        'Product_Title': 'Lámpara Táctica Recargable Xhp360 Campismo Linterna Potente',
        'Product_URL': 'https://www.mercadolibre.com.mx/lampara-tactica-recargable-xhp360-campismo-linterna-potente/up/MLMU474178210',
        'Native_Product_Attachment_ID': '',
        'Native_Product_Attached_At': '',
        'Native_Product_Status': 'Not_Attached',
        'CTA': 'Producto nativo afiliado',
        'Created_Local': '2026-08-20',
        'Published_Local': '',
        'Approval_Status': 'Approved_Product_Not_Attached',
        'Publication_Status': 'Not_Requested',
        'Status': 'Link_Generated_Not_Attached',
        'Clicks': '',
        'Gross_Sales': '',
        'Approved_Sales': '',
        'Units_Sold': '',
        'Revenue_MXN': '',
        'Commission_MXN': '',
        'Confirmed_Commission_MXN': '',
        'Last_Click_At': '',
        'Metrics_Cutoff_Local': '',
        'Source': 'Fernando + Central de Afiliados Mercado Libre',
        'Notes': 'Producto y link aprobados para revisión final de adjunción. Link y etiqueta proporcionados por Fernando. No adjuntar a Facebook sin aprobación final explícita.'
    },
    {
        'Campaign_ID': 'USM-AFF-FB-WINNERS-202608',
        'Link_ID': 'ML-FB-WIN-CNT034-LEDNEON',
        'ML_Link_or_ID': 'https://meli.la/11cbTYc',
        'ML_Tag': 'usmwin260539ek0820',
        'Platform': 'Facebook',
        'Surface': 'FACEBOOK_NATIVE_PRODUCT',
        'Content_ID': 'CNT-034',
        'Meta_Post_ID': '',
        'Reel_ID': '',
        'Character': 'Evan+Kiri',
        'Product_Key': 'led_neon_5m_mlm3088935338',
        'Product_ID': 'MLM-3088935338',
        'Product_Title': 'Tiras de leds luz luces neón flexible manguera con fuente 5m',
        'Product_URL': 'https://articulo.mercadolibre.com.mx/MLM-3088935338-tiras-de-leds-luz-luces-neon-flexible-manguera-con-fuente-5m-_JM?searchVariation=184205480543',
        'Native_Product_Attachment_ID': '',
        'Native_Product_Attached_At': '',
        'Native_Product_Status': 'Not_Attached',
        'CTA': 'Producto nativo afiliado',
        'Created_Local': '2026-08-20',
        'Published_Local': '',
        'Approval_Status': 'Approved_Product_Not_Attached',
        'Publication_Status': 'Not_Requested',
        'Status': 'Link_Generated_Not_Attached',
        'Clicks': '',
        'Gross_Sales': '',
        'Approved_Sales': '',
        'Units_Sold': '',
        'Revenue_MXN': '',
        'Commission_MXN': '',
        'Confirmed_Commission_MXN': '',
        'Last_Click_At': '',
        'Metrics_Cutoff_Local': '',
        'Source': 'Fernando + Central de Afiliados Mercado Libre',
        'Notes': 'Producto y link aprobados para revisión final de adjunción. Link y etiqueta proporcionados por Fernando. No adjuntar a Facebook sin aprobación final explícita.'
    }
]

with LEDGER.open(newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    fieldnames = reader.fieldnames
    rows = list(reader)

existing = {r['Link_ID'] for r in rows}
for new_row in rows_to_add:
    if new_row['Link_ID'] not in existing:
        rows.append(new_row)

with LEDGER.open('w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator='\n')
    writer.writeheader()
    writer.writerows(rows)

print(f'rows={len(rows)} added={len([r for r in rows_to_add if r["Link_ID"] not in existing])}')
