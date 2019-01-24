from experiment import Experiment, visual, event, core
import numpy as np
import os
import config

class AlignExperiment(Experiment):
    def setupData(self):
        pass
    def setupStimuli(self):
        self.current = 0
        allStim = []
        for win in self.windows:
            #textStim = visual.TextStim(win=win,height=.15,pos=[0,0],autoLog=True, flipHoriz=win.flipHoriz)
            #textStim.fontFiles = [os.path.join(self.config.assetsPath,self.config.stimulusFont)]  # set fontFiles to include our local version of snellen rather than using installed version
            #textStim.font = os.path.splitext(self.config.stimulusFont)[0]
            #textStim.text = 'O'
            #allStim.append(textStim)
            stim = visual.GratingStim(win=win, mask="circle", size=.3, pos=[0,0], sf=20, contrast=0, autoLog=True)
            allStim.append(stim)
        indicatorStim = visual.TextStim(win=win,height=.3,pos=[-3,3],autoLog=True, flipHoriz=win.flipHoriz)
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
        if self.joyStateChanged():
            self.changeState()
        event.clearEvents()



if __name__ == '__main__':
    experiment = AlignExperiment(config, False)
    experiment.run()
    experiment.close()