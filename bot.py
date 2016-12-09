from settings import *
from twitter import *
from twill import *

def get_clients():
    auth = OAuth(MY_ACCESS_TOKEN_SECRET,
                 MY_ACCESS_TOKEN_KEY,
                 MY_CONSUMER_SECRET,
                 MY_CONSUMER_KEY)
    t = Twitter(auth=auth)
    t_up = Twitter(domain='upload.twitter.com', auth=auth)
    return t, t_up

if __name__=='__main__':
    n_twills = 1
    t, t_up = get_clients()
    for _ in range(n_twills):
        params, filename = generate_random_twill(16, 64, max_treadles=10)
        status = "treadle sequence: %s, warp: %s, weft: %s" % (
                     ''.join(map(str, params['treadle_sequence'])),
                     ''.join(map(str, params['warp'])),
                     ''.join(map(str, params['weft']))
                     )
        with open(filename, "rb") as image:
            imagedata = image.read()
            id_img1 = t_up.media.upload(media=imagedata)["media_id_string"]
            id_img2 = t_up.media.upload(media=imagedata)["media_id_string"]
            t.statuses.update(status=status,
                              media_ids=",".join([id_img1, id_img2]))
