from __future__ import absolute_import
import abc
import logging
import hashlib
import hmac
import six
import requests

__version__ = "6.0.0"

logger = logging.getLogger(__name__)


DEFAULT_API_VERSION = 2.12


class MessengerClient(object):

    # https://developers.facebook.com/docs/messenger-platform/send-messages#messaging_types
    MESSAGING_TYPES = {
        "RESPONSE",
        "UPDATE",
        "MESSAGE_TAG",
    }

    # https://developers.facebook.com/docs/messenger-platform/reference/send-api/#payload
    NOTIFICATION_TYPES = {"REGULAR", "SILENT_PUSH", "NO_PUSH"}

    def __init__(self, page_access_token, **kwargs):
        """
        @required:
            page_access_token
        @optional:
            session
            api_version
            app_secret
        """

        self.page_access_token = page_access_token
        self.session = kwargs.get("session", requests.Session())
        self.api_version = kwargs.get("api_version", DEFAULT_API_VERSION)
        self.graph_url = "https://graph.facebook.com/v{api_version}".format(
            api_version=self.api_version
        )
        self.app_secret = kwargs.get("app_secret")

    @property
    def auth_args(self):
        if not hasattr(self, "_auth_args"):
            auth = {"access_token": self.page_access_token}
            if self.app_secret is not None:
                appsecret_proof = self.generate_appsecret_proof()
                auth["appsecret_proof"] = appsecret_proof
            self._auth_args = auth
        return self._auth_args

    def get_user_data(self, recipient_id, fields=None, timeout=None):
        params = {}

        if isinstance(fields, six.string_types):
            params["fields"] = fields
        elif isinstance(fields, (list, tuple)):
            params["fields"] = ",".join(fields)
        else:
            params["fields"] = "first_name,last_name,profile_pic,locale,timezone,gender"

        params.update(self.auth_args)

        r = self.session.get(
            "{graph_url}/{recipient_id}".format(
                graph_url=self.graph_url, recipient_id=recipient_id
            ),
            params=params,
            timeout=timeout,
        )
        return r.json()

    def send(
        self,
        payload,
        recipient_id,
        messaging_type="RESPONSE",
        notification_type="REGULAR",
        timeout=None,
        tag=None,
    ):
        if messaging_type not in self.MESSAGING_TYPES:
            raise ValueError(
                "`{}` is not a valid `messaging_type`".format(messaging_type)
            )

        if notification_type not in self.NOTIFICATION_TYPES:
            raise ValueError(
                "`{}` is not a valid `notification_type`".format(notification_type)
            )

        body = {
            "messaging_type": messaging_type,
            "notification_type": notification_type,
            "recipient": {
                "id": recipient_id,
            },
            "message": payload,
        }

        if tag:
            body["tag"] = tag

        r = self.session.post(
            "{graph_url}/me/messages".format(graph_url=self.graph_url),
            params=self.auth_args,
            json=body,
            timeout=timeout,
        )
        return r

    def send_action(self, sender_action, recipient_id, timeout=None):
        r = self.session.post(
            "{graph_url}/me/messages".format(graph_url=self.graph_url),
            params=self.auth_args,
            json={
                "recipient": {
                    "id": recipient_id,
                },
                "sender_action": sender_action,
            },
            timeout=timeout,
        )
        return r.json()

    def send_generic_template(self, payload, recipient_id, timeout=None):
        r = self.session.post(
            f"{self.graph_url}/me/messages",
            params=self.auth_args,
            json={
                "recipient": {"id": recipient_id},
                "message": {
                    "attachment": {
                        "type": "template",
                        "payload": {
                            "template_type": "generic",
                            "elements": [
                                {
                                    "title": "2021 PyCon TW x PyHug Meetup",
                                    "image_url": "https://pbs.twimg.com/media/E_Skh8MVQAUmPHm.jpg",
                                    "subtitle": "PyHug 簡介： 歡迎來到 PyHUG。我們是一群活動於新竹周邊的 Python 程式員。 我們會定期舉辦技術討論與程式設計的聚會。非常歡迎你加入我們！",
                                    "default_action": {
                                        "type": "web_url",
                                        "url": "https://www.youtube.com/watch?v=S_1WBzXFyBs&t=3752s",
                                        "webview_height_ratio": "tall",
                                    },
                                    "buttons": [
                                        {
                                            "type": "web_url",
                                            "url": "https://www.youtube.com/watch?v=S_1WBzXFyBs&t=3752s",
                                            "title": "View Website",
                                        },
                                        {
                                            "type": "postback",
                                            "title": "Like",
                                            "payload": "https://www.youtube.com/watch?v=S_1WBzXFyBs&t=3752s",
                                        },
                                    ],
                                },
                                {
                                    "title": "#7 | FAANG 工作環境跟外面有什麼不一樣？想進入 FAANG 就要聽這集！- Kir Chou",
                                    "image_url": "https://i.imgur.com/GrMYBUa.png",
                                    "subtitle": "這次邀請到的來賓是正在日本 Google 工作的 Kir 跟我們分享他在兩間 FAANG 工作過的經驗。想知道 Kir 在 FAANG 擔任軟體工程師的時候怎麼使用 Python 以及在公司內部推動重要的專案？另外，聽說他沒有刷題就加入 FAANG？！Wow 懶得刷題的聽眾快來聽，這集聽到賺到！PyCast 終於回歸拉！主持人在今年大會過後忙到被 👻 抓走沒時間錄新節目QQ為了讓 PyCast 再次偉大，邀請 Apple Podcast 的聽眾動動手指給我們五星跟留言建議🙏🏼🙏🏼🙏🏼#faang #japan #swe #makepycastgreatagain",
                                    "default_action": {
                                        "type": "web_url",
                                        "url": "https://open.firstory.me/story/ckxnh7hxq2s3s0966ghtw3qzq",
                                        "webview_height_ratio": "tall",
                                    },
                                    "buttons": [
                                        {
                                            "type": "web_url",
                                            "url": "https://open.firstory.me/story/ckxnh7hxq2s3s0966ghtw3qzq",
                                            "title": "View Website",
                                        },
                                        {
                                            "type": "postback",
                                            "title": "Like",
                                            "payload": "https://www.youtube.com/watch?v=S_1WBzXFyBs&t=3752s",
                                        },
                                    ],
                                },
                                {
                                    "title": "贊助商 - Berry AI",
                                    "image_url": "https://i.imgur.com/ktvzhsu.jpg",
                                    "subtitle": "Berry AI 是一間位於台北的 AI 新創，致力於運用電腦視覺技術幫助速食業者蒐集數據，改善現有營運流程。技術團隊由一群充滿熱情的 AI 及軟體工程師組成，分別來自海內外知名學術機構與大型科技公司。此外，我們得到台灣上市公司飛捷科技的注資與支持，該公司擁有多年為大型企業落地工業電腦的經驗，提供穩定的資金來源與客戶關係。如今，Berry AI 已與數間全球 Top-10 速食業者展開合作，業務與團隊都迅速擴張中。欲了解更多訊息，請瀏覽 berry-ai.com。",
                                    "default_action": {
                                        "type": "web_url",
                                        "url": "https://tw.pycon.org/2021/zh-hant",
                                        "webview_height_ratio": "tall",
                                    },
                                    "buttons": [
                                        {
                                            "type": "web_url",
                                            "url": "https://tw.pycon.org/2021/zh-hant",
                                            "title": "View Website",
                                        },
                                        {
                                            "type": "postback",
                                            "title": "Like",
                                            "payload": "https://www.youtube.com/watch?v=S_1WBzXFyBs&t=3752s",
                                        },
                                    ],
                                },
                                {
                                    "title": "他媽的給我買票喔！",
                                    "image_url": "https://i.imgur.com/WYiNl3z.png",
                                    "subtitle": "公道價八萬一",
                                    "default_action": {
                                        "type": "web_url",
                                        "url": "https://pycontw.kktix.cc/events/2021-individual",
                                        "webview_height_ratio": "tall",
                                    },
                                    "buttons": [
                                        {
                                            "type": "web_url",
                                            "url": "https://pycontw.kktix.cc/events/2021-individual",
                                            "title": "View Website",
                                        },
                                        {
                                            "type": "postback",
                                            "title": "Like",
                                            "payload": "https://www.youtube.com/watch?v=S_1WBzXFyBs&t=3752s",
                                        },
                                    ],
                                },
                            ],
                        },
                    }
                },
            },
            timeout=3,
        )
        return r.json()

    def subscribe_app_to_page(self, timeout=None):
        r = self.session.post(
            "{graph_url}/me/subscribed_apps".format(graph_url=self.graph_url),
            params=self.auth_args,
            timeout=timeout,
        )
        return r.json()

    def set_messenger_profile(self, data, timeout=None):
        r = self.session.post(
            "{graph_url}/me/messenger_profile".format(graph_url=self.graph_url),
            params=self.auth_args,
            json=data,
            timeout=timeout,
        )
        return r.json()

    def delete_get_started(self, timeout=None):
        r = self.session.delete(
            "{graph_url}/me/messenger_profile".format(graph_url=self.graph_url),
            params=self.auth_args,
            json={
                "fields": ["get_started"],
            },
            timeout=timeout,
        )
        return r.json()

    def delete_persistent_menu(self, timeout=None):
        r = self.session.delete(
            "{graph_url}/me/messenger_profile".format(graph_url=self.graph_url),
            params=self.auth_args,
            json={
                "fields": ["persistent_menu"],
            },
            timeout=timeout,
        )
        return r.json()

    def link_account(self, account_linking_token, timeout=None):
        r = self.session.post(
            "{graph_url}/me".format(graph_url=self.graph_url),
            params=dict(
                {"fields": "recipient", "account_linking_token": account_linking_token},
                **self.auth_args,
            ),
            timeout=timeout,
        )
        return r.json()

    def unlink_account(self, psid, timeout=None):
        r = self.session.post(
            "{graph_url}/me/unlink_accounts".format(graph_url=self.graph_url),
            params=self.auth_args,
            json={"psid": psid},
            timeout=timeout,
        )
        return r.json()

    def update_whitelisted_domains(self, domains, timeout=None):
        if not isinstance(domains, list):
            domains = [domains]
        r = self.session.post(
            "{graph_url}/me/messenger_profile".format(graph_url=self.graph_url),
            params=self.auth_args,
            json={"whitelisted_domains": domains},
            timeout=timeout,
        )
        return r.json()

    def remove_whitelisted_domains(self, timeout=None):
        r = self.session.delete(
            "{graph_url}/me/messenger_profile".format(graph_url=self.graph_url),
            params=self.auth_args,
            json={
                "fields": ["whitelisted_domains"],
            },
            timeout=timeout,
        )
        return r.json()

    def upload_attachment(self, attachment, timeout=None):
        if not attachment.url:
            raise ValueError("Attachment must have `url` specified")
        if attachment.quick_replies:
            raise ValueError("Attachment may not have `quick_replies`")
        r = self.session.post(
            "{graph_url}/me/message_attachments".format(graph_url=self.graph_url),
            params=self.auth_args,
            json={"message": attachment.to_dict()},
            timeout=timeout,
        )
        return r.json()

    def generate_appsecret_proof(self):
        """
        @outputs:
            appsecret_proof: HMAC-SHA256 hash of page access token
                using app_secret as the key
        """
        app_secret = str(self.app_secret).encode("utf8")
        access_token = str(self.page_access_token).encode("utf8")

        return hmac.new(app_secret, access_token, hashlib.sha256).hexdigest()


