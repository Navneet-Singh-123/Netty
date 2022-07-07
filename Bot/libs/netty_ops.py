from imp import init_builtin
import os
from mimetypes import init
import requests
from threading import Thread

# Fetching the operational state of the network device

class NettyOps:

    def __init__(self, device_name, channel_id, user_id, app, command):
        self.device_name = device_name
        self.channel_id = channel_id
        self.user_id = user_id
        self.app = app
        self.command = command
        self.initial_msg = "Working on your request "
        self.final_msg = "your request is processed!!"

    def initiate(self):
        url = os.environ["URL"] + "/device/" + self.device_name
        PARAMS = {'command': self.command, 'user_id': self.user_id}
        r = requests.get(url=url, params=PARAMS)
        status_code = r.status_code
        user = "<@"+self.user_id+">"
        data = str(r.text)
        print("Processed...")
        data = data.replace(r"\r\n", "\n")

        self.display_result(user, data, status_code)

    def show_header(self, *args, **kwargs):
        self.app.client.chat_postMessage(
            channel=self.channel_id, text=self.initial_msg + "for the command " + "\'" + self.command + "\'" + " on device " + "\'" + self.device_name)
        background = Thread(target=self.initiate, args=[])
        background.start()

    def display_result(self, user, data, status_code):
        if status_code == 200:
            text_msg = "Successful!!"
        else:
            text_msg = "Error!!"
        strs = []
        t_len = 3000
        while len(data) >= t_len:
            start = data[:t_len]
            end = data[t_len:]
            strs.append(start)
            data = end
        if len(data):
            strs.append(data)
        self.app.client.chat_postMessage(channel=self.channel_id, text=text_msg, blocks=[
            {
                "type": "divider"
            },
            {
                "type": "section",
                "text": {
                        "type": "mrkdwn",
                        "text": "Hey " + user + ", " + self.final_msg,
                }
            },
            {
                "type": "divider"
            },
        ])
        for i in range(0, len(strs)):
            self.app.client.chat_postMessage(channel=self.channel_id, text=text_msg, blocks=[
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": strs[i],
                    }
                },
            ])

        self.app.client.chat_postMessage(channel=self.channel_id, text=text_msg, blocks=[
            {
                "type": "divider"
            },
        ])
