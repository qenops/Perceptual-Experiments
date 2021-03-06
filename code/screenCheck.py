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
    win = visual.Window(monitor.getSizePix(), monitor=monitor, screen=monitor.screen, fullscr=True, units="deg", viewPos=monitor.center, color=[-1,-1,-1])
    stim = visual.TextStim(win=win,font='Bookman', height=2, pos=monitor.center, text='%s'%monitor.name, flipHoriz=monitor.flipHoriz) # may want to set fontFiles to include our local version of snellen rather than using installed version
    windStims.append((win,stim))
    #fontFiles = [os.path.join(config.assetsPath,config.stimulusFont)]  # set fontFiles to include our local version of snellen rather than using installed version
    #font = os.path.splitext(config.stimulusFont)[0]
    #textStim = visual.TextStim(win=win,height=15/60,pos=monitor.center,autoLog=True, fontFiles=fontFiles, font=font, text="O")
    #windStims.append((win,textStim))
for win, stim in windStims:
    stim.draw(win)
    win.flip()
core.wait(20.0)
for win, stim in windStims:
    win.flip()
    win.close()
core.quit()
