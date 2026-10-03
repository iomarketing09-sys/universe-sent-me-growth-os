import requests, base64

imagenes = [
    {
        "nombre": "Sticker A (en Existencial 2607913 y Reel Depresión Sonora)",
        "url": "https://scontent.fntr6-1.fna.fbcdn.net/v/t39.1997-6/47270791_937342239796388_4222599360510164992_n.png?_nc_cat=1&ccb=1-7&_nc_sid=23dd7b&_nc_eui2=AeGhwKc1PokoYawPnX9gOoYs-b1tLjff_GL5vW0uN9_8YrVunyfzcfeX_W6qEcti1dWJ42EPMS9xqhWZy29v9DF2&_nc_ohc=vtBcbbBQVNsQ7kNvwESefRw&_nc_oc=AdqHMsKgyigeD7Cn_LmBqhTbunH_szduE2RuH-mMbCt6SGZsNagx3gkHPaw6ZCwn6HhKU5eIKJZ2mN6cnOchzXwp&_nc_zt=26&_nc_ht=scontent.fntr6-1.fna&edm=ANsyT80EAAAA&_nc_gid=b0udmgOqFdre09DWQvr_yQ&_nc_tpa=Q5bMBQJ70_59TS6_4t-squw14fZdP9Tm16C72ksv_sYwd38zApskvQyC2AO-h9pcSc_Xfzs4CjnYokyZjFI&oh=00_AQPSd4ciVvHfYjSiVloupxiANAG_xublZM-Sa7hfYYTwzQ&oe=6AC39D32"
    },
    {
        "nombre": "Sticker B (en 'Universe - pudimos serlo todo')",
        "url": "https://scontent.fntr6-1.fna.fbcdn.net/v/t39.1997-6/64618616_1231656310339052_3046878932545568768_n.png?_nc_cat=1&ccb=1-7&_nc_sid=23dd7b&_nc_eui2=AeGqvEYPH6nCgm66fOZ83aLkd2allvCTHrR3ZqWW8JMetNAnlYBoYeplfnIw_mTyxU4636Zd1oQj6vv1gr5XyNjH&_nc_ohc=r_RPhvqQQ68Q7kNvwH1eygY&_nc_oc=AdowWgkL4hyrsusqgtMkJUonBerNukriaA7tx0Wtt48RlsV8THtSQUBo7hy7ImlMxGaW0OncFdb2oGdczXl0xk8A&_nc_zt=26&_nc_ht=scontent.fntr6-1.fna&edm=ANsyT80EAAAA&_nc_gid=Fid7jv0FX8yrKkfKANnPjQ&_nc_tpa=Q5bMBQLC2Ecl_QJofPvko3jP8W5C-jGi1JsYxgAdJLCRd3wBdN0iZQYWWvFyxg6yApOlDUVTbjnqwtZtu4Q&oh=00_AQO5K4W4pROa3HrxPneNuhghostmTOGfCTt8peE0Hv7CLA&oe=6AC38189"
    },
    {
        "nombre": "Foto C (en 'Existencial 2607954')",
        "url": "https://scontent.fntr6-3.fna.fbcdn.net/v/t39.30808-6/828203511_29011771755087469_6021883049623720785_n.jpg?_nc_cat=106&_nc_map=urlgen_bucketless&ccb=1-7&_nc_sid=bd9a62&_nc_eui2=AeFEGmoOrsPDmRBrROSyadNj47XpfcwCvjLjtel9zAK-MkM64sWn2JIxf8B-0IwiE_FGGIwijfJiR_JcXABuTVVa&_nc_ohc=S3E9gizM5AYQ7kNvwEyhKH5&_nc_oc=AdpiC2J0xLyaVA8-bT-0noO2SGqjL5vghXCWpeAdHMGsCX2CKnZpjXOHIKh_YToqbrIxg6oXC1oICDDHJ42jX6ZE&_nc_zt=23&_nc_ht=scontent.fntr6-3.fna&edm=ANsyT80EAAAA&_nc_gid=bhW6CXxCQzPoxs7584OzPg&_nc_tpa=Q5bMBQIQ90OflAG62K-CAF4mPXgOb-8W_EtZijJycKRe5_qPM-tACf3-C4hdcJiHx5dI8RNCG5VSRHq9LBM&oh=00_AQOdweR1B73vt6nYXnOyA237zSJVhRi1MJzsx3DJJvwt0g&oe=6AC3783E"
    }
]

print("\n" + "="*80)
print("🤖 CONSULTANDO A OMNIROUTE (Universe_Combo - Llama 3.2 Vision)")
print("="*80)

for item in imagenes:
    print(f"\nAnalizando {item['nombre']}...")
    try:
        img_bytes = requests.get(item["url"], timeout=15).content
        b64_str = base64.b64encode(img_bytes).decode("utf-8")
        data_uri = f"data:image/jpeg;base64,{b64_str}"
        
        payload = {
            "model": "Universe_Combo",
            "stream": False,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Describe en una sola frase breve qué sticker o imagen es esta y qué tono, gesto o emoción transmite (ej. risa, burla, ternura, desinterés):"},
                        {"type": "image_url", "image_url": {"url": data_uri}}
                    ]
                }
            ],
            "max_tokens": 80
        }
        res = requests.post("http://localhost:20128/v1/chat/completions", json=payload, timeout=25).json()
        desc = res.get("choices", [{}])[0].get("message", {}).get("content", "").strip()
        print(f"✨ Descripción IA: {desc}")
    except Exception as e:
        print(f"⚠️ Error consultando OmniRoute: {e}")
    print("-" * 80)
