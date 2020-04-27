# -*- coding: utf-8 -*-
"""
Created on Fri Apr  3 19:59:34 2020

@author: SAVVAS PAPAGEORGIADIS - dai18001@uom.edu.gr

~~~~~~~~~~~~~
Requirements:
- Python 3.7
- External Packages: anytree, pandas, daytime (pip install [package])
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

"""


from collections import deque 
import pandas as pd
import copy
from anytree import Node, RenderTree
import sys 
import datetime

scriptmode=False
NUM_OF_STACKS=8

if(scriptmode):
        ARGV=sys.argv
else:
    path='C:\\Users\\papsa\\Desktop\\Εργασία Τεχνητής Νοημοσύνης\\generator tests\\solitaire5.txt'
    pseudoargv=['AI2020-Freecell Solitaire.py','best',path,'output.txt']
    ARGV=pseudoargv


if(scriptmode):
    print("script mode. Inputing thourgh terminal is disabled.")
    #input_file = pd.read_csv(r'argv[2]', sep=" ", header=None)
    #inputs.rows = ["St1", "St2", "St3", "St4", "St5", "St6", "St7", "St8"] 
else:
    path=ARGV[2]
    inputs = pd.read_csv(r'C:\Users\papsa\Desktop\Εργασία Τεχνητής Νοημοσύνης\generator tests\solitaire5.txt', sep=" ", header=None)




  
      
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
         for item in inputs.values[i]:
            if(item == item):  #avoid not assigned values
                tableau[i].append(Card(item[0],item[1:3])) #Slice card to Card arguments
                #print(item, "added in stack no:",i+1)

frontier = []
                


    
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
    
    def add2Foundations(self,card):
        if int(card.number) == int(self.foundations[returnSuit(card.suit)][-1].number) +1:
            self.foundations[returnSuit(card.suit)].append(card)
            self.movement="foundation " +str(card.suit)+ str(card.number)
            print("\n foundation " +str(card.suit)+ str(card.number)+"\n")
            return True
        return False
    
    def freecell2foundation(self):
        for fcard in self.free_cells: #check if they can be added to foundations first
            if fcard.suit:
                if(self.add2Foundations(fcard)):
                    fcard.suit='' #reset freecell
                    fcard.number=-1
                    return True
    
    
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

    
    def copy2freecells(self, card):
         for pos in range(4):
             if(int(self.free_cells[pos].number)==-1):
                 self.free_cells[pos].number=card.number
                 self.free_cells[pos].suit=card.suit
                 self.movement="freecell " +card.suit+card.number
                 print("freecell " +card.suit+card.number)
                 return True
             else:
                print("cell "+str(pos+1) +" is not empty")
         return False
        
    
    def freecells2tableau(self,TStNum): #check whatever card you can add to  tableau from freecells 
        if(self.tableau[TStNum]): #if the stack is not empty
            tabltop = self.tableau[TStNum][-1]
            for FrCard in self.free_cells: #if its empty go to the next card 
                if(FrCard.number==-1):
                    continue
                else:
                    if (tabltop.suit in spades_and_clubs and FrCard.suit in diamonds_and_hearts) or \
                        (tabltop.suit in diamonds_and_hearts and FrCard.suit in spades_and_clubs): #if suits..suit
                        if(int(FrCard.number) == int(tabltop.number) - 1):
                            self.tableau[TStNum].append(copy.deepcopy(FrCard))
                            self.movement="stack "+str(FrCard.suit)+str(FrCard.number) +" "+ str(tabltop.suit)+str(tabltop.number)
                            print("\nstack",str(FrCard.suit)+str(FrCard.number), str(tabltop.suit)+str(tabltop.number)+"\n")
                            FrCard.suit=""
                            FrCard.number=-1
                            return True
        elif(not self.tableau[TStNum]):#if stack is empty, add it anyway
             for FrCard in self.free_cells:  
                if(FrCard.number==-1):
                    continue                                
                else:
                    self.tableau[TStNum].append(copy.deepcopy(FrCard))
                    self.movement="stack "+str(FrCard.suit)+str(FrCard.number) +" "+ str(tabltop.suit)+str(tabltop.number)
                    print("\nstack",str(FrCard.suit)+str(FrCard.number), str(tabltop.suit)+str(tabltop.number)+"\n")
                    FrCard.suit=""
                    FrCard.number=-1
                    return True
                    
        return False
                        
    def stackCard(self,CardsStack):
        if len(CardsStack)>1 and ((CardsStack[-1].suit in spades_and_clubs and CardsStack[-2].suit in diamonds_and_hearts) or \
                            (CardsStack[-1].suit in diamonds_and_hearts and CardsStack[-2].suit in spades_and_clubs)):
                                if(int(CardsStack[-1].number) == int(CardsStack[-2].number) - 1): # if card is already stacked 
                                    return False
        for i in range(NUM_OF_STACKS):
            if(self.tableau[i]):
                if(CardsStack[-1] in self.tableau[i]): #skip cards stack
                    continue
                elif len(CardsStack) < len(self.tableau[i]):
                    currTop=self.tableau[i][-1] #stacks current top card
                    if (currTop.suit in spades_and_clubs and CardsStack[-1].suit in diamonds_and_hearts) or \
                        (currTop.suit in diamonds_and_hearts and CardsStack[-1].suit in spades_and_clubs):
                            if(int(CardsStack[-1].number) == int(currTop.number) - 1):
                                self.tableau[i].append(CardsStack[-1])
                                self.movement="stack "+str(CardsStack[-1].suit)+str(CardsStack[-1].number) +" "+str(currTop.suit)+str(currTop.number)
                                print("stack "+str(CardsStack[-1].suit)+str(CardsStack[-1].number) +" "+str(currTop.suit)+str(currTop.number)+'\n')
                                print(self.printGame())
                                return True
            elif(not self.tableau[i]): #if the stack is empty
                self.tableau[i].append(CardsStack[-1])
                self.movement= "stack "+str(CardsStack[-1].suit)+str(CardsStack[-1].number) +" "+str(currTop.suit)+str(currTop.number)
                print("stack "+str(CardsStack[-1].suit)+str(CardsStack[-1].number) +" "+str(currTop.suit)+str(currTop.number)+'\n')
                print(self.printGame())
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
    def __init__(self, gi,name, h, f, parent, children, movement):
        self.gi=gi
        self.name = name
        self.h = h
        self.g = self.depth
        self.f = f
        if parent:
            self.parent = parent
        if children:
            self.children = children 
        self.movement=movement    
        
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
    
    
def isSolution(self):
    for foundation in self.gi.foundations:
        if int(foundation[-1].number) != 12:
            return False
    return True
            


