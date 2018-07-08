#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import cairo
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# ================================================
# Initial state parameters
# ================================================

# todo

# ================================================
# Leaf growth parameters
# ================================================

# todo

# ================================================
# Auxin source / vein development parameters
# ================================================

# todo

# ================================================
# Other parameters
# ================================================

IMG_WIDTH = 1000
IMG_HEIGHT = 1000
NUM_STEPS = 100
OUT_FILEPATH = 'venation.png'

# ================================================
# Drawing code
# ================================================

class Artist(object):
    def __init__(self):
        self._init_cairo()
        self.iteration = 0
        self.node_no = 0

        self.G = nx.Graph()
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(1, 1, 1)

    def _init_cairo(self):
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, IMG_WIDTH, IMG_HEIGHT)
        context = cairo.Context(surface)
        context.scale(IMG_WIDTH, IMG_HEIGHT)
        context.set_source_rgb(1.0, 1.0, 1.0)  # background color
        context.rectangle(0.0, 0.0, 1.0, 1.0)  # the entire image, due to scale
        context.fill()

        context.set_source_rgba(0.0, 0.0, 0.0, 1.0)  # black, for now

        self.surface = surface
        self.context = context

    def step(self, i):
        self.G.add_node(self.node_no, pos=(np.random.random(), np.random.random()))
        self.G.add_node(self.node_no + 1, pos=(np.random.random(), np.random.random()))
        self.G.add_edge(self.node_no, self.node_no + 1)
        self.node_no += 2

        pos = nx.get_node_attributes(self.G, 'pos')
        self.ax.clear()
        nx.draw(self.G, pos, ax=self.ax)

    def run(self):
        fa = animation.FuncAnimation(
            self.fig, self.step, frames=NUM_STEPS, interval=100, repeat=False)
        plt.show()

    def save_image(self, filepath):
        # todo draw image on Cairo surface, then save
        self.surface.write_to_png(filepath)

# ================================================
# Managerial code
# ================================================

def main():
    artist = Artist()
    artist.run()

if __name__ == '__main__':
    sys.exit(main())
