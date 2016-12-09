import numpy as np
import scipy.misc as smp
from hashlib import md5
from random import randint, random, getrandbits

def create_twill(N, warp, weft, treadles=4, save=False, size=(1000,1000)):

    # Generate the twill
    data = np.zeros((N, N, 3), dtype=np.uint8)
    thread_ix = np.arange(N)
    treadle_sequence = np.random.permutation(treadles)
    for i in range(N):
        k = i % M
        shaft = treadle_sequence[i % treadles]
        data[i,:] = weft[k]
        visible_warp = np.where((thread_ix + shaft) % treadles < treadles / 2)[0]
        for ind in visible_warp:
            data[i,ind] = warp[ind % L]
    
    data = smp.imresize(data, size, interp='nearest')
    #img = smp.toimage(data)
    #img.show()
    if save:
        print getrandbits(128)
        smp.imsave('foo.png', data)
    return data

# Grid size is NxN
N = randint(16,256)

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
warp = [b if random() < 0.5 else w for _ in range(L-1)] + [w]
weft = [b if random() < 0.5 else w for _ in range(M-1)] + [b]
treadles = randint(2, 10)

create_twill(N, warp, weft, treadles=treadles, save=True)
