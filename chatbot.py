import os
import google.generativeai as genai

genai.configure(api_key="your gemini api key")


generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-pro",
  generation_config=generation_config,
)

chat_session = model.start_chat(
  history=[]
)

def answer_anything(txt):
    response = chat_session.send_message(f"{txt}")
    return response.text