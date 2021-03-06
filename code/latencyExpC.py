#!/usr/bin/python
''' 
Perceptual experiment for testing the latency of human perception in relation to focal change, frequency, and contrast
    
David Dunn
Jan 2019 - split from experiment
www.qenops.com
'''
__author__ = ('David Dunn')
__version__ = '1.0'

from experiment import Experiment, visual, event, core, data, SPF, logging
from userAlign import AlignExperiment
from userAcuity import AcuityExperiment

import numpy as np
import random, os, sys

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

class CLatencyExperiment(Experiment):
    def __init__(self, config, append=True):
        if append:
            config.dataPath += '/latency'
        super().__init__(config)
    def setupData(self):
        self.dataKeys = ['trial','primeIter','primeCorrect','primeTime','primeDepth','stimDepth','diopters','nearToFar','direction','size','intensity','requestedLatency','actualLatency','totalLatency','responseTime','correct']
        extra = ['caseLabel','caseTrial','trialsAtStep','stepCorrect','expected', 'w', 'direction', 'stepsize', 'stepChange']
        self.dataKeys.extend(extra)
        # make a text file to save data
        self.fileName = 'c-%s_data_%s'%(self.userInfo['ID'],self.userInfo['Date'][-1])
        self.dataFile = open(os.path.join(config.dataPath,'%s.csv'%self.fileName), 'w')  # a simple text file with 'comma-separated-values'
        self.dataFile.write('%s\n'%','.join(self.dataKeys))
    def setupStimuli(self):
        self.chars = self.config.mainChars
        self.responses = self.config.mainResponses
        self.primeStim = []
        self.mainStim = []
        self.postStim = []
        fontFiles = [os.path.join(self.config.assetsPath,self.config.stimulusFont)]  # set fontFiles to include our local version of snellen rather than using installed version
        font = os.path.splitext(self.config.stimulusFont)[0]
        for win in self.windows[:4]:
            if win == self.windows[3]:
                win = self.windows[4]
            textStim = visual.TextStim(win=win,height=self.config.primeHeight,pos=win.viewPos,autoLog=True, flipHoriz=win.flipHoriz, fontFiles=fontFiles, font=font, text='Default')
            self.primeStim.append(textStim)
            stims = []
            for char in self.chars:
                text = '%s\n\n'%char
                textStim = visual.TextStim(win=win,height=self.config.mainHeight,pos=win.viewPos,autoLog=True,flipHoriz=win.flipHoriz, fontFiles=fontFiles, font=font, text=char)#text=text*12) # '%s\n'%(char * 3)*3
                stims.append(textStim)
            self.mainStim.append(stims)
            text = '%s\n\n'%'O'
            textStim = visual.TextStim(win=win,height=self.config.mainHeight,pos=win.viewPos,autoLog=True,flipHoriz=win.flipHoriz, fontFiles=fontFiles, font=font, text='O')#text=text*12)
            self.postStim.append(textStim)
        #grating = visual.GratingStim(win=self.windows[0], mask="circle", size=3, pos=[0,0], sf=14, autoLog=True)
        #postGrating = visual.GratingStim(win=self.windows[0], mask="circle", size=3, pos=[0,0], sf=14, contrast=0, autoLog=True)
        self.stimuli = [textStim, textStim, textStim]
        self.stimuliTime = [0] * len(self.stimuli)
    def setupHandler(self):
        conditions = [
            {'label':'near_0', 'nearToFar':True, 'diopters':0, 'startVal':60, 'stepSizes':[16,8,4,2,1,1], 'method':'4AFC', 'stepType':'lin', 'minVal':0, 'maxVal':80, 'findlay_m':8, 'nTrials':100},
            {'label':'near_1', 'nearToFar':True, 'diopters':1, 'startVal':60, 'stepSizes':[16,8,4,2,1,1], 'method':'4AFC', 'stepType':'lin', 'minVal':0, 'maxVal':80, 'findlay_m':8, 'nTrials':100},
            {'label':'near_2', 'nearToFar':True, 'diopters':2, 'startVal':60, 'stepSizes':[16,8,4,2,1,1], 'method':'4AFC', 'stepType':'lin', 'minVal':0, 'maxVal':80, 'findlay_m':8, 'nTrials':100},
            {'label':'near_3', 'nearToFar':True, 'diopters':3, 'startVal':60, 'stepSizes':[16,8,4,2,1,1], 'method':'4AFC', 'stepType':'lin', 'minVal':0, 'maxVal':80, 'findlay_m':8, 'nTrials':100},
            {'label':'far_1', 'nearToFar':False, 'diopters':1, 'startVal':60, 'stepSizes':[16,8,4,2,1,1], 'method':'4AFC', 'stepType':'lin', 'minVal':0, 'maxVal':80, 'findlay_m':8, 'nTrials':100},
            {'label':'far_2', 'nearToFar':False, 'diopters':2, 'startVal':60, 'stepSizes':[16,8,4,2,1,1], 'method':'4AFC', 'stepType':'lin', 'minVal':0, 'maxVal':80, 'findlay_m':8, 'nTrials':100},
            {'label':'far_3', 'nearToFar':False, 'diopters':3, 'startVal':60, 'stepSizes':[16,8,4,2,1,1], 'method':'4AFC', 'stepType':'lin', 'minVal':0, 'maxVal':80, 'findlay_m':8, 'nTrials':100},
        ]
        self.handler = data.ExtendedMultiStairHandler(stairType='vpest',conditions=conditions)
    def run(self):
        if self.newUser:
            self.tutorial()
        self.proceedure()
    def tutorial(self):
        # set up instructions
        font = "Bookman"
        height = .5
        winIdx = 2
        win = self.windows[winIdx]
        prompt = visual.TextStim(win=win,height=height,pos=win.viewPos+np.array((0,3)),flipHoriz=win.flipHoriz,font=font,alignHoriz='center',
            text='You will see a series of simple True/False math equations.\nPress "A" if it is True and "B" if it is False.')
        prime = self.primeStim[winIdx]
        right = visual.TextStim(win=win,height=height,pos=win.viewPos+np.array((0,0)),flipHoriz=win.flipHoriz,font=font,alignHoriz='center',
            text='Correct.')
        wrong = visual.TextStim(win=win,height=height,pos=win.viewPos+np.array((0,0)),flipHoriz=win.flipHoriz,font=font,alignHoriz='center',
            text='Wrong, try again.')
        print("Running Tutorial part 1.")
        correct = False
        while not correct:
            self.present(prompt)
            text, primeValue = self.genLogicPrimer()
            prime.text = text
            self.present(prime)
            resp1 = self.waitForResponse(self.joy.getAllButtons,[0,1],true=[[True,False]],false=[[False,True]])
            self.clear(prime)
            self.clear(prompt)
            if resp1 == primeValue:
                self.present(right)
                correct = True
            else:
                self.present(wrong)
            self.waitTime(3)
            self.clear(right)
            self.clear(wrong)
        winIdx = 1
        win = self.windows[winIdx]
        prompt = visual.TextStim(win=win,height=height,pos=win.viewPos+np.array((0,5)),flipHoriz=win.flipHoriz,font=font,alignHoriz='center',
            text='Randomly, a C will appear for a brief period,\nmost likely on a different display. It will then change to a circle.\nUse the d-pad to indicate the direction of the gap.\n                           (up, down, left, or right)')
        print("Running Tutorial part 2.")
        correct = False
        while not correct:
            self.present(prompt)
            direction = random.randint(0,3)
            main = self.mainStim[winIdx][direction]
            self.present(main)
            resp2 = self.waitForResponse(self.joy.getAllHats,[0],true=[self.responses[direction]],false=[i for i in self.responses if i != self.responses[direction]])
            self.clear(main)
            self.clear(prompt)
            if resp2:
                self.present(right)
                correct = True
            else:
                self.present(wrong)
            self.waitTime(3)
            self.clear(right)
            self.clear(wrong)
        self.waitTime(1)
        print("Running practice.")
        winIdx = 2
        win = self.windows[winIdx]
        prompt = visual.TextStim(win=win,height=height,pos=win.viewPos+np.array((0,0)),flipHoriz=win.flipHoriz,font=font,alignHoriz='center',
            text='Try a couple practice rounds....')
        self.present(prompt)
        self.waitTime(3)
        self.clear(prompt)
        correct = 0
        sequence = [(0,3),(2,2),(2,0),(3,0),(1,3),(1,1)]
        sequnceIdx = 0
        while correct < 3:
            primeIdx, winIdx = sequence[sequnceIdx]
            win = self.windows[winIdx]
            prime = self.primeStim[primeIdx]
            primeIter = random.choice(self.config.primePresentations)
            print('Prime Iterations: %s'%primeIter)
            direction = random.randint(0,3)
            main = self.mainStim[winIdx][direction]
            post = self.postStim[winIdx]
            itr = 0
            resp1 = False
            primeValue = True
            while itr < primeIter or resp1 != primeValue:
                text, primeValue = self.genLogicPrimer()
                prime.text = text
                self.present(prime)
                self.waitTime(.5)
                resp1 = self.waitForResponse(self.joy.getAllButtons,[0,1],true=[[True,False]],false=[[False,True]])
                itr += 1
                print('Iteration %s'%itr)
            self.clear(prime)
            self.clearStimuli()
            self.present(main)
            self.waitTime(60*SPF)
            self.present(post)
            self.clear(main)
            resp2 = self.waitForResponse(self.joy.getAllHats,[0],true=[self.responses[direction]],false=[i for i in self.responses if i != self.responses[direction]])
            self.clear(post)
            if resp1 == primeValue and resp2:
                self.present(right)
                correct += 1
            else:
                self.present(wrong)
            self.waitTime(3)
            self.clear(right)
            self.clear(wrong)
            sequnceIdx = (sequnceIdx + 1) % len(sequence)
            print("Practice round %s. Number correct: %s"%(sequnceIdx, correct))
        winIdx = 2
        win = self.windows[winIdx]
        prompt = visual.TextStim(win=win,height=height,pos=win.viewPos+np.array((0,0)),flipHoriz=win.flipHoriz,font=font,alignHoriz='center',
            text='Good job! Now, here we go!')
        self.present(prompt)
        self.waitTime(3)
        self.clear(prompt)
        self.clearStimuli()
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
        self.count = 0
        for frames, condition in self.handler:
            data = {}
            data['trial'] = self.count + 1
            data['intensity'] = frames
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
            prime = self.primeStim[primeWindow]   # choose the right prime text stimulus
            primeIter = random.choice(self.config.primePresentations)
            data['primeDepth'] = self.config.monitors[primeWindow].currentCalib['distance']
            direction = random.randint(0,3)
            main = self.mainStim[mainWindow][direction]
            post = self.postStim[mainWindow]
            data['direction'] = direction
            data['size'] = main.height
            data['stimDepth'] = self.config.monitors[mainWindow].currentCalib['distance']
            # run the proceedure
            itr = 0
            resp1 = False
            primeValue = True
            while itr < primeIter or resp1 != primeValue:
                text, primeValue = self.genLogicPrimer()        # set the text and store the value for the primer
                prime.text = text
                self.present(prime)
                self.stimuliTime[0] = self.clock.getTime()
                self.waitTime(.5)
                resp1 = self.waitForResponse(self.joy.getAllButtons,[0,1],true=[[True,False]],false=[[False,True]])
                itr += 1
            self.clear(prime)
            data['primeIter'] = itr
            data['primeTime'] = self.clock.getTime() - self.stimuliTime[0]
            self.present(main)
            self.stimuliTime[1] = self.clock.getTime()
            self.waitTime(frames*SPF)
            self.present(post)
            self.clear(main)
            data['actualLatency'] = self.clock.getTime() - self.stimuliTime[1]
            data['totalLatency'] = data['actualLatency']
            self.stimuliTime[2] = self.clock.getTime()
            resp2 = None
            while resp2 is None:
                resp2 = self.waitForResponse(self.joy.getAllHats,[0],true=[self.responses[direction]],false=[i for i in self.responses if i != self.responses[direction]])
            self.clear(post)
            data['responseTime'] = self.clock.getTime() - self.stimuliTime[2]
            self.clearStimuli()
            # record the results
            data['primeCorrect'] = resp1 == primeValue
            data['correct'] = resp2
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
            initialRule = False
            if data['primeCorrect']:  # prime was correct - this one counted
                self.handler.addResponse(data['correct'])
                for k, v in data.items():
                    self.handler.addOtherData(k,v)
                # add an inital rule for vPest
                if data['correct'] and len(self.handler.currentStaircase.reversalIntensities) == 0 and self.handler.currentStaircase.currentDirection in ['down', 'start']:
                    self.handler.currentStaircase.stimuliLevelTrialCounts.append(self.handler.currentStaircase.currentLevelTrialCount)
                    self.handler.currentStaircase._intensityDec()
                    self.handler.currentStaircase.stepChangeidx = len(self.handler.currentStaircase.data)
                    initialRule = True
            else:
                self.handler.currentStaircase.intensities.pop()
            if self.storeData:
                self.dataFile.write('%s\n'%','.join(['%s'%data[i] for i in self.dataKeys]))
            # TODO print update on number of trials completed - out of how many? Does the handler know that? probably not
            self.count += 1
            print('Trial # %s:\tFrames = %s\tExpr = %s\tInitial Rule = %s\tReversals: %s'%(self.count,frames,condition['label'],initialRule,len(self.handler.currentStaircase.reversalIntensities)))
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
    if len(sys.argv) > 1:
        userInfo = Experiment.loadUser(os.path.join(config.dataPath,'latency',config.userFile), int(sys.argv[1]))
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
        config.nearacuity = acuityExp.nearAcuity
    config.storeData = True
    experiment = CLatencyExperiment(config)
    experiment.run()
    experiment.close()
