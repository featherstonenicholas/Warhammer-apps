import tkinter as tk
from tkinter import ttk
from tkinter import StringVar
import numpy as np
from statistics import mode
from itertools import combinations
from random import randrange
import json
from tkinter import messagebox
root = tk.Tk()
root.title('Tkinter Window Demo')
root.geometry('1000x700+50+50')
root.configure(bg='#2D033B')
root.columnconfigure(0,weight=1)
root.columnconfigure(1,weight=1)


#~~~~~~~~~~~~~ Styling
s = ttk.Style()
s.configure('matrixinput.TFrame', background='#810CA8')
s.configure('redred.TFrame', background='#B70404')
s.configure('red.TFrame', background='#DF7861')
s.configure('yellow.TFrame', background='#FFE569')
s.configure('green.TFrame', background='#82CD47')
s.configure('greengreen.TFrame', background='#379237')
s.configure('white.TFrame',background='#FFFFFF')
s.configure('results.TFrame',background='#C147E9')
s.configure('output.TFrame',background='#FF6000')
s.configure('teamnames.TLabel',font=("Helvetica", 12,'bold'),background='#810CA8',anchor='center',foreground='#FF6000')
s.configure('matchresults.TLabel',font=("Helvetica", 12),background='#C147E9',anchor='center',foreground='#2D033B')
s.configure('outputtext.TLabel',font=("Helvetica", 12),background='#FF6000',anchor='center',foreground='#2D033B')
s.configure('teamB.TLabel',font=("Helvetica", 12,'bold'),background='#C147E9',anchor='center',foreground='#FF6000')
s.configure('teamA.TLabel',font=("Helvetica", 12,'bold'),background='#810CA8',anchor='center',foreground='#03C988')
s.configure('buttons.TButton',font=("Helvetica", 12),background='#C147E9',anchor='center',foreground='#2D033B')
#~~~~~~~~~~~~~ Create The title of the app

label = ttk.Label(root, text="SLL Pairings",font=("Helvetica", 20),background='#2D033B',anchor='center',foreground='#03C988')
label.grid(row=0, columnspan=2,sticky='WE',pady=20)

#~~~~~~~~~~~~~ Create the Matrix Frame

matrixframe = ttk.Frame(root, height=500, width=500, style='matrixinput.TFrame')
#spread rows and columns evenly
for i in range(5):
    matrixframe.rowconfigure(i+1,weight=1)
    matrixframe.columnconfigure(i+1,weight=1)
    
matrixframe.grid(row=1, column=0,sticky='NSEW')
#~~~~~~~~~~~~~ Create individual frames so to be able to change colours later
inputframes=[]
for i in range(5):
    inputframes.append([])
    for j in range(5):
        inputframes[i].append(ttk.Frame(matrixframe,  style='matrixinput.TFrame'))
        inputframes[i][j].grid(row=i+1,column=j+1,sticky='EW')



#~~~~~~~~~~~~~ Create the results Frame

resultsframe=ttk.Frame(root,height=500, width=200,style='results.TFrame')
resultsframe.grid(row=1,column=1,sticky='NSWE')
#spread rows evenly
for i in range(5):
    resultsframe.rowconfigure(i,weight=1)

#~~~~~~~~~~~~~ Create the output and working frame


outputframe=ttk.Frame(root,height=500, width=200,style='output.TFrame')
outputframe.grid(row=2,column=0,columnspan=2,sticky='NSWE')

#~~~~~~~~~~~~~ load previous data
with open ('save.json','r') as f:
  save=json.loads(f.read())

teamA=save[0]
teamB=save[1]
global matrix
matrix=save[2]
print(teamA)
#~~~~~~~~~~~~~ Create the pairings matrix

#create the matrix of inputs
text_var = []
entries = []
for i in range(5):
    text_var.append([])
    entries.append([])
    for j in range(5):
        # append your StringVar and Entry
        text_var[i].append(StringVar())
        #give default fill
        text_var[i][j].set(matrix[i][j])
        entries[i].append(ttk.Entry(inputframes[i][j], textvariable=text_var[i][j],width=3))
        entries[i][j].grid(row=i+1,column=j+1,padx=20,pady=20)
