import tweepy
import html


class TwitterBot:
    def __init__(self, api, trigger_word="", direct_messages=0):
        self.api = api
        self.direct_messages = direct_messages
        self.trigger_word = trigger_word
        self.me = self.api.me()

    def __get_all_dm(self):
        self.direct_messages = self.api.list_direct_messages()
        print("Total incoming message : ", len(self.direct_messages))

    def __post_all(self):
        for i, dm in enumerate(reversed(self.direct_messages)):
            sender_id = dm.message_create['sender_id']

            if sender_id == str(self.me.id):
                continue

            message_data = dm.message_create['message_data']
            text = html.unescape(message_data['text'])

            if self.trigger_word not in text:
                print("[FAILED] tweeting from DM NO.", i)
                self.__send_response(sender_id, "FAILED")
                continue

            if len(text) > 280:
                try:
                    self.__post_thread(text, sender_id)
                except Exception as e:
                    print("[ERROR] ", e)
                continue

            try:
                self.__post_tweet(text, sender_id)
                self.__send_response(sender_id, "SUCCESS")
            except Exception as e:
                print("[ERROR] ", e)
                self.__send_response(sender_id, "ERROR")
                continue

    def __post_thread(self, text, sender_id):
        print("[THREAD] from ", sender_id)
        status_id = 0
        while len(text) > 280:
            tweet = text[0:272] + " .... "
            if status_id == 0:
                status_send = self.api.update_status(tweet)
                status_id = status_send.id
                print("[TWEET] ", tweet)
            else:
                status_send = self.api.update_status(
                    tweet, in_reply_to_status_id=status_id,
                    auto_populate_reply_metadata=True)
                status_id = status_send.id
                print("[TWEET] ", tweet)
            text = " .... "+text[272:len(text)]
        if status_id != 0:
            print("[TWEET] ", text)
            self.api.update_status(
                text, in_reply_to_status_id=status_id,
                auto_populate_reply_metadata=True)
            self.__send_response(sender_id, "SUCCESS")

    def __post_tweet(self, text, sender_id):
        print("[TWEET] from ", sender_id, ", tweet : ", text)
        self.api.update_status(text)

    def __post_media(self):
        return

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
                continue

    def run(self):
        self.__get_all_dm()
        self.__post_all()
        self.__delete_direct_messages()
