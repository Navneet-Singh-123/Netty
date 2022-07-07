import os
import requests
from threading import Thread
# Authentication using netty


class NettyAuth:

    def __init__(self, user_id, username, password, app, channel_id):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.app = app
        self.channel_id = channel_id

    def authenticate(self):
        url = os.environ["URL"] + "/users/auth"
        data = {
            "user_id": self.user_id,
            "username": self.username,
            "password": self.password
        }
        r = requests.post(url=url, data=data)
        status_code = r.status_code
        user = "<@"+self.user_id+">"
        data = str(r.text)
        self.display_result(user, data, status_code)

    def show_header(self, *args, **kwargs):
        self.app.client.chat_postMessage(
            channel=self.channel_id, text="Securely saving your credentials......")
        background = Thread(target=self.authenticate, args=[])
        background.start()

    def display_result(self, user, data, status_code):
        if status_code == 200:
            text_msg = "Successful!!"
        else:
            text_msg = "Error!!"
        self.app.client.chat_postMessage(channel=self.channel_id, text=text_msg, blocks=[
            {
                "type": "divider"
            },
            {
                "type": "section",
                "text": {
                        "type": "mrkdwn",
                        "text": "Hey " + user + ", " + data,
                }
            },
            {
                "type": "divider"
            },
        ])
