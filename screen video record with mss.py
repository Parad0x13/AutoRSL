import time
import cv2
import numpy as np
from mss import mss

mon = {'top': 160, 'left': 160, 'width': 200, 'height': 200}
lastFew = []
n = 0
N = 1000
with mss() as sct:
    while True:
        last_time = time.time()
        img = sct.grab(mon)

        t = 1.0 / (time.time() - last_time)
        lastFew.append(t)
        if len(lastFew) == N: lastFew = lastFew[1:]
        print(f"n({n})\tAvg: {sum(lastFew) / len(lastFew)}")
        n += 1

        cv2.imshow('test', np.array(img))
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
