from __future__ import print_function

#This analysis script takes one or more staircase datafiles as input
#from a GUI. It then plots the staircases on top of each other on
#the left and a combined psychometric function from the same data
#on the right

import sys, os
sys.path.append('./submodules')
from psychopy import data, gui, core
from psychopy.tools.filetools import fromFile
import pylab

#Open a dialog box to select files from
files = gui.fileOpenDlg('.')
if not files:
    core.quit()

#get the data from all the files
allIntensities, allResponses, labels = [],[], []
for thisFileName in files:
    thisDat = fromFile(thisFileName)
    if isinstance(thisDat, data.staircase.MultiStairHandler):
        for handler in thisDat.staircases:
            allIntensities.append( handler.intensities )
            allResponses.append( handler.data )
            labels.append(handler.condition['label'])
    else:
        allIntensities.append( thisDat.intensities )
        allResponses.append( thisDat.data )
        labels.append(thisFileName)

#plot each staircase
pylab.subplot(121)
colors = 'brgkcmbrgkcm'
lines, names = [],[]
for labelN, thisStair in enumerate(allIntensities):
    #lines.extend(pylab.plot(thisStair))
    #names = labels[labelN]
    pylab.plot(thisStair, label=labels[labelN])

pylab.legend()

'''#get combined data
combinedInten, combinedResp, combinedN = \
             data.functionFromStaircase(allIntensities, allResponses, 5)
#fit curve - in this case using a Weibull function
fit = data.FitWeibull(combinedInten, combinedResp, guess=[0.2, 0.5])
smoothInt = pylab.arange(min(combinedInten), max(combinedInten), 0.001)
smoothResp = fit.eval(smoothInt)
thresh = fit.inverse(0.8)
print(thresh)

#plot curve
pylab.subplot(122)
pylab.plot(smoothInt, smoothResp, '-')
pylab.plot([thresh, thresh],[0,0.8],'--'); pylab.plot([0, thresh],\
[0.8,0.8],'--')
pylab.title('threshold = %0.3f' %(thresh))
#plot points
pylab.plot(combinedInten, combinedResp, 'o')
pylab.ylim([0,1])
'''
pylab.show()
