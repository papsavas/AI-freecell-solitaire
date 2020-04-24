# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 19:59:34 2020

@author: SAVVAS PAPAGEORGIADIS - dai18001@uom.edu.gr

Python 3.7
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

frontier = []             
                
outxt = open("outputs.txt", "a")
outxt.write("Kappa position = "   +"\n")
 
    
class GameInstance(object):  
    def __init__(self, free_cells, tableau, foundations):
        self.free_cells = free_cells  
        self.tableau = tableau
        self.foundations= foundations
        
    def manhattan_distance(self,card,stack): #cd_top is the cards distance from the top of its stack
        cd_top= len(stack)-stack.index(card)
        f_top_number=self.foundations[returnSuit(card.suit)][-1].number
        dist=int(card.number)-int(f_top_number)
        m_dist=dist+cd_top
        return m_dist    
    
    def printCard(self,card): #testing method
        return(card.suit+str(card.number))
        
    def copy2freecells(self, card):
         for pos in range(len(free_cells)):
             if(self.free_cells[pos].number==-1):
                 self.free_cells[pos].number=card.number
                 self.free_cells[pos].suit=card.suit
                 outxt.write("freecell " +card.suit+card.number +" \n")
                 print("freecell " +card.suit+card.number)
                 return True
             else:
                print("cell "+str(pos+1) +" is not empty")
         return False
        
    
    def freecells2tableau(self): #check whatever card you can add to tableau from freecells
            for FrCard in self.free_cells:
                for TStNum in range(NUM_OF_STACKS):
                    if(self.tableau[TStNum]):
                        tabltop = self.tableau[TStNum][-1]
                        if (tabltop.suit in spades_and_clubs and FrCard.suit in diamonds_and_hearts) or \
                            (tabltop.suit in diamonds_and_hearts and FrCard.suit in spades_and_clubs):
                            if(FrCard.number == int(tabltop.number) - 1):
                                self.tableau[TStNum].append(FrCard)
                                outxt.write("stack "+str(FrCard.suit)+str(FrCard.number) +" "+ str(tabltop.suit)+str(tabltop.number)+"\n")
                                print("\nstack",str(FrCard.suit)+str(FrCard.number), str(tabltop.suit)+str(tabltop.number)+"\n")
                                FrCard.suit=""
                                FrCard.number=-1
                                return True
                    
            return False
                        
    def stackCard(self,card):
        for i in range(NUM_OF_STACKS):
            if(self.tableau[i]):
                if(card in self.tableau[i]): #skip cards stack
                    continue
                else:
                    currTop=self.tableau[i][-1] #stacks current top card
                    if (currTop.suit in spades_and_clubs and card.suit in diamonds_and_hearts) or \
                        (currTop.suit in diamonds_and_hearts and card.suit in spades_and_clubs):
                            if(int(card.number) == int(currTop.number) - 1):
                                self.tableau[i].append(card)
                                outxt.write("stack "+str(card.suit)+str(card.number) +" "+str(currTop.suit)+str(currTop.number)+'\n')
                                print("stack "+str(card.suit)+str(card.number) +" "+str(currTop.suit)+str(currTop.number)+'\n')
                                return True
        return False                    
                    
                
                    
    
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
                   return True
                            
        for i in range(NUM_OF_STACKS):
            if(self.tableau[i]):
                #print("cheking for ",self.tableau[i][-1].suit+self.tableau[i][-1].number)
                suit_index=returnSuit(self.tableau[i][-1].suit)
                if self.foundations[suit_index]:
                    if int(self.tableau[i][-1].number) == int(self.foundations[suit_index][-1].number)+1:
                        self.add2Foundations(self.tableau[i].pop())
                        return True
                else:
                    if(int(self.tableau[i][-1].number)==0):
                        self.add2Foundations(self.tableau[i].pop())
                        return True
        return False
    
    
    def returnCardDistances(self):
        GBcards=[]
        for i in range(NUM_OF_STACKS):
            sdist=[]
            for card in self.tableau[i]:
                distNcard=[self.manhattan_distance(card, self.tableau[i]), card]
                sdist.append(distNcard)
            GBcards.append(sdist)
        return GBcards
            
    def BestCard(self):
        C_D=self.returnCardDistances()
        min_card=C_D[0][0][0],C_D[0][0][1] #manhattan_distance of the first card
        for i in range(NUM_OF_STACKS):
            for j in range(len(C_D[i])):
                if(C_D[i][j][0] < min_card[0]):
                    min_card=C_D[i][j]
                
        return min_card
    
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
        
    def equalInstances(self, node2):
        equal=True
        for stN in range(NUM_OF_STACKS): #check tableaus
            for j in range(1,len(self.gi.tableau[stN])):
                if self.gi.tableau[stN] and node2.gi.tableau[stN]:
                    if(self.gi.tableau[stN][-j].number != node2.gi.tableau[stN][-j].number) and (self.gi.tableau[stN][-j].suit != node2.gi.tableau[stN][-j].suit):
                        equal=False
                        return equal
                    
        for i in range(4):
            if (self.gi.free_cells[i].suit != node2.gi.free_cells[i].suit) and (self.gi.free_cells[i].number != node2.gi.free_cells[i].number):
                equal=False
                return equal
        return equal   
    
    def loop_in_parents(self):
        #this function checks if parent nodes contain equal instances
        parent=self.parent
        while(parent != None):
            if(self.equalInstances(parent)):
                return True
            parent=parent.parent
        return False     
        
    

