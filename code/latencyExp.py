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
from psychopy import visual, core, gui, data, event, logging
from psychopy.tools.filetools import fromFile, toFile
from psychopy.hardware import joystick
import config
import numpy as np
import random

BACKEND = 'pyglet'
SPF = .016          # seconds per frame

class Experiment():
    def __init__(self, config=config, storeData=True):
        self.config = config
        self.storeData = storeData
        self.setupLogging()
        self.clock = core.Clock()
        self.timer = core.Clock()
        self.setupWindows()
        self.setupJoystick()
        if self.storeData:
            self.getUser()
            self.dataKeys = None
            self.data = None
            self.dataFile = None
            self.setupData()
        self.setupStimuli()
        self.setupHandler()
    def setupLogging(self):
        logging.console.setLevel(logging.ERROR)
        self.log = logging.LogFile(self.config.logFile, level=self.config.logLevel, filemode='w')
    def setupWindows(self):
        #create the windows
        self.windows = []
        self.activeWindows = []
        for monitor in self.config.monitors:
            win = visual.Window(monitor.getSizePix(), monitor=monitor, screen=monitor.screen, name=monitor.name, fullscr=True, units="deg", viewPos=monitor.center, color=[-1,-1,-1],waitBlanking=False)
            win.flipHoriz = monitor.flipHoriz
            self.windows.append(win)
    def setupJoystick(self):
        joystick.backend = BACKEND
        if not joystick.getNumJoysticks():  # to check if we have any connected
            self.joy = None 
        self.joy = joystick.Joystick(config.joyID)  # id must be <= nJoys - 1
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
    def getUser(self):
        try:  # load the users file
            allUsers = fromFile(os.path.join(self.config.dataPath,self.config.userFile))
        except:  # if not there then use a default set
            allUsers = []
        self.userInfo = {'Name':'','Age':20}
        self.userInfo['Date'] = data.getDateStr()  # add the current time
        self.userInfo['ID'] = len(allUsers)
        # present a dialogue to change params
        dlg = gui.DlgFromDict(self.userInfo, title='User Info', fixed=['Date','ID'])
        if dlg.OK:
            allUsers.append(self.userInfo)
            toFile(os.path.join(self.config.dataPath,self.config.userFile), allUsers)  # save users to file for next time
        else:
            self.userInfo = None
    def setupData(self):
        self.dataKeys = ['primeCorrect','primeTime','primeDepth','stimDepth','diopters','nearToFar','orientation','contrast','frequency','requestedLatency','actualLatency','responseTime','correct']
        # make a text file to save data
        fileName = '%s_data_%s'%(self.userInfo['ID'],self.userInfo['Date'])
        self.dataFile = open(os.path.join(config.dataPath,'%s.csv'%fileName), 'w')  # a simple text file with 'comma-separated-values'
        self.dataFile.write('%s\n'%','.join(self.dataKeys))
    def setupStimuli(self):
        self.primeStim = []
        for win in self.windows:
            textStim = visual.TextStim(win=win,height=.15,pos=win.viewPos,autoLog=True, flipHoriz=win.flipHoriz)
            textStim.fontFiles = [os.path.join(self.config.assetsPath,self.config.stimulusFont)]  # set fontFiles to include our local version of snellen rather than using installed version
            textStim.font = os.path.splitext(self.config.stimulusFont)[0]
            textStim.text = 'Default'
            self.primeStim.append(textStim)
        grating = visual.GratingStim(win=self.windows[0], mask="circle", size=3, pos=[0,0], sf=20, autoLog=True)
        postGrating = visual.GratingStim(win=self.windows[0], mask="circle", size=3, pos=[0,0], sf=20, contrast=0, autoLog=True)
        self.stimuli = [textStim, grating, postGrating]
        self.stimuliTime = [0] * len(self.stimuli)
    def setupHandler(self):
        # create the staircase handler
        #self.handler = data.StairHandler(startVal = 60, minVal=0,
        #                        stepType = 'lin', stepSizes=[8,4,2,2,1,1],
        #                        nUp=1, nDown=3,  # will home in on the 80% threshold
        #                        nTrials=1)
        #self.handler = data.QuestHandler(startVal=60, startValSd=30, pThreshold=0.82,nTrials=20)
        conditions=[
            {'label':'near_0', 'nearToFar':True, 'diopters':0, 'startVal': 60, 'minVal':0, 'stepType':'lin', 'stepSizes':[8,4,2,1,1],'nUp':1,'nDown':3},
            {'label':'near_1', 'nearToFar':True, 'diopters':1, 'startVal': 60, 'minVal':0, 'stepType':'lin', 'stepSizes':[8,4,2,1,1],'nUp':1,'nDown':3},
            {'label':'near_2', 'nearToFar':True, 'diopters':2, 'startVal': 60, 'minVal':0, 'stepType':'lin', 'stepSizes':[8,4,2,1,1],'nUp':1,'nDown':3},
            {'label':'near_3', 'nearToFar':True, 'diopters':3, 'startVal': 60, 'minVal':0, 'stepType':'lin', 'stepSizes':[8,4,2,1,1],'nUp':1,'nDown':3},
            {'label':'far_1', 'nearToFar':False, 'diopters':1, 'startVal': 60, 'minVal':0, 'stepType':'lin', 'stepSizes':[8,4,2,1,1],'nUp':1,'nDown':3},
            {'label':'far_2', 'nearToFar':False, 'diopters':2, 'startVal': 60, 'minVal':0, 'stepType':'lin', 'stepSizes':[8,4,2,1,1],'nUp':1,'nDown':3},
            {'label':'far_3', 'nearToFar':False, 'diopters':3, 'startVal': 60, 'minVal':0, 'stepType':'lin', 'stepSizes':[8,4,2,1,1],'nUp':1,'nDown':3},
        ]
        #self.handler = data.MultiStairHandler(stairType='quest',conditions=conditions)
        self.handler = data.MultiStairHandler(stairType='simple',conditions=conditions)
    def proceedure(self):
        '''The proceedure of the experiment'''
        '''
        ref = visual.GratingStim(win=self.windows[3], size=1, pos=[0,2], sf=20, contrast=0, autoLog=True)
        ref.setAutoDraw(True)
        refText = visual.TextStim(win=self.windows[3],height=.15,pos=[0,-2],autoLog=True)
        refText.fontFiles = [os.path.join(self.config.assetsPath,self.config.stimulusFont)]
        refText.font = os.path.splitext(self.config.stimulusFont)[0]
        refText.text = 'Default'
        refText.setAutoDraw(True)
        for a in range(4):
            for idx, win in enumerate(self.windows):
                for stim in self.stimuli:
                    stim.win = self.windows[idx]
                    #stim.wrapWidth = None
                    #print(stim.wrapWidth)
                    stim._needVertexUpdate = True
                    stim._needUpdate = True
                for idx, stim in enumerate(self.stimuli):
                    self.presentStimulus(idx)
                    self.waitTime(60*SPF)
                    self.clearStimuli()
        '''
        for frames, condition in self.handler:
            primed = False
            #while not primed:
            data = {}
            data['requestedLatency'] = frames * SPF
            # set up windows according to this handler
            i = list(range(len(self.windows)))
            mainWindow = random.choice(i[condition['diopters']:])
            primeWindow = mainWindow - condition['diopters']
            if not condition['nearToFar']:
                primeWindow = mainWindow
                mainWindow = primeWindow - condition['diopters']
            data['nearToFar'] = condition['nearToFar']
            data['diopters'] = condition['diopters']
            # set up stimuli with some randomness
            self.stimuli[0] = self.primeStim[primeWindow]   # choose the right prime text stimulus
            text, primeValue = self.genLogicPrimer()        # set the text and store the value for the primer
            self.stimuli[0].text = text
            data['primeDepth'] = self.config.monitors[primeWindow].currentCalib['distance']
            orientation = random.getrandbits(1)             # set and store the orientation of the grating
            self.stimuli[1].ori = orientation * 90
            data['orientation'] = self.stimuli[1].ori
            data['contrast'] = self.stimuli[1].contrast
            data['frequency'] = self.stimuli[1].sf
            for stim in self.stimuli[1:]:
                stim.win = self.windows[mainWindow]  # set the grating and post grating stimulus window
                stim._needVertexUpdate = True        # make sure it recalculates the size
                stim._needUpdate = True              # make sure it redraws the size
            data['stimDepth'] = self.config.monitors[mainWindow].currentCalib['distance']
            # run the proceedure
            self.presentStimulus(0)
            resp1 = self.waitForResponse(self.joy.getAllButtons,[0,1],true=[[True,False]],false=[[False,True]])
            self.clearStimuli()
            data['primeTime'] = self.stimuliTime[0]
            self.presentStimulus(1)
            self.waitTime(frames*SPF)
            self.clearStimuli()
            data['actualLatency'] = self.stimuliTime[1]
            self.presentStimulus(2)
            resp2 = self.waitForResponse(self.joy.getAllHats,[0],true=[[1,0],[-1,0]],false=[[0,1],[0,-1]])
            self.clearStimuli()
            data['responseTime'] = self.stimuliTime[2]
            # record the results
            data['primeCorrect'] = resp1 == primeValue
            data['correct'] = resp2 == orientation
            if data['primeCorrect']:  # prime was correct - this one counted
                #primed = True
                self.handler.addResponse(data['correct'])
                for k, v in data.items():
                    self.handler.addOtherData(k,v)
            if self.storeData:
                self.dataFile.write('%s\n'%','.join(['%s'%data[i] for i in self.dataKeys]))
            # TODO print update on number of trials completed - out of how many? Does the handler know that? probably not
            logging.flush()
    def run(self):
        self.proceedure()
    def close(self):
        if self.storeData:
            self.handler.saveAsPickle(os.path.join(config.dataPath,'%s_%s'%(self.userInfo['ID'],config.stairFile)))
            #self.handler.saveAsExcel(os.path.join(config.dataPath,'%s_%s.xlsx'%(self.userInfo['ID'],config.stairFile)))
            self.dataFile.close()
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
    @staticmethod
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
    experiment = Experiment(config)
    experiment.run()
    experiment.close()
