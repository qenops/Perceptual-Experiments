from latencyExp import Experiment, visual, event, core
import numpy as np
import os
import config

class AlignExperiment(Experiment):
    def setupStimuli(self):
        self.current = 0
        self.wait = True
        allStim = []
        self.horizStim = []
        self.rightStim = []
        self.leftStim = []
        for win in self.windows:
            horiz = visual.Line(win=win, start=(-10,0), end=(10,0))
            self.horizStim.append(horiz)
            allStim.append(horiz)
            vertR = visual.Line(win=win, units='cm', start=(-3,-100), end=(-3,100))
            vertL = visual.Line(win=win, units='cm', start=(3,-100), end=(3,100))
            self.rightStim.append(vertR)
            self.leftStim.append(vertL)
            allStim.append(vertR)
            allStim.append(vertL)
        indicatorStim = visual.TextStim(win=win,height=.3,pos=[-3,3],autoLog=True, flipHoriz=win.flipHoriz)
        indicatorStim.fontFiles = [os.path.join(self.config.assetsPath,self.config.stimulusFont)]  # set fontFiles to include our local version of snellen rather than using installed version
        indicatorStim.font = os.path.splitext(self.config.stimulusFont)[0]
        indicatorStim.text = '%s'%self.current
        allStim.append(indicatorStim)
        self.stimuli = allStim
        self.stimuliTime = [0] * len(self.stimuli)
    def proceedure(self):
        '''The proceedure of the experiment'''
        for stim in self.horizStim:
            self.presentStimulus(self.stimuli.index(stim))
        while(self.wait):
            self.flip()
        self.wait=True
        self.clearStimuli()
        for stim in self.leftStim:
            self.presentStimulus(self.stimuli.index(stim))
        while(self.wait):
            self.flip()
        self.wait=True
        self.clearStimuli()
        for stim in self.rightStim:
            self.presentStimulus(self.stimuli.index(stim))
        while(self.wait):
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
            v = np.array(self.windows[self.current].viewPos)
            v += np.array(self.joyHats[0])/25
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
            if key == 'return':
                print('continuing...')
                self.wait = False
        if self.joyStateChanged():
            self.changeState()
        event.clearEvents()



if __name__ == '__main__':
    experiment = AlignExperiment(config, False)
    experiment.run()
    experiment.close()