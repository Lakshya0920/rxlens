import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

MODEL = "gemma-4-26b-a4b-it"

PROMPT = (
    "You are reading the printed label of a medicine strip or box. "
    "Copy ONLY the generic (active ingredient) names and strengths exactly as printed, "
    "for example: Paracetamol 500 mg. Reply with just that text on one line. "
    "Do not add explanations, dosage advice or prices. "
    "If no generic name is readable, reply exactly: NONE"
)

def read_label(image_bytes, mime_type):
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    resp = client.models.generate_content(
        model=MODEL,
        contents=[types.Part.from_bytes(data=image_bytes, mime_type=mime_type), PROMPT],
    )
    text = (resp.text or "").strip()
    return "" if text.upper().startswith("NONE") else text