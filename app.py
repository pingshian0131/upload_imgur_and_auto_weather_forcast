from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
     InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    SourceUser, SourceGroup, SourceRoom,ImageSendMessage,
    TemplateSendMessage, ConfirmTemplate, MessageAction,
    ButtonsTemplate, ImageCarouselTemplate, ImageCarouselColumn, URIAction,
    PostbackAction, DatetimePickerAction,
    CameraAction, CameraRollAction, LocationAction,
    CarouselTemplate, CarouselColumn, PostbackEvent,
    StickerMessage, StickerSendMessage, LocationMessage, LocationSendMessage,
    ImageMessage, VideoMessage, AudioMessage, FileMessage,
    UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent,
    FlexSendMessage, BubbleContainer, ImageComponent, BoxComponent,
    TextComponent, SpacerComponent, IconComponent, ButtonComponent,
    SeparatorComponent, QuickReply, QuickReplyButton, CarouselContainer
)
import os
import json
from model import *
import tempfile
from imgurpython import ImgurClient
from config import client_id, client_secret, album_id, access_token, refresh_token, line_bot_api, handler
import sys

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    bodyjson=json.loads(body)
    #app.logger.error("Request body: " + bodyjson['events'][0]['message']['text'])
    app.logger.error("Request body: " + body)
    #insertdata
    print('-----in----------')
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=ImageMessage)
def handle_msg_sticker(event):
    '''
        ImageMessage auto upload to imgur and reply image url  
    '''
    if isinstance(event.message, ImageMessage):
        ext = 'jpg'
    message_content = line_bot_api.get_message_content(event.message.id)
    with tempfile.NamedTemporaryFile(dir=static_tmp_path, prefix=ext + '-', delete=False) as tf:
        for chunk in message_content.iter_content():
            tf.write(chunk)
        tempfile_path = tf.name

    dist_path = tempfile_path + '.' + ext
    dist_name = os.path.basename(dist_path)
    os.rename(tempfile_path, dist_path)
    client = ImgurClient(client_id, client_secret, access_token, refresh_token)
    config = {
        'album': album_id,
        'name': 'Catastrophe!',
        'title': 'Catastrophe!',
        'description': 'Cute kitten being cute on '
    }
    path = os.path.join('static', 'tmp', dist_name)
    image = client.upload_from_path(path, config=config, anon=False)
    os.remove(path)
    print(path)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='You can find image here: {0}'.format (image['link'])))

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

