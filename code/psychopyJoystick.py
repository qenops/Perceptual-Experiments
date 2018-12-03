import sys, os
sys.path.append('./submodules')
from psychopy.hardware import joystick
from psychopy import visual, event, core

joystick.backend='pyglet'  # must match the Window
win = visual.Window([400,400], winType='pyglet')

nJoys = joystick.getNumJoysticks()  # to check if we have any
id = 0
joy = joystick.Joystick(id)  # id must be <= nJoys - 1

while True:  # while presenting stimuli
    #x = joy.getX()
    hats = joy.getAllHats()
    buttons = joy.getAllButtons()
    axes = joy.getAllAxes()
    print('%s\t%s\t%s'%(hats,buttons,axes))
    win.flip()  # flipping implicitly updates the joystick info
    allKeys = event.getKeys()
    for key in allKeys:
        if key == 'escape':
            core.quit()
    event.clearEvents()
