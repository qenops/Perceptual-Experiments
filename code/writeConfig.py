import sys
from collections import OrderedDict
sys.path.append('c:\workspace')
import dUtils.configFiles as configFiles

sys.path.append('./submodules')
from psychopy import monitors
monList = monitors.getAllMonitors()

obj = monitors.Monitor(monList[0])
output = '### loading monitors ###\n'
output += 'import %s\n'%obj.__class__.__module__
default = monitors.Monitor(' ')
for nameStr in monList:
    mon = monitors.Monitor(nameStr)
    name = 'mon_%s'%(nameStr)
    diff = configFiles.dictDiff(mon.currentCalib,default.currentCalib)
    output += '%s = %s.%s(name="%s")\n'%(name, mon.__class__.__module__, mon.__class__.__name__,nameStr) 
    diff = [i for i in diff.__dir__() if i[:2] != '__']
    diff.sort()
    for k in diff:
        output += '%s.currentCalib[%r] = %r\n'%(name,k,mon.currentCalib[k])
    output += '\n'

configFiles.saveModule('config.py',output)
