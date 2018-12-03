import pyglet
window = pyglet.window.Window()
platform = pyglet.window.get_platform()
display = platform.get_default_display()
for idx, screen in enumerate(display.get_screens()):
    print(idx, screen)
window.close()

import sys, os
sys.path.append('./submodules')
from psychopy import visual, core, gui, data, event
import config
windStims = []
for monitor in config.monitors:
    win = visual.Window(monitor.getSizePix(), monitor=monitor, screen=monitor.screen, fullscr=True, units="deg",color=[-1,-1,-1])
    stim = visual.TextStim(win=win,font='Snellen', height=3, pos=[0,0], text='%s'%monitor.screen, flipHoriz=monitor.flipHoriz) # may want to set fontFiles to include our local version of snellen rather than using installed version
    windStims.append((win,stim))
for win, stim in windStims:
    stim.draw(win)
    win.flip()
core.wait(10.0)
for win, stim in windStims:
    win.flip()
    win.close()
core.quit()
