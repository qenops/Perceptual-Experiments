#!/usr/bin/python
''' 
Perceptual experiment for testing the latency of human perception in relation to focal change, frequency, and contrast
    
David Dunn
Oct 2018 - created
www.qenops.com
'''
__author__ = ('David Dunn')
__version__ = '1.0'

import sys, os
sys.path.append('./submodules')
#import dDisplay.varifocal as vf
#import dGraph as dg
#import dGraph.ui as dgui
#import dGraph.cameras as dgc
#import dGraph.shapes as dgs
#import dGraph.render as dgr
#import dGraph.materials as dgm
#import dGraph.shaders as dgshdr
#import dGraph.lights as dgl
#import dGraph.util.imageManip as dgim
#import multiprocessing as mp
from psychopy import visual, core, gui, data, event
from psychopy.tools.filetools import fromFile, toFile
import config
import numpy as np
import time, math

def genLogicPrimer():
    TF = bool(random.getrandbits(1))
    first = random.randint(0, 9)
    second = random.randint(0, 9)
    offset = 0
    if not TF:
        while offset == 0:
            offset = random.randint(-2, 2)
    sum = first + second + offset
    return "%d+%d=%d"%(first, second, sum), TF

def getUser():
    try:  # load the users file
        allUsers = fromFile(os.path.join(config.dataPath,config.userFile))
    except:  # if not there then use a default set
        allUsers = []
    userInfo = {'Name':'','Age':20}
    userInfo['Date'] = data.getDateStr()  # add the current time
    userInfo['ID'] = len(allUsers)
    # present a dialogue to change params
    dlg = gui.DlgFromDict(userInfo, title='User Info', fixed=['Date','ID'])
    if dlg.OK:
        allUsers.append(userInfo)
        toFile(os.path.join(config.dataPath,config.userFile), allUsers)  # save users to file for next time
    else:
        core.quit()  # the user hit cancel so exit
    return userInfo

def setup():
    userInfo = getUser()
    # make a text file to save data
    fileName = 'data_%s_%s'%(userInfo['ID'],userInfo['Date'])
    dataFile = open(os.path.join(config.dataPath,'%s.csv'%fileName), 'w')  # a simple text file with 'comma-separated-values'
    dataFile.write('primeDepth,primeCorrect,stimDepth,orientation,contrast,frequency,latency,correct\n')

    # create the staircase handler
    staircase = data.StairHandler(startVal = 60,
                            stepType = 'db', stepSizes=[8,4,4,2],
                            nUp=1, nDown=3,  # will home in on the 80% threshold
                            nTrials=1)
    #staircase = data.QuestHandler(startVal=60, startValSd=30, pThreshold=0.82,nTrials=20)

    #create the windows and stimuli
    windows = []
    for monitor in config.monitors:
        win = visual.Window(monitor.getSizePix(), monitor=monitor, screen=monitor.screen, fullscr=True, units="deg",color=[-1,-1,-1])
        windows.append(win)

    primeStim = visual.TextStim(win=win,font='Snellen', height=.5,pos=[0,0]) # may want to set fontFiles to include our ennumbered version of snellen (once it is complete)
    #text, answer = genLogicPrimer()
    #primeStim.text = text
    grating = visual.GratingStim(win=win, mask="circle", size=3, pos=[0,0], sf=10)
    postGrating = visual.GratingStim(win=win, mask="circle", size=3, pos=[0,0], sf=10)
    return windows, grating


def loop(windows, grating):
    for i in range(3):
        for win in windows:
            grating.draw(win)
            win.flip()
            core.wait(3.0)
            win.flip()

    for win in windows:
        win.close()
    core.quit()

if __name__ == '__main__':
    loop(*setup())
