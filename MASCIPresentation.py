#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 18 16:27:43 2024
This script presents the MASC social cognition stimuli
(Dziobek et al., 2006; DOI: 10.1007/s10803-006-0107-0), comprised of a 15 minute
film broken into several clips. In this script, a question is posed to the research
participant on the content of the previous clip. Possible answers are presented
in a multiple choice format. A metacognitive scale is then presented to participans.
This script relies on the psychopy library and is customised for presentation in
an MRI scanner. 
@author: Leyla Loued-Khenissi (sysadmin), CHUV, Lausanne, 2024, lkhenissi@gmail.com

"""

import os
import numpy as np
import glob
import random
import pandas as pd

from psychopy import visual, core, constants, event
from psychopy.hardware import keyboard
from psychopy.visual import form as Form

#Experiment Datapath
outPath = '/Users/sysadmin/Documents/NeuroScape/Output/Behavioral'



subjNum = input("Enter main participant identifier: ") 
subjPath = os.path.join(outPath, 'MASCI_' + subjNum)
os.chdir(subjPath)

subjData = pd.read_csv('MASCI_'+subjNum +'_IntakeData.csv')

#Go to where the movie files live
stimPath =  '/Users/sysadmin/Documents/NeuroScape/MASC_FR/'
os.chdir(stimPath)
clip = glob.glob('*.wmv')
clip.sort()
clips = []
for c in clip:
    clips.append(os.path.join(stimPath, c))
    
pic = glob.glob('*.png')
pics = []
for p in pic:
    pics.append(os.path.join(stimPath, p))
    
# keyboard to listen for keys
kb = keyboard.Keyboard()
#MASC questions
Questions = pd.read_csv(os.path.join(stimPath,'MASC_Questions_newCTRL2.csv'))
jitter = random.uniform(1,2)

Qs = []
Answers = []
Response = []
TOMCat = []
Correct = []
Category = []
Target = []
RespRT = []
Score = []
confidence = []
confidenceRT = []
t0 = []
t1 = []
t2 = []
t3 = []
t4 = []
t5 = []

#response positions; add interval of 0.05 over the box width
respPos = [(-0.75, 0),
                (-0.30, 0),
                (0.15, 0),
                (0.60,0)]
#MASC Answers
qOptions = pd.read_csv(os.path.join(stimPath, 'MASC_Answers_newCTRL2.csv'))
logFile = os.path.join(subjPath, "output" + subjNum + ".txt")
with open(logFile, "a") as f:
    # window to present the video
    win = visual.Window((1000, 800), fullscr=False, allowStencil=True)
    
    instr1 = visual.TextStim(win, text = "Vous allez visionner un film d‘une durée de 15 minutes. Regardez attentivement ce film et essayez de comprendre ce que chaque personnage pense ou ressent. \n\n Appuyez sur une touche pour continuer.", 
    font='', pos=(0, 0), depth=0, rgb=None, color= 'black', colorSpace='rgb', opacity=1.0, contrast=1.0, units='', 
    ori=0.0, height=None, antialias=True, bold=False, italic=False, alignHoriz='center', alignVert='center',
    fontFiles=(), wrapWidth=None, flipHoriz=False, flipVert=False, languageStyle='LTR', name=None, autoLog=None)    
    
    instr2 = visual.TextStim(win, text = "Nous vous proposons maintenant de rencontrer chacun des personnages. \n\n Appuyez sur une touche pour continuer.", 
    font='', pos=(0, 0), depth=0, rgb=None, color= 'black', colorSpace='rgb', opacity=1.0, contrast=1.0, units='', 
    ori=0.0, height=None, antialias=True, bold=False, italic=False, alignHoriz='center', alignVert='center',
    fontFiles=(), wrapWidth=None, flipHoriz=False, flipVert=False, languageStyle='LTR', name=None, autoLog=None)   
    
    pic1 = visual.ImageStim(win, image=pics[0])
    pic2 = visual.ImageStim(win, image=pics[1])
    pic3 = visual.ImageStim(win, image=pics[2])
    pic4 = visual.ImageStim(win, image=pics[3])
    
    instr3 = visual.TextStim(win, text = "Le film met en scène ces quatre personnagesqui se rencontrent un samedi soir. \n\n Appuyez sur une touche pour continuer.", 
    font='', pos=(0, 0), depth=0, rgb=None, color= 'black', colorSpace='rgb', opacity=1.0, contrast=1.0, units='', 
    ori=0.0, height=None, antialias=True, bold=False, italic=False, alignHoriz='center', alignVert='center',
    fontFiles=(), wrapWidth=None, flipHoriz=False, flipVert=False, languageStyle='LTR', name=None, autoLog=None)   
    
    instr4 = visual.TextStim(win, text = "La vidéo va être arrêtée à différents moments. Chaque arrêt sera accompagné d’une question. Vous devrez sélectionner une seule réponse parmi les quatre options présentées.  Il n’y a pas de bonne ou mauvaise réponse. Si vous n’êtes pas certain de la réponse, choisissez l’option qui vous apparaît la plus vraisemblable. \n\n Appuyez sur une touche pour continuer.", 
    font='', pos=(0, 0), depth=0, rgb=None, color= 'black', colorSpace='rgb', opacity=1.0, contrast=1.0, units='', 
    ori=0.0, height=None, antialias=True, bold=False, italic=False, alignHoriz='center', alignVert='center',
    fontFiles=(), wrapWidth=None, flipHoriz=False, flipVert=False, languageStyle='LTR', name=None, autoLog=None)   
    
    instr5 = visual.TextStim(win, text = "Lorsque vous répondrez, essayez d’imaginer ce que le personnage en question pense ou ressent au moment où la vidéo a été arrêtée. \n\n Appuyez sur une touche pour continuer." , 
    font='', pos=(0, 0), depth=0, rgb=None, color= 'black', colorSpace='rgb', opacity=1.0, contrast=1.0, units='', 
    ori=0.0, height=None, antialias=True, bold=False, italic=False, alignHoriz='center', alignVert='center',
    fontFiles=(), wrapWidth=None, flipHoriz=False, flipVert=False, languageStyle='LTR', name=None, autoLog=None)   
    
    instr6 = visual.TextStim(win, text = "La vidéo est sur le point de commencer. Êtes-vous prêt? N’oubliez pas de regarder la vidéo avec beaucoup d’attention. Chaque séquence ne sera présentée qu’une seule fois. \n\n Appuyez sur une touche pour commencer l'experience.", 
    font='', pos=(0, 0), depth=0, rgb=None, color= 'black', colorSpace='rgb', opacity=1.0, contrast=1.0, units='', 
    ori=0.0, height=None, antialias=True, bold=False, italic=False, alignHoriz='center', alignVert='center',
    fontFiles=(), wrapWidth=None, flipHoriz=False, flipVert=False, languageStyle='LTR', name=None, autoLog=None)   
    
    instCtrl = visual.TextStim(win, text = "Appuyez sur une touche pour continuer.", 
        font='', pos=(0, -0.75), depth=0, rgb=None, color= 'black', colorSpace='rgb', opacity=1.0, contrast=1.0, units='', 
        ori=0.0, height=None, antialias=True, bold=False, italic=False, alignHoriz='center', alignVert='center',
        fontFiles=(), wrapWidth=None, flipHoriz=False, flipVert=False, languageStyle='LTR', name=None, autoLog=None) 
    
    
    FixationText = visual.TextStim(win=win, text='+', font='', pos=(0, 0),
    depth=0, rgb=None, color='black', colorSpace='rgb', opacity=1.0, contrast=1.0, units='', 
    ori=0.0, height=None, antialias=True, bold=True, italic=False, alignHoriz='center', alignVert='center',
    fontFiles=(), wrapWidth=None, flipHoriz=False, flipVert=False, languageStyle='LTR', name=None, autoLog=None)
    
    confQuestion= visual.TextStim(win, text = 'A quel point êtes vous sur de votre réponse?', 
    font='', pos=(0, 0), depth=0, rgb=None, color= 'black', colorSpace='rgb', opacity=1.0, contrast=1.0, units='', 
    ori=0.0, height=None, antialias=True, bold=False, italic=False, alignHoriz='center', alignVert='center',
    fontFiles=(), wrapWidth=None, flipHoriz=False, flipVert=False, languageStyle='LTR', name=None, autoLog=None) 
       
    clock = core.Clock()
    instr1.draw()
    win.flip()
    event.waitKeys()
    instr2.draw()
    win.flip()
    event.waitKeys()
    
    instCtrl.draw()
    pic1.draw()
    win.flip()
    event.waitKeys()
    instCtrl.draw()
    pic2.draw()
    win.flip()
    event.waitKeys()
    instCtrl.draw()
    pic3.draw()
    win.flip()
    event.waitKeys()
    instCtrl.draw()
    pic4.draw()
    win.flip()
    event.waitKeys()
    
    instr3.draw()
    win.flip()
    event.waitKeys()
    instr4.draw()
    win.flip()
    event.waitKeys()
    instr5.draw()
    win.flip()
    event.waitKeys()
    instr6.draw()
    win.flip()
    event.waitKeys()
    
    
    
    scannerWait = visual.TextStim(win, text = 'Please wait for scanner...', 
            font='', pos=(0, 0), depth=0, rgb=None, color= 'black', colorSpace='rgb', opacity=1.0, contrast=1.0, units='', 
            ori=0.0, height=None, antialias=True, bold=False, italic=False, alignHoriz='center', alignVert='center',
            fontFiles=(), wrapWidth=None, flipHoriz=False, flipVert=False, languageStyle='LTR', name=None, autoLog=None) 
    
    scannerWait.draw()
    win.flip()
    trigger = event.waitKeys(keyList = ['5'], clearEvents=True, timeStamped=True) 
    
    #block key 5 to keep console clear
    #keyboard.block_key("5")
    
    trigTime = trigger[0][1]
    startExp1 = clock.getTime()
    print('Trigger at ' + str(startExp1), file=f)
    print('Trigger at ' + str(startExp1)) 

    for m in range(len(clips)):
        print('Trial number ' + str(m), file=f)
        print('Trial number ' + str(m))
    #Set up question
        thisQ = Questions.Question.iloc[m]
    #Set up related answers
        answers = qOptions.loc[qOptions['QuestionNum'] == m +1]
        imShow1 = visual.TextStim(win, text=answers.Answers.iloc[0], pos = respPos[0], height = 0.05, wrapWidth = 0.3)
        imR1 = visual.Rect(win=win, size = [0.4, 0.4], lineColor = [-1, -1, -1], pos = respPos[0])
        imS1 = visual.Rect(win=win, size = [0.4, 0.4], lineColor = [255, 0, 0], pos = respPos[0], name = 'imS1')
        imShow2 = visual.TextStim(win, text=answers.Answers.iloc[1], pos = respPos[1], height = 0.05, wrapWidth = 0.3)
        imR2 = visual.Rect(win=win, size = [0.4, 0.4], lineColor = [-1, -1, -1], pos = respPos[1])
        imS2 = visual.Rect(win=win, size = [0.4, 0.4], lineColor = [255, 0, 0], pos = respPos[1], name = 'imS2')
        imShow3 = visual.TextStim(win, text=answers.Answers.iloc[2], pos = respPos[2], height = 0.05, wrapWidth = 0.3)
        imR3 = visual.Rect(win=win, size = [0.4, 0.4], lineColor = [-1, -1, -1], pos = respPos[2])
        imS3 = visual.Rect(win=win, size = [0.4, 0.4], lineColor = [255, 0, 0], pos = respPos[2], name = 'imS3')
        imShow4 = visual.TextStim(win, text=answers.Answers.iloc[3], pos = respPos[3], height = 0.05, wrapWidth = 0.3)
        imR4 = visual.Rect(win=win, size = [0.4, 0.4], lineColor = [-1, -1, -1], pos = respPos[3])
        imS4 = visual.Rect(win=win, size = [0.4, 0.4], lineColor = [255, 0, 0], pos = respPos[3], name = 'imS4')
        
        sImList = [imS1, imS2, imS3, imS4]
        sImListn = [imS1.name, imS2.name, imS3.name, imS4.name]
                
                
        startImInd = random.randint(0, len(respPos) -1)
        s = 'imS' + str(startImInd +1)
        findSinList = sImListn.index(s)
        # Set up initial position
        cursor_x, cursor_y = respPos[startImInd]
        
        # Create a single red rectangle (cursor)
        cursor = visual.Rect(win=win, size = [0.4, 0.4],lineColor=[255, 0, 0], pos=(cursor_x, cursor_y), name='cursor')
        
        ansShowList = [visual.TextStim(win, text=answers.Answers.iloc[i], pos=respPos[i],  height = 0.05, wrapWidth = 0.3) for i in range(4)]
        imRList = [visual.Rect(win=win, size = [0.4, 0.4], lineColor=[-1, -1, -1], pos=respPos[i]) for i in range(4)]
        imSList = [visual.Rect(win=win, size = [0.4, 0.4], lineColor=[255, 0, 0], pos=respPos[i], name=f'imS{i + 1}') for i in range(4)]
    
        confScale = visual.RatingScale(win, low=1, high=10, markerStart= random.randint(1,10), choices =None,scale= None, acceptPreText =None, 
        showValue = None, showAccept = None, labels=None, 
        leftKeys='1', rightKeys = '4', acceptKeys=['2','3'], textColor = 'black')
        confScale.reset()
        # create a new movie stimulus instance
        thisMov = clips[m]
        # thisMov = '/Users/sysadmin/Documents/NeuroScape/MASC_FR/20.wmv'
        mov = visual.MovieStim(
            win,
            thisMov,    # path to video file
            size=(640, 480),
            flipVert=False,
            flipHoriz=False,
            loop=False,
            noAudio=False,
            volume=0.1,
            autoStart=False)
        
        # print some information about the movie
        print('orig movie size={}'.format(mov.frameSize))
        print('orig movie duration={}'.format(mov.duration))
        
        # instructions
        instrText = "`Appuyez pour commencer le film"
        instr = visual.TextStim(win, instrText, pos=(0.0, -0.75))
        
        # main loop, exit when the status is finished
        while not mov.isFinished:
            # draw the movie
            mov.draw()
            # draw the instruction text
            if m == 0:
                instr.draw()
            # flip buffers so they appear on the window
            win.flip()
        
            # process keyboard input
            if kb.getKeys('q'):   # quit
                break
            elif kb.getKeys(['1', '2', '3', '4']):  # play/start
                mov.play()
                thisT0 = clock.getTime()
                t0.append(thisT0)
                print('Movie started at ' + str(thisT0), file = f)
                print('Movie started at ' + str(thisT0))
            # elif kb.getKeys('p'):  # pause
            #     mov.pause()
            # elif kb.getKeys('s'):  # stop the movie
            #     mov.stop()
        
        # stop the movie, this frees resources too
        mov.unload()  # unloads when `mov.status == constants.FINISHED`
        thisT1 = clock.getTime()
        t1.append(thisT1)
        print('Movie ended at ' + str(thisT1), file = f)
        print('Movie ended at ' + str(thisT1))
        quest = visual.TextStim(win, text= thisQ, font='', pos=(0.0, 0.5), depth=0, rgb=None, 
                    color=(1.0, 1.0, 1.0), colorSpace='rgb', opacity=1.0, contrast=1.0, units='', 
                    ori=0.0, height=None, antialias=True, bold=False, italic=False, alignHoriz=None, 
                    alignVert=None, alignText='center', anchorHoriz='center', anchorVert='center', 
                    fontFiles=(), wrapWidth=None, flipHoriz=False, flipVert=False, languageStyle='LTR', 
                    draggable=False, name=None, autoLog=None, autoDraw=False)

    
        for imShow, imR, sIm, pos in zip(ansShowList, imRList, sImList, respPos):
                imShow.pos = pos
                imR.pos = pos
                imShow.draw()
                imR.draw()
            
        # Draw the red rectangle (cursor) at the initial position
        cursor.setPos((cursor_x, cursor_y))
        cursor.draw()
        quest.draw()
        win.flip()
        thisT2 = clock.getTime()
        t2.append(thisT2)
    
         
        keyState = {'4': False, '1': False, '2': False, '3': False}
         
        thisResp =[]
        while '2' not in thisResp and '3' not in thisResp:
          move = event.waitKeys(keyList = ['4', '1', '2', '3'], clearEvents=True, timeStamped=True)  
                
        # Set up initial variables for continuous key presses
          if move:
            # press = move[len(move) - 1].name
            press = move[0][0]
            thisResp = press
            thisRT = move[0][1]
        
            #Check for key presses and update keyState
            for key in keyState:
              # keyState[key] = any(press.name == key for press in move)
              keyState[key] = any(press == key for press in move)
            if '4' in press:
                  if cursor_x == -0.75 and cursor_y == 0:
                    cursor_x = -0.3
                    cursor_y = 0
                  elif cursor_x == -0.3 and cursor_y == 0:
                      cursor_x = 0.15
                      cursor_y = 0  
                  elif cursor_x == 0.15 and cursor_y == 0:
                      cursor_x = 0.6
                      cursor_y = 0
                  elif cursor_x == 0.6 and cursor_y == 0:
                      cursor_x = 0.6
                      cursor_y = 0 
                  event.clearEvents()
                   
                 
            elif '1' in press:
                  if cursor_x == 0.6 and cursor_y == 0:
                    cursor_x = 0.15
                    cursor_y = 0
                  elif cursor_x == 0.15 and cursor_y == 0:
                    cursor_x = -0.3
                    cursor_y = 0
                  elif cursor_x == -0.3 and cursor_y == 0:
                    cursor_x = -0.75
                    cursor_y = 0
                  elif cursor_x == -0.75 and cursor_y == 0:
                    cursor_x = -0.75
                    cursor_y = 0
                  event.clearEvents()
                  
                       
            elif '2' in thisResp or '3' in thisResp:
                    cursor_x = cursor_x
                    cursor_y = cursor_y
                    thisTrialResp= True
                    thisT3 = clock.getTime()
                    t3.append(thisT3)
                    imSelectedPos = cursor_x, cursor_y
                    imSelectedInd = respPos.index((imSelectedPos))
                    imSelectedIm = answers.Answers.iloc[imSelectedInd]
                    Response.append(imSelectedIm)
                    if answers.Score.iloc[imSelectedInd] == 0:
                        Correct.append(1)
                        print('Subject chose correctly at ' + str(thisT3) , file = f)
                        print('Subject chose correctly at ' + str(thisT3))
                        
                    else:
                        Correct.append(0)
                        print('Subject chose ' + str(answers.Score.iloc[imSelectedInd]) +' incorrectly at ' + str(thisT3), file = f)
                        print('Subject chose ' + str(answers.Score.iloc[imSelectedInd]) +' incorrectly at ' + str(thisT3))
                    Score.append(answers.Score.iloc[imSelectedInd])
                    Category.append(answers.Category.iloc[imSelectedInd])
                    Target.append(answers.Target.iloc[imSelectedInd])
                    TOMCat.append(answers.QuestionType.iloc[imSelectedInd])
                    event.clearEvents()
            
            
            # Draw all elements
            for imShow, imR, sIm, pos in zip(ansShowList, imRList, sImList, respPos):
              imShow.pos = pos
              imR.pos = pos
              imShow.draw()
              imR.draw()
              quest.draw()
               
            # Draw the red rectangle (cursor) at the updated position
            cursor.setPos((cursor_x, cursor_y))
            cursor.draw()
            win.flip()  
            if '2' in thisResp or '3' in thisResp:
            # Display FixationText and collect confScale input
                FixationText.draw()
                win.flip()
                core.wait(2)
                thisT4 = clock.getTime()
                t4.append(thisT4)  
                while confScale.noResponse:
                    confQuestion.draw()
                    confScale.draw()
                    win.flip()    
                thisT5 = clock.getTime()
                t5.append(thisT5)    
                rating = confScale.getRating()
                print('Subject reprorted a confidence of ' + str(rating) + ' at ' + str(thisT5), file = f)
                print('Subject reprorted a confidence of ' + str(rating) + ' at ' + str(thisT5))
                decision_time = confScale.getRT()
                confidence.append(rating)
                confidenceRT.append(decision_time)
                FixationText.draw()
                win.flip()
                # core.wait(2)
                core.wait(3.5 + jitter)
                event.clearEvents()
        allResults = pd.concat([pd.Series(Response), pd.Series(Correct), pd.Series(Score), pd.Series(Target), pd.Series(TOMCat), pd.Series(confidence), pd.Series(confidenceRT), pd.Series(t0), pd.Series(t1), pd.Series(t2), pd.Series(t3), pd.Series(t4), pd.Series(t5)], axis=1)
    
        allResults.columns =['Response', 'Correct', 'Score', 'Target', 'TOMCat', 'confidence', 'confidenceRT', 't0', 't1', 't2', 't3', 't4', 't5']
        allResults.to_csv(os.path.join(subjPath, 'MASCI_' + subjNum + '_expData.csv'))
            
    endExp = clock.getTime()    
    subjData.endExp = endExp
            

    
thankYou = visual.TextStim(win, text = "Vous avez terminé l'experience. Merci de votre participation.",
    font='', pos=(0, 0), depth=0, rgb=None, color= 'black', colorSpace='rgb', opacity=1.0, contrast=1.0, units='', 
    ori=0.0, height=None, antialias=True, bold=False, italic=False, alignHoriz='center', alignVert='center',
    fontFiles=(), wrapWidth=None, flipHoriz=False, flipVert=False, languageStyle='LTR', name=None, autoLog=None)  

        
thankYou.draw()
win.flip()
core.wait(2)
win.close()
core.quit()