def add2tree(parent, gi):
    node=TreeNode(copy.deepcopy(gi),"Node"+str(parent.depth), 0,0,parent,None,None)
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
        if(frontier): #if the frontier is not empty
            for index in range(len(frontier)):
                if node.f < frontier[index].f or (node.f == frontier[index].f and node.h<frontier[index].h):
                    continue
        else:
            frontier.insert(0,node)
            return True
    
    else:      
        print(str(node.name())+" is not a leaf")
        return False



def find_children(sub_root,method):
    parent=sub_root
    foundrejected=False
    f2trejected=False
    s2srejected = False
    freecellrejected = False
    index=0
    while index in range(NUM_OF_STACKS):
            print('\nstack no:',(index)+1)   
            
            temp_node=copy.deepcopy(parent)
            currCard=temp_node.gi.tableau[index%4][-1]
            print("card is: " +temp_node.gi.printCard(currCard))
            
            s2foundationsMove1 = temp_node.gi.freecell2foundation() #attempt to add current card from freecells to Foundations
            if(s2foundationsMove1):
                #temp_node.gi.tableau[index].pop() #get rid of clone card
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
                    #new_node.h=(coming soon...)
                    if(method=='best'):
                        new_node.f=new_node.h
                    elif(method=='astar'):
                        new_node.f= new_node.g + new_node.h
                    else:
                        new_node.f=0
                    
                    if(method=='depth'):
                        add_frontier_front(new_node)  #returns bool
                    elif(method=='breadth'):
                        add_frontier_back(new_node)
                    elif(method=='best' or method=='astar'):
                        add_frontier_in_order(new_node)
                    print("dfs foundations")
                    return True
            
            temp_node=copy.deepcopy(parent)
            currCard=temp_node.gi.tableau[index][-1]
            print("card is: " +temp_node.gi.printCard(currCard))
            
            s2foundationsMove = temp_node.gi.add2Foundations(temp_node.gi.tableau[index][-1]) #attempt to add current card to Foundations
            if(s2foundationsMove):
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
                    #new_node.h=???
                    if(method=='best'):
                        new_node.f=new_node.h
                    elif(method=='astar'):
                        new_node.f= new_node.g + new_node.h
                    else:
                        new_node.f=0
                    
                    if(method=='depth'):
                        add_frontier_front(new_node)  #returns bool
                    elif(method=='breadth'):
                        add_frontier_back(new_node)
                    elif(method=='best' or method=='astar'):
                        add_frontier_in_order(new_node)
                    print("dfs foundations")
                    return True
                    
            
            
            
            temp_node=copy.deepcopy(parent) #clean temp_node from previous changes
            freecells2tableauMove = temp_node.gi.freecells2tableau(index)
            
            if(freecells2tableauMove and not f2trejected):
                temparent=parent
                while(temparent!=None):
                    if(not temp_node.equalInstances(temparent)):
                        temparent=temparent.parent
                        continue
                    else:
                        print("loop detected")
                        f2trejected=True
                        return False
                if(not f2trejected):
                    new_node=add2tree(parent,temp_node.gi)
                    #new_node.h=???
                    if(method=='best'):
                        new_node.f=new_node.h
                    elif(method=='astar'):
                        new_node.f= new_node.g + new_node.h
                    else:
                        new_node.f=0
                    
                    if(method=='depth'):
                        add_frontier_front(new_node)  #returns bool
                    elif(method=='breadth'):
                        add_frontier_back(new_node)
                    elif(method=='best' or method=='astar'):
                        add_frontier_in_order(new_node)
                    print("fromfreecells")
                    return True
                    
                    
           
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
                    #new_node.h=???
                    if(method=='best'):
                        new_node.f=new_node.h
                    elif(method=='astar'):
                        new_node.f= new_node.g + new_node.h
                    else:
                        new_node.f=0
                    
                    if(method=='depth'):
                        add_frontier_front(new_node)  #returns bool
                    elif(method=='breadth'):
                        add_frontier_back(new_node)
                    elif(method=='best' or method=='astar'):
                        add_frontier_in_order(new_node)
                    print("stacking")
                    return True
                   
                    
                
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
                        #new_node.h=???
                        if(method=='best'):
                            new_node.f=new_node.h
                        elif(method=='astar'):
                            new_node.f= new_node.g + new_node.h
                        else:
                            new_node.f=0
                        
                        if(method=='depth'):
                            add_frontier_front(new_node)  #returns bool
                        elif(method=='breadth'):
                            add_frontier_back(new_node)
                        elif(method=='best' or method=='astar'):
                            add_frontier_in_order(new_node)
                        print("2freecells")
                        return True
            index+=1 #if it reaches here means that this card had no other move, so check the next one
            
    return False

