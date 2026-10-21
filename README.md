# 💊 MedLens

Find the Jan Aushadhi generic price for a medicine, and see how much you could save.

## Problem
Patients often pay brand prices without knowing that a generic with the same molecule costs far less at a Jan Aushadhi Kendra.

## What it does
- Type a medicine name (spelling mistakes are okay) and get the Jan Aushadhi price.
- Enter the price you were charged to see your saving, e.g. ₹40 → ₹4.51.
- Upload a photo of a strip or box and Gemma 4 reads the name off it.

## How Gemma 4 is used
- Model: `gemma-4-26b-a4b-it` (open-weight), via the Gemini API.
- Its only job is reading the printed medicine name from a photo.
- It never generates drug information, doses or prices. Every price comes from the CSV in `data/`. If a medicine is not there, the app says "not found".

## How matching works
`search.py` uses RapidFuzz to correct misspelt words against a vocabulary built from the Jan Aushadhi product list.

## Run it
    pip install -r requirements.txt
    copy .env.example .env
    (then open .env and add your Gemini API key)
    streamlit run app.py

## Limitations
- Photo reading can fail on blurry or handwritten text; typing always works.
- Prices are indicative and may change.
- Not medical advice. Confirm with your doctor or pharmacist before switching any medicine.

## Credits
- Data: Jan Aushadhi product list published by PMBI
- Tools: Streamlit, pandas, RapidFuzz, Google Gemini API, Gemma 4
- Built at Hackfest Lucknow 2026 (GDGoC SRMCEM × MLH)

## Licence
See `LICENSE`.