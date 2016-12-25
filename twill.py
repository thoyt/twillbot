import numpy as np
import scipy.misc as smp
from hashlib import md5
from random import randint, random, getrandbits

def create_twill(N, warp, weft, treadles=4, treadle_sequence=np.array([1,2,3,4]),
                 save=False, size=(1000,1000)):
    L = len(warp)
    M = len(weft)
    # Generate the twill
    data = np.zeros((N, N, 3), dtype=np.uint8)
    thread_ix = np.arange(N)
    for i in range(N):
        k = i % M
        shaft = treadle_sequence[i % treadles]
        data[i,:] = weft[k]
        visible_warp = np.where((thread_ix + shaft) % treadles < treadles / 2)[0]
        for ind in visible_warp:
            data[i,ind] = warp[ind % L]

    data = smp.imresize(data, size, interp='nearest')
    if save:
        filename = 'patterns/twill_%s.png' % getrandbits(32)
        smp.imsave(filename, data)
        return data, filename
    else:
        return data, None

def generate_random_twill(min_N, max_N, min_treadles=2, max_treadles=10, size=(1000,1000)):
    # Grid size is NxN
    N = randint(min_N, max_N)

    # Color selection
    COMPLEMENT, GRAYSCALE, RANDOM = 1, 2, 3
    colorscheme = randint(1,3)
    if colorscheme == COMPLEMENT:
        rr, gg, bb = randint(0,255), randint(0,255), randint(0,255)
        b = np.array([rr,gg,bb])
        w = np.array([255-rr,255-gg,255-bb])
    elif colorscheme == GRAYSCALE:
        n, m = randint(0,255), randint(0,255)
        b = np.array([n,n,n])
        w = np.array([m,m,m])
    elif colorscheme == RANDOM:
        r1, g1, b1 = randint(0,255), randint(0,255), randint(0,255)
        r2, g2, b2 = randint(0,255), randint(0,255), randint(0,255)
        b = np.array([r1,g1,b1])
        w = np.array([r2,g2,b2])

    # Warp and weft sizes are 1-4
    L, M = randint(1,4), randint(1,4)

    # Construct the warp and weft
    warp_seed = [1 if random() < 0.5 else 0 for _ in range(L-1)] + [0]
    if all(v == 0 for v in warp_seed):
        warp_seed[0] = 1
    weft_seed = [1 if random() < 0.5 else 0 for _ in range(M-1)] + [1]
    if all(weft_seed):
        weft_seed[0] = 0
    warp = [b if x == 1 else w for x in warp_seed]
    weft = [b if x == 1 else w for x in weft_seed]
    treadles = randint(min_treadles, max_treadles)
    treadle_sequence = np.random.permutation(treadles).tolist()

    params = {'treadles': treadles,
              'treadle_sequence': treadle_sequence,
              'warp': warp_seed,
              'weft': weft_seed
              }
    _, filename = create_twill(N, warp, weft, treadles=treadles,
                               treadle_sequence=treadle_sequence,
                               save=True, size=size)
    return params, filename