def search(method):
    startTime=datetime.datetime.now()
    while(frontier): #while the frontier is not empty
        nowtime=datetime.datetime.now()
        if(nowtime > startTime +datetime.timedelta(minutes=5)):
            print("--Timeout-- \n")
            return None
        current_node=frontier.pop(0)
        if(isSolution(current_node)):
            return current_node
        found=find_children(current_node, method)
        if(not found):
            return None
    return None
    
"""
def recursDFS(sub_root,visited):
    parent_node=find_children(sub_root)
    if(parent_node not in visited):
        visited.append(parent_node)  #node examined
   
        if(isSolution(parent_node)):
            print("----------SOLVED----------")
            parent_node.gi.printGame()
            add_frontier_front(parent_node)
            return parent_node
        if(parent_node.children): #if parent has children
            for child in parent_node.children:
                recursDFS(child,visited)
        else:
            add_frontier_front(parent_node)
    else:    
        recursDFS(parent_node.parent_node,visited)
    

def BFS(node,visited):
    visited.append(node)
    queue=[]
    queue.append(node)
    while queue and not isSolution(node):
        node = find_children(queue.pop(0)) 
        for neighbour in node.children:
            if neighbour not in visited:
                visited.append(neighbour)
                queue.append(neighbour)
            else:
                add_frontier_back(node)
    if(isSolution(node)):
        print("------------SOLVED WITH BFS---------------")
        node.gi.printGame()
        return node
        
        
   
def BEST(root):
    parent=add2tree(root)
    
    init_stack=0
    while(not(isSolution(parent.gi.foundations))):
        bestCard=BestCard(parent)
        if(bestCard.add2found)
"""      
def syntax_message():
    	print("puzzle <method> <input-file> <output-file>\n\n");
    	print("where: ");
    	print("<method> = breadth|depth|best|astar\n");
    	print("<input-file> is a file containing stacked cards");
    	print("<output-file> is the file where the solution will be written.\n");

def initialize_search(method):
    #initialize game instance
    g0=GameInstance(free_cells,tableau,foundations)  
    #initialize root
    root=TreeNode(g0,"root",0,0,None,None,None)
    
    if method=='best':
        root.f=root.h
    elif method=='astar':
        root.f=root.g+root.h
    else:
        root.f=0
    
    add_frontier_front(root)
    
def extract_solution(sol_node):
    solutionList=[]
    tempnode=sol_node
    while(tempnode.parent):
        solutionList.append(tempnode.movement)
        tempnode=tempnode.parent
    return solutionList  

def write_solution_to_file(filename, SOLUTION):
    outxt = open(filename, "a")
    outxt.write("K ="+str(len(SOLUTION))+"\n")
    for sol in SOLUTION:
        outxt.write(str(sol.movement)+'\n')
    outxt.close()  
    
    
    
def main(argv):
    #sys.setrecursionlimit(2000)
    

    if(len(argv) != 4):
        print("Wrong number of arguments. Use correct syntax:\n")
        syntax_message()
    
    method=str(argv[1])
    print("method imported was:",method)
    if method not in ['depth','breadth','best','astar']:
        print("Wrong method. Use correct syntax:\n")
        syntax_message()
        return 
    
    if(scriptmode):
        #inputs=returnInputs(argv[2])
        if(not inputs.values):
            print("input error")
            return
    
    print("Solving "+argv[2]+" using "+argv[1]+'...\n')
    
    t1=datetime.datetime.now()
    
    initialize_search(method)
    
    solution_node=search(method)
    
    t2=datetime.datetime.now()
    
    if(solution_node):
        SOLUTION=extract_solution(solution_node)
        if(solution_node.g>0):
            print("Solution found! "+solution_node.g+"steps \n")
            print("Time spent ???????")
            write_solution_to_file(argv[3], SOLUTION)
    else:
        print("No solution found.\n")
    
    
    
    
    return
    
    
if __name__ == "__main__":
    main(ARGV)

      