#create the team A names

teamAlabels=[]

for i in range(len(teamA)):
    teamAlabels.append(ttk.Label(matrixframe,text=teamA[i],style='teamA.TLabel'))
    teamAlabels[i].grid(row=1+i,column=0)
      
#create the team B names
oppo_var = []
oppo_entries = []
for i in range(5):
    # append your StringVar and Entry
    oppo_var.append(StringVar())
    #give default fill
    oppo_var[i].set(teamB[i])
    oppo_entries.append(ttk.Entry(matrixframe, textvariable=oppo_var[i],width=3,font=("Helvetica", 12,'bold'),foreground='#FF6000'))
    oppo_entries[i].grid(row=0,column=i+1,padx=20,pady=20)

# create the tie breaker button, control the tiebreaker INSIDE arrayminmax
global tiebreaker
tiebreaker=0
tb = ttk.Checkbutton(outputframe,text="Set tiebreaker (checked is Mode, blank is Max)",variable=tiebreaker)
#tb.grid(row=0,column=3,padx=10)
# create print button
global printcheck
printcheck=True
pt = ttk.Checkbutton(outputframe,text="Print?",variable=printcheck,onvalue=True,offvalue=False)
#pt.grid(row=0,column=3,padx=10)
#~~~~~~~~~~~~~ Create the results output

matches=[]
vs=[]
matchA=[]
matchB=[]
for i in range(5):
    matches.append(ttk.Label(resultsframe,text=("Match "+str(i+1)+" : "),style='matchresults.TLabel'))
    matches[i].grid(row=i+1,column=0,pady=5,padx=5,sticky='W')
    matchA.append(ttk.Label(resultsframe,text=("??? "),style='matchresults.TLabel'))
    matchA[i].grid(row=i+1,column=1,pady=5)
    vs.append(ttk.Label(resultsframe,text=("VS"),style='matchresults.TLabel'))
    vs[i].grid(row=i+1,column=2,pady=5)
    matchB.append(ttk.Label(resultsframe,text=(" ???"),style='matchresults.TLabel'))
    matchB[i].grid(row=i+1,column=3,pady=5)

#~~~~~~~~~~~~~ Generate TeamB and Matrix
#global matrix 
#matrix= []
#for i in range(5):
    #matrix.append([])
    #for j in range(5):
        #matrix[i].append([])

def get_mat():
    for i in range(5):
        teamB[i]=oppo_var[i].get()
        for j in range(5):
            matrix[i][j]=(int(text_var[i][j].get()))
    save=[teamA,teamB,matrix]
    json_save=json.dumps(save)
    with open('save.json','w') as f:
      f.write(json_save)
    
def run_analysis():
    colourise()
            
    for i in range(5):
        for j in range(5):
            entries[i][j].destroy()
    colourbutton.grid_forget()
    pt.grid_forget()
    tb.destroy()
    runthematch(teamA,teamB,matrix,False)        
    #mainbutton.configure(text="Analyse matchup",command=lambda:runthematch(teamA,teamB,matrix,False))
mainbutton=ttk.Button(outputframe,text="Analyse match",command=run_analysis,style='buttons.TButton')
mainbutton.grid(row=0,column=0,padx=20,pady=20)

#~~~~~~~~~~~~~ create the colourise the matrix options
def colourise():
    get_mat()
    for i in range(5):
        for j in range(5):
            if matrix[i][j] == 0:
                inputframes[i][j].configure(style='yellow.TFrame')
            elif matrix[i][j] == 1:
                inputframes[i][j].configure(style='green.TFrame')
            elif matrix[i][j] > 1:
                inputframes[i][j].configure(style='greengreen.TFrame')
            elif matrix[i][j] == -1:
                inputframes[i][j].configure(style='red.TFrame')
            elif matrix[i][j] < -1:
                inputframes[i][j].configure(style='redred.TFrame')
