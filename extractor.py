import json
import re
from gpt4all import GPT4All

MODEL_NAME = "mistral-7b-instruct-v0.1.Q4_0.gguf"
_model = None


def load_model():
    global _model
    if _model is None:
        _model = GPT4All(
            model_name=MODEL_NAME,
            allow_download=True
        )
    return _model


def clean_latex(latex: str) -> str:
    if not latex:
        return ""

    # Remove spaces between single characters (OCR/LLM artifact)
    latex = re.sub(r'(?<=\w)\s+(?=\w)', '', latex)

    # Fix common LaTeX mistakes
    replacements = {
        " imes ": " \\times ",
        "imes": "\\times",
        " x ": " \\times ",
        "rac": "\\frac",
    }

    for wrong, correct in replacements.items():
        latex = latex.replace(wrong, correct)

    # Normalize whitespace
    latex = re.sub(r"\s+", " ", latex)

    return latex.strip()



def extract_math_questions(text: str):
    """
    Extract algebra OR calculus questions without solving them.
    """

    model = load_model()

    prompt = f"""
You are a math question extraction system.

TASK:
Identify ALL math questions in the text below.

IMPORTANT:
- Questions may be algebra, calculus, or functions
- Include problems involving:
  • derivatives or anti-derivatives
  • functions like f(x), F(x)
  • graph transformations (scaling, dilation, translation)
  • symbolic reasoning
- Numbers ARE allowed in question text
- Do NOT solve numerically
- Do NOT compute values
- Provide SYMBOLIC relationships only

LATEX RULES:
- Use symbolic math only
- Do NOT substitute numbers
- Examples:
  VALID: F'(x) = f(x)
  VALID: y = mF(x)
  INVALID: m = 2
  INVALID: c = 5

OUTPUT:
- Return ONLY valid JSON
- No markdown
- No explanation text
- If no math questions exist, return []

FORMAT:
[
  {{
    "question_text": "clean math question",
    "latex": "symbolic LaTeX expression",
    "difficulty": 3,
    "tags": ["calculus", "functions"]
  }}
]

TEXT:
{text}
"""

    with model.chat_session():
        response = model.generate(
            prompt=prompt,
            max_tokens=600,
            temp=0.0
        )

    cleaned = re.sub(r"```json|```", "", response).strip()

    try:
        data = json.loads(cleaned)
        for item in data:
            item["latex"] = clean_latex(item.get("latex", ""))
        return data
    except json.JSONDecodeError:
        return []
