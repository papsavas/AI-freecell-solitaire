# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 19:59:34 2020

@author: SAVVAS PAPAGEORGIADIS - dai18001@uom.edu.gr
"""

from collections import deque 
import pandas as pd
import copy
from anytree import NodeMixin, RenderTree
import sys 


NUM_OF_STACKS=8



frontier = deque()

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


  

#scan inputs 
inputs = pd.read_csv(r"C:\Users\papsa\Desktop\Εργασία Τεχνητής Νοημοσύνης\generator tests\solitaire5.txt", sep=" ", header=None)
#inputs.rows = ["St1", "St2", "St3", "St4", "St5", "St6", "St7", "St8"]   
      
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




outxt = open("outputs.txt", "a")
outxt.write("Kappa position = "   +"\n")


tableau=[]
for i in range(NUM_OF_STACKS):
    stackT=deque()     #instead of stack=[], deque is quicker 
    tableau.append(stackT)
    for item in inputs.iloc[i]:
        if(item == item):  #avoid not assigned values
            tableau[i].append(Card(item[0],item[1:3])) #Slice card to Card arguments
            print(item, "added in stack no:",i+1)    
#________________________________________________________Add Generator Data to tableau 
            
root= Node("root", copy.deepcopy(tableau), fc=copy.deepcopy(free_cells), fnd=copy.deepcopy(foundations))

def manhattan_distance(card,stack):
    #cd_top is the cards distance from the top of its stack 
    cd_top= len(stack)-stack.index(card)
    f_top_number=foundations[returnSuit(card.suit)][-1].number
    dist=int(card.number)-int(f_top_number)
    m_dist=dist+cd_top
    return m_dist

def equalInstances(node1, node2):
    equal = True
    for stN in range(NUM_OF_STACKS):  #check tableaus
        for j in range(-1,-len(node1.t[stN])):
            if(node1.t[stN][j] and node2.t[stN][j]):
                if (node1.t[stN][j].number != node2.t[stN][j].number) and (node1.t[stN][j].suit != node2.t[stN][j].suit):
                    equal=False
                    print("stN, j = " ,stN,j)
                    return equal
                
    for i in range(4):  #check Freecells
        if (node1.fc[i].suit != node2.fc[i].suit) and (node1.fc[i].number != node2.fc[i].number):
            equal=False
            return equal
        
    return equal           
            
    

def copy2freecells(node, card):
    for pos in range(len(node.fc)):
        if(node.fc[pos].number==-1):
            node.fc[pos].number=card.number
            node.fc[pos].suit=card.suit
            outxt.write("freecell " +card.suit+card.number +" \n")
            print("freecell " +card.suit+card.number)
            return
    print("freecells are full")
    
def moveAll2tableau(): #check whatever card you can add to tableau from freecells
    for FrCard in free_cells:
        for TStNum in range(NUM_OF_STACKS):
            popped = tableau[TStNum].pop()
            if (popped.suit in spades_and_clubs and FrCard.suit in diamonds_and_hearts) or (popped.suit in diamonds_and_hearts and FrCard.suit in spades_and_clubs):
                if(FrCard.number == int(popped.number) - 1):
                    tableau[TStNum].append(popped)
                    FrCard_copy = copy.deepcopy(FrCard)  #Requires deep copy to maintain the value of the variable in the stack when changing it to the free_cells list
                    tableau[TStNum].append(FrCard_copy)
                    outxt.write("stack "+str(FrCard.suit)+str(FrCard.number) +" "+ str(popped.suit)+str(popped.number)+"\n")
                    print("\nstack",str(FrCard.suit)+str(FrCard.number), str(popped.suit)+str(popped.number)+"\n")
                    FrCard.suit=""
                    FrCard.number=-1
            else:
                tableau[TStNum].append(popped)
                
            
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
               
               
   #check from tableau        
    for i in range(NUM_OF_STACKS):
        if(tableau[i]):
            print("cheking for ",tableau[i][-1].suit+tableau[i][-1].number)
            suit_index=returnSuit(tableau[i][-1].suit)
            if foundations[suit_index]:                 #if foundation is not empty
                if int(tableau[i][-1].number) == int(foundations[suit_index][-1].number)+1:
                    add2Foundations(tableau[i].pop())
                    
            else:                                       #if foundation is empty
                if(int(tableau[i][-1].number)==0):
                    add2Foundations(tableau[i].pop())

def ok_with_parents(node):#this function checks if parent nodes contain equal instances
    parent=node.parent
    while(parent != None):
        if(equalInstances(node, parent)):
            return False
        parent=parent.parent
    return True

c1 = Node("child1", t=tableau, fc=free_cells, fnd=foundations, parent=root)


def main(argv):
    
    print("main")
    """  
    if(len(argv) != 4):
        print("error in arguments. Use correct syntax")
        
    if(str(argv[2]) in ['breadth','depth','best','astar']):
        method=argv[1]
    else:
        print("error in method")
        
    print(argv)
    print("method is:" +method)
    
"""
    
        
if __name__ == "__main__":
   main(sys.argv)


#outxt.close()        


