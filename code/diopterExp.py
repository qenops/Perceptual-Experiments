
from latencyExp import LatencyExperiment, visual, event, core, data, logging, SPF
import numpy as np
import os, random, math
import config

class DiopterExperiment(LatencyExperiment):
    def setupHandler(self):
        '''
        conditions=[
            {'label':'1_diopter_1-2', 'prime':1, 'stim':2, 'startVal': 60, 'minVal':0, 'stepType':'lin', 'stepSizes':[8,4,2,1,1],'nUp':1,'nDown':3},
            {'label':'1_diopter_2-3', 'prime':2, 'stim':3, 'startVal': 60, 'minVal':0, 'stepType':'lin', 'stepSizes':[8,4,2,1,1],'nUp':1,'nDown':3},
            {'label':'1_diopter_2-1', 'prime':2, 'stim':1, 'startVal': 60, 'minVal':0, 'stepType':'lin', 'stepSizes':[8,4,2,1,1],'nUp':1,'nDown':3},
            {'label':'1_diopter_1-0', 'prime':1, 'stim':0, 'startVal': 60, 'minVal':0, 'stepType':'lin', 'stepSizes':[8,4,2,1,1],'nUp':1,'nDown':3},
            {'label':'2_diopter_1-3', 'prime':1, 'stim':3, 'startVal': 60, 'minVal':0, 'stepType':'lin', 'stepSizes':[8,4,2,1,1],'nUp':1,'nDown':3},
            {'label':'2_diopter_2-0', 'prime':2, 'stim':0, 'startVal': 60, 'minVal':0, 'stepType':'lin', 'stepSizes':[8,4,2,1,1],'nUp':1,'nDown':3},
        ]
        self.handler = data.MultiStairHandler(stairType='simple',conditions=conditions)
        '''
        '''
        conditions=[
            {'label':'1_diopter_1-2', 'prime':1, 'stim':2, 'startVal': math.log(25), 'startValSd': 25, 'pThreshold':0.82, 'minVal':0, 'stopInterval':.95},
            #{'label':'1_diopter_2-3', 'prime':2, 'stim':3, 'startVal': 25, 'startValSd': 25, 'minVal':0, 'stepType':'lin', 'stepSizes':[8,4,2,1,1],'nUp':1,'nDown':3},
            #{'label':'1_diopter_2-1', 'prime':2, 'stim':1, 'startVal': 25, 'startValSd': 25, 'minVal':0, 'stepType':'lin', 'stepSizes':[8,4,2,1,1],'nUp':1,'nDown':3},
            #{'label':'1_diopter_1-0', 'prime':1, 'stim':0, 'startVal': 25, 'startValSd': 25, 'minVal':0, 'stepType':'lin', 'stepSizes':[8,4,2,1,1],'nUp':1,'nDown':3},
            #{'label':'2_diopter_1-3', 'prime':1, 'stim':3, 'startVal': 25, 'startValSd': 25, 'minVal':0, 'stepType':'lin', 'stepSizes':[8,4,2,1,1],'nUp':1,'nDown':3},
            #{'label':'2_diopter_2-0', 'prime':2, 'stim':0, 'startVal': 25, 'startValSd': 25, 'minVal':0, 'stepType':'lin', 'stepSizes':[8,4,2,1,1],'nUp':1,'nDown':3},
        ]
        self.handler = data.ExtendedMultiStairHandler(stairType='quest',conditions=conditions)
        '''
        '''
        conditions=[
            {'label':'1_diopter_1-2', 'prime':1, 'stim':2, 'startVal':25, 'stepSizes':[8,4,2,1], 'method':'2AFC', 'stepType':'lin', 'minVal':1, 'maxVal':80, 'pest_w':1},
        ]
        self.handler = data.ExtendedMultiStairHandler(stairType='pest',conditions=conditions)
        '''
        conditions=[
            {'label':'1_diopter_1-2', 'prime':1, 'stim':2, 'startVal': 60, 'stepSizes':[8,4,2,1,1], 'method':'2AFC', 'stepType':'lin', 'minVal':1, 'maxVal':80, 'findlay_m':8, 'nTrials':100},
            {'label':'1_diopter_2-3', 'prime':2, 'stim':3, 'startVal': 60, 'stepSizes':[8,4,2,1,1], 'method':'2AFC', 'stepType':'lin', 'minVal':1, 'maxVal':80, 'findlay_m':8, 'nTrials':100},
            {'label':'1_diopter_2-1', 'prime':2, 'stim':1, 'startVal': 60, 'stepSizes':[8,4,2,1,1], 'method':'2AFC', 'stepType':'lin', 'minVal':1, 'maxVal':80, 'findlay_m':8, 'nTrials':100},
            {'label':'1_diopter_1-0', 'prime':1, 'stim':0, 'startVal': 60, 'stepSizes':[8,4,2,1,1], 'method':'2AFC', 'stepType':'lin', 'minVal':1, 'maxVal':80, 'findlay_m':8, 'nTrials':100},
            {'label':'2_diopter_1-3', 'prime':1, 'stim':3, 'startVal': 60, 'stepSizes':[8,4,2,1,1], 'method':'2AFC', 'stepType':'lin', 'minVal':1, 'maxVal':80, 'findlay_m':8, 'nTrials':100},
            {'label':'2_diopter_2-0', 'prime':2, 'stim':0, 'startVal': 60, 'stepSizes':[8,4,2,1,1], 'method':'2AFC', 'stepType':'lin', 'minVal':1, 'maxVal':80, 'findlay_m':8, 'nTrials':100},
        ]
        self.handler = data.ExtendedMultiStairHandler(stairType='vpest',conditions=conditions)
    def proceedure(self):
        '''The proceedure of the experiment'''
        self.count = 0
        for frames, condition in self.handler:
            primed = False
            #while not primed:
            data = {}
            data['trial'] = self.count + 1
            data['intensity'] = frames
            data['requestedLatency'] = frames * SPF
            # set up windows according to this handler
            i = list(range(len(self.windows)))
            mainWindow = condition['stim']
            primeWindow = condition['prime']
            data['nearToFar'] = primeWindow < mainWindow
            data['diopters'] = abs(primeWindow-mainWindow)
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
            #print(primeValue, orientation)
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
                #primed = True
                self.handler.addResponse(data['correct'])
                for k, v in data.items():
                    self.handler.addOtherData(k,v)
                if data['correct'] and len(self.handler.currentStaircase.reversalIntensities) == 0 and self.handler.currentStaircase.currentDirection in ['down', 'start']:
                    # add an inital rule for vPest
                    self.handler.currentStaircase.stimuliLevelTrialCounts.append(self.handler.currentStaircase.currentLevelTrialCount)
                    self.handler.currentStaircase._intensityDec()
                    self.handler.currentStaircase.stepChangeidx = len(self.handler.currentStaircase.data)
                    #self.handler.currentStaircase.calculateNextIntensity()
            else:
                self.handler.currentStaircase.intensities.pop()
            if self.storeData:
                self.dataFile.write('%s\n'%','.join(['%s'%data[i] for i in self.dataKeys]))
            self.count += 1
            print('Trial # %s:\tFrames = %s\tExpr = %s'%(self.count,frames,condition['label']))
            logging.flush()


if __name__ == '__main__':
    experiment = DiopterExperiment(config)
    experiment.run()
    experiment.close()