colourbutton=ttk.Button(outputframe,text="Colourise",command=colourise,style='buttons.TButton')
colourbutton.grid(row=0,column=1)
#~~~~~~~~~~~~~ define the functions needed for algorithm
#arrayinmax to optimise an array choice
def arrayminmax(array,tie):
#if tie = 0, looks for max in row, if tie =1 then looks for modal result
  tie=int(tiebreaker)
  x=0
  y=0
  Max=float('-inf')
  Min=float('inf')
  for i in range(len(array)):
    score=min(array[i])
    if score>Max:
      Max=score
      x=i
    elif score==Max:
      if sum(array[x])< sum(array[i]):
        x=i
      elif sum(array[x])== sum(array[i]):
        if tie ==0:
          if max(array[i]) > max(array[x]):
            Max=score
        elif tie == 1:
          if mode(array[i]) > mode(array[x]):
            Max=score
    
  array=np.transpose(array)          
  for j in range(len(array[0])) :
    score=max(array[j])
    if score<Min:
      Min=score
      y=j
    elif score==Min:
      if sum(array[y])> sum(array[j]):
        y=j
  array=np.transpose(array)
  scorex=Max
  scorey=Min
  return x , y , scorex , scorey
#picks the correct attacker from a pair in 3 man situation and the score
def threepickmatch(defA,defB,attA,attB,refA,refB,matrix,Print):
  scores=[]
  for i in range(len(attB)):
    scores.append([])
    for j in range(len(attA)):
      x1=refA.index(defA)
      y1=refB.index(attB[i])
      y2=refB.index(defB)
      x2=refA.index(attA[j])
      y3=refB.index(attB[abs(i-1)])
      x3=refA.index(attA[abs(j-1)])
      score=matrix[x1][y1]+matrix[x2][y2]+matrix[x3][y3]
      scores[i].append(score)
  if Print == True:
    print(scores)
  return arrayminmax(scores,0)
# returns the best defender pick for a given 3man team matchup
def threepicksolve(teamA,teamB,refA,refB,matrix,Print):
  scores=[]
  for i in range(len(teamA)):
    scores.append([])
    for j in range(len(teamB)):
      attA=teamA.copy()
      attB=teamB.copy()
      attA.pop(i)
      attB.pop(j)
      output=threepickmatch(teamA[i],teamB[j],attA,attB,refA,refB,matrix,False)
      scores[i].append(output[2])
  if Print == True:
    top= tk.Toplevel(root)
    top.geometry("300x300")
    top.configure(bg='#FF6000')
    top.title("Defender Matrix")
    #Create a label in Toplevel window
    for i in range(len(teamA)):
      ttk.Label(top, text=teamA[i],style='outputtext.TLabel' ).grid(row=i+1,column=0,padx=10,pady=10)
      ttk.Label(top, text=teamB[i],style='outputtext.TLabel' ).grid(row=0,column=i+1,padx=10,pady=10)
      for j in range(len(teamB)):
        ttk.Label(top, text=scores[i][j],style='outputtext.TLabel' ).grid(row=i+1,column=j+1,sticky='NSEW')
  
  return arrayminmax(scores,0)
# picks the correct attacker from a pair in 5man situation
def fivepickmatch(defA,defB,attA,attB,refA,refB,matrix,Print):
  scores=[]
  for i in range(len(attB)):
    scores.append([])
    for j in range(len(attA)):
      x1=refA.index(defA)
      y1=refB.index(attB[i])
      y2=refB.index(defB)
      x2=refA.index(attA[j])
      teamA=refA.copy()
      teamB=refB.copy()
      teamA.pop(teamA.index(defA))
      teamA.pop(teamA.index(attA[j]))
      teamB.pop(teamB.index(defB))
      teamB.pop(teamB.index(attB[i]))
      s=threepicksolve(teamA,teamB,refA,refB,matrix,False)
      score=matrix[x1][y1]+matrix[x2][y2]+s[2]
      scores[i].append(score)
  if Print == True:
    print(scores)
  return arrayminmax(scores,0)
