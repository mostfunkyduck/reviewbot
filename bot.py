import os
import db
import re
import logging
import traceback
from slack import RTMClient

class Bot:
    def __init__(self):
        # this is the same environment variable that postgres uses, so you only
        # need to pass it once to compose
        self.db = db.PGDriver(password=os.environ["POSTGRES_PASSWORD"])
        self.userid = None
        slack_token = os.environ["SLACK_BOT_USER_TOKEN"]
        self.rtm_client = RTMClient(token=slack_token)

    # if we don't call this separately, the 'open' command will be processed
    # before the bot finishes initializing 
    def start(self):
        self.rtm_client.start()

    def store_review(self, **kwargs):
        r = db.Review(
            text=kwargs["text"],
            tag=kwargs["tag"]
        )

        return self.db.store_review(r)

    def retrieve_reviews(self, tag=None):
        results = self.db.retrieve_reviews(tag)
        if not results:
            return None
        return results

    def remove_review_by_key(self, key):
        return self.db.remove_review(key)

    # given the message sent to the bot with the leading tag and command stripped
    # parses out the review
    def add(self, message):
        # quick and dirty way to do it, could also use regex backcaptures, but I hate regexes
        components = message.split(" ")
        tag = components[0]
        text = components[1:]
        bot.store_review(text=" ".join(text), tag=tag)
        return f"review tagged with '{tag}' added, use list to see its ID" 

    def list(self, tag=None):
        results = [str(r) for r in self.retrieve_reviews(tag)]
        logging.debug(f"retrieved list results {results}")
        if not results:
            return f"no results for tag '{tag}'!"
        return "\n".join(results)

    def remove(self, key):
        self.db.remove_review(key)
        return f"removed {key}"

    def help(self):
        return """
        I am a reviewbot, I help with reviews. Isn't that nice of me?
        Currently, I respond to the following commands when tagged:

            add <tag> <review information>: adds a review to the list, with an author for reference purposes

            list [<tag>]: shows reviews currently in motion

            remove <review ID>: removes a review from the list
        """

    # takes original payload, picks out what it needs, sends it to the channel
    # current sending as a thread response
    def send_message(self, **kwargs):
        message = kwargs["message"]
        logging.debug(f'sending {message}')
        channel_id = kwargs["channel"]
        thread_ts  = kwargs["ts"]
        kwargs["web_client"].chat_postMessage(
            channel=channel_id,
            text=message,
            thread_ts=thread_ts
        )

    def set_userid(self, userid):
        self.userid = userid

@RTMClient.run_on(event="open")
def process_open(**payload):
    logging.info("connection has been opened, extracting user ID for bot")
    if "data" not in payload or "self" not in payload["data"] \
        or "id" not in payload["data"]["self"]:
        logging.error(f"i don't know who i am!, this payload was not correctly formatted: [{payload}]")

    myself = payload["data"]["self"]["id"]
    logging.debug(f'I am: {str(myself)}')
    bot.userid = myself

@RTMClient.run_on(event="message")
def process_message(**payload):

    data = payload["data"]
    user = data.get("user", "")
    text = data.get("text", "")

    if not re.match(r"^<@" + bot.userid + ">", text):
        # this isn't tagging the bot
        logging.debug("saw message that wasn't intended for us")
        return

    logging.info(f"received message from [{user}]: [{text}]")

    logging.debug(f"received payload: [{payload}]")
    logging.debug(data)

    
    if "text" not in data:
        return 

    if "subtype" in data and data["subtype"] == "bot_message":
        logging.info("received bot message, not responding")
        return

    if "channel" in payload:
        # just for fun
        bot.rtm_client.typing(channel=payload["channel"])

    if text: 
        logging.debug("received a non-bot message, responding")
        
        # split it up by spaces to pick out author 
        contents = text.replace(f'<@{bot.userid}> ', '').split(" ")
        command = contents[0]
        arguments = " ".join(contents[1:])
        message = ""
        try:
            if command == "add":
                message = bot.add(arguments)
            elif command == "list":
                message = bot.list(arguments)
            elif command == "remove":
                message = bot.remove(arguments)
            elif command == "help":
                message = bot.help()

        except Exception as e:
            message = f'something bad happened :freakout: : {traceback.format_exc()}'

        logging.debug(f"{payload}")
        if message:
            bot.send_message(
                channel=data["channel"],
                ts=data["ts"], 
                web_client=payload["web_client"],
                message=message
            )

logging.getLogger().setLevel(logging.DEBUG)
logging.info("starting bot")
bot = Bot()
bot.start()
