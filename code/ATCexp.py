#!/usr/bin/python
''' 
Perceptual experiment for testing the latency of human perception in relation to focal change, frequency, and contrast
    
David Dunn
Jan 2019 - split from experiment
www.qenops.com
'''
__author__ = ('David Dunn')
__version__ = '1.0'

from experiment import Experiment, visual, event, core, data, SPF, logging, tools
from userAlign import AlignExperiment
from userAcuity import AcuityExperiment

import numpy as np
import random, os, sys
from datetime import datetime  
from datetime import timedelta 

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

TAXI = [(-.16,-8.3),(-.16,-9.35),(-.16,-10.4),]
APRON = [(-7.23,-8.3)]
RUNWAY = [(6.91,-8.3)]

PLANES = ['A220','A319','A320','A321','A330','A350','A380','B737','B738','B739','B73B','B73C','B73M','B74I','B74J','B763','B772','B773','B77X','B788','B789','B78J','B78X']
AIRPORTS = ['KJFK','KDFW','KORD','KRDU','KLAX','KSFO','KATL','KSLC','EGLL','EGKK','ZBAA','ZSPD','OMDB','RJTT','VHHH']
AIRLINES = ['SIG','ACM','TEA','POT','SAC','IES','DPG','JTW','JFB','PEB','AVD','DCE']

def genFlightStrip(win,back,offset=0,out=True):
    font = "Bookman"
    delta = np.array((0,0)) if win.viewPos is None else win.viewPos
    flightStr = '%s%03d'%(random.choice(AIRLINES), random.randint(2,895))
    planeStr = random.choice(PLANES)
    destStr = random.choice(AIRPORTS)
    timeStr = (datetime.now() + timedelta(minutes=offset)).strftime('%H%M')
    size = np.array(back.size)
    flightStim = visual.TextStim(win,height=(size[0]*.05),pos=(size*np.array((-.47*(win.flipHoriz*-2+1),.02)))+back.pos+delta,autoLog=True, flipHoriz=win.flipHoriz, font=font, text=flightStr, alignHoriz='left')
    planeStim = visual.TextStim(win,height=(size[0]*.04),pos=(size*np.array((.01*(win.flipHoriz*-2+1),.21)))+back.pos+delta,autoLog=True, flipHoriz=win.flipHoriz, font=font, text=planeStr, alignHoriz='right')
    destStim = visual.TextStim(win,height=(size[0]*.04),pos=(size*np.array((.01*(win.flipHoriz*-2+1),-.2)))+back.pos+delta,autoLog=True, flipHoriz=win.flipHoriz, font=font, text=destStr, alignHoriz='right')
    timeStim = visual.TextStim(win,height=(size[0]*.05),pos=(size*np.array((.35*(win.flipHoriz*-2+1),.02)))+back.pos+delta,autoLog=True, flipHoriz=win.flipHoriz, font=font, text=timeStr, alignHoriz='right')
    #calculate the rectangle
    _, leftBotPix, _, rightTopPix = back.verticesPix
    monPix = np.array(win.monitor.getSizePix())/2
    left, bot = leftBotPix/monPix #- win.viewPos/2
    right, top = rightTopPix/monPix #- win.viewPos/2
    rect = [left,top,right,bot] if not win.flipHoriz else [right,top,left,bot]
    #create the stim
    stim = visual.BufferImageStim(win, stim=[back,flightStim,planeStim,destStim,timeStim],rect=rect,flipHoriz=False)
    stim.units = 'deg'
    stim.size = back.size
    #print(stim.size)
    #print(rightTopPix-leftBotPix)
    #stim.size = tools.monitorunittools.pix2deg(rightTopPix-leftBotPix,win.monitor)
    #print(stim.size)
    #print(back.size)
    #print(np.array((right-left,top-bot)))
    #stim.size = np.array((right-left,top-bot))
    #print(stim._texID)
    #img = visual.ImageStim(win,units='deg')
    #img.image = np.array(((0,),))
    #img._needTextureUpdate=False
    #img._texID = stim._texID
    #img._updateList()
    #print(img._texID)
    #print(img.useShaders)
    #print(img.image)
    #img.size = back.size
    #img.pos = back.pos
    #debugging
    #vertR = visual.Line(win=win, units='norm', start=(rect[0],rect[1]), end=(rect[0],rect[3]))
    #vertL = visual.Line(win=win, units='norm', start=(rect[2],rect[1]), end=(rect[2],rect[3]))
    #vertT = visual.Line(win=win, units='norm', start=(rect[0],rect[1]), end=(rect[2],rect[1]))
    #vertB = visual.Line(win=win, units='norm', start=(rect[0],rect[3]), end=(rect[2],rect[3]))
    #lines = [vertR,vertL,vertT,vertB]
    return stim 

