
import json
from groq import Groq


# Read API key from file
with open("apikey.txt", "r") as f:
    API_KEY = f.read().strip()

client = Groq(api_key=API_KEY)


SYSTEM_PROMPT = """
You are an information extraction system.

Your task:
From the user's text, extract and infer the following fields.
Return ONLY valid JSON. No explanations.

Fields:
- document: the document the user wants to make or apply for
- criteria_not_met: any missing, lost, or unmet requirement (even if implicit)
- address: where the user lives or is located

IMPORTANT RULES:
- You MAY infer criteria_not_met if the user mentions losing or missing something required.
- Informal language like "I live in", "staying at", "from", or city names count as address.
- If a field truly cannot be inferred, set it to null.

Examples:

Input:
"I want a passport but I lost my citizenship. I live in Jhapa."
Output:
{
  "document": "passport",
  "criteria_not_met": "lost citizenship",
  "address": "Jhapa"
}

Input:
"Need a driving license. Not old enough yet. From Pokhara."
Output:
{
  "document": "driving license",
  "criteria_not_met": "not old enough",
  "address": "Pokhara"
}
"""


def parse_text():
    user_text = input("Enter the text to parse: ")

    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_text}
        ],
        temperature=0
    )

    try:
        result = json.loads(completion.choices[0].message.content)
    except json.JSONDecodeError:
        result = {
            "document": None,
            "criteria_not_met": None,
            "address": None
        }

    print("Parsed Result:")
    print(json.dumps(result, indent=2))

parse_text()