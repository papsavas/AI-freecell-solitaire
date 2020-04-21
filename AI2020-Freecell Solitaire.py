# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 19:59:34 2020

@author: SAVVAS PAPAGEORGIADIS - dai18001@uom.edu.gr

External Packages: anytree, pandas 


"""

from collections import deque 
import pandas as pd
import copy
from anytree import NodeMixin, RenderTree
import sys 


NUM_OF_STACKS=8

#scan inputs 
inputs = pd.read_csv(r"C:\Users\papsa\Desktop\Εργασία Τεχνητής Νοημοσύνης\generator tests\solitaire5.txt", sep=" ", header=None)
#inputs.rows = ["St1", "St2", "St3", "St4", "St5", "St6", "St7", "St8"]   
      
#-------------------------------set the field---------------------------------------------------------------------------------
spades_and_clubs = ['S', 'C']
diamonds_and_hearts = ['D', 'H'] 

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

class Card(object): 
  def __init__(self, suit, number):
      self.suit = suit
      self.number = number
#__________________________________seperate card inputs to card arguments


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

frontier = deque()

tableau=[]
for i in range(NUM_OF_STACKS): #input data to the tableau
         stackT=deque()     #instead of stack=[], deque is quicker 
         tableau.append(stackT)
         for item in inputs.iloc[i]:
            if(item == item):  #avoid not assigned values
                tableau[i].append(Card(item[0],item[1:3])) #Slice card to Card arguments
                print(item, "added in stack no:",i+1)
  
    
class GameInstance(object):  
    def __init__(self, free_cells, tableau, foundations):
        self.free_cells = copy.deepcopy(free_cells)  #deepcopy provides privacy to changes between instances 
        self.tableau = copy.deepcopy(tableau)
        self.foundations= copy.deepcopy(tableau)
        
    def manhattan_distance(self,card,stack): #cd_top is the cards distance from the top of its stack
        cd_top= len(stack)-stack.index(card)
        f_top_number=foundations[returnSuit(card.suit)][-1].number
        dist=int(card.number)-int(f_top_number)
        m_dist=dist+cd_top
        return m_dist    
    
    def printCard(self,card): #testing method
        print(card.suit+card.number)
        
    def copy2freecells(self,node, card):
         for pos in range(len(node.fc)):
             if(node.fc[pos].number==-1):
                 node.fc[pos].number=card.number
                 node.fc[pos].suit=card.suit
                 outxt.write("freecell " +card.suit+card.number +" \n")
                 print("freecell " +card.suit+card.number)
                 return
                 #print("freecells are full")
                 
    
    def moveAll2tableau(self): #check whatever card you can add to tableau from freecells
            for FrCard in free_cells:
                for TStNum in range(NUM_OF_STACKS):
                    tabltop = tableau[TStNum][-1]
                    if (tabltop.suit in spades_and_clubs and FrCard.suit in diamonds_and_hearts) or (tabltop.suit in diamonds_and_hearts and FrCard.suit in spades_and_clubs):
                        if(FrCard.number == int(tabltop.number) - 1):
                            FrCard_copy = copy.deepcopy(FrCard)  #Requires deep copy to maintain the value of the variable in the stack when changing it to the free_cells list
                            tableau[TStNum].append(FrCard_copy)
                            outxt.write("stack "+str(FrCard.suit)+str(FrCard.number) +" "+ str(tabltop.suit)+str(tabltop.number)+"\n")
                            print("\nstack",str(FrCard.suit)+str(FrCard.number), str(tabltop.suit)+str(tabltop.number)+"\n")
                            FrCard.suit=""
                            FrCard.number=-1
                            
    
    def add2Foundations(self,card):
        foundations[returnSuit(card.suit)].append(card)
        outxt.write("foundation " +str(card.suit)+ str(card.number)+"\n")
        print("\n foundation " +str(card.suit)+ str(card.number)+"\n")
    
    
    def check4Moving2Foundations(self): #check if any last or freecells card can be added to foundations
        #check from free cells
        for frcard in free_cells:
            if (int(frcard.number)) > -1: #if there is a card
                if int(frcard.number) == int(foundations[returnSuit(frcard.suit)][-1].number) +1:
                   add2Foundations(frcard)
                   frcard.suit=""
                   frcard.number=-1
                            
        for i in range(NUM_OF_STACKS):
            if(tableau[i]):
                print("cheking for ",tableau[i][-1].suit+tableau[i][-1].number)
                suit_index=returnSuit(tableau[i][-1].suit)
                if foundations[suit_index]:
                    if int(tableau[i][-1].number) == int(foundations[suit_index][-1].number)+1:
                        add2Foundations(tableau[i].pop())
                    else:
                        if(int(tableau[i][-1].number)==0):
                            add2Foundations(tableau[i].pop())
    
    def returnTableau(self):
        return tableau
    
    def returnFreeCells(self):
        return free_cells
    
    def returnFoundations(self):
        return foundations


            
        
             
     
class TreeNode(GameInstance, NodeMixin):  # Add Node feature
    def __init__(self, name, h, g, f, parent, children, direction):
        super(TreeNode,self).__init__(free_cells,tableau,foundations)
        self.name = name
        self.h = h
        self.g = g
        self.f = f
        if parent:
            self.parent = parent
        if children:
            self.children = children 
        self.direction=direction    
        
    def equalInstances(self,node1, node2):
        equal=True
        for stN in range(NUM_OF_STACKS): #check tableaus
            for j in range(-1,-len(node1.t[stN])):
                if(node1.t[stN][j].number != node2.t[stN][j].number) and (node1.t[stN][j].suit != node2.t[stN][j].suit):
                    equal=False
                    print("stN, j = " ,stN,j)
                    return equal
        for i in range(4):
            if (node1.fc[i].suit != node2.fc[i].suit) and (node1.fc[i].number != node2.fc[i].number):
                equal=False
        return equal   
    
    def ok_with_parents(self,node):
        #this function checks if parent nodes contain equal instances
        parent=node.parent
        while(parent != None):
            if(equalInstances(node, parent)):
                return False
            parent=parent.parent
            return True     
        
#set starting values to gi        
g0=GameInstance(copy.deepcopy(free_cells),copy.deepcopy(tableau), copy.deepcopy(foundations))  

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


