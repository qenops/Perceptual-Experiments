from experiment import Experiment, visual, event, core
import numpy as np
import os
import config

class AlignExperiment(Experiment):
    def setupData(self):
        pass
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
        # set up text prompts:
        font = "Bookman"
        height = .5
        win = self.windows[2]
        promptHoriz = visual.TextStim(win=win,height=height,pos=win.viewPos+np.array((0,3)),flipHoriz=win.flipHoriz,font=font,alignHoriz='center',
            text='Raise/lower chinrest until lines align.\nPress "A" button to continue...')
        self.horizStim.append(promptHoriz)
        allStim.append(promptHoriz)
        promptLeft = visual.TextStim(win=win,height=height,pos=win.viewPos+np.array((4,0)),flipHoriz=win.flipHoriz,font=font,alignHoriz='right',
            text='Close right eye.\nPress up/down on the d-pad until lines align.\nPress "A" button to continue...')
        self.leftStim.append(promptLeft)
        allStim.append(promptLeft)
        promptRight = visual.TextStim(win=win,height=height,pos=win.viewPos+np.array((-4,0)),flipHoriz=win.flipHoriz,font=font,alignHoriz='left',
            text='Close left eye.\nPress up/down on the d-pad until lines align.\nPress "A" button to continue...and "B" button to go back.')
        self.rightStim.append(promptRight)
        allStim.append(promptRight)
        promptEnd = visual.TextStim(win=win,height=height,pos=win.viewPos+np.array((4.5,3)),flipHoriz=win.flipHoriz,font=font,alignHoriz='right',
            text='Without moving your head,\nmake sure both eyes are aligned.\nPress "Start" when done.')
        allStim.append(promptEnd)
        self.stimuli = allStim
        self.stimuliTime = [0] * len(self.stimuli)
        self.states = [self.horizStim, self.leftStim, self.rightStim, self.leftStim + self.rightStim + [promptEnd]]
    def proceedure(self):
        '''The proceedure of the experiment'''
        while not self.done:
            for stim in self.states[self.curState]:
                self.presentStimulus(self.stimuli.index(stim))
            while(self.wait):
                self.flip()
            self.wait=True
            self.clearStimuli()
        self.ipd = abs(self.rightStim[0].start[0]) + abs(self.leftStim[0].start[0])
    def changeState(self):
        if self.joyButs[0]:
            print('continuing...')
            self.curState = (self.curState + 1) % len(self.states)
            self.wait = False
        if self.joyButs[1]:
            print('continuing...')
            self.curState = (self.curState - 1) % len(self.states)
            self.wait = False
        if self.joyButs[7]:
            print('quitting...')
            self.done = True
            self.wait = False
        if self.joyHats != [[0,0]]:
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
    config.storeData = False
    experiment = AlignExperiment(config)
    experiment.run()
    print('IPD is: %s'%experiment.ipd)
    experiment.close()