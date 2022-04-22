from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

from flask import render_template

from googletrans import Translator

app = Flask(__name__)


line_bot_api = LineBotApi('JNeCDV6nXXEG1jsNvgLCRdYieAPOdfSIUZCMikwghPUU8xkGJErjjQrAtf9ZcBS0C7kC+NgvogdHLcg0FGvL/uKXSydk3agYbCKr8UJZ/Ug+CU0x/0fSmXGc1XjJSYYIbBxtR44Imjhyfo6XejrNpQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('b5794abe4250b5c733950248c9aa7c31')
translator = Translator()

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    detect_language = translator.detect(event.message.text).lang
    if detect_language == 'zh-tw':
        text = translator.translate(event.message.text, dest='ja').text
    elif detect_language == 'ja':
        text = translator.translate(event.message.text, dest='zh-tw').text
    else:
        text = event.message.text
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=text)
    )
    
if __name__ == "__main__":
    app.run()