class BaseMessenger(object):
    __metaclass__ = abc.ABCMeta

    last_message = {}

    def __init__(self, page_access_token, app_secret=None):
        self.page_access_token = page_access_token
        self.app_secret = app_secret
        self.client = MessengerClient(
            self.page_access_token, app_secret=self.app_secret
        )

    @abc.abstractmethod
    def account_linking(self, message):
        """Method to handle `account_linking`"""

    @abc.abstractmethod
    def message(self, message):
        """Method to handle `messages`"""

    @abc.abstractmethod
    def delivery(self, message):
        """Method to handle `message_deliveries`"""

    @abc.abstractmethod
    def optin(self, message):
        """Method to handle `messaging_optins`"""

    @abc.abstractmethod
    def postback(self, message):
        """Method to handle `messaging_postbacks`"""

    @abc.abstractmethod
    def read(self, message):
        """Method to handle `message_reads`"""

    def handle(self, payload):
        for entry in payload["entry"]:
            for message in entry["messaging"]:
                self.last_message = message
                if message.get("account_linking"):
                    return self.account_linking(message)
                elif message.get("delivery"):
                    return self.delivery(message)
                elif message.get("message"):
                    return self.message(message)
                elif message.get("optin"):
                    return self.optin(message)
                elif message.get("postback"):
                    return self.postback(message)
                elif message.get("read"):
                    return self.read(message)

    def get_user(self, fields=None, timeout=None):
        return self.client.get_user_data(
            self.get_user_id(), fields=fields, timeout=timeout
        )

    def send(
        self,
        payload,
        messaging_type="RESPONSE",
        notification_type="REGULAR",
        timeout=None,
        tag=None,
    ):
        return self.client.send(
            payload,
            self.get_user_id(),
            messaging_type=messaging_type,
            notification_type=notification_type,
            timeout=timeout,
            tag=tag,
        )

    def send_generic_template(
        self,
        payload,
        timeout=None,
    ):
        return self.client.send_generic_template(
            payload,
            self.get_user_id(),
            timeout=timeout,
        )

    def send_action(self, sender_action, timeout=None):
        return self.client.send_action(
            sender_action, self.get_user_id(), timeout=timeout
        )

    def get_user_id(self):
        return self.last_message["sender"]["id"]

    def subscribe_app_to_page(self, timeout=None):
        return self.client.subscribe_app_to_page(timeout=timeout)

    def set_messenger_profile(self, data, timeout=None):
        return self.client.set_messenger_profile(data, timeout=timeout)

    def delete_get_started(self, timeout=None):
        return self.client.delete_get_started(timeout=timeout)

    def link_account(self, account_linking_token, timeout=None):
        return self.client.link_account(account_linking_token, timeout=timeout)

    def unlink_account(self, psid, timeout=None):
        return self.client.unlink_account(psid, timeout=timeout)

    def add_whitelisted_domains(self, domains, timeout=None):
        return self.client.update_whitelisted_domains(domains, timeout=timeout)

    def remove_whitelisted_domains(self, timeout=None):
        return self.client.remove_whitelisted_domains(timeout=timeout)

    def upload_attachment(self, attachment, timeout=None):
        return self.client.upload_attachment(attachment, timeout=timeout)
