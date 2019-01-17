import sys, os
sys.path.append('./submodules')
from psychopy import visual, core
import config

win = visual.Window([400,400], screen=1, winType='pyglet',color=[-1,-1,-1])#,fullscr=True)
stim = visual.TextStim(win=win,text='01234',pos=[0,100],units='pix',height=20)
stim.fontFiles = [os.path.join(config.assetsPath,config.stimulusFont)]  # set fontFiles to include our local version of snellen rather than using installed version
stim.font = os.path.splitext(config.stimulusFont)[0]
stim2 = visual.TextStim(win=win,text='01234',pos=[0,-100],units='pix',height=300)
stim2.fontFiles = [os.path.join(config.assetsPath,config.stimulusFont)]  # set fontFiles to include our local version of snellen rather than using installed version
stim2.font = os.path.splitext(config.stimulusFont)[0]

for i in range(20,300):
    stim.height = 2**(i/40)
    stim.draw(win)
    stim2.height = 202-2**(i/40)
    stim2.draw(win)
    win.flip()
    core.wait(.05)

win.close()
core.quit()