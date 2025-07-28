from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
import base64
from config import api_key
import logging
import text
import json
import present_pptx
client = genai.Client(api_key=api_key)

async def get_gemini_response(content):

    try:

        response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=content
        )
        return response.text
    except Exception as e:
        logging.error(e)


async def create_presentation(theme,slides,type):
    prompt = text.presentation_prompt.format(theme=theme,number=slides,type=type)
    try:

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        replaced_text = response.text.replace("```json","").replace("```","").strip()
        data = json.loads(replaced_text)
        images = []

        for i in range(1,6,2):
            images.append(data[i]["image"])
        if len(images) > 0:
            await create_image(images)
        present_pptx.create_presentation(data)
    except Exception:
        print("exception")

async def create_image(images):
    try:

        for i in range(len(images)):

            response = client.models.generate_content(
                model="gemini-2.0-flash-preview-image-generation",
                contents=images[i],
                config=types.GenerateContentConfig(
                response_modalities=['TEXT', 'IMAGE']
                )
            )

            for part in response.candidates[0].content.parts:
                if part.inline_data is not None:
                    image = Image.open(BytesIO((part.inline_data.data)))
                    image.save(f'images\\gemini-native-image{i}.png')

    except Exception:
        print("Failed with creating photos")
