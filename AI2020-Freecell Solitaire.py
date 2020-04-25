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
    inputs = pd.read_csv(r"C:\Users\papsa\Desktop\Εργασία Τεχνητής Νοημοσύνης\generator tests\solitaire7.txt", sep=" ", header=None)
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
                #print(item, "added in stack no:",i+1)

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
         for pos in range(4):
             if(int(self.free_cells[pos].number)==-1):
                 self.free_cells[pos].number=card.number
                 self.free_cells[pos].suit=card.suit
                 outxt.write("freecell " +card.suit+card.number +" \n")
                 print("freecell " +card.suit+card.number)
                 return True
             else:
                print("cell "+str(pos+1) +" is not empty")
         return False
        
    
    def freecells2tableau(self,TStNum): #check whatever card you can add to tableau from freecells
            
            if(self.tableau[TStNum]):
                tabltop = self.tableau[TStNum][-1]
                for FrCard in self.free_cells:
                    if(FrCard.number==-1):
                        continue
                    else:
                        if (tabltop.suit in spades_and_clubs and FrCard.suit in diamonds_and_hearts) or \
                            (tabltop.suit in diamonds_and_hearts and FrCard.suit in spades_and_clubs):
                            if(int(FrCard.number) == int(tabltop.number) - 1):
                                self.tableau[TStNum].append(copy.deepcopy(FrCard))
                                outxt.write("stack "+str(FrCard.suit)+str(FrCard.number) +" "+ str(tabltop.suit)+str(tabltop.number)+"\n")
                                print("\nstack",str(FrCard.suit)+str(FrCard.number), str(tabltop.suit)+str(tabltop.number)+"\n")
                                FrCard.suit=""
                                FrCard.number=-1
                                return True
            else:
                self.tableau[TStNum].append(copy.deepcopy(FrCard))
                outxt.write("stack "+str(FrCard.suit)+str(FrCard.number) +" "+ str(tabltop.suit)+str(tabltop.number)+"\n")
                print("\nstack",str(FrCard.suit)+str(FrCard.number), str(tabltop.suit)+str(tabltop.number)+"\n")
                FrCard.suit=""
                FrCard.number=-1
                return True
                        
            return False
                        
    def stackCard(self,CardsStack):
        if len(CardsStack)>1 and (CardsStack[-1].suit in spades_and_clubs and CardsStack[-2].suit in diamonds_and_hearts) or \
                            (CardsStack[-1].suit in diamonds_and_hearts and CardsStack[-2].suit in spades_and_clubs):
                                if(int(CardsStack[-1].number) == int(CardsStack[-2].number) - 1):
                                    return False
        for i in range(NUM_OF_STACKS):
            if(self.tableau[i]):
                if(CardsStack[-1] in self.tableau[i]): #skip cards stack
                    continue
                else:
                    if len(CardsStack) < len(self.tableau[i]):
                        currTop=self.tableau[i][-1] #stacks current top card
                        if (currTop.suit in spades_and_clubs and CardsStack[-1].suit in diamonds_and_hearts) or \
                            (currTop.suit in diamonds_and_hearts and CardsStack[-1].suit in spades_and_clubs):
                                if(int(CardsStack[-1].number) == int(currTop.number) - 1):
                                    self.tableau[i].append(CardsStack[-1])
                                    outxt.write("stack "+str(CardsStack[-1].suit)+str(CardsStack[-1].number) +" "+str(currTop.suit)+str(currTop.number)+'\n')
                                    print("stack "+str(CardsStack[-1].suit)+str(CardsStack[-1].number) +" "+str(currTop.suit)+str(currTop.number)+'\n')
                                    print(self.printGame())
                                    return True
        return False                    
                    
                
                    
    
    def add2Foundations(self,card):
        if int(card.number) == int(self.foundations[returnSuit(card.suit)][-1].number) +1:
            self.foundations[returnSuit(card.suit)].append(card)
            outxt.write("foundation " +str(card.suit)+ str(card.number)+"\n")
            print("\n foundation " +str(card.suit)+ str(card.number)+"\n")
            return True
        return False
    
    def checkAll4Foundations(self): #check if any top or freecells card can be added to foundations
        #check from free cells
        for frcard in self.free_cells:
            if (int(frcard.number)) > -1: #if there is a card
                if self.add2Foundations(frcard):
                   frcard.suit=""
                   frcard.number=-1
                   return True
                            
        for i in range(NUM_OF_STACKS):
            if(self.tableau[i]):
                #print("cheking for ",self.tableau[i][-1].suit+self.tableau[i][-1].number)
                #suit_index=returnSuit(self.tableau[i][-1].suit)
                #if self.foundations[suit_index]:
                if self.add2Foundations(self.tableau[i][-1]):
                    self.tableau[i].pop()  #get rid of clone card
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
            
    def BestCard(self): #search and find the best card in current situations
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
                if (not self.gi.tableau[stN][-j]) ^ (not node2.gi.tableau[stN][-j]): #if some node stack is out of range means that somethings different
                    return False
                if self.gi.tableau[stN] and node2.gi.tableau[stN]:
                    if(self.gi.tableau[stN][-j].number != node2.gi.tableau[stN][-j].number) and \
                    (self.gi.tableau[stN][-j].suit != node2.gi.tableau[stN][-j].suit):
                        equal=False
                        return equal
                    
        for i in range(4):
            if (self.gi.free_cells[i].suit != node2.gi.free_cells[i].suit) and (self.gi.free_cells[i].number != node2.gi.free_cells[i].number):
                equal=False
                return equal
        return equal   
    
    def loop_in_parents(self):
        #this function checks if parent nodes contain equal instances
        parent1=self.parent
        while(parent1!= None):
            if(self.equalInstances(parent1)):
                return True
            parent1=parent1.parent
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

