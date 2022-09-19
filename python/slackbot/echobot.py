import os
from pathlib import Path
from dotenv import load_dotenv
from slack_bolt import App

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

app = App(token=os.environ.get("SLACK_BOT_TOKEN"),
          signing_secret=os.environ.get("SLACK_SIGN_SECRET"))


@app.message("")
def message_hello(message, say):
    say(
        blocks=[
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"Hey there <@{message['user']}>!"},
                "accessory": {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "Click Me"},
                    "action_id": "button_click"
                }
            }
        ],
        text=f"Hey there <@{message['user']}>!"
    )


@app.action("button_click")
def action_button_click(body, ack, say):
    # Acknowledge the action
    ack()
    say(f"<@{body['user']['id']}> clicked the button")


@app.command("/echo")
def echo_back(ack, say, command):
    ack()
    say(command['text'])
    say(f"you said... {command['text']}")


if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))