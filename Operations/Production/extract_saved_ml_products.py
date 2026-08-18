import json
import re
from pathlib import Path

FILES = {
    "AFF-04": "/home/ubuntu/upload/listado.mercadolibre.com.mx_lampara-antorcha-led-recargable-usb_1787067406996.html",
    "AFF-05": "/home/ubuntu/upload/listado.mercadolibre.com.mx_soporte-taza-telefono-escritorio_1787065511684.html",
    "AFF-06": "/home/ubuntu/upload/listado.mercadolibre.com.mx_accesorios-celular-taza-escritorio_1787041118776.html",
}
TARGETS = {
    "AFF-04": ["Linterna Táctica Recargable 120000 Lúmenes Led Campismo", "Lámpara Táctica Recargable Campismo Linterna Potente", "Lámpara Led Recargable 200000lm Luz Blanca"],
    "AFF-05": ["Soporte ajustable para taza y teléfono 2 en 1", "Soporte ajustable para mesa, taza y teléfono", "Soporte para taza y teléfono 2 en 1"],
    "AFF-06": ["regalo", "rosa", "pareja"],
}

for aff, filename in FILES.items():
    path = Path(filename)
    text = path.read_text(errors="ignore")
    print(f"\n## {aff} :: {path.name}")
    found = []
    for match in re.finditer(r'"@type":"Product"', text):
        fragment = text[match.start():match.start() + 1800]
        name = re.search(r'"name":"(.*?)"', fragment)
        offer = re.search(r'"offers":\{"@type":"Offer".*?"price":([0-9.]+).*?"url":"(https?:\\/\\/www\\.mercadolibre\\.com\\.mx\\/.*?)"', fragment)
        if name and offer:
            title = name.group(1).encode().decode("unicode_escape", errors="ignore")
            url = offer.group(2).replace("\\u002F", "/")
            price = offer.group(1)
            item = (title, price, url)
            if item not in found:
                found.append(item)
    for title, price, url in found[:40]:
        print(json.dumps({"title": title, "price": price, "url": url}, ensure_ascii=False))
