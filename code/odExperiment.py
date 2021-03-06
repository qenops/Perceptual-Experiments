#!/usr/bin/python
''' 
Perceptual experiment for testing overdriving the latency human perception in relation to focal change
    
David Dunn
Jan 2019 - split from experiment
www.qenops.com
'''
__author__ = ('David Dunn')
__version__ = '1.0'

from experiment import Experiment, visual, event, core, data, SPF, logging
from latencyExp import LatencyExperiment
from userAlign import AlignExperiment
from userAcuity import AcuityExperiment

import numpy as np
import random, os, sys

import config

class ODExperiment(LatencyExperiment):
    def __init__(self, config, append=True):
        if append:
            config.dataPath += '/od'
        super().__init__(config, append=False)
    def setupData(self):
        super().setupData()
        self.dataKeys = ['trial','primeCorrect','primeTime','primeDepth','stimDepth','extraDepth','driveFrames','actualDriveTime','nearToFar','diopters','orientation','contrast','frequency','intensity','requestedLatency','actualLatency','responseTime','correct']
        extra = ['caseLabel','caseTrial','trialsAtStep','stepCorrect','expected', 'w', 'direction', 'stepsize', 'stepChange']
        self.dataKeys.extend(extra)
    def setupStimuli(self):
         super().setupStimuli()
         grating = visual.GratingStim(win=self.windows[0], mask="circle", size=3, pos=[0,0], sf=21, contrast=0, autoLog=True)
         self.stimuli.append(grating)
         self.stimuliTime = [0] * len(self.stimuli)
    def setupHandler(self):
        conditions=[
            #{'label':'near-000', 'dummy':False, 'prime':3, 'stim':1, 'extra':0 , 'driveFrames':0 , 'startVal': 60, 'stepSizes':[16,8,4,2,1,1], 'method':'2AFC', 'stepType':'lin', 'minVal':0, 'maxVal':80, 'findlay_m':8, 'nTrials':100},
            #{'label':'near-080', 'dummy':False, 'prime':3, 'stim':1, 'extra':0 , 'driveFrames':5 , 'startVal': 60, 'stepSizes':[16,8,4,2,1,1], 'method':'2AFC', 'stepType':'lin', 'minVal':0, 'maxVal':80, 'findlay_m':8, 'nTrials':100},
            #{'label':'near-160', 'dummy':False, 'prime':3, 'stim':1, 'extra':0 , 'driveFrames':10, 'startVal': 60, 'stepSizes':[16,8,4,2,1,1], 'method':'2AFC', 'stepType':'lin', 'minVal':0, 'maxVal':80, 'findlay_m':8, 'nTrials':100},
            #{'label':'near-rndm', 'dummy':True, 'prime':3, 'stim':None, 'extra':1 , 'driveFrames':0, 'startVal': 60, 'stepSizes':[16,8,4,2,1,1], 'method':'2AFC', 'stepType':'lin', 'minVal':0, 'maxVal':80, 'findlay_m':8, 'nTrials':100},
            #{'label':'near-rnd2', 'dummy':True, 'prime':3, 'stim':None, 'extra':1 , 'driveFrames':0, 'startVal': 60, 'stepSizes':[16,8,4,2,1,1], 'method':'2AFC', 'stepType':'lin', 'minVal':0, 'maxVal':80, 'findlay_m':8, 'nTrials':100},
            {'label':'far-000', 'dummy':False, 'prime':0, 'stim':2, 'extra':3 , 'driveFrames':0, 'startVal': 60, 'stepSizes':[16,8,4,2,1,1], 'method':'2AFC', 'stepType':'lin', 'minVal':0, 'maxVal':80, 'findlay_m':8, 'nTrials':100},
            {'label':'far-080', 'dummy':False, 'prime':0, 'stim':2, 'extra':3 , 'driveFrames':5, 'startVal': 60, 'stepSizes':[16,8,4,2,1,1], 'method':'2AFC', 'stepType':'lin', 'minVal':0, 'maxVal':80, 'findlay_m':8, 'nTrials':100},
            {'label':'far-160', 'dummy':False, 'prime':0, 'stim':2, 'extra':3 , 'driveFrames':10, 'startVal': 60, 'stepSizes':[16,8,4,2,1,1], 'method':'2AFC', 'stepType':'lin', 'minVal':0, 'maxVal':80, 'findlay_m':8, 'nTrials':100},
            {'label':'far-rndm', 'dummy':True, 'prime':0, 'stim':None, 'extra':2 , 'driveFrames':0, 'startVal': 60, 'stepSizes':[16,8,4,2,1,1], 'method':'2AFC', 'stepType':'lin', 'minVal':0, 'maxVal':80, 'findlay_m':8, 'nTrials':100},
            {'label':'far-rnd2', 'dummy':True, 'prime':0, 'stim':None, 'extra':2 , 'driveFrames':0, 'startVal': 60, 'stepSizes':[16,8,4,2,1,1], 'method':'2AFC', 'stepType':'lin', 'minVal':0, 'maxVal':80, 'findlay_m':8, 'nTrials':100},
        ]
        self.handler = data.ExtendedMultiStairHandler(stairType='vpest',conditions=conditions)
        self.dummies = [i for i in self.handler.staircases if i.condition['dummy']]
    def proceedure(self):
        '''The proceedure of the experiment'''
        self.count = 0
        for frames, condition in self.handler:
            data = {}
            data['trial'] = self.count + 1
            data['intensity'] = frames
            data['requestedLatency'] = frames * SPF
            # set up windows according to this handler
            primeWindow = condition['prime']
            mainWindow = condition['stim']
            if mainWindow is not None:
                extraWindow = condition['extra']
            else:
                i = list(range(len(self.windows)))
                i.pop(condition['extra'])
                mainWindow = random.choice(i)
                extraWindow = condition['extra']
            data['nearToFar'] = primeWindow < mainWindow
            data['diopters'] = abs(primeWindow-mainWindow)
            # set up stimuli with some randomness
            self.stimuli[0] = self.primeStim[primeWindow]   # choose the right prime text stimulus
            text, primeValue = self.genLogicPrimer()        # set the text and store the value for the primer
            self.stimuli[0].text = text
            data['primeDepth'] = self.config.monitors[primeWindow].currentCalib['distance']
            orientation = random.getrandbits(1)             # set and store the orientation of the grating
            self.stimuli[1].ori = orientation * 90
            self.stimuli[3].ori = orientation * 90
            data['orientation'] = self.stimuli[1].ori
            data['contrast'] = self.stimuli[1].contrast
            data['frequency'] = self.stimuli[1].sf
            for stim in self.stimuli[1:3]:
                stim.win = self.windows[mainWindow]  # set the grating and post grating stimulus window
                stim._needVertexUpdate = True        # make sure it recalculates the size
                stim._needUpdate = True              # make sure it redraws the size
            data['stimDepth'] = self.config.monitors[mainWindow].currentCalib['distance']
            self.stimuli[3].win = self.windows[extraWindow]
            self.stimuli[3]._needVertexUpdate = True
            self.stimuli[3]._needUpdate = True
            data['extraDepth'] = self.config.monitors[extraWindow].currentCalib['distance']
            driveFrames = condition['driveFrames']
            # run the proceedure
            self.presentStimulus(0)
            resp1 = self.waitForResponse(self.joy.getAllButtons,[0,1],true=[[True,False]],false=[[False,True]])
            self.clearStimuli()
            data['primeTime'] = self.stimuliTime[0]
            if driveFrames > 0:
                self.presentStimulus(3)
                self.waitTime(driveFrames*SPF)
                self.clearStimuli()
            self.presentStimulus(1)
            self.waitTime(frames*SPF)
            self.clearStimuli()
            data['driveFrames'] = driveFrames
            data['actualDriveTime']= self.stimuliTime[3]
            data['actualLatency'] = self.stimuliTime[1]
            self.presentStimulus(2)
            resp2 = self.waitForResponse(self.joy.getAllHats,[0],true=[[1,0],[-1,0]],false=[[0,1],[0,-1]])
            self.clearStimuli()
            data['responseTime'] = self.stimuliTime[2]
            # record the results
            data['primeCorrect'] = resp1 == primeValue
            data['correct'] = resp2 == orientation
            # extra results
            data.update({'caseLabel':condition['label'],
                'stepCorrect': sum(self.handler.currentStaircase.data[self.handler.currentStaircase.stepChangeidx:]) + data['correct'],
                'w': self.handler.currentStaircase.pest_w,
                'direction': self.handler.currentStaircase.currentDirection, 
                'stepsize': self.handler.currentStaircase.stepSizes[self.handler.currentStaircase.currentStepSizeIdx], 
            })
            data['caseTrial'] = len(self.handler.currentStaircase.data) + 1
            data['trialsAtStep'] = data['caseTrial'] - self.handler.currentStaircase.stepChangeidx
            data['expected'] = data['trialsAtStep'] * self.handler.currentStaircase.targetProb
            data['stepChange'] = int(self.handler.currentStaircase.currentLevelTrialCount / self.handler.currentStaircase.findlay_m)
            if data['primeCorrect']:  # prime was correct - this one counted
                self.handler.addResponse(data['correct'])
                for k, v in data.items():
                    self.handler.addOtherData(k,v)
                # add an inital rule for vPest
                #if data['correct'] and len(self.handler.currentStaircase.reversalIntensities) == 0 and self.handler.currentStaircase.currentDirection in ['down', 'start']:
                #    self.handler.currentStaircase.stimuliLevelTrialCounts.append(self.handler.currentStaircase.currentLevelTrialCount)
                #    self.handler.currentStaircase._intensityDec()
                #    self.handler.currentStaircase.stepChangeidx = len(self.handler.currentStaircase.data)
                #    #self.handler.currentStaircase.calculateNextIntensity()
            else:
                self.handler.currentStaircase.intensities.pop()
            if self.storeData:
                self.dataFile.write('%s\n'%','.join(['%s'%data[i] for i in self.dataKeys]))
            # TODO print update on number of trials completed - out of how many? Does the handler know that? probably not
            self.count += 1
            print('Trial # %s:\tFrames = %s\tExpr = %s'%(self.count,frames,condition['label']))
            logging.flush()

            # Do some checking to make sure we aren't only running random Experiments or not running any?
            #if set(self.handler.runningStaircases).issubset(self.dummies):
            if all(i in self.dummies for i in self.handler.runningStaircases):
                print('All running staircases are dummies. Ending run.')
                for stair in self.dummies:
                    stair.finished = True
            #if not set(self.handler.runningStaircases).intersection(self.dummies):
            if not [i for i in self.handler.runningStaircases if i in self.dummies]:
                print('No running staircases are dummies. Restarting all dummies.')
                for stair in self.dummies:
                    stair.finished = False
                    stair.reversalIntensities = []
                    stair.intensities = []
                    stair.currentStepSizeIdx = 0
                    stair.currentDirectionStepCount = 0
                    stair.correctCounter = 0
                    #stair._nextIntensity = stair.startVal
                    self.handler.runningStaircases.append(stair)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        userInfo = Experiment.loadUser(os.path.join(config.dataPath,'od',config.userFile), int(sys.argv[1]))
        print('Running with user %s'%userInfo['Name'])
        config.userInfo = userInfo
    else:

        config.storeData = False
        alignExp = AlignExperiment(config)
        alignExp.run()
        alignExp.close(False)
        config.ipd = alignExp.ipd
        config.windows = alignExp.windows
        config.joy = alignExp.joy
        acuityExp = AcuityExperiment(config)
        acuityExp.run()
        acuityExp.close(False)
        config.acuity = acuityExp.acuity
        config.storeData = True
        #'''
    experiment = ODExperiment(config)
    experiment.run()
    experiment.close()