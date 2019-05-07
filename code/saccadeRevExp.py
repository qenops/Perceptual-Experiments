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

class saccadeExperiment(CODExperiment):
    def __init__(self, config, append=True):
        if append:
            config.dataPath += '/saccadeFar'
        super().__init__(config, append=False)
    def setupHandler(self):
        conditions=[
            #{'label':'near-000', 'dummy':False, 'prime':3, 'stim':1, 'extra':0 , 'driveFrames':0 , 'startVal': 60, 'stepSizes':[16,8,4,2,1,1], 'method':'4AFC', 'stepType':'lin', 'minVal':0, 'maxVal':80, 'findlay_m':8, 'nTrials':100},
            #{'label':'near-080', 'dummy':False, 'prime':3, 'stim':1, 'extra':0 , 'driveFrames':5 , 'startVal': 60, 'stepSizes':[16,8,4,2,1,1], 'method':'4AFC', 'stepType':'lin', 'minVal':0, 'maxVal':80, 'findlay_m':8, 'nTrials':100},
            #{'label':'near-160', 'dummy':False, 'prime':3, 'stim':1, 'extra':0 , 'driveFrames':10, 'startVal': 60, 'stepSizes':[16,8,4,2,1,1], 'method':'4AFC', 'stepType':'lin', 'minVal':0, 'maxVal':80, 'findlay_m':8, 'nTrials':100},
            ##{'label':'near-240', 'dummy':False, 'prime':3, 'stim':1, 'extra':0 , 'driveFrames':15, 'startVal': 60, 'stepSizes':[16,8,4,2,1,1], 'method':'4AFC', 'stepType':'lin', 'minVal':0, 'maxVal':80, 'findlay_m':8, 'nTrials':100},
            #{'label':'near-rndm', 'dummy':True, 'prime':3, 'stim':3, 'extra':1 , 'driveFrames':0, 'startVal': 60, 'stepSizes':[16,8,4,2,1,1], 'method':'4AFC', 'stepType':'lin', 'minVal':0, 'maxVal':80, 'findlay_m':8, 'nTrials':100},
            #{'label':'near-rnd2', 'dummy':True, 'prime':3, 'stim':2, 'extra':1 , 'driveFrames':0, 'startVal': 60, 'stepSizes':[16,8,4,2,1,1], 'method':'4AFC', 'stepType':'lin', 'minVal':0, 'maxVal':80, 'findlay_m':8, 'nTrials':100},
            #{'label':'near-rnd3', 'dummy':True, 'prime':3, 'stim':0, 'extra':1 , 'driveFrames':0, 'startVal': 60, 'stepSizes':[16,8,4,2,1,1], 'method':'4AFC', 'stepType':'lin', 'minVal':0, 'maxVal':80, 'findlay_m':8, 'nTrials':100},
            {'label':'far-000', 'dummy':False, 'prime':0, 'stim':2, 'extra':3 , 'driveFrames':0 , 'startVal': 60, 'stepSizes':[16,8,4,2,1,1], 'method':'4AFC', 'stepType':'lin', 'minVal':0, 'maxVal':80, 'findlay_m':8, 'nTrials':100},
            {'label':'far-080', 'dummy':False, 'prime':0, 'stim':2, 'extra':3 , 'driveFrames':5 , 'startVal': 60, 'stepSizes':[16,8,4,2,1,1], 'method':'4AFC', 'stepType':'lin', 'minVal':0, 'maxVal':80, 'findlay_m':8, 'nTrials':100},
            {'label':'far-160', 'dummy':False, 'prime':0, 'stim':2, 'extra':3 , 'driveFrames':10, 'startVal': 60, 'stepSizes':[16,8,4,2,1,1], 'method':'4AFC', 'stepType':'lin', 'minVal':0, 'maxVal':80, 'findlay_m':8, 'nTrials':100},
            #{'label':'far-240', 'dummy':False, 'prime':0, 'stim':2, 'extra':3 , 'driveFrames':15, 'startVal': 60, 'stepSizes':[16,8,4,2,1,1], 'method':'4AFC', 'stepType':'lin', 'minVal':0, 'maxVal':80, 'findlay_m':8, 'nTrials':100},
            {'label':'far-rnd3', 'dummy':True, 'prime':0, 'stim':3, 'extra':2 , 'driveFrames':0, 'startVal': 60, 'stepSizes':[16,8,4,2,1,1], 'method':'4AFC', 'stepType':'lin', 'minVal':0, 'maxVal':80, 'findlay_m':8, 'nTrials':100},
            {'label':'far-rnd1', 'dummy':True, 'prime':0, 'stim':1, 'extra':2 , 'driveFrames':0, 'startVal': 60, 'stepSizes':[16,8,4,2,1,1], 'method':'4AFC', 'stepType':'lin', 'minVal':0, 'maxVal':80, 'findlay_m':8, 'nTrials':100},
            {'label':'far-rnd0', 'dummy':True, 'prime':0, 'stim':0, 'extra':2 , 'driveFrames':0, 'startVal': 60, 'stepSizes':[16,8,4,2,1,1], 'method':'4AFC', 'stepType':'lin', 'minVal':0, 'maxVal':80, 'findlay_m':8, 'nTrials':100},
        ]
        self.handler = data.ExtendedMultiStairHandler(stairType='vpest',conditions=conditions)
        self.dummies = [i for i in self.handler.staircases if i.condition['dummy']]
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
    '''
    def proceedure(self):
        self.present(self.primeStim[-1])
        for stim in self.postStim:
            self.present(stim)
        self.waitForResponse(self.joy.getAllButtons,[0,1],true=[[True,False]],false=[[False,True]])
    '''

if __name__ == '__main__':
    if len(sys.argv) > 1:
        userInfo = Experiment.loadUser(os.path.join(config.dataPath,'saccadeFar',config.userFile), int(sys.argv[1]))
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
        config.nearacuity = acuityExp.nearAcuity
        #'''
    #config.storeData = True
    experiment = saccadeExperiment(config)
    experiment.run()
    experiment.close()