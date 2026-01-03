import json
from groq import Groq

# Read API key from file
with open("apikey.txt", "r") as f:
    API_KEY = f.read().strip()

client = Groq(api_key=API_KEY)

SYSTEM_PROMPT = """
You are an information extraction system for Nepal Government Services.
Your task is to extract fields from user text into JSON.

VALID DOCUMENTS (Exact enum):
- "Citizenship"
- "NIDCard"
- "DrivingLicense"
- "Passport"
- null (if none of the above are clearly mentioned)

RULES:
1. document: Map the user's request to one of the VALID DOCUMENTS. 
   - Example: "driving license", "license", "bike trial" -> "drivinglicense"
   - Example: "rastriya parichaya patra", "NID" -> "nidcard"
2. criteria_not_met: Identify any missing requirement mentioned. Limit it to the mention of VALID DOCUMENTS only.
    criteria_not_met should be in the format (VALID DOCUMENT) eg, "Citizenship", "DrivingLicense" etc
    use null if the above doesnt hold true.
    
3. address: Extract location if present.

Output JSON ONLY.

Input: "I need a passport but lost my citizenship"
Output: {"document": "Passport", "criteria_not_met": "Citizenship,NIDCard", "address": null}
"""

def parse_text(formText):
    user_text = formText
    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_text}
            ],
            temperature=0
        )
        result = json.loads(completion.choices[0].message.content)
    except Exception as e:
        print(f"LLM Error: {e}")
        # Fallback if LLM fails
        result = {
            "document": None,
            "criteria_not_met": None,
            "address": None
        }
    return result