def getMethod(argv):
    if(len(argv) != 4):
        print("error in arguments. Use correct syntax")
        
    if(str(argv[2]) in ['breadth','depth','best','astar']):
        method=argv[1]
    else:
        print("error in method")
        
    print(argv)
    print("method is:" +method)
    
    
def isSolution(foundations):
    flag=True
    for i in range(4):
        if int(foundations[i][-1].number) != 12:
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


def add_frontier_top(node):
    if(node.is_leaf()):
        frontier.insert(0,node)
        return True
    else:
        print(str(node.name())+" is not a leaf")
        return False

def add_frontier_back(node):
    if(node.is_leaf()):
        frontier.append(node)
        return True
    else:
        print(str(node.name())+" is not a leaf")
        return False
    
def add_frontier_in_order(node):
    if(node.is_leaf()):
        frontier.append(node)
        frontier.sort(key=(node.f,node.h))
        return True
    else:
        print(str(node.name())+" is not a leaf")
        return False

"""    
def loopHandling(last_node,new_node):
    if(new_node.loop_in_parents()):
        print("loop detected")
        new_node.parent=None
        del new_node                
    else:
        last_node=new_node
"""

def DFS(root):
    returnNewInstance(GI[-1])
    last_node=add2tree(GI[-1], root)
    stack_number=0
    dead_end = False

    while (not(isSolution(last_node.gi.foundations))) and (not dead_end) and stack_number<8:
        if(not last_node.gi.tableau[stack_number]):
            stack_number+=1
        print('\nstack no:',stack_number)
        returnNewInstance(GI[-1])
        print("selected card is: "+last_node.gi.printCard(tableau[stack_number][-1]))
        if(last_node.gi.check4Moving2Foundations()):
            new_node=add2tree(GI[-1], last_node)
            if(new_node.loop_in_parents()):
                print("loop detected")
                new_node.parent=None
                del new_node                
            else:
                last_node=new_node
            print("dfs foundations")
            continue
        
        elif(last_node.gi.freecells2tableau()):
            new_node=add2tree(GI[-1], last_node) 
            if(new_node.loop_in_parents()):
                print("loop detected")
                new_node.parent=None
                del new_node                
            else:
                last_node=new_node
            print("dfs freecells2tableau")
            continue
        
        elif(last_node.gi.stackCard(last_node.gi.tableau[stack_number][-1])):
            last_node.gi.tableau[stack_number].pop() #get rid of the clone card 
            new_node=add2tree(GI[-1], last_node) 
            if(new_node.loop_in_parents()):
                print("loop detected")
                new_node.parent=None
                del new_node                
            else:
                last_node=new_node
            print("dfs stack2stack")
            continue
        
        elif(last_node.gi.copy2freecells(last_node.gi.tableau[stack_number][-1])):
            last_node.gi.tableau[stack_number].pop()
            new_node=add2tree(GI[-1], last_node) 
            if(new_node.loop_in_parents()):
                print("loop detected")
                new_node.parent=None
                del new_node                
            else:
                last_node=new_node
            print("dfs 2freecells")
            continue
        
        else:
            print('dead end')
            dead_end=True
            break
            
    
    return last_node
                    
                
        
    
            
            
    
    

g0=GameInstance(free_cells,tableau,foundations)  
#initialize root
root=TreeNode(g0,"root",0,0,0,None,None,-1)

GI= [] #LIST WITH ALL GAME INSTANCES
GI.append(g0)


def main(argv):
    print("main")
    dfs=DFS(root)
    """
    returnNewInstance(GI[-1])
    print("new instance created")
    last_node=add2tree(GI[-1], root)  #initiate first child of root
    #while(not isSolution(GI[-1].foundations)):
    returnNewInstance(GI[-1])
    print("new instance created")
    
    GI[-1].check4Moving2Foundations()      #move example
    GI[-1].printGame()
    #add to tree the new node and prepare for the next one
   """

    
  #  c11=root.children[0].children[0]
   # bc1=c11.gi.BestCard()

     
    
    
if __name__ == "__main__":
   main(sys.argv)


#outxt.close()        


