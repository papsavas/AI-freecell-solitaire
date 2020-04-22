# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 19:59:34 2020

@author: SAVVAS PAPAGEORGIADIS - dai18001@uom.edu.gr

External Packages: anytree, pandas 


"""

from collections import deque 
import pandas as pd
import copy
from anytree import Node, RenderTree
import sys 


NUM_OF_STACKS=8

def returnInputs(argv):
    inputs = pd.read_csv(r"C:\Users\papsa\Desktop\Εργασία Τεχνητής Νοημοσύνης\generator tests\solitaire5.txt", sep=" ", header=None)
    #inputs.rows = ["St1", "St2", "St3", "St4", "St5", "St6", "St7", "St8"] 
    return inputs


  
      
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

tableau=[]
for i in range(NUM_OF_STACKS): #input data to the tableau
         stackT=deque()     #instead of stack=[], deque is quicker 
         tableau.append(stackT)
         for item in returnInputs(sys.argv).iloc[i]:
            if(item == item):  #avoid not assigned values
                tableau[i].append(Card(item[0],item[1:3])) #Slice card to Card arguments
                print(item, "added in stack no:",i+1)

frontier = deque()                
                
outxt = open("outputs.txt", "a")
outxt.write("Kappa position = "   +"\n")
 
    
class GameInstance(object):  
    def __init__(self, free_cells, tableau, foundations):
        self.free_cells = free_cells  
        self.tableau = tableau
        self.foundations= foundations
        
    def manhattan_distance(self,card,stack): #cd_top is the cards distance from the top of its stack
        cd_top= len(stack)-stack.index(card)
        f_top_number=foundations[returnSuit(card.suit)][-1].number
        dist=int(card.number)-int(f_top_number)
        m_dist=dist+cd_top
        return m_dist    
    
    def printCard(self,card): #testing method
        print(card.suit+card.number)
        
    def copy2freecells(self, card):
         for pos in range(len(free_cells)):
             if(self.free_cells[pos].number==-1):
                 self.free_cells[pos].number=card.number
                 self.free_cells[pos].suit=card.suit
                 outxt.write("freecell " +card.suit+card.number +" \n")
                 print("freecell " +card.suit+card.number)
                 return 
             else:
                print("cell "+str(pos+1) +" is not empty")
                 
    
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
        self.foundations[returnSuit(card.suit)].append(card)
        outxt.write("foundation " +str(card.suit)+ str(card.number)+"\n")
        print("\n foundation " +str(card.suit)+ str(card.number)+"\n")
    
    
    def check4Moving2Foundations(self): #check if any top or freecells card can be added to foundations
        #check from free cells
        for frcard in self.free_cells:
            if (int(frcard.number)) > -1: #if there is a card
                if int(frcard.number) == int(self.foundations[returnSuit(frcard.suit)][-1].number) +1:
                   self.add2Foundations(frcard)
                   frcard.suit=""
                   frcard.number=-1
                            
        for i in range(NUM_OF_STACKS):
            if(self.tableau[i]):
                print("cheking for ",self.tableau[i][-1].suit+self.tableau[i][-1].number)
                suit_index=returnSuit(self.tableau[i][-1].suit)
                if self.foundations[suit_index]:
                    if int(self.tableau[i][-1].number) == int(self.foundations[suit_index][-1].number)+1:
                        self.add2Foundations(self.tableau[i].pop())
                    else:
                        if(int(self.tableau[i][-1].number)==0):
                            self.add2Foundations(self.tableau[i].pop())
    
    
    def printGame(self):
        print('\n')
        print("Freecells: ",self.free_cells[0].suit+str(self.free_cells[0].number)+\
        ','+self.free_cells[1].suit+str(self.free_cells[1].number) +\
        ','+self.free_cells[2].suit+str(self.free_cells[2].number) +\
        ','+self.free_cells[3].suit+str(self.free_cells[3].number) +',')
        
        print('\nTableau:\n')
        ststr=[]
        for i in range(NUM_OF_STACKS):
            stri=''
            for j in range(len(self.tableau[i])):
                 stri+=(self.tableau[i][j].suit+str(self.tableau[i][j].number) +' ')
            ststr.append(stri)
            print(ststr[i]) 
        
        print('\nFoundations:\n')
        ststr2=[]   
        for k in range(4):
            strii=''
            for l in range(len(self.foundations[k])):
                 strii+=(self.foundations[k][l].suit+str(self.foundations[k][l].number) +' ')
            ststr2.append(strii)
            print(ststr2[k])
     
    


            
        
             
     
class TreeNode(GameInstance, Node):  # Add Node feature
    def __init__(self, gi,name, h, g, f, parent, children, direction):
        #super(TreeNode,self).__init__(free_cells,tableau,foundations)
        self.gi=gi
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
            if(self.equalInstances(node, parent)):
                return False
            parent=parent.parent
            return True     
        
#set starting values to gi        

    

g0=GameInstance(free_cells,tableau,foundations)  
#initialize root
root=TreeNode(g0,"root",0,0,0,None,None,-1)

GI= [] #LIST WITH ALL GAME INSTANCES
GI.append(g0)


def getMethod(argv):
    if(len(argv) != 4):
        print("error in arguments. Use correct syntax")
        
    if(str(argv[2]) in ['breadth','depth','best','astar']):
        method=argv[1]
    else:
        print("error in method")
        
    print(argv)
    print("method is:" +method)
    
    
def isSolution(foundation):
    flag=True
    for i in range(4):
        if int(foundation[i][-1].number) != 12:
            flag=False
            break
    return flag
            
def returnNewInstance(last_gi):
    gi=GameInstance(copy.deepcopy(last_gi.free_cells),copy.deepcopy(last_gi.tableau),copy.deepcopy(last_gi.foundations))   #deepcopy to prevent instance privacy
    GI.append(gi)
    return GI

def add2tree(gi, parent):
    node=TreeNode(gi,"Node"+str(len(GI)-1), 0,0,0, parent, None,None)
    return node



def main(argv):
    print("main")
    returnNewInstance(GI[-1])
    print("new instance created")
    last_node=add2tree(GI[-1], root)  #initiate first child of root
    #while(not isSolution(GI[-1].foundations)):
    returnNewInstance(GI[-1])
    print("new instance created")
    
    GI[-1].check4Moving2Foundations()      #move example
    GI[-1].printGame()
    #add to tree the new node and prepare for the next one
    new_node=add2tree(GI[-1], last_node) 
    last_node=new_node
    
    
    
    
    
    
    
    
    
        
if __name__ == "__main__":
   main(sys.argv)


#outxt.close()        


