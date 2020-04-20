# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 19:59:34 2020

@author: SAVVAS PAPAGEORGIADIS - dai18001@uom.edu.gr
"""

from collections import deque 
import pandas as pd
import copy
from anytree import Node, RenderTree


NUM_OF_STACKS=8




class Card(object): 
  def __init__(self, suit, number):
      self.suit = suit
      self.number = number
#__________________________________seperate card inputs to card arguments

def returnSuit(suit):
    if(suit=="S"):
        return 0
    elif(suit=="H"):
        return 1
    elif(suit=="D"):
        return 2
    elif(suit=="C"):
        return 3
    elif(suit==0):
        return 'S'
    elif(suit==1):
        return 'H'
    elif(suit==2):
        return'D'
    elif(suit==3):
        return 'C'
    else:
        print("Error in returning suit assigment")

#-------------------------------set the field---------------------------------------------------------------------------------
spades_and_clubs = ['S', 'C']
diamonds_and_hearts = ['D', 'H']      
      
free_cells = []
for i in range(4):
    free_cells.append(Card('',-1))
        
foundations=[]
for i in range(4):
    stackF=deque()  #instead of stack=[], deque is quicker
    foundations.append(stackF)
    foundations[i].append(Card(returnSuit(i),-1))


#scan inputs 
inputs = pd.read_csv(r"C:\Users\papsa\Desktop\Εργασία Τεχνητής Νοημοσύνης\generator tests\solitaire5.txt", sep=" ", header=None)
#inputs.rows = ["St1", "St2", "St3", "St4", "St5", "St6", "St7", "St8"]

outxt = open("outputs.txt", "a")
outxt.write("Kappa position = "   +"\n")


tableu=[]
for i in range(NUM_OF_STACKS):
    stackT=deque()     #instead of stack=[], deque is quicker 
    tableu.append(stackT)
    for item in inputs.iloc[i]:
        if(item == item):  #avoid not assigned values
            tableu[i].append(Card(item[0],item[1:3])) #Slice card to Card arguments
            print(item, "added in stack no:",i+1)    


def manhattan_distance(card,stack):
    #cd_top is the cards distance from the top of its stack 
    cd_top= len(stack)-stack.index(card)
    f_top_number=foundations[returnSuit(card.suit)][-1].number
    dist=int(card.number)-int(f_top_number)
    m_dist=dist+cd_top
    return m_dist

def copy2freecells(card):
    for pos in range(len(free_cells)):
        if(free_cells[pos].number==-1):
            free_cells[pos].number=card.number
            free_cells[pos].suit=card.suit
            outxt.write("freecell " +card.suit+card.number +" \n")
            print("freecell " +card.suit+card.number)
            return
    print("freecells are full")
    
def moveAll2tableu(): #check whatever card you can add to tableu from freecells
    for FrCard in free_cells:
        for TStNum in range(NUM_OF_STACKS):
            popped = tableu[TStNum].pop()
            if (popped.suit in spades_and_clubs and FrCard.suit in diamonds_and_hearts) or (popped.suit in diamonds_and_hearts and FrCard.suit in spades_and_clubs):
                if(FrCard.number == int(popped.number) - 1):
                    tableu[TStNum].append(popped)
                    FrCard_copy = copy.deepcopy(FrCard)  #Requires deep copy to maintain the value of the variable in the stack when changing it to the free_cells list
                    tableu[TStNum].append(FrCard_copy)
                    outxt.write("stack "+str(FrCard.suit)+str(FrCard.number) +" "+ str(popped.suit)+str(popped.number)+"\n")
                    print("\nstack",str(FrCard.suit)+str(FrCard.number), str(popped.suit)+str(popped.number)+"\n")
                    FrCard.suit=""
                    FrCard.number=-1
            else:
                tableu[TStNum].append(popped)
                
            
def add2Foundations(card):
    foundations[returnSuit(card.suit)].append(card)
    outxt.write("foundation " +str(card.suit)+ str(card.number)+"\n")
    print("\n foundation " +str(card.suit)+ str(card.number)+"\n")
    
    
def check4Moving2Foundations(): #check if any last or freecells card can be added to foundations
   
    #check from free cells
    for frcard in free_cells:
        if (int(frcard.number)) > -1: #if there is a card
            if int(frcard.number) == int(foundations[returnSuit(frcard.suit)][-1].number) +1:
               add2Foundations(frcard)
               frcard.suit=""
               frcard.number=-1
               
               
   #check from Tableu        
    for i in range(NUM_OF_STACKS):
        if(tableu[i]):
            print("cheking for ",tableu[i][-1].suit+tableu[i][-1].number)
            suit_index=returnSuit(tableu[i][-1].suit)
            if foundations[suit_index]:                 #if foundation is not empty
                if int(tableu[i][-1].number) == int(foundations[suit_index][-1].number)+1:
                    add2Foundations(tableu[i].pop())
                    
            else:                                       #if foundation is empty
                if(int(tableu[i][-1].number)==0):
                    add2Foundations(tableu[i].pop())
                    
    



check4Moving2Foundations()


        


#outxt.close()        
"""   
Giving a number n, this function returns the row
of this number in a solution puzzle. For example,
in a 3x3 puzzle, number 7 should appear in the row 2
in the solution (note that the first row is numbered as 0).
Inputs:
int n;	A number between 1 and N^2-1
Output:
An integer indicating the vertical position of the number n in the solution.

def get_x(n):
	return (n-1)/N    
"""
    

"""

if ((popped.suit =="S" or popped.suit == "C") and (FrCard.suit=="D" or FrCard.suit=="H")) or ((popped.suit =="H" or popped.suit == "D") and (FrCard.suit=="S" or FrCard.suit=="C")):

    
    # could be rewritten as
    
    
spades_and_clubs = ['S', 'C']
diamonds_and_hearts = ['D', 'H']
if (popped.suit in spades_and_clubs and FrCard.suit in diamonds_and_hearts) or (popped.suit in diamonds_and_hearts and FrCard.suit in spades_and_clubs):


"""

