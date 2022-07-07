import os
from libs.netty_ops import NettyOps
from libs.netty_auth import NettyAuth
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from pathlib import Path
from dotenv import load_dotenv
import json

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)
SLACK_BOT_TOKEN = os.environ['SLACK_BOT_TOKEN']
SLACK_APP_TOKEN = os.environ['SLACK_APP_TOKEN']

app = App(token=SLACK_BOT_TOKEN)


@app.event("app_home_opened")
def update_home_tab(client, event, logger):
    user_id = event["user"]
    try:
        client.views_publish(
            user_id=user_id,
            view={
                "type": "home",
                "blocks": [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "*Welcome home, <@{}> :house:*".format(user_id),
                        },
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "Learn how to use Netty to interact with your devices :sunglasses:",
                        },
                    },
                    {"type": "divider"},
                    {
                        "type": "section",
                        "text": {
                                "type": "mrkdwn",
                                "text": "*Slash Commands*: \n/netty\n/netty-auth"
                        }
                    },
                    {
                        "type": "section",
                        "text": {
                                "type": "mrkdwn",
                                "text": "*Arguments*: \n-c : Command to execute\n-d : Name of the device\n-u : Username\n-p : Password"
                        }
                    },
                    {
                        "type": "section",
                        "text": {
                                "type": "mrkdwn",
                                "text": "*Usage*: \n/netty -c <command-name> -d <device-name>\n/netty-auth -u <user-name> -p <password>"
                        }
                    }
                ],
            },
        )
    except Exception as e:
        logger.error(f"Error publishing home tab: {e}")


def isArg(str):
    args = ["-c", "-d", "-u", "-p"]
    return str in args


@app.command("/netty")
def nettyOps(ack, respond, command):
    ack()
    user_id = command["user_id"]
    channel_id = command["channel_id"]
    text = command["text"].split()
    arg_pair = {}
    i = 0
    while i < len(text):
        if(isArg(text[i])):
            cur_arg = text[i]
            str = ""
            j = i+1
            while(j < len(text) and not isArg(text[j])):
                str += text[j]
                str += " "
                j += 1
            if len(str) >= 1:
                str = str.rstrip(str[-1])
            arg_pair[cur_arg] = str
            i = j
        else:
            i += 1
    device_name = ""
    command = ""
    try:
        device_name = arg_pair["-d"]
    except:
        app.client.chat_postMessage(
            channel=channel_id, text="Device name not provided!!")
    try:
        command = arg_pair["-c"]
    except:
        app.client.chat_postMessage(
            channel=channel_id, text="Command not provided!!")
    obj = NettyOps(device_name=device_name, channel_id=channel_id,
                   user_id=user_id, app=app, command=command)
    obj.show_header()


@app.command("/netty-auth")
def nettyOps(ack, respond, command):
    ack()
    user_id = command["user_id"]
    channel_id = command["channel_id"]
    text = command["text"].split()
    arg_pair = {}
    i = 0
    while i < len(text):
        if(isArg(text[i])):
            cur_arg = text[i]
            str = ""
            j = i+1
            while(j < len(text) and not isArg(text[j])):
                str += text[j]
                str += " "
                j += 1
            if len(str) >= 1:
                str = str.rstrip(str[-1])
            arg_pair[cur_arg] = str
            i = j
        else:
            i += 1
    username = ""
    password = ""
    try:
        username = arg_pair["-u"]
    except:
        app.client.chat_postMessage(
            channel=channel_id, text="Username not provided!!")
    try:
        password = arg_pair["-p"]
    except:
        app.client.chat_postMessage(
            channel=channel_id, text="Password not provided!!")
    obj = NettyAuth(user_id=user_id, username=username,
                    password=password, app=app, channel_id=channel_id)
    obj.show_header()


if __name__ == "__main__":
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    handler.start()
