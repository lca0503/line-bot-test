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

app = Flask(__name__)

line_bot_api = LineBotApi('JNeCDV6nXXEG1jsNvgLCRdYieAPOdfSIUZCMikwghPUU8xkGJErjjQrAtf9ZcBS0C7kC+NgvogdHLcg0FGvL/uKXSydk3agYbCKr8UJZ/Ug+CU0x/0fSmXGc1XjJSYYIbBxtR44Imjhyfo6XejrNpQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('b5794abe4250b5c733950248c9aa7c31')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + "hi" + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))
    
if __name__ == "__main__":
    app.run()
