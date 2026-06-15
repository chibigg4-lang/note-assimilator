import os
from PIL import Image
from dotenv import load_dotenv
import google.generativeai as genai
load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

genai.configure(api_key = api_key)
PROMPT = PROMPT = """
Transcribe this note image exactly into Markdown.

Rules:
- Do not summarize.
- Do not translate Vietnamese.
- Preserve mathematical notation using LaTeX.
- Wrap display formulas in $$ ... $$.
- Wrap code in Markdown code fences.
- Keep headings, bullet points, and numbering if visible.
- If something is unreadable, write [unreadable].
- Return only the extracted Markdown.
"""

def extract_markdown_from_image(image_path: str) -> str:
    image = Image.open(image_path)
    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content([PROMPT, image])
    return response.text


if __name__ == "__main__":
    result = extract_markdown_from_image("uploads/classification_test_note.jpg")
    print(result)