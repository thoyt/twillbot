from settings import *
from twitter import *
from twill import *
from random import random

TWEET_PROBABILITY = 0.25
MIN_SIZE = 24
MAX_SIZE = 175
MIN_TREADLES = 4
MAX_TREADLES = 16
TWEET = True

def get_clients():
    auth = OAuth(MY_ACCESS_TOKEN_KEY,
                 MY_ACCESS_TOKEN_SECRET,
                 MY_CONSUMER_KEY,
                 MY_CONSUMER_SECRET,
                 )
    t = Twitter(auth=auth)
    t_up = Twitter(domain='upload.twitter.com', auth=auth)
    return t, t_up

if __name__=='__main__':
    if random() < TWEET_PROBABILITY:
        t, t_up = get_clients()
        params, filename = generate_random_twill(MIN_SIZE, MAX_SIZE,
                min_treadles=MIN_TREADLES, max_treadles=MAX_TREADLES)
        status = "sequence: %s warp: %s weft: %s" % (
                     ''.join(map(str, params['treadle_sequence'])),
                     ''.join(map(str, params['warp'])),
                     ''.join(map(str, params['weft']))
                     )
        if TWEET:
            with open(filename, "rb") as image:
                imagedata = image.read()
                img_id = t_up.media.upload(media=imagedata)["media_id_string"]
                t.statuses.update(status=status, media_ids=img_id)