def add2tree(parent, gi):
    node=TreeNode(copy.deepcopy(gi),"Node"+str(parent.depth), 0,0,0, parent, None,None)
    return node


def add_frontier_front(node):
    if(node.is_leaf):
        frontier.insert(0,node)
        return True
    else:
        print(str(node.name+" is not a leaf"))
        return False

def add_frontier_back(node):
    if(node.is_leaf):
        frontier.append(node)
        return True
    else:
        print(str(node.name())+" is not a leaf")
        return False
    
def add_frontier_in_order(node):
    if(node.is_leaf):
        frontier.append(node)
        frontier.sort(key=(node.f,node.h))
        return True
    else:
        print(str(node.name())+" is not a leaf")
        return False

""" 
def loopHandling(parent_node,current_node,rejected_flag):
    if(current_node.loop_in_parents()):
        print("loop detected")
        del current_node
        rejected_flag=True
        return parent_node,rejected_flag        
    else:
        rejected_flag=False
        return current_node,rejected_flag
"""


visited=[]
def recursDFS(sub_root):
    #returnNewInstance(GI[-1])
    if(not sub_root):
        print("ROOT reached, returning")
        return sub_root
   
    parent=sub_root
    
    if(parent in visited):
        if(parent.parent):
            recursDFS(parent.parent)
   
    
    dead_end=True
    foundrejected=False
    f2trejected=False
    s2srejected = False
    freecellrejected = False

    for index in range(NUM_OF_STACKS):
        print('\nstack no:',(index)+1)   
        
        temp_node=copy.deepcopy(parent)
        currCard=temp_node.gi.tableau[index][-1]
        print("card is: " +temp_node.gi.printCard(currCard))
        
        foundationsMove = temp_node.gi.add2Foundations(temp_node.gi.tableau[index][-1]) #attempt to add current card to Foundations
        if(foundationsMove):
            temp_node.gi.tableau[index].pop() #get rid of clone card
            temparent=parent
            while(temparent!=None):
                if(not temp_node.equalInstances(temparent)):
                    temparent=temparent.parent
                    continue
                else:
                    print("loop detected")
                    foundrejected=True
                    break
            if(not foundrejected):
                new_node=add2tree(parent,temp_node.gi)
                print("dfs foundations")
                
        
        temp_node=copy.deepcopy(parent) #clean temp_node from previous changes
        freecells2TableauMove = temp_node.gi.freecells2tableau(index)
        
        if(freecells2TableauMove and not f2trejected):
            temparent=parent
            while(temparent!=None):
                if(not temp_node.equalInstances(temparent)):
                    temparent=temparent.parent
                    continue
                else:
                    print("loop detected")
                    f2trejected=True
                    break
            if(not f2trejected):
                new_node=add2tree(parent,temp_node.gi)
                print("dfs foundations")
                
       
        temp_node=copy.deepcopy(parent)
        StackingMove = temp_node.gi.stackCard(temp_node.gi.tableau[index])
        
        if(StackingMove):
            temp_node.gi.tableau[index].pop()
           
            temparent=parent
            while(temparent!=None):
                if(not temp_node.equalInstances(temparent)):
                    temparent=temparent.parent
                    continue
                else:
                    print("loop detected")
                    s2srejected=True
                    break
            if(not s2srejected):
                new_node=add2tree(parent,temp_node.gi)
                print("dfs foundations")
                
            
        temp_node=copy.deepcopy(parent)
        #check if the top 2 cards are already stacked 
        if len(temp_node.gi.tableau[index])>1 and not ((int(currCard.number) == int(temp_node.gi.tableau[index][-2].number) -1) and ((currCard.suit in diamonds_and_hearts and temp_node.gi.tableau[index][-2].suit in spades_and_clubs) or (currCard.suit in spades_and_clubs and temp_node.gi.tableau[index][-2].suit in diamonds_and_hearts))):
            freecellsMove = temp_node.gi.copy2freecells(temp_node.gi.tableau[index][-1])
            if(freecellsMove):
                temp_node.gi.tableau[index].pop() #get rid of clone card
                
                temparent=parent
                while(temparent!=None):
                    if(not temp_node.equalInstances(temparent)):
                        temparent=temparent.parent
                        continue
                    else:
                        print("loop detected")
                        freecellrejected=True
                        break
                if(not freecellrejected):
                    new_node=add2tree(parent,temp_node.gi)
                    print("dfs foundations")
        temp_node.gi.printGame()               
                
    if(parent not in visited):
        visited.append(parent)  #node examined
   
    if(isSolution(parent.gi.foundations)):
        print("----------SOLVED----------")
        parent.gi.printGame()
        add_frontier_front(parent)
        return parent
        
    #parent.gi.printGame()
    
    if(parent.children): #if parent has children
        for child in parent.children:
            if child not in visited:
                recursDFS(child)
    else:
        add_frontier_front(parent)
        recursDFS(parent.parent)
    
            

    
                            
    
#return parent
                    
    
def BEST(root):
    parent=add2tree(root)
    
    init_stack=0
    while(not(isSolution(parent.gi.foundations))):
        bestCard=BestCard(parent)
        
    
    

g0=GameInstance(free_cells,tableau,foundations)  
#initialize root
root=TreeNode(g0,"root",0,0,0,None,None,-1)

GI= [] #LIST WITH ALL GAME INSTANCES
GI.append(g0)


def main(argv):
    print("main")
    dfs=recursDFS(root)
    #best=BEST(root)
    """
    returnNewInstance(GI[-1])
    print("new instance created")
    last_node=add2tree(GI[-1], root)  #initiate first child of root
    #while(not isSolution(GI[-1].foundations)):
    returnNewInstance(GI[-1])
    print("new instance created")
    
    GI[-1].checkAll4Foundations()      #move example
    GI[-1].printGame()
    #add to tree the new node and prepare for the next one
   """

    
  #  c11=root.children[0].children[0]
   # bc1=c11.gi.BestCard()

     
    
    
if __name__ == "__main__":
   main(sys.argv)


#outxt.close()        


