#!/usr/bin/python
''' 
Perceptual experiment for testing human perception 
    
David Dunn
Oct 2018 - created
www.qenops.com
'''
__author__ = ('David Dunn')
__version__ = '1.0'

import sys, os
sys.path.append('./submodules')
import numpy as np
import random
from abc import ABC, abstractmethod

from psychopy import visual, core, gui, data, event, logging
from psychopy.tools.filetools import fromFile, toFile
from psychopy.hardware import joystick

BACKEND = 'pyglet'
SPF = .016          # seconds per frame

class Experiment(ABC):
    def __init__(self, config, storeData=True, windows=None, joystick=True, joy=None, acuity=None, ipd=None):
        self.config = config
        self.storeData = storeData
        self.setupLogging()
        self.clock = core.Clock()
        self.timer = core.Clock()
        self.setupWindows(windows)
        if joystick:
            self.setupJoystick(joy)
        if self.storeData:
            self.getUser(acuity,ipd)
            self.dataKeys = None
            self.data = None
            self.dataFile = None
            self.setupData()
        self.setupStimuli()
        self.setupHandler()
    def setupLogging(self):
        logging.console.setLevel(logging.ERROR)
        self.log = logging.LogFile(self.config.logFile, level=self.config.logLevel, filemode='w')
    def setupWindows(self, windows=None):
        if windows is not None:
            self.windows = windows
        else:
            #create the windows
            self.windows = [] 
            for monitor in self.config.monitors:
                win = visual.Window(monitor.getSizePix(), monitor=monitor, screen=monitor.screen, name=monitor.name, fullscr=True, units="deg", viewPos=monitor.center, color=monitor.color,waitBlanking=False)
                win.flipHoriz = monitor.flipHoriz
                self.windows.append(win)
        self.activeWindows = []
    def setupJoystick(self, joy=None):
        if joy is not None:
            self.joy = joy
        else:
            joystick.backend = BACKEND
            if not joystick.getNumJoysticks():  # to check if we have any connected
                self.joy = None 
            self.joy = joystick.Joystick(self.config.joyID)  # id must be <= nJoys - 1
        self.joyHats = self.joy.getAllHats()
        self.joyButs = self.joy.getAllButtons().copy()
    def joyStateChanged(self):
        hats = self.joy.getAllHats()
        buts = self.joy.getAllButtons()
        if hats != self.joyHats or buts != self.joyButs:
            self.joyHats = hats
            self.joyButs = buts.copy()
            return True
        return False
    def getUser(self, acuity=None, ipd=None):
        try:  # load the users file
            allUsers = fromFile(os.path.join(self.config.dataPath,self.config.userFile))
        except:  # if not there then use a default set
            allUsers = []
        self.userInfo = {'Name':'','Age':20}
        self.userInfo['Date'] = data.getDateStr()  # add the current time
        self.userInfo['ID'] = len(allUsers)
        self.userInfo['Acuity'] = acuity if acuity is not None else '20'
        self.userInfo['IPD'] = ipd if ipd is not None else '60'
        #labels = {'Acuity':'Acuity: \t20/'}
        labels = {}
        fixed=['Date','ID']
        if acuity is not None:
            fixed.append('Acuity')
        if ipd is not None:
            fixed.append('IPD')
        order = ['Name','Age','Acuity','IPD','ID','Date']
        # present a dialogue to change params
        dlg = gui.DlgFromDict(self.userInfo, labels=labels, title='User Info', order=order, fixed=fixed)
        if dlg.OK:
            allUsers.append(self.userInfo)
            toFile(os.path.join(self.config.dataPath,self.config.userFile), allUsers)  # save users to file for next time
        else:
            self.userInfo = None
    @abstractmethod
    def setupData(self):
        pass
    @abstractmethod
    def setupStimuli(self):
        pass
    def setupHandler(self):
        # create the staircase handler
        #self.handler = data.StairHandler(startVal = 60, minVal=0,
        #                        stepType = 'lin', stepSizes=[8,4,2,2,1,1],
        #                        nUp=1, nDown=3,  # will home in on the 80% threshold
        #                        nTrials=1)
        #self.handler = data.QuestHandler(startVal=60, startValSd=30, pThreshold=0.82,nTrials=20)
        pass
    @abstractmethod
    def proceedure(self):
        '''The proceedure of the experiment'''
        pass
    def run(self):
        self.proceedure()
    def close(self, ui=True):
        if self.storeData:
            self.handler.saveAsPickle(os.path.join(self.config.dataPath,'%s_%s'%(self.userInfo['ID'],self.config.stairFile)))
            #self.handler.saveAsExcel(os.path.join(self.config.dataPath,'%s_%s.xlsx'%(self.userInfo['ID'],self.config.stairFile)))
            self.dataFile.close()
        if ui:
            for win in self.windows:
                win.close()
        # something with joystick?
    def presentStimulus(self,idx):
        #set the stimulus to autodraw
        self.stimuli[idx].setAutoDraw(True)
        self.activeWindows.append(self.stimuli[idx].win)
        self.flip()
        self.stimuliTime[idx] = self.clock.getTime()
    def clearStimuli(self):
        for stim in self.stimuli:
            stim.setAutoDraw(False)
        self.flip()
        for idx, stim in enumerate(self.stimuli):
            if stim.win in self.activeWindows:      # calculate displayed time
                self.stimuliTime[idx] = self.clock.getTime() - self.stimuliTime[idx]
        self.activeWindows = []
    def flip(self):
        for window in self.activeWindows:
            window.flip()
        allKeys = event.getKeys()
        for key in allKeys:
            if key == 'escape':
                self.close()
                core.quit()
        event.clearEvents()
    def waitFrames(self,value):
        self.activeWindows[0].waitBlanking = True
        for i in range(value):
            self.flip()
        self.activeWindows[0].waitBlanking = False
    def waitTime(self,value):
        self.timer.reset()
        while self.timer.getTime() < value:
            self.flip()
    def waitForResponse(self,function,items,timeout=None,initial=None,true=None,false=None):
        if initial is None:
            original = function()
            initial = np.array([original[i] for i in items])
        else:
            initial = np.array(initial)
        current = np.copy(initial)
        if timeout is not None:
            timer = core.Clock()
            timer.add(timeout)
        while np.array_equal(initial, current):
            if timeout is not None:
                if timer.getTime() < 0:
                    break
            self.flip()
            new = function()
            current = np.array([new[i] for i in items])
        if true is not None:
            if current.flatten().tolist() in true:
                return True
            elif false is not None:
                if current.flatten().tolist() in false:
                    return False
                else:
                    return None
        return current == initial
