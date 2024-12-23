import os
import requests
import feedparser
import logging
from datetime import timedelta, datetime, timezone
from dateutil import parser
from dotenv import load_dotenv
from time import sleep

TRIPS_CHANNEL_ID: str = None
MANAGEMENT_CHANNEL_ID: str = None
BOT_TOKEN: str = None

ATOM_FEED_URLS = [
    'https://travelfree.info/feed',
    'https://www.fly4free.com/flights/flight-deals/europe/feed/'
]

MATCHES = [
    "argentina", "bogota", "buenos aires", "chile",
    "hanoi", "japan", "korea", "lima", "peru", "santiago",
    "seoul", "tokyo"
]

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def send_message(channel, message):
    response = requests.post(f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={channel}&text={message}')
    
    if response.status_code != 200:
        logging.error(f'Error sending message to channel {channel}: {response.status_code} - {response.json()}')
        print(f'Error sending message to channel {channel}: {response.status_code} - {response.json()}')
    

def match_destination(deal):
    intersection = set(MATCHES).intersection(set(deal.lower().split()))
    return len(intersection) > 0


def parse_feed(feed_url):
    print(f'Parsing {feed_url}..')
    rss_feed = feedparser.parse(feed_url)
    for entry in rss_feed.entries:
        print("Processing entry: " + entry.title + " " + entry.published)
        parsed_date = parser.parse(entry.published)
        ## this feed is in UTC
        parsed_date = parsed_date.astimezone(timezone.utc)
        ## parsed_date = (parsed_date + timedelta(hours=2)).replace(tzinfo=None) # remove timezone offset
        now_date = datetime.now(timezone.utc)
        published_hour_ago = now_date - parsed_date < timedelta(minutes=60)
        
        if published_hour_ago and match_destination(entry.title):
            send_message(TRIPS_CHANNEL_ID, entry.title + "\n" + parsed_date.strftime("%d/%m/%Y, %H:%M:%S") + "\n" + entry.link)

def parse_feeds():
    for feed in ATOM_FEED_URLS:
        parse_feed(feed)

def load_globals():
    global TRIPS_CHANNEL_ID, MANAGEMENT_CHANNEL_ID, BOT_TOKEN
    
    TRIPS_CHANNEL_ID = os.environ.get('TRIPS_CHANNEL_ID')
    MANAGEMENT_CHANNEL_ID = os.environ.get('MANAGEMENT_CHANNEL_ID')
    BOT_TOKEN = os.environ.get('BOT_TOKEN')

def lambda_handler(event, context):
    load_globals()
    send_message(MANAGEMENT_CHANNEL_ID, "⌛ Executing TripWatcher.. ")
    parse_feeds()


if __name__ == "__main__":
    load_dotenv()
    load_globals()

    while(True):
      parse_feeds()
      sleep(60 * 60)