#finds all the possible attacker pairs when sending a defender in 5man
def possattack(defA,teamA):
  teamAcopy=teamA.copy()
  defA=teamAcopy.pop(teamA.index(defA))
  possattA=list(combinations(teamAcopy,2))
  return possattA
#finds the best attacker pair when presented a defender
def fivepickbestattacker(defA,defB,teamA,teamB,matrix,Print):
  
  possattA=possattack(defA,teamA)
  possattB=possattack(defB,teamB)
  #here we have essentially set up diag 1
  scores=[]
  #print(possattA,possattB)
  for k in range(len(possattA)):
    scores.append([])
    for l in range(len(possattB)):
      attA=possattA[k]
      attB=possattB[l]
      s=fivepickmatch(defA,defB,attA,attB,teamA,teamB,matrix,False)
      score=s[2]
      scores[k].append(score)
  output=arrayminmax(scores,0)
  x=output[0]
  y=output[1]
  attAchoice=possattA[x]
  attBchoice=possattB[y]
  if Print == True:
    top= tk.Toplevel(root)
    top.geometry("300x300")
    top.configure(bg='#FF6000')
    top.title("Attackers 1 Matrix")
    #Create a label in Toplevel window
    for i in range(len(possattA)):
      ttk.Label(top, text=possattA[i],style='outputtext.TLabel' ).grid(row=i+1,column=0,padx=10,pady=10)
      ttk.Label(top, text=possattB[i],style='outputtext.TLabel' ).grid(row=0,column=i+1,padx=10,pady=10)
      for j in range(len(possattB)):
        ttk.Label(top, text=scores[i][j],style='outputtext.TLabel' ).grid(row=i+1,column=j+1,sticky='NSEW')
  return attAchoice, attBchoice, output[2]
#finds the best first defender to send in 5man
def fivepicksolve(teamA,teamB,matrix,Print):
  bigscores=[]
  
  for i in range(len(teamA)):
    bigscores.append([])
    
    for j in range(len(teamB)):
      output=fivepickbestattacker(teamA[i],teamB[j],teamA,teamB,matrix,False)
      bigscores[i].append(output[2])
      
  if Print == True:
    #print(bigscores)
    top= tk.Toplevel(root)
    top.geometry("300x300")
    top.configure(bg='#FF6000')
    top.title("Defender 1 Matrix")
    #Create a label in Toplevel window
    for i in range(len(teamA)):
      ttk.Label(top, text=teamA[i],style='outputtext.TLabel' ).grid(row=i+1,column=0,padx=10,pady=10)
      ttk.Label(top, text=teamB[i],style='outputtext.TLabel' ).grid(row=0,column=i+1,padx=10,pady=10)
      for j in range(len(teamB)):
        ttk.Label(top, text=bigscores[i][j],style='outputtext.TLabel' ).grid(row=i+1,column=j+1,sticky='NSEW')
  
     
  output=arrayminmax(bigscores,0)
  
  return output
def framewhiteout(x,y,frame):
    for i in range(5):
        for j in range(5):
            if (i == x and j != y) or (i != x and j == y):
                frame[i][j].configure(style='white.TFrame')
#~~~~~~~~~~~~~~~ lets get some outputs
# Step 0 Analyse the matchups overall and setup entry for defender1

