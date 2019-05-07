################################################################################
# Config automatically generated by dUtils.configFiles version 0.1
################################################################################

### loading monitors ###
import psychopy.monitors.calibTools

mon_33cm = psychopy.monitors.calibTools.Monitor(name="33cm")
mon_33cm.currentCalib['distance'] = 33.0
mon_33cm.currentCalib['sizePix'] = [2048, 1536]
mon_33cm.currentCalib['width'] = 20.0
mon_33cm.screenPos = (-2560, 1440)
mon_33cm.center = (0.56,2.84)  # position of center in units
#mon_33cm.screen = 2
mon_33cm.flipHoriz = True
mon_33cm.color = [-1,-1,-1]

mon_50cm = psychopy.monitors.calibTools.Monitor(name="50cm")
mon_50cm.currentCalib['distance'] = 50.0
mon_50cm.currentCalib['sizePix'] = [2048, 1536]
mon_50cm.currentCalib['width'] = 20.0
mon_50cm.screenPos = (-512, 1440)
mon_50cm.center = (0,0.24)  # position of center in units
#mon_50cm.screen = 4
mon_50cm.flipHoriz = True
mon_50cm.color = [-1,-1,-1]

mon_100cm = psychopy.monitors.calibTools.Monitor(name="100cm")
mon_100cm.currentCalib['distance'] = 100.0
mon_100cm.currentCalib['sizePix'] = [2560, 1440]
mon_100cm.currentCalib['width'] = 70.8
mon_100cm.screenPos = (1536, 1440)
mon_100cm.center = (-.66,6.24)  # position of center in units
#mon_100cm.screen = 5
mon_100cm.flipHoriz = True
mon_100cm.color = [-1,-1,-1]

mon_800cm = psychopy.monitors.calibTools.Monitor(name="800cm")
mon_800cm.currentCalib['distance'] = 800.0
mon_800cm.currentCalib['sizePix'] = [1080, 1920]
mon_800cm.currentCalib['width'] = 86.5
mon_800cm.screenPos = (-2560, 2976)
mon_800cm.center = (-0.08,-0.08)  # position of center in units
#mon_800cm.screen = 3
mon_800cm.flipHoriz = False
mon_800cm.color = [-1,-1,-1]

mon_801cm = psychopy.monitors.calibTools.Monitor(name="801cm")
mon_801cm.currentCalib['distance'] = 800.0
mon_801cm.currentCalib['sizePix'] = [1080, 1920]
mon_801cm.currentCalib['width'] = 86.5
mon_801cm.screenPos = (-1480, 2976)
mon_801cm.center = (-0.08,-0.08)  # position of center in units
mon_801cm.flipHoriz = False
mon_801cm.color = [-1,-1,-1]

mon_802cm = psychopy.monitors.calibTools.Monitor(name="802cm")
mon_802cm.currentCalib['distance'] = 800.0
mon_802cm.currentCalib['sizePix'] = [1080, 1920]
mon_802cm.currentCalib['width'] = 86.5
mon_802cm.screenPos = (-400, 2976)
mon_802cm.center = (-0.08,-0.08)  # position of center in units
mon_802cm.flipHoriz = False
mon_802cm.color = [-1,-1,-1]

monitors=[mon_33cm,mon_50cm,mon_100cm,mon_800cm,mon_801cm,mon_802cm]
#monitors=[mon_33cm,mon_50cm]
#monitors=[mon_33cm]

#figure out which monitor is which pyglet screen
import pyglet
window = pyglet.window.Window()
platform = pyglet.window.get_platform()
display = platform.get_default_display()
screens = display.get_screens()
for monitor in monitors:
    monitor.screen = screens.index(list(filter(lambda x: x.x==monitor.screenPos[0] and x.y==monitor.screenPos[1],screens))[0])
window.close()

### joystick parameters ###
joyID = 0

### data parameters ###
dataPath = './airData'
userFile = 'users.psydat'
stairFile = 'stair'

### stimulus parameters ###
primeHeight = .15
primePresentations = [1,1,1,1,2,2,2,2,3,3,4]
mainHeight = 10/60  # gap size = 2 arc min
mainChars = ['{','|','}','~'] # L, D, R, U (in font)
mainResponses = [[-1,0],[0,-1],[1,0],[0,1]] # L, D, R, U (on joystick hat)

### assets parameters ###
assetsPath = './assets'
stimulusFont = 'Snellen.ttf'

### log file ###
from psychopy import logging
logFile = 'experimentLog.log'
logLevel = logging.INFO
