from experiment import Experiment, visual, event, core, data
import numpy as np
import os, random
import config

class ScreenGrating(Experiment):
    def __init__(self, config):
        config.storeData = False
        super().__init__(config)
    def setupData(self):
        pass
    def setupStimuli(self):
        # create the 4 stimuli
        self.stimuli = []
        for idx, win in enumerate(self.windows):
            grating = visual.GratingStim(win=win, mask="circle", size=3, pos=[-2*(2*win.flipHoriz-1),-9+(4*idx)], sf=14, ori=45,interpolate=True)
            self.stimuli.append(grating)
            grating = visual.GratingStim(win=win, mask="circle", size=3, pos=[2*(2*win.flipHoriz-1),-9+(4*idx)], sf=14, ori=135,interpolate=True)
            self.stimuli.append(grating)
        self.stimuliTime = [0] * len(self.stimuli)
    def proceedure(self):
        '''The proceedure of the experiment'''
        for stim in self.stimuli:
            self.present(stim)
        while(True):
            self.flip()
    def changeState(self):
        if self.joyHats != [[0,0]]:
            for stim in self.stimuli:
                stim.sf += self.joyHats[0][0]
                stim._needVertexUpdate = True
                stim._needUpdate = True
            print(stim.sf)
    def flip(self):
        if self.joyStateChanged():
            self.changeState()
        super().flip()

if __name__ == '__main__':
    experiment = ScreenGrating(config)
    experiment.run()
    experiment.close()
