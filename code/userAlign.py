from latencyExp import Experiment, visual, event, core
import numpy as np
import os
import config

class AlignExperiment(Experiment):
    def setupStimuli(self):
        self.curState = 0
        self.wait = True
        self.done = False
        allStim = []
        self.horizStim = []
        self.rightStim = []
        self.leftStim = []
        for win in self.windows:
            horiz = visual.Line(win=win, start=(-10,0), end=(10,0))
            self.horizStim.append(horiz)
            allStim.append(horiz)
            sign = -1 if win.flipHoriz else 1
            vertR = visual.Line(win=win, units='cm', start=(3*sign,-100), end=(3*sign,100))
            vertL = visual.Line(win=win, units='cm', start=(3*sign*-1,-100), end=(3*sign*-1,100))
            vertR.sign = sign
            vertL.sign = sign
            self.rightStim.append(vertR)
            self.leftStim.append(vertL)
            allStim.append(vertR)
            allStim.append(vertL)
        self.stimuli = allStim
        self.stimuliTime = [0] * len(self.stimuli)
        self.states = [self.horizStim, self.leftStim, self.rightStim, self.leftStim + self.rightStim]
    def proceedure(self):
        '''The proceedure of the experiment'''
        while not self.done:
            for stim in self.states[self.curState]:
                self.presentStimulus(self.stimuli.index(stim))
            while(self.wait):
                self.flip()
            self.wait=True
            self.clearStimuli()
    def changeState(self):
        if self.joyButs[0]:
            print('continuing...')
            self.curState = (self.curState + 1) % len(self.states)
            self.wait = False
        if self.joyButs[1]:
            print('continuing...')
            self.curState = (self.curState - 1) % len(self.states)
            self.wait = False
        if self.joyHats != [0,0]:
            for stim in self.rightStim:
                stim.start = (stim.start[0] + self.joyHats[0][1] * stim.sign / 20, stim.start[1])
                stim.end = (stim.end[0] + self.joyHats[0][1] * stim.sign / 20, stim.end[1])
            print(stim.start[0],end=', ')
            for stim in self.leftStim:
                stim.start = (stim.start[0] + self.joyHats[0][1] * stim.sign / -20, stim.start[1])
                stim.end = (stim.end[0] + self.joyHats[0][1] * stim.sign / -20, stim.end[1])
            print(stim.start[0])
    def flip(self):
        for window in self.activeWindows:
            window.flip()
        allKeys = event.getKeys()
        for key in allKeys:
            if key == 'escape':
                core.quit()
            if key == 'return':
                print('continuing...')
                self.curState = (self.curState + 1) % len(self.states)
                self.wait = False
        if self.joyStateChanged():
            self.changeState()
        event.clearEvents()



if __name__ == '__main__':
    experiment = AlignExperiment(config, False)
    experiment.run()
    experiment.close()