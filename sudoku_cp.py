import copy
default_domain = [1,2,3,4,5,6,7,8,9]
import time 
class board():
    """
    This class is what I have used to handle the sudoku arrays.
    It packs some features which allows me to use contraint propagation and
    domain reduction to solve the puzzle
    """

    def __init__(self,board_array):
        self.board_array = board_array
        self.cs_board = self.create_box_board(self.board_array) # This is a list of box objects.Scroll down to learn the
                                                                # function of box objects

    def create_box_board(self,array):
        """
        This class method is used to create self.cs_board which is made up of box objects
        """
        box_array = [[box(val) for val in m_row] for m_row in array]
        
        for index,row in enumerate(box_array):
            sub_grid_pos = 1 + (index//3)*3
            for h_index,element in enumerate(row):
                element.pos = sub_grid_pos + h_index//3
                element.cordinates = (h_index,index)
                if element[0]!=0:
                    element.domain=[element[0]]
                
        return box_array

    def get_sub_grid(self,pos):
        """
        returns the elements in the called 3x3 grid of the sudoku board
        subgrids are arranged as follows

        1    2    3
        4    5    6
        7    8    9

        """
        return [element for row in self.cs_board for element in row if element.pos==pos ]

    def get_row(self,row):
        return copy.deepcopy(self.cs_board[row])    #returns a row of the sudoku board 

    def get_column(self,column):
        return [row[column] for row in self.cs_board] #returns a coloumn of the sudoku board

    def clean_domains(self,box):
        """
        This function performs domain redution for all box objects 
        in the same row,coloumn and sub grid as the input box.If there is
        a box whose domain reduces to one possible element the box will be assigned
        with that value.While reducing the domains this function also finds out the
        box object with the smallest domain.This allows us to speed up the search
        which is a normal depth first search.
        """

        min_constraints = None
        
        #domain reduction for boxes in the same sub_grid
        s_grid_num = box.pos
        sub_grid = self.get_sub_grid(s_grid_num)
        sub_grid.remove(box)
        for sub_element in sub_grid:
            box_cord = sub_element.cordinates
            
            try:
                if self.cs_board[box_cord[1]][box_cord[0]][0]==0:
                    #print("#m1")
                    self.cs_board[box_cord[1]][box_cord[0]].domain.remove(box[0])
                    if len(self.cs_board[box_cord[1]][box_cord[0]].domain)==1:
                        self.cs_board[box_cord[1]][box_cord[0]].fix_domain_value()
                        self.board_array[box_cord[1]][box_cord[0]] = self.cs_board[box_cord[1]][box_cord[0]].domain[0]
                    
                    elif min_constraints == None or \
                         len(self.cs_board[box_cord[1]][box_cord[0]].domain) < len(min_constraints.domain):
                        min_constraints = self.cs_board[box_cord[1]][box_cord[0]]
                            
            except ValueError:
                pass
                
        #domain reduction for box objects in the same row
        row_num = box.cordinates[1]
        row_elements = self.get_row(row_num)
        row_elements.remove(box)
        for row_element in row_elements:
            box_cord = row_element.cordinates
            try:
                if self.cs_board[box_cord[1]][box_cord[0]][0]==0:
                    #print("#m2")
                    self.cs_board[box_cord[1]][box_cord[0]].domain.remove(box[0])
                    if len(self.cs_board[box_cord[1]][box_cord[0]].domain)==1:
                        self.cs_board[box_cord[1]][box_cord[0]].fix_domain_value()
                        self.board_array[box_cord[1]][box_cord[0]] = self.cs_board[box_cord[1]][box_cord[0]].domain[0]
     
                    elif min_constraints == None or \
                         len(self.cs_board[box_cord[1]][box_cord[0]].domain) < len(min_constraints.domain):
                        min_constraints = self.cs_board[box_cord[1]][box_cord[0]]
                        
            except ValueError:
                pass

        
        #domain reduction for box objects in the same coloumn
        col_num = box.cordinates[0]
        col_elements = self.get_column(col_num)
        col_elements.remove(box)
        for col_element in col_elements:
            box_cord = col_element.cordinates
            try:
                if self.cs_board[box_cord[1]][box_cord[0]][0]==0:
                    #print("#m3")
                    self.cs_board[box_cord[1]][box_cord[0]].domain.remove(box[0])
                    if len(self.cs_board[box_cord[1]][box_cord[0]].domain)==1:
                        self.cs_board[box_cord[1]][box_cord[0]].fix_domain_value()
                        self.board_array[box_cord[1]][box_cord[0]] = self.cs_board[box_cord[1]][box_cord[0]].domain[0]

                    elif min_constraints == None or \
                         len(self.cs_board[box_cord[1]][box_cord[0]].domain) < len(min_constraints.domain):
                        min_constraints = self.cs_board[box_cord[1]][box_cord[0]]
                        
            except ValueError:
                pass

        return min_constraints

            
    def print(self):
        #prints out the board 
        for row in self.cs_board:
            print(row)

    def check_repetition(self,inList,inSet):
        #checks if the same muber is repeated in the same sub-grid,row or column
        return 0 if len(inList)!=len(inSet) else 1

    def check_valid(self):
        #checks is the board is a valid sudoku board with no repititions 
        for i in range(1,10):
            m_list = [e[0] for e in self.get_sub_grid(i) if e[0]!=0]
            if not self.check_repetition(m_list,set(m_list)):
                return 0
        for i in range(9):
            
            row_list = [e[0] for e in self.get_row(i) if e[0]!=0]
            if not self.check_repetition(row_list,set(row_list)):
                return 0
            
            col_list = [e[0] for e in self.get_column(i) if e[0]!=0]
            if not self.check_repetition(col_list,set(col_list)):
                return 0            
        return 1


    
class box(list):
    """
    box class inherit from the python list class.The important additions in this class,
    1)Each box object has its own domain
    2)Each box object has attributes containing its location on the sudoku board
    """
    def __init__(self,initial_value):
        super().__init__()
        self.append(initial_value)
        self.initial_value = initial_value
        self.domain = copy.deepcopy(default_domain)
        self.pos = None
        self.cordinates = None

    def fix_domain_value(self):
        self[0] = self.domain[0]
        

def solve_board(input_board):
    global count,backtrack
    count+=1
    #recursion part
    starting_box = None
    for row in input_board.cs_board:
        for element in row:
            if element[0] != 0:
                new_starting_box = input_board.clean_domains(element)
                if new_starting_box!=None and (starting_box == None or \
                   len(new_starting_box.domain) < len(starting_box.domain)) :
                    starting_box = new_starting_box
                    
    if starting_box != None:
        
        for value in starting_box.domain:
            new_array = copy.deepcopy(input_board.board_array)
            new_array[starting_box.cordinates[1]][starting_box.cordinates[0]] = value
            new_board_object = board(new_array)

            if new_board_object.check_valid():
                #new_board_object.print()
                #print("Attempted ",value," at ",starting_box.cordinates)
                solution = solve_board(new_board_object)
                if solution!=None:
                    return solution
                else:
                    backtrack+=1

    # This is the terminating step in the recursion.When the input_board
    # has no empty spaces(0's) recursion stops
    else:
        #print("004")       
        return input_board

def run(array):
    global count,backtrack
    start_time = time.time()
    count = 0
    backtrack=0
    test = board(array)
    solved_board = solve_board(test)
    print("\n\nProblem 3\nSolution is\n")
    solved_board.print()
    print("\nRecursions: ",count)
    print("Backtracking: ",backtrack)
    print("Elapsed Time: ",round(time.time()-start_time,3))
    

#The following were used in the debugging process
#test = board(input_array1)
#print(test.cs_board[0][3].pos)
#print(test.cs_board[3][8].pos)
#print(test.cs_board[0][8])
#print(test.get_sub_grid(5))
#print(test.get_row(2))
#print(test.cs_board[0][1].domain)
#test.reduce_domain(test.cs_board[0][0])
#print(test.cs_board[1][5].domain)
#print(test.cs_board)
#test.clean_domains(test.cs_board[8][6])


        
#These are the sample problems given to the program

input_array1 = [ [3, 0, 6, 5, 0, 8, 4, 0, 0], 
                 [5, 2, 0, 0, 0, 0, 0, 0, 0], 
                 [0, 8, 7, 0, 0, 0, 0, 3, 1], 
                 [0, 0, 3, 0, 1, 0, 0, 8, 0], 
                 [9, 0, 0, 8, 6, 3, 0, 0, 5], 
                 [0, 5, 0, 0, 9, 0, 6, 0, 0], 
                 [1, 3, 0, 0, 0, 0, 2, 5, 0], 
                 [0, 0, 0, 0, 0, 0, 0, 7, 4], 
                 [0, 0, 5, 2, 0, 6, 3, 0, 0] ]

input_array2 = [ [0, 0, 0, 0, 0, 5, 0, 8, 0],
                 [0, 7, 9, 0, 0, 0, 0, 0, 6],
                 [0, 0, 0, 0, 4, 0, 0, 9, 2],
                 [0, 3, 0, 6, 0, 0, 0, 0, 0],
                 [2, 0, 4, 0, 0, 0, 1, 0, 8],
                 [0, 0, 0, 0, 0, 1, 0, 4, 0],
                 [6, 2, 0, 0, 3, 0, 0, 0, 0],
                 [4, 0, 0, 0, 0, 0, 8, 7, 0],
                 [0, 8, 0, 1, 0, 0, 0, 0, 0] ]

input_array3 = [ [8, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 3, 6, 0, 0, 0, 0, 0],
                 [0, 7, 0, 0, 9, 0, 2, 0, 0],
                 [0, 5, 0, 0, 0, 7, 0, 0, 0],
                 [0, 0, 0, 0, 4, 5, 7, 0, 0],
                 [0, 0, 0, 1, 0, 0, 0, 3, 0],
                 [0, 0, 1, 0, 0, 0, 0, 6, 8],
                 [0, 0, 8, 5, 0, 0, 0, 1, 0],
                 [0, 9, 0, 0, 0, 0, 4, 0, 0] ]

input_array4 = [ [0, 0, 5, 3, 0, 0, 0, 0, 0],
                 [8, 0, 0, 0, 0, 0, 0, 2, 0],
                 [0, 7, 0, 0, 1, 0, 5, 0, 0],
                 [4, 0, 0, 0, 0, 5, 3, 0, 0],
                 [0, 1, 0, 0, 7, 0, 0, 0, 6],
                 [0, 0, 3, 2, 0, 0, 0, 8, 0],
                 [0, 6, 0, 5, 0, 0, 0, 0, 9],
                 [0, 0, 4, 0, 0, 0, 0, 3, 0],
                 [0, 0, 0, 0, 0, 9, 7, 0, 0] ]



#first problem, relatively easy
run(input_array1)

#second problem, hard
run(input_array2)

#third problem, very hard
run(input_array3)

#fourth problem, moderate
run(input_array4)
