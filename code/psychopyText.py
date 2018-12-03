import sys, os
sys.path.append('./submodules')
from psychopy import visual, core

win = visual.Window([400,400], winType='pyglet',color=[-1,-1,-1])#,fullscr=True)
stim = visual.TextStim(win=win,font='Snellen',text='01234',pos=[0,100],units='pix',height=20)
stim2 = visual.TextStim(win=win,font='Snellen',text='01234',pos=[0,-100],units='pix',height=300)

for i in range(20,300):
    stim.height = 2**(i/40)
    stim.draw(win)
    stim2.height = 202-2**(i/40)
    stim2.draw(win)
    win.flip()
    core.wait(.05)

win.close()
core.quit()