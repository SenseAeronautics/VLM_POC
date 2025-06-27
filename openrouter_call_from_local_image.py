import requests
import json
import base64
import mimetypes
import os

def query_qwen_with_image(image_path, prompt_text):
    # Guess MIME type
    mime_type, _ = mimetypes.guess_type(image_path)
    if mime_type is None:
        raise ValueError("Cannot determine the MIME type of the image.")

    # Load and encode image
    with open(image_path, "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode('utf-8')

    # Data URL
    data_url = f"data:{mime_type};base64,{base64_image}"

    # Prepare payload
    payload = {
        "model": "qwen/qwen2.5-vl-32b-instruct:free",
        "messages": [
            {
                "role": "user",
                "content": [
                    { "type": "text", "text": prompt_text },
                    { "type": "image_url", "image_url": { "url": data_url } }
                ]
            }
        ]
    }

    headers = {
        # This is jartolazabal's API Key on OpenRouter.ai
        "Authorization": "Bearer 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",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://yourdomain.com",  # Optional
        "X-Title": "MyApp"                          # Optional
    }

    # POST request
    response = requests.post("https://openrouter.ai/api/v1/chat/completions",
                             headers=headers, data=json.dumps(payload))

    # Output
    if response.status_code == 200:
        result = response.json()
        return result['choices'][0]['message']['content']
    else:
        raise RuntimeError(f"Request failed: {response.status_code} {response.text}")

# Ask user for input image and prompt
if __name__ == "__main__":
    image_path = input("Enter the full path to the image file: ").strip()
    if not os.path.exists(image_path):
        print(f"Error: file '{image_path}' does not exist.")
        exit(1)

    prompt_text = input("Enter the question or prompt for the image: ").strip()

    try:
        response = query_qwen_with_image(image_path, prompt_text)
        print("\nResponse:\n", response)
    except Exception as e:
        print("Error querying OpenRouter:", e)