#<=============================== Imports ===================================>#
import sys
import queue
import operator
import numpy as np
from os import system
from time import time 
from datetime import datetime

#<========================= Puzzle Class Definition =========================>#
class Puzzle:

    # One can pass in an explicit grid as a list of lists (or matrix) OR a grid size. Second option will randomly generate grid.
    def __init__(self, size_grid=None, grid=None, test_type='') -> None:
        
        self.file_name = 'nodePath_'+ test_type + '.txt'

        # If explicit grid is given...  
        if grid is not None:
            # Cast grid as np.array and define size
            self.grid = np.asarray(grid, dtype=np.uint8)
            self.size_grid = self.grid.shape[0]
        else:
            # If a size is give, randomly generate a grid of that size
            self.size_grid = size_grid
            nums = list(range(0, size_grid**2))
            self.grid = np.zeros((size_grid, size_grid), dtype=np.uint8)
            for row in range(size_grid):
                for col in range(size_grid):
                    num = np.random.choice(nums)
                    nums.remove(num)
                    self.grid[row, col] = num

        self.depth_counter = 0                                                  # Counts depth of BFS
        self.orig_parent = Puzzle.grid2str(self.grid)                           # Define the original parent node as string
        self.state_dict = {self.orig_parent: {"count": self.depth_counter}}     # Define dictionary of all states. All other keys
                                                                                # will contain parent node and depth
        self.current_set = queue.Queue()                                        # Queue of states to inspect 
        self.current_set.put_nowait(self.orig_parent)

        # Generate a string representation of the winning state
        winning_state = list(range(1,self.size_grid**2))
        winning_state.append(0)
        self.winning_state = Puzzle.list2str(winning_state, sep=" ")

    # Static method for converting a list to its corresponding string representation
    @staticmethod
    def list2str(list_, sep=""):
        str_ = ""
        add_sep = False
        for val in list_:
            if not add_sep:
                str_ += str(val)
                add_sep = True
            else:
                str_ += sep + str(val)
        return str_

    # Static method for converting grid into its corresponding string reprentation
    @staticmethod
    def grid2str(grid_):
        return Puzzle.list2str(grid_.flatten(), sep=" ")

    # Method for converting string representation back into grid
    def str2grid(self, str_):
        nums = np.asarray([int(s) for s in str_.split(' ')], dtype=np.uint8)
        return nums.reshape((self.size_grid, self.size_grid))

    # Write information to file
    def write_str_to_file(self, string, start='', end='\n', overwrite=False):
        write_type = None
        if overwrite:
            write_type = 'w'
        else:
            write_type = 'a'
        with open(self.file_name, write_type) as writer:
            writer.write(start + str(string) + end)

    # Utility method for printing out grid
    def print(self, grid_str=None, to_file=True):
        grid = []
        if grid_str == None:
            grid = self.grid
        else:
            grid = self.str2grid(grid_str)

        # Print grid to file
        if to_file:
            for row in grid:
                for col in row:
                    end = None
                    if len(str(col)) > 1:
                        start = ''
                    else:
                        start = ' '
                    self.write_str_to_file(col, start=start, end='  ')
                self.write_str_to_file("")
            self.write_str_to_file("")
            
        # Print grid to terminal
        else:
            for row in grid:
                for col in row:
                    print(col, end="  ")
                print("")

    # Switches string elements to create new state
    def switch_elements_in_str(self, str_, pos1, pos2):
        arr = str_.split(' ')
        str1_index = self.size_grid*pos1[0] + pos1[1]
        str2_index = self.size_grid*pos2[0] + pos2[1]
        temp = arr[str1_index]
        arr[str1_index] = arr[str2_index]
        arr[str2_index] = temp
        return Puzzle.list2str(arr, sep=" ")

    # Gets next branch in the given direction
    def get_next_branch(self, parent, zero_pos, from_dir):
        # Get the new position using tuple addition
        pos = tuple(map(operator.add, zero_pos, (from_dir)))

        # Check if move is legal and generate that new state
        if (pos[0] < self.size_grid and pos[1] < self.size_grid and pos[0] > -1 and pos[1] > -1):
            mat_str = self.switch_elements_in_str(parent, pos, zero_pos)
            
            # If that corresponds to the winning state, return True
            if mat_str == self.winning_state:
                self.state_dict[mat_str] = {"parent": parent, "count": self.depth_counter}
                return True
            
            # Check if the current state is defined.
            if self.state_dict.get(mat_str) == None:
                # If not, add it to the dictionary along with its parent, count info then add it to queue
                self.state_dict[mat_str] = {"parent": parent, "count": self.depth_counter}
                self.current_set.put_nowait(mat_str)
        return False

    # Check all directions for a given 0 position
    def fill_void(self, parent):
        # Calculate 0 pos
        zero_pos_str = parent.split(" ").index('0')
        zero_pos = (zero_pos_str//self.size_grid, zero_pos_str%self.size_grid)

        # Check all directions
        down = self.get_next_branch(parent, zero_pos, (1, 0))
        up = self.get_next_branch(parent, zero_pos, (-1, 0))
        right = self.get_next_branch(parent, zero_pos, (0, 1))
        left = self.get_next_branch(parent, zero_pos, (0, -1))

        # If any of these are true, we have reached the goal state. Propogate the true to the next level
        if down or up or right or left:
            return True
        return False
    
    # Search the current current queue and generate all depth levels
    def find_path(self):
        self.solution_found = False
        try:
            while True:
                self.depth_counter += 1
                if self.current_set.empty():
                    break
                parent = self.current_set.get_nowait()
                if self.fill_void(parent):
                    self.solution_found = True
                    break
            
            if self.solution_found:
                # Go up the tree to find all parent nodes and optimized path
                next_set = self.state_dict[self.winning_state]
                path = [self.winning_state]
                try:
                    while True:
                        next_set_ind = next_set['parent']
                        next_set = self.state_dict[next_set_ind]
                        path.append(next_set_ind)
                except KeyError:
                    pass

                # Print full move set
                path.reverse()
                self.path = path
                
        except KeyboardInterrupt:
            print("Keyboard Interrupt")

# Runs algorithm and prints results to terminal and screen   
def run_case(case, overwrite=False, custom=None, disp_file=True):
    puzzle = None

    # Custom puzzle
    if custom != None:
        puzzle = Puzzle(grid=custom, test_type='custom')                                                            # This method takes in a puzzle directly and solves
        print("--------------------------- Custom Case ---------------------------")
        puzzle.write_str_to_file("--------------------------- Custom Case ---------------------------", overwrite=overwrite)

    # Random Puzzle
    elif len(case) > 1:
        case = case[-1]
        puzzle = Puzzle(size_grid=int(case), test_type='random')                                                     # This method takes in a puzzle size and randomly generates a puzzle
        print("--------------------------- Random Case "+case+"x"+case+" ---------------------------")
        puzzle.write_str_to_file("--------------------------- Random Case "+case+"x"+case+" ---------------------------", overwrite=overwrite)

    # Pre-determined test cases
    else:
        test_case = {'1': [[1, 2, 3, 4],[ 5, 6, 0, 8], [9, 10, 7, 12], [13, 14, 11, 15]],
                     '2': [[1, 0, 3, 4],[ 5, 2, 7, 8], [9, 6, 10, 11], [13, 14, 15, 12]],
                     '3': [[0, 2, 3, 4],[ 1, 5, 7, 8], [9, 6, 11, 12], [13, 10, 14, 15]],
                     '4': [[5, 1, 2, 3],[ 0, 6, 7, 4], [9, 10, 11, 8], [13, 14, 15, 12]],
                     '5': [[1, 6, 2, 3],[ 9, 5, 7, 4], [0, 10, 11, 8], [13, 14, 15, 12]]}

        puzzle = Puzzle(grid=test_case[case], test_type='test_cases')                                                     
        print("\n--------------------------- Test Case "+case+" ---------------------------")
        puzzle.write_str_to_file("--------------------------- Test Case "+case+" ---------------------------", overwrite=overwrite)
    
    puzzle.print()
    print("")

    start_time = time()                                                                         # Time the BFS algorithm

    # Run Algorithm
    puzzle.find_path()                                                                          
    
    # Calculate time
    time_elapsed_s = time() - start_time
    time_elapsed_mins = time_elapsed_s//60
    time_elapsed_hrs = time_elapsed_s//60**2
    time_elapsed_secs = time_elapsed_s%60

    # Write info to file. 
    # Solution found
    if puzzle.solution_found:
        for string in puzzle.path:
            puzzle.write_str_to_file(string)

        puzzle.write_str_to_file(f"\nThis puzzle can be solved in {len(puzzle.path)-1} operations")

        print(f"All contents written to file ./{puzzle.file_name}")
        print(f"This puzzle can be solved in {len(puzzle.path)-1} operations")
    # No solution detected
    else:
        print("No solutions to current puzzle. Please select another puzzle.")
        puzzle.write_str_to_file("No solutions to current puzzle. Please select another puzzle.")

    puzzle.write_str_to_file(f"The BFS algorithm took {time_elapsed_hrs} hrs, {time_elapsed_mins} mins, and {time_elapsed_secs} s to implement", end='\n\n\n')
    print(f"The BFS algorithm took {time_elapsed_hrs} hrs, {time_elapsed_mins} mins, and {time_elapsed_secs} s to implement")

    if disp_file:
        system(puzzle.file_name)

#<========================= Main =========================>#
if __name__ == '__main__':
    # system('cls')

    # Command line parsing
    
    # Run all 5 given cases
    if len(sys.argv) == 1:
        overwrite = True
        for case in range(1,5):
            if overwrite:
                run_case(str(case), overwrite=True, disp_file=False)
                overwrite = False
            else:
                run_case(str(case), disp_file=False)
        run_case('5')

    # Run custom grid
    elif sys.argv[1] == 'custom':
        custom_list = [[1, 2, 3, 4],[ 5, 6, 0, 8], [9, 10, 7, 12], [13, 14, 11, 15]]
        run_case(None, custom=custom_list, overwrite=True)

    # Run individual case
    elif len(sys.argv) == 2:
        case = sys.argv[1]
        run_case(case, overwrite=True)
        
    # Run random grid
    elif len(sys.argv) == 3:
        case = sys.argv[1] + sys.argv[2]
        run_case(case, overwrite=True)