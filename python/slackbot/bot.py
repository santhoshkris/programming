#!/usr/local/bin/python
"""Bot in Slack."""

import slack
from dotenv import load_dotenv
import os
from flask import Flask
from flask import request
from slackeventsapi import SlackEventAdapter


env_file = os.path.dirname(os.path.realpath(__file__)) + os.sep + ".env"

load_dotenv(env_file)

client = slack.WebClient(token=os.getenv('SLACK_BOT_TOKEN'))
BOT_ID = client.api_call("auth.test")['user_id']

slack_events_adapter = SlackEventAdapter(os.getenv('SLACK_SIGNING_SECRET'), endpoint="/slack/events")


# Create an event listener for 'message sent to channel'
@slack_events_adapter.on('message')
def message(payLoad):
    # print(payLoad)
    event = payLoad.get('event', {})
    channel_id = event.get('channel')
    user_id = event.get('user')
    text = event.get('text')
    if user_id != BOT_ID:
        client.chat_postMessage(channel=channel_id, text=text)


# Create an event listener for "reaction_added" events and print the emoji name
@slack_events_adapter.on("reaction_added")
def reaction_added(event_data):
    emoji = event_data["event"]["reaction"]
    print(emoji)


# Start the server on port 3000
slack_events_adapter.start(port=3000)
