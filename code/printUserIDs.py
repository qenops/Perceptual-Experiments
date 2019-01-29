import sys, os
sys.path.append('./submodules')
from operator import itemgetter
from psychopy.tools.filetools import fromFile, toFile

import config

if len(sys.argv) > 1:
    allUsers = fromFile(os.path.join(config.dataPath,str(sys.argv[1]),config.userFile))
else:
    allUsers = fromFile(os.path.join(config.dataPath,str(sys.argv[1]),config.userFile))
newlist = sorted(allUsers, key=itemgetter('Name'))
for user in newlist:
    print('ID: %s   \t%s'%(user['ID'],user['Name']))
