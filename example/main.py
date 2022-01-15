import os
from datetime import datetime
from flask import Flask, request
from fbmessenger import BaseMessenger
from fbmessenger.templates import GenericTemplate
from fbmessenger.elements import Text, Button, Element
from fbmessenger import quick_replies
from fbmessenger.attachments import Image, Video
from fbmessenger.thread_settings import (
    GreetingText,
    GetStartedButton,
    PersistentMenuItem,
    PersistentMenu,
    MessengerProfile,
)
import dialogflow
from google.api_core.exceptions import InvalidArgument
from google.cloud import bigquery



def get_button(ratio):
    return Button(
        button_type='web_url',
        title='facebook {}'.format(ratio),
        url='https://facebook.com/',
        webview_height_ratio=ratio,
    )


def get_element(btn):
    return Element(
        title='Testing template',
        item_url='http://facebook.com',
        image_url='http://placehold.it/300x300',
        subtitle='Subtitle',
        buttons=[btn]
    )


def process_message(message):
    app.logger.debug('Message received: {}'.format(message))

    if 'attachments' in message['message']:
        if message['message']['attachments'][0]['type'] == 'location':
            app.logger.debug('Location received')
            response = Text(text='{}: lat: {}, long: {}'.format(
                message['message']['attachments'][0]['title'],
                message['message']['attachments'][0]['payload']['coordinates']['lat'],
                message['message']['attachments'][0]['payload']['coordinates']['long']
            ))
            return response.to_dict()

    if 'text' in message['message']:
        msg = message['message']['text'].lower()
        response = Text(text='Sorry didn\'t understand that: {}'.format(msg))
        if 'text' in msg:
            response = Text(text='This is an example text message.')
        if 'image' in msg:
            response = Image(url='https://unsplash.it/300/200/?random')
        if 'video' in msg:
            response = Video(url='http://techslides.com/demos/sample-videos/small.mp4')
        if 'quick replies' in msg:
            qr1 = quick_replies.QuickReply(title='Location', content_type='location')
            qr2 = quick_replies.QuickReply(title='Payload', payload='QUICK_REPLY_PAYLOAD')
            qrs = quick_replies.QuickReplies(quick_replies=[qr1, qr2])
            response = Text(text='This is an example text message.', quick_replies=qrs)
        if 'payload' in msg:
            txt = 'User clicked {}, button payload is {}'.format(
                msg,
                message['message']['quick_reply']['payload']
            )
            response = Text(text=txt)
        if 'webview-compact' in msg:
            btn = get_button(ratio='compact')
            elem = get_element(btn)
            response = GenericTemplate(elements=[elem])
        if 'webview-tall' in msg:
            btn = get_button(ratio='tall')
            elem = get_element(btn)
            response = GenericTemplate(elements=[elem])
        if 'webview-full' in msg:
            btn = get_button(ratio='full')
            elem = get_element(btn)
            response = GenericTemplate(elements=[elem])

        return response.to_dict()


class Messenger(BaseMessenger):
    def __init__(self, page_access_token):
        self.page_access_token = page_access_token
        super(Messenger, self).__init__(self.page_access_token)

    def message(self, message):
        action = process_message(message)
        res = self.send(action, 'RESPONSE')
        self.send_generic_template('placeholder_of_payload')
        app.logger.debug('Response: {}'.format(res))

    def delivery(self, message):
        pass

    def read(self, message):
        pass

    def account_linking(self, message):
        pass

    def postback(self, message):
        payload = message['postback']['payload']
        if 'start' in payload:
            txt = ('Hey, let\'s get started! Try sending me one of these messages: '
                   'text, image, video, "quick replies", '
                   'webview-compact, webview-tall, webview-full')
            self.send({'text': txt}, 'RESPONSE')
        if 'help' in payload:
            self.send({'text': 'A help message or template can go here.'}, 'RESPONSE')

    def optin(self, message):
        pass

    def init_bot(self):
        self.add_whitelisted_domains('https://facebook.com/')
        greeting = GreetingText(text='Welcome to the fbmessenger bot demo.')
        self.set_messenger_profile(greeting.to_dict())

        get_started = GetStartedButton(payload='start')
        self.set_messenger_profile(get_started.to_dict())

        menu_item_1 = PersistentMenuItem(
            item_type='postback',
            title='Help',
            payload='help',
        )
        menu_item_2 = PersistentMenuItem(
            item_type='web_url',
            title='Messenger Docs',
            url='https://developers.facebook.com/docs/messenger-platform',
        )
        persistent_menu = PersistentMenu(menu_items=[
            menu_item_1,
            menu_item_2
        ])

        res = self.set_messenger_profile(persistent_menu.to_dict())
        app.logger.debug('Response: {}'.format(res))


app = Flask(__name__)
app.debug = True
messenger = Messenger(os.getenv('FB_PAGE_TOKEN'))

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        if request.args.get('hub.verify_token') == os.getenv('FB_VERIFY_TOKEN'):
            if request.args.get('init') and request.args.get('init') == 'true':
                messenger.init_bot()
                return ''
            return request.args.get('hub.challenge')
        raise ValueError('FB_VERIFY_TOKEN does not match.')
    elif request.method == 'POST':
        messenger.handle(request.get_json(force=True))
        print(request.get_json(force=True))
        print(request.get_json(force=True)['entry'][0]['messaging'][0]['message']['text'])
        reply = _get_result_from_dialogflow(text_to_be_analyzed=request.get_json(force=True)['entry'][0]['messaging'][0]['message']['text'])
        try:
            upload_message_to_bigquery(request.get_json(force=True))
        except Exception as e:
            print(e)
        try:
            messenger.send({'text': reply}, 'RESPONSE', notification_type='REGULAR', timeout=4)
        except Exception as e:
            print(e)
            messenger.send({'text': '我不知道'}, 'RESPONSE', notification_type='REGULAR', timeout=4)
    return ''


def _get_result_from_dialogflow(text_to_be_analyzed: str) -> str:
    DIALOGFLOW_PROJECT_ID = 'pycontw-225217'
    DIALOGFLOW_LANGUAGE_CODE = 'en'
    SESSION_ID = 'anything'

    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)
    text_input = dialogflow.types.TextInput(text=text_to_be_analyzed, language_code=DIALOGFLOW_LANGUAGE_CODE)
    query_input = dialogflow.types.QueryInput(text=text_input)
    try:
        response = session_client.detect_intent(session=session, query_input=query_input)
    except InvalidArgument:
        raise
    return '\n'.join(fulfillment_message.text.text[0] for fulfillment_message in response.query_result.fulfillment_messages)

def upload_message_to_bigquery(json : dict):
    # PROJECT_ID =os.getenv("BIGQUERY_PROJECT")
    project_id = 'pycontw-225217'
    client = bigquery.Client(project=project_id)
    table = client.dataset('ods').table('ods_pycontw_fb_messages')    
    message = json['entry'][0]['messaging'][0]['message']['text']
    timestamp = json['entry'][0]['messaging'][0]['timestamp']   
    date = datetime.fromtimestamp(timestamp/1000).strftime('%Y-%m-%d %H:%M:%S')
    upload_message = [{"dates":date,"messages":message}]
    client.load_table_from_json(upload_message,table)

if __name__ == '__main__':
    app.run(host='0.0.0.0')