def runthematch(teamA,teamB,matrix,Print):
    #Analyse
    output=fivepicksolve(teamA,teamB,matrix,printcheck)
    #Initialise main output area and suggest defenders
    global suggA
    suggA=ttk.Label(outputframe,style='outputtext.TLabel',text=("Suggested Stag defender is "+str(teamA[output[0]])))
    suggA.grid(row=0,column=1,pady=20,padx=20)
    global suggB
    suggB=ttk.Label(outputframe,style='outputtext.TLabel',text=("Suggested Oppo defender is "+str(teamB[output[1]])))
    suggB.grid(row=0,column=2,pady=20,padx=20)
    
    
    #print score in results frame
    global currentminscore
    currentminscore=ttk.Label(resultsframe,style='matchresults.TLabel',text=("Minimum score is "+str(output[2])))
    currentminscore.grid(row=0,column=0,columnspan=3,pady=20,padx=20, sticky='NSWE')
    #change button to validate defenders
    mainbutton.configure(text="Pick Defenders",command=pickdefenders1)
     # create defender input areas
    global label1
    label1=ttk.Label(outputframe,style='outputtext.TLabel',text=("Stag defender 1 is "))
    label1.grid(row=1,column=0,pady=20,padx=20, sticky='E')
    global label2
    label2=ttk.Label(outputframe,style='outputtext.TLabel',text=("Oppo defender 1 is "))
    label2.grid(row=1,column=2,pady=20,padx=20,sticky='E')
    global string1
    string1=StringVar()
    global string2
    string2=StringVar()
    global input1
    input1=ttk.Combobox(outputframe,textvariable=string1, width=4, values=teamA)
    input1.grid(row=1,column=1,sticky='W',padx=5)
    global input2
    input2=ttk.Combobox(outputframe, textvariable=string2, width=4, values=teamB)
    input2.grid(row=1,column=3,sticky='W',padx=5)
 
# Define defenders and suggest attackers
def pickdefenders1():
    global defA 
    global defB
    defA=string1.get()
    defB=string2.get()
    
    matchA[0].config(text=defA,style='teamA.TLabel',background='#C147E9')
    matchB[1].config(text=defB,style='teamB.TLabel')
    output=fivepickbestattacker(defA,defB,teamA,teamB,matrix,True)
    #print the picked defenders
    suggA.config(text=("Suggested Stag attackers are "+ str(output[0])))
    suggB.config(text=("Suggested Oppo attackers are "+ str(output[1])))
    currentminscore.config(text=("Minimum score is "+str(output[2])))
    label1.config(text=("Stag attackers 1 are "))
    label2.config(text=("Oppo attackers 1 are "))
    # now set up for choosing attackers to send out
    global possattA
    possattA=possattack(defA,teamA)
    global possattB
    possattB=possattack(defB,teamB)
    input1.delete(0,'end')
    input2.delete(0,'end')
    input1.config(values=possattA,width=8)
    input2.config(values=possattB,width=8)
    mainbutton.configure(text="Choose attacker pair",command=pickattackers1)

def pickattackers1():
    global attA
    attA=string1.get()
    attA = tuple(map(str, attA.split(' ')))
    global attB
    attB=string2.get()
    attB = tuple(map(str, attB.split(' ')))
    output=fivepickmatch(defA,defB,attA,attB,teamA,teamB,matrix,False)
            
    suggA.config(text=("Suggested attacker pick for Stag is "+ str(attB[output[0]])))
    suggB.config(text=("Suggested attacker pick for Oppo is "+ str(attA[output[1]])))
    currentminscore.config(text=("Minimum score is "+str(output[2])))
    label1.config(text=(str(defA)+" will face "))
    label2.config(text=(str(defB)+" will face "))
    input1.delete(0,'end')
    input2.delete(0,'end')
    input1.config(values=attB,width=8)
    input2.config(values=attA,width=8)
    mainbutton.configure(text="Choose first matches",command=choosefirstmatch)
#lock in first 2 matches and set up to choose 2nd defender

