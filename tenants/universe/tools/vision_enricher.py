import base64
import json
import os
import requests

# Configuration - These would ideally come from your environment or config
# Since I'm running in your environment, I'll assume the OmniRoute endpoint is available.
# For the prototype, I'll use standard OpenAI-compatible patterns.
API_KEY = os.getenv("OPENAI_API_KEY", "your-api-key-here")
BASE_URL = os.getenv("OPENAI_BASE_URL", "http://localhost:8000/v1") # Adjust to your OmniRoute URL
MODEL = "gpt-4o" # Or your preferred vision model

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def enrich_image_context(image_path):
    if not os.path.exists(image_path):
        return f"Error: Image not found at {image_path}"

    base64_image = encode_image(image_path)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": (
                            "Describe esta imagen de forma breve y táctica para un contexto de redes sociales. "
                            "Enfócate en: 1. Personajes u objetos principales. 2. La acción o situación. 3. El tono o emoción visual. "
                            "Mantén la descripción en menos de 2 frases y en español. "
                            "Usa un estilo descriptivo que sirva como 'contexto de meme'."
                        )
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 150
    }

    try:
        response = requests.post(f"{BASE_URL}/chat/completions", headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        return result['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"Error during API call: {str(e)}"

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python3 vision_enricher.py <path_to_image>")
    else:
        img_path = sys.argv[1]
        print(f"--- Processing: {img_path} ---")
        context = enrich_image_context(img_path)
        print(f"Meme Context (Tactical): {context}")
