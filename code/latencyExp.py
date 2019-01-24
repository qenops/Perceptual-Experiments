#!/usr/bin/python
''' 
Perceptual experiment for testing the latency of human perception in relation to focal change, frequency, and contrast
    
David Dunn
Jan 2019 - split from experiment
www.qenops.com
'''
__author__ = ('David Dunn')
__version__ = '1.0'

from experiment import Experiment, visual, event, core, data
from userAlign import AlignExperiment
from acuityExp import AcuityExperiment

import numpy as np
import random

import config

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

class LatencyExperiment(Experiment):
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
        conditions=[
            {'label':'near_0', 'nearToFar':True, 'diopters':0, 'startVal': 60, 'minVal':0, 'stepType':'lin', 'stepSizes':[8,4,2,1,1],'nUp':1,'nDown':3},
            {'label':'near_1', 'nearToFar':True, 'diopters':1, 'startVal': 60, 'minVal':0, 'stepType':'lin', 'stepSizes':[8,4,2,1,1],'nUp':1,'nDown':3},
            {'label':'near_2', 'nearToFar':True, 'diopters':2, 'startVal': 60, 'minVal':0, 'stepType':'lin', 'stepSizes':[8,4,2,1,1],'nUp':1,'nDown':3},
            {'label':'near_3', 'nearToFar':True, 'diopters':3, 'startVal': 60, 'minVal':0, 'stepType':'lin', 'stepSizes':[8,4,2,1,1],'nUp':1,'nDown':3},
            {'label':'far_1', 'nearToFar':False, 'diopters':1, 'startVal': 60, 'minVal':0, 'stepType':'lin', 'stepSizes':[8,4,2,1,1],'nUp':1,'nDown':3},
            {'label':'far_2', 'nearToFar':False, 'diopters':2, 'startVal': 60, 'minVal':0, 'stepType':'lin', 'stepSizes':[8,4,2,1,1],'nUp':1,'nDown':3},
            {'label':'far_3', 'nearToFar':False, 'diopters':3, 'startVal': 60, 'minVal':0, 'stepType':'lin', 'stepSizes':[8,4,2,1,1],'nUp':1,'nDown':3},
        ]
        self.handler = data.MultiStairHandler(stairType='simple',conditions=conditions)
        self.handler = data.ExtendedMultiStairHandler(stairType='vpest',conditions=conditions)
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
        count = 0
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
            count += 1
            print('Trial # %s: Expr = %s'%(count,condition['label']))
            logging.flush()
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

if __name__ == '__main__':
    alignExp = AlignExperiment(config,False)
    alignExp.run()
    alignExp.close()
    config.mon_800cm.color = [1,1,1]
    acuity = AcuityExperiment(config, False)
    acuity.run()
    acuity.close()
    config.mon_800cm.color = [-1,-1,-1]
    #experiment = Experiment(config, True, ipd=alignExp.ipd, acuity=acuity.acuity)
    experiment = Experiment(config, False, ipd=alignExp.ipd, acuity=acuity.acuity)
    experiment.run()
    experiment.close()
