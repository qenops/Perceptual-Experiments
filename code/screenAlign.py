from experiment import Experiment, visual, event, core
import numpy as np
import os
import config

class AlignExperiment(Experiment):
    def __init__(self, config):
        config.storeData = False
        super().__init__(config)
    def setupData(self):
        pass
    def setupStimuli(self):
        self.current = 0
        allStim = []
        self.rightStim = []
        self.leftStim = []
        for win in self.windows:
            stim = visual.Circle(win=win, units='deg',radius=.3, edges=32)
            allStim.append(stim)
            '''
            sign = -1 if win.flipHoriz else 1
            vertR = visual.Line(win=win, units='cm', start=(3*sign,-100), end=(3*sign,100))
            vertL = visual.Line(win=win, units='cm', start=(3*sign*-1,-100), end=(3*sign*-1,100))
            vertR.sign = sign
            vertL.sign = sign
            self.rightStim.append(vertR)
            self.leftStim.append(vertL)
            allStim.append(vertR)
            allStim.append(vertL)
            '''
        indicatorStim = visual.TextStim(win=win,units='deg',height=.3,pos=[-3,3],autoLog=True, flipHoriz=win.flipHoriz)
        indicatorStim.fontFiles = [os.path.join(self.config.assetsPath,self.config.stimulusFont)]  # set fontFiles to include our local version of snellen rather than using installed version
        indicatorStim.font = os.path.splitext(self.config.stimulusFont)[0]
        indicatorStim.text = '%s'%self.current
        allStim.append(indicatorStim)
        self.stimuli = allStim
        self.stimuliTime = [0] * len(self.stimuli)
    def proceedure(self):
        '''The proceedure of the experiment'''
        for idx in range(len(self.stimuli)):
            self.presentStimulus(idx)
        while(True):
            self.flip()
    def changeState(self):
        if self.joyButs[0]:
            self.current += 1
            #print(self.current)
        if self.joyButs[1]:
            self.current -= 1
            #print(self.current)
        self.current %= len(self.windows)
        self.stimuli[-1].text = '%s'%self.current
        if self.joyHats != [0,0]:
            '''
            for stim in self.rightStim:
                if isinstance(stim,visual.Line):
                    stim.start = (stim.start[0] + self.joyHats[0][1] * stim.sign / 40, stim.start[1])
                    stim.end = (stim.end[0] + self.joyHats[0][1] * stim.sign / 40, stim.end[1])
            print(self.rightStim[0].start[0],end=', ')
            for stim in self.leftStim:
                if isinstance(stim,visual.Line):
                    stim.start = (stim.start[0] + self.joyHats[0][1] * stim.sign / -40, stim.start[1])
                    stim.end = (stim.end[0] + self.joyHats[0][1] * stim.sign / -40, stim.end[1])
            print(self.leftStim[0].start[0])
            '''
            v = np.array(self.windows[self.current].viewPos)
            v += np.array(self.joyHats[0])
            self.windows[self.current].viewPos = v
            self.stimuli[self.current]._needVertexUpdate = True
            self.stimuli[self.current]._needUpdate = True
            for win in self.windows:
                print(win.viewPos, end=", ")
            print('\n')
    def flip(self):
        for window in self.activeWindows:
            window.flip()
        allKeys = event.getKeys()
        for key in allKeys:
            if key == 'escape':
                core.quit()
        if self.joyStateChanged():
            self.changeState()
        event.clearEvents()



if __name__ == '__main__':
    experiment = AlignExperiment(config)
    experiment.run()
    experiment.close()