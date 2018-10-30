#!/usr/bin/python
''' 
Perceptual experiment for testing the latency of human perception in relation to focal change, frequency, and contrast
    
David Dunn
Oct 2018 - created
www.qenops.com
'''
__author__ = ('David Dunn')
__version__ = '1.0'

import sys, os
sys.path.append('./submodules')
import dDisplay.varifocal as vf
import dGraph as dg
import dGraph.ui as dgui
import dGraph.cameras as dgc
import dGraph.shapes as dgs
import dGraph.render as dgr
import dGraph.materials as dgm
import dGraph.shaders as dgshdr
import dGraph.lights as dgl
import dGraph.util.imageManip as dgim
import multiprocessing as mp
import numpy as np
import time, math
import config