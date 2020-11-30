"""
CS 4613 - AI Project 2
Authors: Tatyana Graesser (tg1625), Helen Xu (hjx201)
"""

width = 9
height = 9

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

def backtrack(csp, assignment):
    print("Backtracking")


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


def main():  
    filepath = ""
    while True:
        filepath = input("Enter filepath for input file. Enter EXIT to end code: ")
        if filepath == "EXIT":
            print("Goodbye :)")
            break
        try:   
            root = createStates(filepath) #read in initial and goal states from starting node
        except:
            print("Incorrect filepath")
        else:
            printOutput(root)

    
if __name__ == "__main__":
    main()
