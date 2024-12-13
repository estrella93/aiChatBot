from flask import Flask
app = Flask(__name__)

from flask import request, abort
from linebot import  LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import google.generativeai as genai
import os 

line_bot_api = LineBotApi(os.environ.get('Line_bot_token'))
handler = WebhookHandler(os.environ.get('Line_bot_secret'))

genai.configure(api_key=os.environ.get('gemini_api_key'))

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_prompt=event.message.text
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(user_prompt)
    result=response.text
    line_bot_api.reply_message(event.reply_token,TextSendMessage(text=result))



imagen = genai.ImageGenerationModel("imagen-3.0-generate-001")

result = imagen.generate_images(
    prompt="Fuzzy bunnies in my kitchen",
    number_of_images=4,
    safety_filter_level="block_only_high",
    person_generation="allow_adult",
    aspect_ratio="3:4",
    negative_prompt="Outside",
)

for image in result.images:
  print(image)

# Open and display the image using your local operating system.
for image in result.images:
  image._pil_image.show()
if __name__ == '__main__':
    app.run()
