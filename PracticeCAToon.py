#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 16:45:22 2025

@author: sysadmin
"""


from psychopy import visual, event, core
import math
import numpy as np
import pandas as pd
import random
import os
from psychopy.hardware import keyboard
from psychopy_visionscience.noise import NoiseStim
import glob
from PIL import Image
from psychopy import prefs
import unicodedata

prefs.general['windowType'] ='pygame'
from memory_profiler import profile

# @profile
#def run_experiment():
    
mainPath = '/Users/sysadmin/Documents/NeuroScape/CAToon/CAToon_Task_Download/'
stimPath ='/Users/sysadmin/Documents/NeuroScape/CAToon/CAToon_Task_Download/CAToon_Task' 
practicePath = '/Users/sysadmin/Documents/NeuroScape/CAToon/CAToon_Task_Download/Practice' 
outPath = '/Users/sysadmin/Documents/NeuroScape/CAToon/Output'


os.chdir(outPath)
def subjInfo(outPath):
    subjNum = input("Enter main participant identifier: ") 
    if os.path.isdir(subjNum):
      subjPath = os.path.join(outPath, subjNum)  
    else: 
      os.mkdir(subjNum)
      subjPath = os.path.join(outPath, subjNum)
    return subjNum, subjPath

subjNum, subjPath = subjInfo(outPath)
os.chdir(subjPath)
if os.path.isfile('CAToon' + subjNum + '_pilotData.csv'):
    print('Warning! This subject data exists already! Please enter another subject number.')
    subjInfo(outPath)


answerKey = pd.read_csv(os.path.join(mainPath, 'AnswerKeyExample.csv'))
for a in range(answerKey.shape[0]):
    for b in range(answerKey.shape[1]):
        thisString = answerKey.iloc[a,b]
        thisString = thisString.replace(u'\xa0', u' ')
        answerKey.iloc[a,b] = thisString

answerKey.columns = ["trial", "top left", "top right", "bottom"]
for a in range(len(answerKey.trial)):
        thisStr = answerKey.loc[a, "trial"]
        thisStr = thisStr.strip()
        answerKey.loc[a, "trial"] = thisStr
        if len(thisStr) == 3:
            newStr = thisStr[0:2] + '0' + thisStr[2:len(thisStr)]
            answerKey.loc[a, "trial"] = newStr


 
os.chdir(practicePath)
allImgs = glob.glob("*.jpg")

Seq = []
Cond = []
stID = []
stimID = []

for i in range(len(allImgs)):
    thisStr = allImgs[i]
    strSeq = thisStr.split('_')
    if len(strSeq[0]) == 3:
        newStr = thisStr[0:2] + '0' + thisStr[2:len(thisStr)]
        os.rename(thisStr, newStr)
        allImgs[i] = newStr
        
        
allImg= sorted(allImgs)

for a in allImg:
    tr =+ 1
    strSeq = a.split('_')
    Seq.append(strSeq[2][:-4])
    Cond.append(a[0:2])
    
for j in range(len(allImg)):
    thisStr= allImg[j].split('_')
    stimID.append(thisStr[0])
    
    
uStimID = pd.unique(stimID)
trLen = np.arange(len(uStimID))

for t in trLen:
    u = t
    stID.extend([u, u, u, u])

for f in range(len(allImg)):
    allImg[f] = os.path.join(practicePath,allImg[f])
    
   
trIdx = np.arange(3)
seed = np.random.choice(10, 1)[0]
random.Random(seed).shuffle(trIdx)

popTrI = []
for i in trIdx:
    for j in np.arange(4):
        popTrI.append(i)

bigMat = pd.concat([pd.Series(allImg), pd.Series(Cond), pd.Series(Seq), pd.Series(stimID), pd.Series(stID), pd.Series(popTrI)], axis = 1)
bigMat.columns = ['Images', 'Condition', 'SequenceNum', 'stimID1', 'stimID2', 'trIdx']
bigMat2 = bigMat

win = visual.Window([1512,982], [0, 0], monitor="testMonitor", units="deg")

stims =pd.Series(0, index=np.arange(len(bigMat)), name='stims')
for b in range(0,len(bigMat),4):
    stimRow= bigMat.loc[(bigMat.trIdx == popTrI[b]) & (bigMat.SequenceNum == '1')]
    thisStim = stimRow.Images.iloc[0]
    s = visual.ImageStim(win, image=thisStim, size = [35, 20])
    stims.loc[b] = s
    
for b in range(1,len(bigMat),4):
    stimRow= bigMat.loc[(bigMat.trIdx == popTrI[b]) & (bigMat.SequenceNum == '2')]
    thisStim = stimRow.Images.iloc[0]
    s = visual.ImageStim(win, image=thisStim, size = [35, 20])
    stims.loc[b] = s
    
for b in range(2,len(bigMat),4):
    stimRow= bigMat.loc[(bigMat.trIdx == popTrI[b]) & (bigMat.SequenceNum == '3')]
    thisStim = stimRow.Images.iloc[0]
    s = visual.ImageStim(win, image=thisStim, size = [35, 20])
    stims.loc[b] = s
    
for b in range(3,len(bigMat),4):
    stimRow= bigMat.loc[(bigMat.trIdx == popTrI[b]) & (bigMat.SequenceNum == 'dec')]
    thisStim = stimRow.Images.iloc[0]
    s = visual.ImageStim(win, image=thisStim, size = [40, 24])
    stims.loc[b] = s

# # Create a PsychoPy window

bigMat2 = pd.concat([bigMat2, stims], axis = 1)

Instr = visual.TextStim(win, text = "Dans les séquences qui suivent, on vous montrera une série d'images qui constituent une petite histoire. Veuillez appuyez sur n'importe quelle touche pour passer d'une image à l'autre. Vous verrez ensuite un groupe de 3 images. Veuillez sélectionner de ces 3 panneaux, l'image qui représente la suite la plus probable de l'histoire. Pour se déplacer dans l'écran réponse, servez-vous des touches 1 et 4. Pour valider votre choix, appuyer sur la touche 2 ou 3. Appuyez sur une touche pour commencer.", 
font='', pos=(0, 0), depth=0, rgb=None, color= 'black', colorSpace='rgb', opacity=1.0, contrast=1.0, units='', 
ori=0.0, height=None, antialias=True, bold=False, italic=False, alignHoriz='center', alignVert='center',
fontFiles=(), wrapWidth=None, flipHoriz=False, flipVert=False, languageStyle='LTR', name=None, autoLog=None)  


FixationText = visual.TextStim(win=win, text='+', font='', pos=(0, 0),
depth=0, rgb=None, color='black', colorSpace='rgb', opacity=1.0, contrast=1.0, units='', 
ori=0.0, height=None, antialias=True, bold=True, italic=False, alignHoriz='center', alignVert='center',
fontFiles=(), wrapWidth=None, flipHoriz=False, flipVert=False, languageStyle='LTR', name=None, autoLog=None)


bigMat = pd.concat([bigMat, pd.Series(stims)], axis = 1)
bigMat.columns = ['Images', 'Condition', 'SequenceNum', 'stimID1', 'stimID2', 'popTRi','stim']

ul = -9.8,5.75
ur = 9.45,5.75
bm = 0.15, -5.6

im_positions = [(ul),
        (ur),
        (bm)]

posKeys = {
  im_positions[0]: "top left",
  im_positions[1]: "top right",
  im_positions[2]: "bottom"
}

imR1 = visual.Rect(win=win, size = [18.3,10],  lineColor = [-1, -1, -1],lineWidth = 5, pos = im_positions[0])
imS1 = visual.Rect(win=win, size = [18.3,10],  lineColor = [255, 0, 0], lineWidth = 5, pos = im_positions[0], name = 'imS1')
imR2 = visual.Rect(win=win, size = [18.5,10], lineColor = [-1, -1, -1], lineWidth = 5, pos = im_positions[1])
imS2 = visual.Rect(win=win, size = [18.5,10],  lineColor = [255, 0, 0], lineWidth = 5, pos = im_positions[1], name = 'imS2')
imR3 = visual.Rect(win=win, size = [18.5,10],  lineColor = [-1, -1, -1],lineWidth = 5, pos = im_positions[2])
imS3 = visual.Rect(win=win, size = [18.5,10],  lineColor = [255, 0, 0], lineWidth = 5, pos = im_positions[2], name = 'imS3')

sImList = [imS1, imS2, imS3]
sImListn = [imS1.name, imS2.name, imS3.name]

startImInd = random.randint(0, len(im_positions) -1)
s = 'imS' + str(startImInd +1)
findSinList = sImListn.index(s)
# Set up initial position
cursor_x, cursor_y = im_positions[startImInd]

# Create a single red rectangle (cursor)
cursor = visual.Rect(win=win, size = [18.5,10],   lineColor = [255, 0, 0], lineWidth = 5,  pos=(cursor_x, cursor_y), name='cursor')
imRList = [visual.Rect(win=win, size = [18.5,10],  lineColor=[-1, -1, -1], lineWidth = 5,    pos=im_positions[i]) for i in range(3)]
imSList = [visual.Rect(win=win, size = [18.5,10],    lineColor = [255, 0, 0], lineWidth = 5,  pos=im_positions[i], name=f'imS{i + 1}') for i in range(3)]


clock = core.Clock()
Instr.draw()
win.flip(clearBuffer=True)
startExp = clock.getTime()
print('Experiment Started at', startExp)
event.waitKeys()

FixationText.draw()
core.wait(1)
win.flip(clearBuffer=True)

    
trial = 0

for tr in trIdx:
    trial +=1
    # print("Trial Number", trial, " and trIndex ", tr, file=f)
    print("Trial Number", trial, " and trIndex ", tr)
    littleMat = bigMat2[bigMat2.stimID2 == tr]
    littleMat.index = range(len(littleMat.index))
    # stimulusID1.append(littleMat.stimID1.iloc[0])
    # stimulusID2.append(littleMat.stimID2.iloc[0])
    # condition.append(littleMat.Condition.iloc[0])

    stim1 = littleMat.stims.iloc[0]
    stim2 = littleMat.stims.iloc[1]
    stim3 = littleMat.stims.iloc[2]
    stim4 = littleMat.stims.iloc[3]
    
    stim1.draw()
    win.flip(clearBuffer=True)
    event.waitKeys()
    thisT0 = clock.getTime()
   # print("Stimulus  ", stim1.image, " presented at time ", thisT0, file=f)
    print("Stimulus  ", stim1.image, " presented at time ", thisT0)
    # t0.append(thisT0)
    
    stim2.draw()
    win.flip(clearBuffer=True)
    event.waitKeys()
    thisT1 = clock.getTime()
    #print("Stimulus  ", stim2.image, " presented at time ", thisT1, file=f)
    print("Stimulus  ", stim2.image, " presented at time ", thisT1)
    # t1.append(thisT1)
    
    stim3.draw()
    win.flip(clearBuffer=True)
    event.waitKeys()
    thisT2 = clock.getTime()
    #print("Stimulus  ", stim3.image, " presented at time ", thisT2, file=f)
    print("Stimulus  ", stim3.image, " presented at time ", thisT2)
    # t2.append(thisT2)
     
    thisTrialResp = []
    for imR, sIm, pos in zip(imRList, sImList, im_positions):
      imR.pos = pos
      stim4.draw()
      #imR.draw()
  
    # Draw the red rectangle (cursor) at the initial position
    cursor.setPos((cursor_x, cursor_y))
    # stim4.draw()
    cursor.draw()
    win.flip()
     
    keyState = {'4': False, '1': False, '2': False, '3': False}
     
    thisResp =[]
    while '2' not in thisResp and '3' not in thisResp:
      move = event.waitKeys(keyList = ['4', '1', '2', '3'], clearEvents=True, timeStamped=True)        
    # Set up initial variables for continuous key presses
      if move:
        # press = move[len(move) - 1].name
        press = move[0][0]
        thisResp = press
       
  
      #Check for key presses and update keyState
      for key in keyState:
        # keyState[key] = any(press.name == key for press in move)
        keyState[key] = any(press == key for press in move)
        if '4' in press:
            if cursor_x == ul[0] and cursor_y == ul[1]:
                cursor_x = ur[0]
                cursor_y = ur[1]
            elif cursor_x == ur[0] and cursor_y == ur[1]:
                cursor_x = bm[0]
                cursor_y = bm[1]    
            elif cursor_x == bm[0] and cursor_y == bm[1] :
                cursor_x = ul[0]
                cursor_y = ul[1] 
       
        elif '1' in press:
            if cursor_x == bm[0] and cursor_y == bm[1] :
                cursor_x = ur[0]
                cursor_y = ur[1]
            elif cursor_x == ur[0]  and cursor_y == ur[1]:
                cursor_x = ul[0]
                cursor_y = ul[1]
            elif cursor_x == ul[0] and cursor_y == ul[1]:
                cursor_x = bm[0]
                cursor_y = bm[1]
             
        elif '2' in press or '3' in press:
          thisTrialResp= True
          choice = posKeys.get((cursor_x, cursor_y))
          #response.append(choice)
          print(choice)
          thisRT = move[0][1]
          imSelectedPos = cursor_x, cursor_y
          imSelectedInd = im_positions.index((imSelectedPos))
          imSelectedIm = posKeys.get(imSelectedPos)
          thisStimIdFull = littleMat.stimID1.iloc[0]
          selectedResp = answerKey[imSelectedIm][answerKey.trial == thisStimIdFull + '_EXAMPLE']
          selResp = selectedResp.iloc[0]
          print('Subject selected ' + selResp)
          break  # Exit loop after response is recorded


    # Draw all elements
      for imR, sIm, pos in zip(imRList, sImList, im_positions):
          imR.pos = pos
          stim4.draw()
          #imR.draw()
        # Draw the red rectangle (cursor) at the updated position
      cursor.setPos((cursor_x, cursor_y))
      cursor.draw()
      win.flip()  
      if thisTrialResp:
        # Display FixationText and collect confScale input
        FixationText.draw()
        win.flip()
        core.wait(5)

endExp = clock.getTime()
print('Experiment ended at ', endExp)
print('Experiment took ', endExp - startExp)

    
win.close()
core.quit()