def choosefirstmatch():
    global att1A
    global att1B
    att1A=string2.get()
    att1B=string1.get()
    x=teamA.index(defA)
    y=teamB.index(att1B)
    framewhiteout(x,y,inputframes)
    x=teamA.index(att1A)
    y=teamB.index(defB)
    framewhiteout(x,y,inputframes)
    matchB[0].configure(text=att1B,style='teamB.TLabel')
    matchA[1].configure(text=att1A,style='teamA.TLabel',background='#C147E9')
    global teamAleft
    global teamBleft
    teamAleft=teamA.copy()
    teamBleft=teamB.copy()
    teamAleft.pop(teamAleft.index(defA))
    teamAleft.pop(teamAleft.index(att1A))
    teamBleft.pop(teamBleft.index(defB))
    teamBleft.pop(teamBleft.index(att1B))
    output=threepicksolve(teamAleft,teamBleft,teamA,teamB,matrix,True)
    suggA.config(text=("Suggested defender pick for Stag is "+ str(teamAleft[output[0]])))
    suggB.config(text=("Suggested defender pick for Oppo is "+ str(teamBleft[output[1]])))
    global score1 
    global score2
    score1=matrix[teamA.index(defA)][teamB.index(att1B)]
    score2=matrix[teamA.index(att1A)][teamB.index(defB)]    
    midwayscore=output[2]+score1+score2
    currentminscore.config(text=("Minimum score is "+str(midwayscore)))
    input1.delete(0,'end')
    input2.delete(0,'end')
    input1.config(values=teamAleft,width=8)
    input2.config(values=teamBleft,width=8)
    label1.config(text=(" Stag defender 2 is:  "))
    label2.config(text=" Oppo defender 2 is  ")
    mainbutton.configure(text="Pick 2nd defenders",command=defender2)
    
#lock in 2nd defender and set up last choice

def defender2():
    
    global def2A
    global def2B
    def2A=string1.get()
    def2B=string2.get()
    teamAleft.pop(teamAleft.index(def2A))
    teamBleft.pop(teamBleft.index(def2B))
    matchA[2].config(text=def2A,style='teamA.TLabel',background='#C147E9')
    matchB[3].config(text=def2B,style='teamB.TLabel')
    
    output=threepickmatch(def2A,def2B,teamAleft,teamBleft,teamA,teamB,matrix,False)
    suggA.config(text=("Suggested attacker pick for Stag is "+ str(teamBleft[output[1]])))
    suggB.config(text=("Suggested defender pick for Oppo is "+ str(teamAleft[output[0]])))
    lastscoreprojection=score1+score2+output[2]
    label1.config(text=(str(def2A)+" will face "))
    label2.config(text=(str(def2B)+" will face "))
    currentminscore.config(text=("Final min score is "+str(lastscoreprojection)))
    
    input1.delete(0,'end')
    input2.delete(0,'end')
    input1.config(values=teamBleft,width=8)
    input2.config(values=teamAleft,width=8)
    mainbutton.configure(text="Choose final matches",command=finalselection)

# final choice
def finalselection():
    att2B=string1.get()
    att2A=string2.get()
    j=teamBleft.index(att2B)
    i=teamAleft.index(att2A)
    matchA[3].config(text=att2A,style='teamA.TLabel',background='#C147E9')
    matchB[2].config(text=att2B,style='teamB.TLabel')
    finalA=teamAleft[abs(i-1)]
    finalB=teamBleft[abs(j-1)]
    matchA[4].config(text=finalA,style='teamA.TLabel',background='#C147E9')
    matchB[4].config(text=finalB,style='teamB.TLabel')
    x=teamA.index(def2A)
    y=teamB.index(att2B)
    framewhiteout(x,y,inputframes)
    x=teamA.index(att2A)
    y=teamB.index(def2B)
    framewhiteout(x,y,inputframes)
    x=teamA.index(finalA)
    y=teamB.index(finalB)
    framewhiteout(x,y,inputframes)
    match1=(defA,att1B)
    match2=(att1A,defB)
    match3=(def2A,att2B)
    match4=(att2A,def2B)
    match5=(finalA,finalB)
    matches=(match1,match2,match3,match4,match5)
    finalscore=0
    scores=[]
    for i in range(len(matches)):
        x=teamA.index(matches[i][0])
        y=teamB.index(matches[i][1])
        score=matrix[x][y]
        scores.append(score)
        finalscore+=score
        pass
    currentminscore.config(text=("Final score is "+str(finalscore)))
    label1.destroy()
    label2.destroy()
    suggA.destroy()
    suggB.destroy()
    mainbutton.destroy()
    input1.destroy()
    input2.destroy()
root.mainloop()
