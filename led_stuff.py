import numpy as np
from matplotlib import pyplot as plt
from matplotlib.colors import hsv_to_rgb
from itertools import cycle, permutations
from matplotlib.animation import FuncAnimation



def make_rgb_color(h,s,v):
    
    return tuple(int(np.round(c * 255)) for c in hsv_to_rgb((h, s, v)))

def make_frgb_color(h, s, v):
    clr = list(hsv_to_rgb((h,s,v)))
    clr.append(1.0)
    
    return tuple(clr)

def hue_to_rgb_cycler(num_values, h_offset=0, s=1.0, v=1.0):
    hue_cycler = cycle(np.arange(0.0, 1.0, 1.0 / num_values))
    
    for i in range(h_offset):
        next(hue_cycler)
    
    for h in hue_cycler:
        #yield make_rgb_color(h, s, v)
        yield make_frgb_color(h, s, v)


def calc_lissajous(r1, r2, num_vals):
    
    #t_fac = r1 % r2 if r1 > r2 else r2 % r1
    t_fac = max((r1%r2, r2%r1)) * 10
    
    t_vals = np.linspace(0, 2 * np.pi * t_fac, num_vals)
    data = np.ndarray(shape=(2, num_vals))
    data[0, :] = np.sin(t_vals * r1 + 0.5*np.pi)
    data[1, :] = np.sin(t_vals * r2)

    return data

def fraction_cycler(num_values):

    perms = list(np.linspace(0.25, 8, num_values))
    yield from cycle(permutations(perms, 2))
    

numframes = 1000
num_leds = 400
step = 1.0 / num_leds
v = s = 1.0
color_pos = 0
cycler = hue_to_rgb_cycler(num_values=num_leds, h_offset=color_pos)
f_cycle = fraction_cycler(num_leds)


class LissajousScatterAnimation(object):

    def __init__(self, num_leds, num_frames):

        self.fig = plt.figure(facecolor='k')

        self.ax = self.fig.add_subplot(1,1,1)#, axisbg='k')
        self.ax.get_xaxis().set_visible(False)
        self.ax.get_yaxis().set_visible(False)
        self.numframes = num_frames
        self.num_leds = num_leds
        
        color_pos = 0
        self.clr_cycler = hue_to_rgb_cycler(num_values=self.num_leds, h_offset=color_pos)
        self.f_cycler = fraction_cycler(self.num_leds)

        self.animation = FuncAnimation(self.fig, self.update, interval=25, 
                                           init_func=self.setup_plot, blit=True)

        self.stream = self.data_stream()

    def setup_plot(self):
        data, clrs = next(self.stream)
        self.scat = self.ax.scatter(data[0,:], data[1,:], c=clrs, animated=True, s=150)
        self.ax.axis([-1.2, 1.2, -1.2, 1.2])

        # For FuncAnimation's sake, we need to return the artist we'll be using
        # Note that it expects a sequence of artists, thus the trailing comma.
        return self.scat,

    def data_stream(self):

        while True:
            f1, f2 = next(self.f_cycler)
            t_vals = np.linspace(0, 2*np.pi, self.num_leds)
            
            data = calc_lissajous(f1, f2, self.num_leds)
            next(self.clr_cycler)
            clrs = [next(self.clr_cycler) for i in range(self.num_leds)]
            yield data, clrs
        
    def update(self, i):
        """Update the scatter plot."""
        data, clrs = next(self.stream)

        self.scat.set_offsets(data)

        self.scat.set_facecolor(clrs)

        return self.scat,

    def show(self):

        self.fig.show()


class LissajousLineAnimation(object):
    def __init__(self, num_leds, num_frames):
        self.fig = plt.figure(facecolor='k')

        self.ax = self.fig.add_subplot(1, 1, 1) # , axisbg='k')
        self.ax.set_facecolor((0,0,0))
        self.ax.get_xaxis().set_visible(False)
        self.ax.get_yaxis().set_visible(False)
        self.numframes = num_frames
        self.num_leds = num_leds

        color_pos = 0
        self.clr_cycler = hue_to_rgb_cycler(num_values=self.num_leds, h_offset=color_pos)
        self.f_cycler = fraction_cycler(self.num_leds)

        self.animation = FuncAnimation(self.fig, self.update, interval=50,
                                       init_func=self.setup_plot, blit=False)

        self.stream = self.data_stream()

    def setup_plot(self):
        print("setup")
        data, clr = next(self.stream)
        self.lines, = self.ax.plot(data[0, :], data[1, :], c=clr, lw=3)
        self.ax.axis([-1.2, 1.2, -1.2, 1.2])

        # For FuncAnimation's sake, we need to return the artist we'll be using
        # Note that it expects a sequence of artists, thus the trailing comma.
        return self.lines,

    def data_stream(self):
        while True:
            f1, f2 = next(self.f_cycler)
            t_vals = np.linspace(0, 2 * np.pi, self.num_leds)

            data = calc_lissajous(f1, f2, self.num_leds)
            #next(self.clr_cycler)
            #clrs = [next(self.clr_cycler) for i in range(self.num_leds)]
            yield data, next(self.clr_cycler)

    def update(self, i):
        """Update the scatter plot."""
        data, clr = next(self.stream)

        self.lines.set_data(data)

        self.lines.set_color(clr)

        return self.lines,

    def show(self):
        self.fig.show()


if __name__ == '__main__':
    anim = LissajousLineAnimation(num_frames=1000, num_leds=500)
    anim.show()

