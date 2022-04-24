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

from utils import get_qa_dict
import config
from googletrans import Translator


app = Flask(__name__)


line_bot_api = LineBotApi(config.CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(config.CHANNEL_SECRET)
QA_dict = get_qa_dict(config.CONTEXT_PATH)
language_list = config.LANGUAGE_LIST


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
    message_text_list = event.message.text.lower().split(' ')
    reply_text = ""
    find_token = False
    
    for message_text in message_text_list:
        if message_text in QA_dict:
            for answer in QA_dict[message_text]:
                reply_text = reply_text + answer + '\n'
                find_token = True
        if message_text in language_list:
            language = message_text

    if not find_token:
        reply_text = "Sorry, there is no answer to " + "\"" + event.message.text + "\""
    '''
    if language is not None:
        translator = Translator()
        reply_text = translator.translate(reply_text, dest=language)
    '''
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_text)
    )

    
if __name__ == "__main__":
    app.run()
