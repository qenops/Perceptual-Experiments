#!/usr/bin/python
''' 
Perceptual experiment for testing overdriving the latency human perception in relation to focal change
    
David Dunn
Jan 2019 - split from experiment
www.qenops.com
'''
__author__ = ('David Dunn')
__version__ = '1.0'

from experiment import Experiment, visual, event, core, data, SPF, logging
from latencyExp import LatencyExperiment
from userAlign import AlignExperiment
from userAcuity import AcuityExperiment

import numpy as np
import random, os

import config

class ODExperiment(LatencyExperiment):
    def setupData(self):
        pass
    def setupStimuli(self):
        pass
    def setupHandler(self):
        pass
    def proceedure(self):
        '''The proceedure of the experiment'''
        pass