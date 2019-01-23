from latencyExp import Experiment, visual, event, core, data
import numpy as np
import os, random
import config

class AcuityExperiment(Experiment):
    def setupStimuli(self):
        # create the 4 stimuli
        self.stimuli = []
        win = self.windows[-1]
        self.chars = ['{','|','}','~'] # L, D, R, U (in font)
        self.responses = [[-1,0],[0,-1],[1,0],[0,1]] # L, D, R, U (on joystick hat)
        for char in self.chars:
            textStim = visual.TextStim(win=win,height=25/60,units='deg',pos=win.viewPos,autoLog=True,flipHoriz=win.flipHoriz)
            textStim.fontFiles = [os.path.join(self.config.assetsPath,self.config.stimulusFont)]  # set fontFiles to include our local version of snellen rather than using installed version
            textStim.font = os.path.splitext(self.config.stimulusFont)[0]
            textStim.text = char
            self.stimuli.append(textStim)
        self.stimuliTime = [0] * len(self.stimuli)
    def setupHandler(self):
        # create the staircase handler
        self.handler = data.StairHandler(startVal = 60, minVal=0,
                                stepType = 'db', stepSizes=[10,5,2.5,2.5,1.25,1.25],
                                nUp=1, nDown=3,  # will home in on the 80% threshold
                                nTrials=10)
        #self.handler = data.QuestHandler(startVal=25, startValSd=25, pThreshold=0.82,nTrials=50,stopInterval=.9,minVal=1)
    def proceedure(self):
        '''The proceedure of the experiment'''
        count = 0
        for size in self.handler:
            current = random.randint(0,len(self.stimuli)-1)
            self.stimuli[current].height = size/60
            self.presentStimulus(current)
            correct = self.waitForResponse(self.joy.getAllHats,[0],true=[self.responses[current]],false=[i for i in self.responses if i != self.responses[current]])
            self.clearStimuli()
            self.handler.addResponse(correct)
            count += 1
            print('Trial # %s: size = %s'%(count,size))
            self.waitTime(1)
        self.acuity = size*4
        




if __name__ == '__main__':
    experiment = AcuityExperiment(config, False)
    experiment.run()
    print('Acuity is: 20/%s'%experiment.acuity)
    experiment.close()