import time
import pygetwindow as gw

import cv2
import numpy as np
from mss import mss

from ARSL import mouse

class AutoRSL:
    def __init__(self):
        self.renderFPS = False
        self.imgCache = {}

        self.activateRSL()

    def activateRSL(self):
        RSL = gw.getWindowsWithTitle("RAID: Shadow Legends")[0]
        RSL.maximize()
        RSL.activate()
        time.sleep(0.25)

    def getImage(self, filename):
        if filename in self.imgCache: return self.imgCache[filename]
        else: self.imgCache[filename] = cv2.imread(filename)
        return self.getImage(filename)

    def rectsForTemplateInFrame(self, filename, threshold = 0.9):
        template = self.getImage(filename)
        h, w = template.shape[:-1]

        res = cv2.matchTemplate(self.frame, template, cv2.TM_CCOEFF_NORMED)    # This seems to be what is slowing things down so much
        loc = np.where(res >= threshold)[::-1]    # [::-1] to swap collumns with rows (still not sure why this is backwards by default...)

        rects = []
        for pt in zip(*loc): rects.append((pt[0], pt[1], pt[0] + w, pt[1] + h))

        return rects

    # Returns only the first occurrance
    def centerPointForTemplateInFrame(self, template, threshold = 0.9) -> tuple:
        rects = self.rectsForTemplateInFrame(template, threshold = threshold)
        if len(rects) == 0: return None    # [TODO] Decide if I want to change this up to be... better somehow?

        pt = rects[0]
        pt = (pt[0] + (pt[2] - pt[0]) // 2, pt[1] + (pt[3] - pt[1]) // 2)
        return pt

    def currentLocation(self):
        locs = {}
        locs["bastion"] = "Loc_Bastion.png"
        locs["greatHall"] = "Loc_GreatHall.png"
        locs["classicArena"] = "Loc_ClassicArena.png"
        locs["sparringPit"] = "Loc_SparringPit.png"
        locs["tavern"] = "Loc_Tavern.png"

        for loc in locs:
            if self.centerPointForTemplateInFrame(locs[loc]) is not None:
                return loc

        return "Unknown Location"

    # The screenshot scanning is done here since I don't want to figure out how to do it asynchronously
    # Also calling it seperatly seems to require mss().grab() to reinstantiate each time slowing things down considerably
    def run(self):
        with mss() as sct:
            time_last = time.time()
            while True:
                # [TODO] I REALLY want to make this asynchronous...
                monitor_1 = sct.monitors[1]
                self.frame = sct.grab(monitor_1)
                self.frame = cv2.cvtColor(np.array(self.frame), cv2.COLOR_BGRA2BGR)    # Converts to correct color schmema

                # It seems image recognition is the thing that takes such a long time
                # [TODO] Find a way of accomplishing this faster?
                #a = self.rectsForTemplateInFrame("LOC_Bastion.png")
                #print(a)

                loc = self.currentLocation()
                print(loc)

                time_curr = time.time()
                time_delta = time_curr - time_last
                time_last = time_curr
                fps = int(time_delta * 1000)    # [TODO/BUG] Find out if this is the correct calculation... Not really sure if it is accurate
                if self.renderFPS: print(f"FPS: {fps}")

arsl = AutoRSL()
arsl.run()
