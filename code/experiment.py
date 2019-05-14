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

from psychopy import visual, core, gui, data, event, logging, tools
from psychopy.tools.filetools import fromFile, toFile
from psychopy.hardware import joystick

BACKEND = 'pyglet'
SPF = .016          # seconds per frame

class Experiment(ABC):
    def __init__(self, config): 
        self.config = config
        self.storeData = getattr(config,'storeData',True)
        self.setupLogging()
        self.clock = core.Clock()
        self.timer = core.Clock()
        self.setupWindows(getattr(config,'viewPos',True))
        if getattr(config,'joystick',True):
            self.setupJoystick()
        self.newUser = True if getattr(self,'userInfo',None) is None else False
        if self.storeData:
            self.getUser()
            if self.userInfo is None:
                raise AssertionError('User info was not entered')
            self.dataKeys = None
            self.data = None
            self.dataFile = None
            self.setupData()
        self.setupStimuli()
        self.setupHandler()
    def setupLogging(self):
        logging.console.setLevel(logging.ERROR)
        self.log = logging.LogFile(self.config.logFile, level=self.config.logLevel, filemode='w')
    def setupWindows(self, viewPos=True):
        self.windows = getattr(self.config,'windows',None)
        if self.windows is None:
            #create the windows
            self.windows = [] 
            for monitor in self.config.monitors:
                if viewPos:
                    win = visual.Window(monitor.getSizePix(), monitor=monitor, screen=monitor.screen, name=monitor.name, fullscr=True, units="deg", viewPos=monitor.center, color=monitor.color,waitBlanking=False)
                else:
                    win = visual.Window(monitor.getSizePix(), monitor=monitor, screen=monitor.screen, name=monitor.name, fullscr=True, units="deg", color=monitor.color,waitBlanking=False)
                win.flipHoriz = monitor.flipHoriz
                self.windows.append(win)
        self.activeWindows = []
    def setupJoystick(self):
        self.joy = getattr(self.config,'joy',None)
        if self.joy is None:
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
    @staticmethod
    def loadUser(path, id):
        try:
            allUsers = fromFile(path)
        except:
            raise AttributeError('No user file exists')
        try:
            return [u for u in allUsers if u['ID'] == id][0]
        except IndexError:
            raise AttributeError('No user of that ID exists')
    def getUser(self):
        print("Verify subject's information.")
        font = "Bookman"
        height = .5
        winIdx = 2
        win = self.windows[winIdx]
        prompt = visual.TextStim(win=win,height=height,pos=win.viewPos+np.array((0,0)),flipHoriz=win.flipHoriz,font=font,alignHoriz='center',
            text='Please wait while we verify your information....')
        self.present(prompt)
        try:  # load the users file
            print('Reading file %s'%os.path.join(self.config.dataPath,self.config.userFile))
            allUsers = fromFile(os.path.join(self.config.dataPath,self.config.userFile))
        except:  # if not there then use a default set
            allUsers = []
        # prepare the dialoge
        #labels = {'Acuity':'Acuity: \t20/'}
        labels = {}
        order = ['Name','Age','Far Acuity', 'Near Acuity','IPD','ID','Date']
        self.userInfo = getattr(self.config,'userInfo',None)
        if self.userInfo is None:
            self.userInfo = {'Name':'','Age':20}
            self.userInfo['Date'] = [data.getDateStr()]  # add the current time
            self.userInfo['ID'] = len(allUsers)
            self.userInfo['Far Acuity'] = getattr(self.config,'acuity',20) #acuity if acuity is not None else '20'
            self.userInfo['Near Acuity'] = getattr(self.config,'nearacuity',20) #acuity if acuity is not None else '20'
            self.userInfo['IPD'] = getattr(self.config,'ipd',60) #ipd if ipd is not None else '60'
            fixed=['Date','ID']
            if getattr(self.config,'acuity',None) is not None:
                fixed.append('Far Acuity')
            if getattr(self.config,'nearacuity',None) is not None:
                fixed.append('Near Acuity')
            if getattr(self.config,'ipd',None) is not None:
                fixed.append('IPD')
        else:
            # we have user info - need to update Date with a new trial
            self.userInfo['Date'].append(data.getDateStr())
            fixed=order
            try:
                user = [u for u in allUsers if u['ID'] == self.userInfo['ID']][0]
                user['Date'] = self.userInfo['Date']
                self.newUser = False
            except IndexError:
                pass
        # present a dialogue to change params
        dlg = gui.DlgFromDict(self.userInfo, labels=labels, title='User Info', order=order, fixed=fixed)
        if dlg.OK:
            if self.newUser:
                allUsers.append(self.userInfo)
            toFile(os.path.join(self.config.dataPath,self.config.userFile), allUsers)  # save users to file for next time
        else:
            self.userInfo = None
        self.clear(prompt)
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
            # add user data to handler
            self.userInfo.pop('Name')
            self.handler.userInfo = self.userInfo
            # write out handler
            self.handler.saveAsPickle(os.path.join(self.config.dataPath,'%s_%s'%(self.fileName,self.config.stairFile)))
            #self.handler.saveAsExcel(os.path.join(self.config.dataPath,'%s_%s.xlsx'%(self.userInfo['ID'],self.config.stairFile)))
            self.dataFile.close()
        if ui:
            for win in self.windows:
                win.close()
        # something with joystick?
    def present(self,stim):
        #show a stimulus without timing
        stim.setAutoDraw(True)
        self.activeWindows.append(stim.win)
        self.flip()
    def presentStimulus(self,idx):
        #set the stimulus to autodraw
        self.stimuli[idx].setAutoDraw(True)
        self.activeWindows.append(self.stimuli[idx].win)
        self.flip()
        self.stimuliTime[idx] = self.clock.getTime()
    def clear(self,stim):
        stim.setAutoDraw(False)
        self.flip()
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
        #print(current.flatten().tolist())
        #print(true, false)
        if true is not None:
            if current.flatten().tolist() in true:
                return True
            elif false is not None:
                if current.flatten().tolist() in false:
                    return False
                else:
                    return None
        return current == initial
