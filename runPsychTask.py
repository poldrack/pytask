"""
runPsychTask
"""

import psychopy
from psychopy import visual, core, event, logging, data, misc, sound
import os, socket, random
import json

from psychtask import psychTask


#set-up some variables

verbose=True
fullscr=False  # change to True for full screen display
subdata=[]

# set things up

task=psychTask('test.yaml','test1')


task.writeToLog(task.toJSON())

# prepare to start
task.setupWindow()
task.presentTextToWindow('Waiting for key to begin (or press 5)\nPress q to quit')
resp,task.startTime=task.waitForKeypress(task.trigger_key)
task.checkRespForQuitKey(resp)
event.clearEvents()

for trial in task.stimulusInfo:
    # wait for onset time
    while core.getTime() < trial['onset'] + task.startTime:
            key_response=event.getKeys(None,True)
            if len(key_response)==0:
                continue
            for key,response_time in key_response:
                if task.quit_key==key:
                    task.shutDownEarly()
                elif task.trigger_key==key:
                    task.trigger_times.append(response_time-task.startTime)
                    continue

    trial=task.presentTextTrial(trial)
    task.writeToLog(json.dumps(trial))
    task.alldata.append(trial)

task.writeToLog(json.dumps({'trigger_times':task.trigger_times}))

# clean up
task.shutDownAndSave()

task.closeWindow()
