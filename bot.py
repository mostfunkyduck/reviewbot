import os
import db
import re
import logging
from slack import RTMClient

class Bot:
    def __init__(self):
        self.db = db.PGDriver()

    def store_review(self, **kwargs):
        return self.db.store_review(reviewtext=kwargs['reviewtext'])

    def retrieve_reviews(self):
        return "\n".join(str(review[0]) for review in self.db.retrieve_reviews())


@RTMClient.run_on(event="message")
def process_message(**payload):
    data = payload["data"]
    user = data["user"] if "user" in data else ""
    text = data["text"] if "text" in data else ""
    web_client = payload["web_client"]
    logging.info(f"received message from [{user}]: [{text}]")

    logging.debug(f"received payload: [{payload}]")
    logging.debug(data)

    
    if "text" not in data:
        return 

    bot_message = False
    if "subtype" in data and data["subtype"] == "bot_message":
        logging.info("received bot message, not responding")
        bot_message = True

    if text and not bot_message:
        logging.debug("received a non-bot message, responding")
        contents = " ".join(text.split(" ")[1:])
        bot.store_review(reviewtext=contents)
        channel_id = data["channel"]
        thread_ts = data["ts"]
        allreviews = bot.retrieve_reviews()
        outgoing_message = str(allreviews)
        logging.debug(f'sending {outgoing_message}')
        web_client.chat_postMessage(
            channel=channel_id,
            text=outgoing_message,
            thread_ts=thread_ts
        )

bot = Bot()
logging.getLogger().setLevel(logging.DEBUG)
slack_token = os.environ["SLACK_BOT_USER_TOKEN"]
rtm_client = RTMClient(token=slack_token)
rtm_client.start()
