#This analysis script takes one or more staircase datafiles as input
#from a GUI. It then plots the staircases on top of each other on
#the left and a combined psychometric function from the same data
#on the right

import sys, os
sys.path.append('./submodules')
from psychopy import data, gui, core
from psychopy.tools.filetools import fromFile
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

#Open a dialog box to select files from
files = gui.fileOpenDlg('.')
if not files:
    core.quit()

#plot each staircase
fig = Figure()
canvas = FigureCanvas(fig)
ax = fig.add_subplot(111)
colors = 'brgkcmbrgkcm'
lines, names = [],[]
#get the data from all the files
for thisFileName in files:
    thisDat = fromFile(thisFileName)
    if isinstance(thisDat, data.staircase.MultiStairHandler):
        for handler in thisDat.staircases:
            if not handler.condition.get('dummy',False):
                ax.plot(handler.intensities, label=handler.condition['label'])
            #ax.plot(handler.data)
            '''
            combinedInten, combinedResp, combinedN = \
             data.functionFromStaircase(handler.intensities, handler.data, 10)
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
        ax.legend()
        canvas.print_figure(os.path.splitext((thisFileName))[0])
