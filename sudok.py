"""
CS 4613 - AI Project 2
Authors: Tatyana Graesser (tg1625), Helen Xu (hjx201)
"""

#globals
width = 9
height = 9

import random

domains = [[[] for j in range(width)] for i in range(height)] #create data structure for domains. it is a 3d array also this was the only way to do it w/o pythons weird pointer system being weird
assignment = [[0 for j in range(width)] for i in range(height)]


#all of backtracking is done in here cuz python globals are stoopid
class CSP:
  def __init__(self, domain, assignment):
    self.domain = domain
    self.assignment = assignment
    self.isSolved = False
    
  def findSolution(self):
    #check if assignment complettt
    if self.isComplete(): 
      return self.assignment

    currVar = self.getNext() #get next variable
    
    for val in self.domain[currVar[0]][currVar[1]]:#for each value in that domain; don't need to sort domain values as they are already sorted
      if(self.isConsistent(currVar[0], currVar[1], val)): #check consistency w/ assignment
        self.assignment[currVar[0]][currVar[1]] = val #assign variable
        self.findSolution() #result = backtrack(csp, assignment)

    if(not self.isComplete()):
      self.assignment[currVar[0]][currVar[1]] = 0  #remove var=value from assignment if there is a failure but also don't do it if a solution has been found

    return self.assignment

  #check for completed assignment
  def isComplete(self):
    if(self.isSolved):
      return True
      
    for rowi in range(height):
      for coli in range(width):
        if(self.assignment[rowi][coli] == 0):
          return False
          
    self.isSolved = True
    return True
    
  def getUnassignedVars(self):
    unassigned = []
    
    for rowi in range(height):
      for colj in range(width):
        if(self.assignment[rowi][colj] == 0):
          unassigned.append((rowi, colj))

    return unassigned
    
  def isConsistent(self, row, col, num):
    neighbors = getNeighbors(row, col)
    
    for rowi, colj in neighbors:
        if(self.assignment[rowi][colj] == num):
          return False
    return True

  def getDegree(self, row, col): #check #of unassigned neighbors
    degree = 0
    neighbors = getNeighbors(row, col)
    
    for row, col in neighbors:
      if(self.assignment[row][col] == 0):
        degree += 1

    return degree

  def getNext(self):
    #use minimum remaining value and then degree to find next node to try

    unassigned = self.getUnassignedVars() #first get a list of the unassigned variables
    MRVs = {} #get minimum remaining vals of all unassinged vars
    
    for row, col in unassigned:
      rv = len(self.domain[row][col])
      if rv in MRVs:
        MRVs[rv].append((row, col))
      else:
        MRVs[rv] = [(row, col)]
        
    mrv =  min(MRVs.keys())
        
    if(len(MRVs[mrv]) == 1):  #return tuple coords of next var
      return MRVs[mrv][0]
    else: # if there is a tie, calculate degree
      unassigned2 = MRVs[mrv]
      degrees = {}
      
      for row, col in unassigned2:
        deg = self.getDegree(row, col)
        
        if deg in degrees:
          degrees[deg].append((row, col))
        else:
          degrees[deg] = [(row, col)]
          
      maxdeg = max(degrees.keys())
      
      return degrees[maxdeg][0] #if there is yet another tie, just pick the first one idk


def createStates(filepath): #create 2D matrices for initial state and goal state from file
  state = [[]] #initial state matrix
  with open(filepath, 'r') as fp:
    char = '' #keeping track of number
    row = 0 #keeping track of matrix row
    for c in fp.read():
      if c.isnumeric():
        char += c
      elif c == ' ':
        state[row].append(int(char))
        char = ''
      elif c == '\n':
        if (char != ''): #add any found numbers 
          state[row].append(int(char))
          char = ''
        row += 1 #move to a new row 
        state.append([ ])
    if char != '':
      state[row].append(int(char)) #getting last character we may have missed
  #cleaning up any extra rows, probably a better way of making sure we just don't have to do this
  # initialS = initialS[:3]
  return state

def printOutput(initial): #print final output to file
    printed = False
    while not printed:
      filepath = input("Enter output file name: ")
      try:
        with open(filepath, "w") as fp:
          #printing out initial state
          for row in initial:
            for char in row:
              fp.write(str(char) + " ")
            fp.write("\n")
          fp.write("\n")
      except:
        print("An error occurred, please try again")
      else:
        print("Output printed to", filepath)
        printed = True

