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
from matplotlib.font_manager import FontProperties

#Open a dialog box to select files from
files = gui.fileOpenDlg('.')
if not files:
    core.quit()

#plot each staircase
fig = Figure()
canvas = FigureCanvas(fig)
sc = fig.add_subplot(111)
fig2 = Figure()
canvas2 = FigureCanvas(fig2)
ax = fig2.add_subplot(111)
fig3 = Figure()
canvas3 = FigureCanvas(fig3)
ax2 = fig3.add_subplot(111)
allData = [[],[],[],[]]
#get the data from all the files
for thisFileName in files:
    sc.clear()
    handler = fromFile(thisFileName)
    if isinstance(handler, data.staircase.MultiStairHandler):
        t1 = []
        t3 = []
        lat = []
        for staircase in handler.staircases:
            if not staircase.condition.get('dummy',False):
                sc.plot(staircase.intensities, label=staircase.condition['label'])
                t1.append(staircase.otherData['extraLatency'][-1])
                t3.append(staircase.otherData['totalLatency'][-1])
            if staircase.condition['driveFrames'] == 0:
                di = staircase.condition['prime']-staircase.condition['stim']
                la = staircase.otherData['totalLatency'][-1]
                lat.append((di,la))
                
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
        sc.legend()
        sc.set_title('User %s - %s staircase'%(handler.userInfo['ID'],handler.userInfo['Date'][-1]))
        sc.xaxis.set_label_text('Trial')
        sc.yaxis.set_label_text('T2')
        canvas.print_figure(os.path.splitext((thisFileName))[0])
        #ax.plot(t1[:4],t3[:4],label=os.path.split(os.path.splitext((thisFileName))[0])[1])
        #ax.plot(t1[:4],t3[:4],'.-',label='User %s - %s'%(handler.userInfo['ID'],handler.userInfo['Date'][-1]),linewidth=0.5)
        ax.plot(t1[:4],t3[:4],'.-',label='User %s'%(handler.userInfo['ID']),linewidth=0.5)
        #ax.scatter(t1[:4],t3[:4])
        for idx, d in enumerate(zip(t1,t3)):
            allData[idx].append(d)
        lat.sort(key=lambda a: a[0])
        #ax2.plot(list(zip(*lat))[0],list(zip(*lat))[1],label='User %s - %s'%(handler.userInfo['ID'],handler.userInfo['Date'][-1]))
        ax2.plot(list(zip(*lat))[0],list(zip(*lat))[1],label='User %s'%(handler.userInfo['ID']))
        ax2.scatter(list(zip(*lat))[0],list(zip(*lat))[1])
fontP = FontProperties()
fontP.set_size('small')
# plot averages
avg = [[sum(x)/len(x) for x in zip(*i)] for i in allData]
ax.plot(list(zip(*avg))[0],list(zip(*avg))[1],'.-',label='Mean',linewidth=2.0)
ax.legend(prop=fontP)
ax.xaxis.set_label_text('T1 (seconds)')
ax.yaxis.set_label_text('T1+T2 (seconds)')
ax.set_title('Overdriven Latency')
ax.set_ylim(bottom=0)
ax.set_xlim(left=0,right=.3)
ax.plot([0,.1,.2,.3],[0,.1,.2,.3],'-.',color='gray',linewidth=1)
canvas2.print_figure('sac-0')

ax2.legend()
ax2.xaxis.set_label_text('Diopters')
ax2.yaxis.set_label_text('Re-focus Time (seconds)')
ax2.set_title('Latency')
ax2.set_ylim(bottom=0)
canvas3.print_figure('sac-1')

def make_od_plot():
    near = []
    for stair in handler.staircases:
        print(stair.condition['label'],stair.otherData['totalLatency'][-1])
    t1 = []
    t3 = []
    for stair in handler.staircases:
        t1.append(stair.otherData['extraLatency'][-1])
        t3.append(stair.otherData['totalLatency'][-1])
    fig = Figure()
    canvas = FigureCanvas(fig)
    ax = fig.add_subplot(111)
    colors = 'brgkcmbrgkcm'
    ax.plot(t1[:4],t3[:4],label='near 2 diopters')
    ax.legend()
    ax.xaxis.set_label_text('T1')
    ax.yaxis.set_label_text('T1+T2')
    ax.scatter(t1[:4],t3[:4])
    ax.set_title('Latency for User 0')
    ax.set_ylim(bottom=0,top=.5)
    ax.plot([0,.1,.2,.25],[0,.1,.2,.25],'--',color='gray',linewidth=1)
    canvas.print_figure('OD-0')


def make_latency_plot():    
    near = [0.048, 0.224, 0.384, 0.56]
    far = [0.048, 0.192, 0.336, 0.41600000000000004]
    diopters = [0,1,2,3]
    fig = Figure()
    canvas = FigureCanvas(fig)
    ax = fig.add_subplot(111)
    colors = 'brgkcmbrgkcm'
    ax.plot(far, label='far')
    ax.plot(near, label='near')
    ax.legend()
    ax.xaxis.set_label_text('Diopters')
    ax.yaxis.set_label_text('Seconds')
    ax.scatter(diopters,far)
    ax.scatter(diopters,near)
    ax.set_title('Latency for User: 0')
    canvas.print_figure('latency_0')
