import os
import json
from google import genai

client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])

SYSTEM_PROMPT = """
You are a regulatory reporting assistant.
Generate ONLY valid JSON matching the COREP schema structure.
The JSON must have a root key "rows" which is a list of objects.
Each object in "rows" must represent a reporting row and contain:
- "row_code": The row identifier (e.g., "r010", "r060").
- "amount": The numeric value.
- "rule_reference": The regulatory text citation justifying this value.
- "description": A short description of the row.

Ensure you generate rows "r010" (Common Equity Tier 1 capital) and "r060" (Retained earnings) at a minimum if applicable.
Every populated field MUST include a rule_reference.
"""

def generate_corep(question, scenario, retrieved_text):
    prompt = f"""
{SYSTEM_PROMPT}

Question:
{question}

Scenario:
{scenario}

Regulatory Text:
{retrieved_text}

Return ONLY valid JSON.
"""

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )

    raw_text = response.text
    # Strip markdown code blocks if present
    if raw_text.startswith("```"):
        # Remove first line (```json or ```) and last line (```)
        lines = raw_text.splitlines()
        if len(lines) >= 2:
            raw_text = "\n".join(lines[1:-1])
    
    try:
        return json.loads(raw_text)
    except json.JSONDecodeError as e:
        print(f"JSON Decode Error: {e}")
        print(f"Raw Response: {raw_text}")
        # Return an empty structure or re-raise with more info
        raise e