class ATCExperiment(Experiment):
    def __init__(self, config, append=True):
        config.viewPos=False
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
        #setup some globals
        self.farWin = self.windows[3:6]
        targetWin = self.windows[1]
        overdriveWin = self.windows[0]
        #fontFiles = [os.path.join(self.config.assetsPath,self.config.stimulusFont)]  # set fontFiles to include our local version of snellen rather than using installed version
        #font = os.path.splitext(self.config.stimulusFont)[0]
        #font = "Bookman"
        #setup some progress strips
        win = targetWin
        self.fpsOutBlank = visual.ImageStim(targetWin,os.path.join(self.config.assetsPath,'stripOutbound.png'),pos=[0,0],flipHoriz=targetWin.flipHoriz)
        self.fpsInBlank  = visual.ImageStim(targetWin,os.path.join(self.config.assetsPath,'stripInbound.png') ,flipHoriz=targetWin.flipHoriz)
        back = self.fpsOutBlank
        self.strip2 = genFlightStrip(win,back)
        #flightStr = '%s%03d'%(random.choice(AIRLINES), random.randint(2,895))
        #planeStr = random.choice(PLANES)
        #destStr = random.choice(AIRPORTS)
        #timeStr = (datetime.now() + timedelta(minutes=0)).strftime('%H%M')
        #size = np.array(back.size)
        #self.flightStim = visual.TextStim(win,height=(size[0]*.05),pos=(size*np.array((-.47*(win.flipHoriz*-2+1),.02)))+back.pos+win.viewPos,autoLog=True, flipHoriz=win.flipHoriz, fontFiles=fontFiles, font=font, text=flightStr, alignHoriz='left')
        #self.planeStim = visual.TextStim(win,height=(size[0]*.04),pos=(size*np.array((.01*(win.flipHoriz*-2+1),.21)))+back.pos+win.viewPos,autoLog=True, flipHoriz=win.flipHoriz, fontFiles=fontFiles, font=font, text=planeStr, alignHoriz='right')
        #self.destStim = visual.TextStim(win,height=(size[0]*.04),pos=(size*np.array((.01*(win.flipHoriz*-2+1),-.2)))+back.pos+win.viewPos,autoLog=True, flipHoriz=win.flipHoriz, fontFiles=fontFiles, font=font, text=destStr, alignHoriz='right')
        #self.timeStim = visual.TextStim(win,height=(size[0]*.05),pos=(size*np.array((.35*(win.flipHoriz*-2+1),.02)))+back.pos+win.viewPos,autoLog=True, flipHoriz=win.flipHoriz, fontFiles=fontFiles, font=font, text=timeStr, alignHoriz='right')
        for win in self.windows:
            win.viewPos = np.array(win.monitor.center)
        
        #setup arrows
        arrows = []
        for direction in ['Left', 'Down', 'Right', 'Up']:
            stim = visual.ImageStim(self.windows[1],os.path.join(self.config.assetsPath,'buttonW%s.png'%direction))

        self.strip2.win = self.windows[0]
        self.strip2.pos = TAXI[0] + self.windows[0].viewPos
        #print(self.strip1.size)
        
        #self.fpsOutBlank.pos = TAXI[0]
        #print(self.strip1.units)
        #setup backgrounds
        self.background = []
        imgs = os.path.join(self.config.assetsPath,"runway_%s.png")
        for idx, win in enumerate(self.farWin):
            back = visual.ImageStim(win,imgs%(idx+1),pos=-win.viewPos)
            self.background.append(back)
        self.fpsBoard = visual.ImageStim(targetWin,os.path.join(self.config.assetsPath,'FPSboard.png'),pos=(-.16,-11.54)+targetWin.viewPos,flipHoriz=targetWin.flipHoriz)
        self.fpsBoarda = visual.ImageStim(overdriveWin,os.path.join(self.config.assetsPath,'FPSboard.png'),pos=(-.16,-11.54)+targetWin.viewPos,flipHoriz=overdriveWin.flipHoriz,size=self.fpsBoard.size)
        
        self.animated = []
    def setupHandler(self):
        pass
    def flip(self):
        self.animate()
        for window in self.activeWindows:
            window.flip()
        allKeys = event.getKeys()
        for key in allKeys:
            if key == 'escape':
                core.quit()
        if self.joyStateChanged():
            self.changeState()
        event.clearEvents()
    def animate(self):
        for element in self.animated:
            element.animate()
    def run(self):
        #if self.newUser:
        self.demo()
        #self.tutorial()
        #self.proceedure()
    def demo(self):
        for stim in self.background:
            self.present(stim)
        self.present(self.fpsBoard)
        self.present(self.fpsBoarda)
        #self.present(self.fpsOutBlank)
        self.present(self.strip2)
        self.waitTime(1000)
    def changeState(self):
        if self.joyButs[0]:  # 'A'
            pass
        if self.joyButs[1]:  # 'B'
            pass
        if self.joyButs[7]:  # 'Start'
            pass
        if self.joyHats != [[0,0]]:
            self.strip2.pos += np.array((self.joyHats[0][0]*.1,self.joyHats[0][1]*.1))
            #self.fpsOutBlank.pos += np.array((self.joyHats[0][0]*1,self.joyHats[0][1]*1))
            print(self.strip2.pos-self.windows[1].viewPos)
            #print(self.strip1._verticesBase)
            #self.strip2._updateVertices()
            #pix = tools.monitorunittools.convertToPix(self.strip2._verticesBase,self.strip2.pos,self.strip2.units,self.windows[1])
            #print(self.strip2._verticesBase)
            #print(self.strip2.pos)
            #print(self.strip2.win)
            #print(self.strip2.units)
            #print(self.strip2.size)
            #print(self.strip2.verticesPix)
            #print(self.strip2.thisScale)
            #print(self.strip1.verticesPix)
            #print(pix)
            #self.strip2._needVertexUpdate = True
            #self.strip2._needUpdate = True
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

class AnimatedStim(object):
    def __init__(self, stim):
        self._stim = stim
        self.goal = np.array(self._stim.pos)
        self.speed = np.array((1,1))
    def __getattr__(self,attr):
        return getattr(self._stim, attr)
    def __setattr__(self,attr,value):
        setattr(self._stim, attr, value)
    def animate(self):
        sign = np.sign(self.goal-self._stim.pos)
        self._stim.pos += self.speed * sign


if __name__ == '__main__':
    '''
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
    '''
    config.storeData = False
    experiment = ATCExperiment(config)
    experiment.run()
    experiment.close()