#gets list of neighbors for a cell
def getNeighbors(row, col):
  neighbors = []

  for rowi in range(height): #row
    if(rowi != row and (rowi, col) not in neighbors): 
      neighbors.append((rowi, col))

  for coli in range(width): #column
    if(coli != col and (row, coli) not in neighbors):
      neighbors.append((row, coli))
    
  for rowi in range(row//3*3, row//3*3+3):  #square
    for coli in range(col//3*3, col//3*3+3):
      if(coli != col or rowi != row and (rowi, coli) not in neighbors):
        neighbors.append((rowi, coli))

  if(row%4 != 0 and col%4 != 0):  #hyper square
    leftbound = (row-row//3)//3*4 + 1 # weird maths to get upper left corner of square
    upbound = (col-col//3)//3*4 + 1
    
    for rowi in range(leftbound, leftbound+3):  
      for coli in range(upbound, upbound+3):
        if(coli != col or rowi != row and (rowi, coli) not in neighbors):
          neighbors.append((rowi, coli))
  
  return neighbors

# methods used for forward checking
def initCSP(root): #initialize domain of problem using forward checking  
  for rowi in range(height):
    for colj in range(width):
      domains[rowi][colj] = [1, 2, 3, 4, 5, 6, 7, 8, 9].copy()

  for rowi in range(height):
    for colj in range(width):
      if (root[rowi][colj] != 0):
        domains[rowi][colj] = [ int(root[rowi][colj])].copy()
        assignment[rowi][colj] = int(root[rowi][colj])
        forwardCheck(rowi, colj)
        #print(domains)

  return domains, assignment

'''
def forwardCheck(row, col, num): #check its constraining buddies
#do column buddies first
  for rowi in range(height): 
    if(rowi != row):  #do not remove the value ur checking for
      removeDomainVal(rowi, col, num)
  
#then row buddies
  for coli in range(width):  
    if(coli != col):
      removeDomainVal(row, coli, num)

  #print("Checking outer square") #then outer square buddies
  for rowi in range(row//3*3, row//3*3+3):  
    for coli in range(col//3*3, col//3*3+3):
      if(coli != col or rowi != row):
        removeDomainVal(rowi, coli, num)
  
  #print("Checking inner square") #then inner square buddies
  if(row%4 != 0 and col%4 != 0):
    leftbound = (row-row//3)//3*4 + 1 # weird maths to get upper left corner of square
    upbound = (col-col//3)//3*4 + 1
    
    for rowi in range(leftbound, leftbound+3):  
      for coli in range(upbound, upbound+3):
        if(coli != col or rowi != row):
          removeDomainVal(rowi, coli, num)
'''

def forwardCheck(row, col):
  num = domains[row][col][0]
  neighbors = getNeighbors(row, col)
  
  for cell in neighbors:
    removeDomainValFC(cell[0], cell[1], num)

#remove value from domain, forward checking ver.
def removeDomainValFC(row, col, num):
    #print("removing value in (" + str(row) + ", " + str(col) + ")")
    if (num in domains[row][col]):
      domains[row][col].remove(num)
      
    if (len(domains[row][col]) == 0): #check for empty domain
      print("Empty domain at (" + str(row) + ", " + str(col) + "). Puzzle has no solution")
      exit(0)
 
def main():  

  root = None  
  solution = None
  
  filepath = ""
  while True:
    filepath = input("Enter filepath for input file. Enter EXIT to end code: ")
    if filepath == "EXIT":
      print("Goodbye :)")
      exit(0)
    try:   
      root = createStates(filepath) #read in initial and goal states from starting node
    except:
      print("Incorrect filepath")
    else:
      #printOutput(root)
      csp = None
      
      domains = [[[] for j in range(width)] for i in range(height)] #create data structure for domains. it is a 3d array also this was the only way to do it w/o pythons weird pointer system being weird
      assignment = [[0 for j in range(width)] for i in range(height)]
      domains, assignment = initCSP(root)
      print(domains)
      print(assignment)
      
      csp = CSP(domains, assignment)
      
      solution = csp.findSolution()
      
      print(solution)
      printOutput(solution)
  
if __name__ == "__main__":
  main()
