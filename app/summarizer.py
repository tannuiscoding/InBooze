import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Optional tuning parameters
generation_config = {
    "temperature": 0.7,
    "top_p": 1,
    "top_k": 40,
    "max_output_tokens": 1024,
}

model = genai.GenerativeModel("gemini-2.0-flash", generation_config=generation_config)

def generate_summary(content):
    try:
        prompt = f"Summarize this email thread:\n\n{content}"
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"[Gemini] Failed to generate summary: {e}")
        return "Summary could not be generated."
