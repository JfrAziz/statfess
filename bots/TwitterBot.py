import html
import re
import tempfile
import config as c
import requests
import tweepy
from requests_oauthlib import OAuth1


class TwitterBot:
    def __init__(self):
        self.api = c.create_api()
        self.direct_messages = []
        self.trigger_word = c.TRIGER_WORD
        self.me = self.api.me()

    def __get_all_dm(self):
        try:
            self.direct_messages = self.api.list_direct_messages()
            print("[INFO] Total incoming message : ", len(self.direct_messages))
        except Exception as e:
            print("[ERROR] ", e)

    # TODO : add video attachment
    def __post_all(self):
        for i, dm in enumerate(reversed(self.direct_messages)):
            sender_id = dm.message_create['sender_id']
            media_ids = []
            if sender_id == str(self.me.id):
                continue

            message_data = dm.message_create['message_data']
            text = html.unescape(message_data['text'])

            if self.trigger_word not in text:
                print("[FAILED] tweeting from DM NO.", i)
                self.__send_response(sender_id, "FAILED")
                continue

            if 'attachment' in message_data:
                if message_data['attachment']['media']['type'] == 'photo':
                    media_url = message_data['attachment']['media']['media_url']
                    media_id = self.__get_photo_id(media_url)
                    media_ids.append(media_id)
                    text = ' '.join(
                        re.sub(r"(@[A-Za-z0-9]+)|(\w+:\/\/\S+)", " ", text).split())
                else:
                    continue

            if len(text) > 280:
                try:
                    self.__post_thread(sender_id, text, media_ids)
                except Exception as e:
                    print("[ERROR] ", e)
                continue

            try:
                self.__post_tweet(sender_id, text, media_ids)
                self.__send_response(sender_id, "SUCCESS")
            except Exception as e:
                print("[ERROR] ", e)

    # TODO : make better cut of text
    def __post_thread(self, sender_id, text, media_ids=[]):
        print("[THREAD] from ", sender_id)
        status_id = 0
        while len(text) > 280:
            tweet = text[0:272] + " ... "
            if status_id == 0:
                status_send = self.api.update_status(
                    tweet, media_ids=media_ids)
                status_id = status_send.id
                print("[TWEET] ", tweet)
            else:
                status_send = self.api.update_status(
                    tweet, in_reply_to_status_id=status_id,
                    auto_populate_reply_metadata=True)
                status_id = status_send.id
                print("[TWEET] ", tweet)
            text = " ... "+text[272:len(text)]
        if status_id != 0:
            print("[TWEET] ", text)
            self.api.update_status(
                text, in_reply_to_status_id=status_id,
                auto_populate_reply_metadata=True)
            self.__send_response(sender_id, "SUCCESS")

    def __post_tweet(self, sender_id, text, media_ids=[]):
        print("[TWEET] from ", sender_id, ", tweet : ", text)
        self.api.update_status(text,  media_ids=media_ids)

    def __get_photo_id(self, media_url):
        oauth = OAuth1(client_key=c.CONSUMER_KEY,
                       client_secret=c.CONSUMER_SECRET,
                       resource_owner_key=c.ACCESS_TOKEN,
                       resource_owner_secret=c.ACCESS_TOKEN_SECRET)
        respon = requests.get(media_url, auth=oauth)
        tmp = tempfile.NamedTemporaryFile()
        if respon.status_code == 200:
            with open(tmp.name, 'wb') as image:
                for chunk in respon:
                    image.write(chunk)
            photo_ids = self.api.media_upload(tmp.name).media_id
        else:
            photo_ids = []
        return photo_ids

    def __send_response(self, sender_id, status="SUCCESS"):
        if sender_id == str(self.me.id):
            return
        if status == "SUCCESS":
            self.api.send_direct_message(
                recipient_id=sender_id,
                text="Thank You, we will process your message")
        if status == "FAILED":
            self.api.send_direct_message(
                recipient_id=sender_id,
                text="Failed, please check your message")
        if status == "ERROR":
            self.api.send_direct_message(
                recipient_id=sender_id,
                text="You got an rrror, keep calm it's not your fault")
        print("Sending respon to ", sender_id, " with status : ", status)

    def __delete_direct_messages(self):
        direct_messages = self.direct_messages
        for i, dm in enumerate(reversed(direct_messages)):
            try:
                self.api.destroy_direct_message(dm.id)
                print("Deleting DM NO.", i)
            except Exception as e:
                print("Error : ", e)

    def run(self):
        self.__get_all_dm()
        self.__post_all()
        self.__delete_direct_messages()
