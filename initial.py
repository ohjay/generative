#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import cairo
import numpy as np

# =====================
# Parameters
# =====================

IMG_WIDTH = 1000
IMG_HEIGHT = 1000
ALPHA = 1.0
NUM_STEPS = 9500
EPS = 1e-9
PROPORTION_NEW = 0.05
INIT_X = 0.5
INIT_Y = 0.45

OUT_FILEPATH = 'initial.png'

# =====================
# Drawing code
# =====================

class Artist(object):
    def __init__(self):
        self._init_cairo()
        self.pos = np.array([INIT_X, INIT_Y])  # (x, y)
        self.direction = np.array([1.0, 0.0])  # (x, y)
        self.iteration = 0
        self.noise = 0.000005

    def _init_cairo(self):
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, IMG_WIDTH, IMG_HEIGHT)
        context = cairo.Context(surface)
        context.scale(IMG_WIDTH, IMG_HEIGHT)
        context.set_source_rgb(1.0, 1.0, 1.0)  # background color
        context.rectangle(0.0, 0.0, 1.0, 1.0)  # the entire image, due to scale
        context.fill()

        self.surface = surface
        self.context = context

    def step(self):
        color = self.iteration % 16777216  # hex representation as an integer
        b = color % 256
        g = (color // 256) % 256
        r = (color // 65536) % 256
        self.context.set_source_rgba(float(r) / 255, float(g) / 255, float(b) / 255, ALPHA)

        # Select location
        scale = float(self.iteration) / 256 + np.random.normal(1, self.noise)
        self.pos += (self.direction + np.random.normal(0, self.noise, (2,))) * scale / max(IMG_WIDTH, IMG_HEIGHT)
        self.context.rectangle(self.pos[0], self.pos[1],
                               1.0 / IMG_WIDTH * scale, 1.0 / IMG_HEIGHT * scale)
        self.context.fill()

        # Update
        direction_perp = [None, None]  # perpendicular, right-facing direction
        if self.direction[1] > 0:
            # First or second quadrant
            direction_perp[0] = -100.0  # recall that +y is down
        else:
            direction_perp[0] = 100.0  # otherwise these would be reversed
        direction_perp[1] = -direction_perp[0] * self.direction[0] / (self.direction[1] + EPS)
        direction_perp = np.array(direction_perp) / (np.linalg.norm(direction_perp) + EPS)

        self.direction = PROPORTION_NEW * direction_perp + (1.0 - PROPORTION_NEW) * self.direction
        self.direction /= np.linalg.norm(self.direction) + EPS
        self.iteration += 1
        self.noise += np.random.normal(0, self.noise / 2)
        if self.noise <= 0:
            self.noise = EPS

    def save_image(self, filepath):
        self.surface.write_to_png(filepath)

# =====================
# Managerial code
# =====================

def main():
    artist = Artist()
    for _ in range(NUM_STEPS):
        artist.step()
    artist.save_image(OUT_FILEPATH)

if __name__ == '__main__':
    sys.exit(main())
