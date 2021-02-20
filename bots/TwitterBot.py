import tweepy
import html


class TwitterBot:
    def __init__(self, api, trigger_word="", direct_messages=0):
        self.api = api
        self.direct_messages = direct_messages
        self.trigger_word = trigger_word
        self.me = self.api.me()

    def get_all_dm(self):
        api = self.api
        self.direct_messages = api.list_direct_messages()
        print("Total incoming message : ", len(self.direct_messages))

    def post_all(self):
        direct_messages = self.direct_messages
        api = self.api

        for i, dm in enumerate(reversed(direct_messages)):
            sender_id = dm.message_create['sender_id']

            if sender_id == self.me.id:
                continue

            message_data = dm.message_create['message_data']
            text = html.unescape(message_data['text'])

            if self.trigger_word in text:
                try:
                    api.update_status(text)
                    print("Tweeting from DM NO.", i)
                    api.send_direct_message(recipient_id=sender_id, text="Thank You")
                except Exception as e:
                    print("Error : ", e)
                    api.send_direct_message(recipient_id=sender_id, text="Failed")
                    continue
            else:
                api.send_direct_message(recipient_id=sender_id, text="Failed")
                print("Failed tweeting from DM NO.", i)
            print("Sending respon to sender")

    def delete_direct_messages(self):
        direct_messages = self.direct_messages
        api = self.api
        for i, dm in enumerate(reversed(direct_messages)):
            try:
                api.destroy_direct_message(dm.id)
                print("Deleting DM NO.", i)
            except Exception as e:
                print("Error : ", e)
                continue


    def run(self):
        self.get_all_dm()
        self.post_all()
        self.delete_direct_messages()
