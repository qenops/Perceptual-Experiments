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
from odExperimentC import CODExperiment
from userAlign import AlignExperiment
from userAcuity import AcuityExperiment

import numpy as np
import random, os, sys

import config

class stimExperiment(CODExperiment):
    def __init__(self, config, append=True):
        if append:
            config.dataPath += '/saccadeFar'
        super().__init__(config, append=False)
        self.concurrent = True
        #self.concurrent = False
    def setupStimuli(self):
        super().setupStimuli()
        # move the stimuli to the side
        for stim in self.primeStim[:-1]:
            stim.pos += np.array((-5,0))
        for depth in self.mainStim[:-1]:
            for stim in depth:
                stim.pos += np.array((5,0))
        for stim in self.postStim[:-1]:
            stim.pos += np.array((5,0))
        self.primeStim[-1].pos += np.array((2.5,0))
        for stim in self.mainStim[-1]:
            stim.pos += np.array((-2.5,0))
        self.postStim[-1].pos += np.array((-2.5,0))
        # replace overdrive stim odStim[stimType][x4] (all on win 0)
        self.odStim = []
        win = self.windows[0]
        self.odStim.append(self.mainStim[0])
        # grating stim
        #scale = 1
        scale = 3
        stim = [visual.GratingStim(win, mask='circle', size=self.config.primeHeight*4*scale, pos=np.array((5,0)),ori=45,sf=8)]*4
        self.odStim.append(stim)
        stim = [visual.GratingStim(win, mask='gauss', size=self.config.primeHeight*8*scale, pos=np.array((5,0)),ori=45,sf=8)]*4
        self.odStim.append(stim)
        # radial stim - annulus, rotating wedge, checkerboard
        stim = [visual.RadialStim(win, mask='circle', size=self.config.primeHeight*4*scale, pos=np.array((5,0)),angularCycles=12,radialCycles=4)]*4  #checkerboard
        self.odStim.append(stim)
        stim = [visual.RadialStim(win, mask='circle', size=self.config.primeHeight*4*scale, pos=np.array((5,0)),angularCycles=0,radialCycles=4)]*4  # anulus
        self.odStim.append(stim)
        stim = [visual.RadialStim(win, mask='circle', size=self.config.primeHeight*4*scale, pos=np.array((5,0)),angularCycles=12,radialCycles=0)]*4  # star
        self.odStim.append(stim)
        # noise stim
        #stim = [visual.NoiseStim(win, mask='circle', size=self.config.primeHeight*4*scale, pos=win.viewPos+np.array((5,0)),noiseElementSize=4,noiseType='binary')]*4 
        #self.odStim.append(stim)
        # envelope grating? (I think 2d gratings)
        
    def setupHandler(self):  # use 'extra' to choose type of od stim
        conditions=[
            {'label':'near-000',      'dummy':False, 'prime':3, 'stim':1, 'extra':0 , 'driveFrames':0 , 'startVal': 60, 'stepSizes':[16,8,4,2,1,1], 'method':'4AFC', 'stepType':'lin', 'minVal':0, 'maxVal':80, 'findlay_m':8, 'nTrials':100},
            {'label':'orig-stim',     'dummy':False, 'prime':3, 'stim':1, 'extra':0 , 'driveFrames':8, 'startVal': 60, 'stepSizes':[16,8,4,2,1,1], 'method':'4AFC', 'stepType':'lin', 'minVal':0, 'maxVal':80, 'findlay_m':8, 'nTrials':100},
            {'label':'grating-circ',  'dummy':False, 'prime':3, 'stim':1, 'extra':1 , 'driveFrames':8, 'startVal': 60, 'stepSizes':[16,8,4,2,1,1], 'method':'4AFC', 'stepType':'lin', 'minVal':0, 'maxVal':80, 'findlay_m':8, 'nTrials':100},
            {'label':'grating-gauss', 'dummy':False, 'prime':3, 'stim':1, 'extra':2 , 'driveFrames':8, 'startVal': 60, 'stepSizes':[16,8,4,2,1,1], 'method':'4AFC', 'stepType':'lin', 'minVal':0, 'maxVal':80, 'findlay_m':8, 'nTrials':100},
            {'label':'radial-check',  'dummy':False, 'prime':3, 'stim':1, 'extra':3 , 'driveFrames':8, 'startVal': 60, 'stepSizes':[16,8,4,2,1,1], 'method':'4AFC', 'stepType':'lin', 'minVal':0, 'maxVal':80, 'findlay_m':8, 'nTrials':100},
            {'label':'radial-anulus', 'dummy':False, 'prime':3, 'stim':1, 'extra':4 , 'driveFrames':8, 'startVal': 60, 'stepSizes':[16,8,4,2,1,1], 'method':'4AFC', 'stepType':'lin', 'minVal':0, 'maxVal':80, 'findlay_m':8, 'nTrials':100},
            {'label':'radial-star',   'dummy':False, 'prime':3, 'stim':1, 'extra':5 , 'driveFrames':8, 'startVal': 60, 'stepSizes':[16,8,4,2,1,1], 'method':'4AFC', 'stepType':'lin', 'minVal':0, 'maxVal':80, 'findlay_m':8, 'nTrials':100},
            #{'label':'noise',   'dummy':False, 'prime':3, 'stim':1, 'extra':6 , 'driveFrames':60, 'startVal': 60, 'stepSizes':[16,8,4,2,1,1], 'method':'4AFC', 'stepType':'lin', 'minVal':0, 'maxVal':80, 'findlay_m':8, 'nTrials':100},
            {'label':'near-rndm', 'dummy':True, 'prime':3, 'stim':3, 'extra':1 , 'driveFrames':0, 'startVal': 60, 'stepSizes':[16,8,4,2,1,1], 'method':'4AFC', 'stepType':'lin', 'minVal':0, 'maxVal':80, 'findlay_m':8, 'nTrials':100},
            {'label':'near-rnd2', 'dummy':True, 'prime':3, 'stim':2, 'extra':1 , 'driveFrames':0, 'startVal': 60, 'stepSizes':[16,8,4,2,1,1], 'method':'4AFC', 'stepType':'lin', 'minVal':0, 'maxVal':80, 'findlay_m':8, 'nTrials':100},
            {'label':'near-rnd3', 'dummy':True, 'prime':3, 'stim':0, 'extra':1 , 'driveFrames':0, 'startVal': 60, 'stepSizes':[16,8,4,2,1,1], 'method':'4AFC', 'stepType':'lin', 'minVal':0, 'maxVal':80, 'findlay_m':8, 'nTrials':100},
            #{'label':'far-000', 'dummy':False, 'prime':0, 'stim':2, 'extra':3 , 'driveFrames':0, 'startVal': 60, 'stepSizes':[16,8,4,2,1,1], 'method':'4AFC', 'stepType':'lin', 'minVal':0, 'maxVal':80, 'findlay_m':8, 'nTrials':100},
            #{'label':'far-080', 'dummy':False, 'prime':0, 'stim':2, 'extra':3 , 'driveFrames':5, 'startVal': 60, 'stepSizes':[16,8,4,2,1,1], 'method':'4AFC', 'stepType':'lin', 'minVal':0, 'maxVal':80, 'findlay_m':8, 'nTrials':100},
            #{'label':'far-160', 'dummy':False, 'prime':0, 'stim':2, 'extra':3 , 'driveFrames':10, 'startVal': 60, 'stepSizes':[16,8,4,2,1,1], 'method':'4AFC', 'stepType':'lin', 'minVal':0, 'maxVal':80, 'findlay_m':8, 'nTrials':100},
            #{'label':'far-rndm', 'dummy':True, 'prime':0, 'stim':None, 'extra':2 , 'driveFrames':0, 'startVal': 60, 'stepSizes':[16,8,4,2,1,1], 'method':'4AFC', 'stepType':'lin', 'minVal':0, 'maxVal':80, 'findlay_m':8, 'nTrials':100},
            #{'label':'far-rnd2', 'dummy':True, 'prime':0, 'stim':None, 'extra':2 , 'driveFrames':0, 'startVal': 60, 'stepSizes':[16,8,4,2,1,1], 'method':'4AFC', 'stepType':'lin', 'minVal':0, 'maxVal':80, 'findlay_m':8, 'nTrials':100},
        ]
        self.handler = data.ExtendedMultiStairHandler(stairType='vpest',conditions=conditions)
        self.dummies = [i for i in self.handler.staircases if i.condition['dummy']]
    '''
    def proceedure(self):
        self.present(self.primeStim[-1])
        for stim in self.postStim:
            self.present(stim)
        self.waitForResponse(self.joy.getAllButtons,[0,1],true=[[True,False]],false=[[False,True]])
    '''

if __name__ == '__main__':
    if len(sys.argv) > 1:
        userInfo = Experiment.loadUser(os.path.join(config.dataPath,'saccade',config.userFile), int(sys.argv[1]))
        print('Running with user %s'%userInfo['Name'])
        config.userInfo = userInfo
        #config.storeData = False
        alignExp = AlignExperiment(config)
        alignExp.run()
        alignExp.close(False)
        config.windows = alignExp.windows
        config.joy = alignExp.joy
    else:
        #config.storeData = False
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
        #'''
    #config.storeData = True
    experiment = stimExperiment(config)
    experiment.run()
    experiment.close()