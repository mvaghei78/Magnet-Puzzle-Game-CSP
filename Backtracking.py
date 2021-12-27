from MagnetPuzzle import MagnetPuzzle
from CheckConsistency import CheckConsistency
import numpy as np
import copy
from Timer import Timer
from Heuristics import Heuristics
class Backtrack:
    def __init__(self, input_path):
        self.x = 0
        self.magnet_puzzle = MagnetPuzzle(input_path)
        self.heuristics = Heuristics(self.magnet_puzzle)
        self.check_consistency = CheckConsistency(self.magnet_puzzle)
        Pieces = np.full((self.magnet_puzzle.NumberOfRows, self.magnet_puzzle.NumberOfColumns), None)
        assignment = np.zeros(shape=(self.magnet_puzzle.NumberOfRows, self.magnet_puzzle.NumberOfColumns, 3), dtype=np.int)
        for i in range(self.magnet_puzzle.NumberOfRows):
            for j in range(self.magnet_puzzle.NumberOfColumns):
                Pieces[i][j] = None
                assignment[i][j][0] = 1
                assignment[i][j][1] = -1
                assignment[i][j][2] = 0
        Pieces = Pieces.tolist()
        assignment = assignment.tolist()
        # print(self.magnet_puzzle.get_all_pairs())
        result = self.solve(Pieces, assignment)
        if result:
            self.magnet_puzzle.print_magnet_puzzle(result[1])
        else:
            print("magnet puzzle with this information has no answer.")


    def solve2(self, table, assignment):
        self.x += 1
        print(self.x)
        if self.magnet_puzzle.is_goal(table):
            return True, table
        row, col = self.heuristics.mrv_heuristic(table, assignment)
        if row != None:
            pair = self.magnet_puzzle.get_pair(row, col)
            ordered_domain = self.heuristics.lcv_heuristic(assignment, row, col)
            for num in ordered_domain:
                copy_table = copy.deepcopy(table)
                copy_assignment = copy.deepcopy(assignment)
                if self.magnet_puzzle.is_consistent(table, row, col, num):
                    table[row][col] = num
                    table[pair[0]][pair[1]] = num*-1
                    if num in assignment[row][col]:
                        assignment[row][col].remove(num)
                    flag = self.check_consistency.forward_checking(table, assignment, row, col, num)
                    if flag:
                        result = self.solve2(table, assignment)
                    else:
                        return False
                    if result:
                        return result
                table = copy_table
                assignment = copy_assignment
            return False
    # backtracking algorithm
    def solve(self, table, assignment):
        self.x += 1
        print(self.x)
        # print(start_row, start_column)
        if self.magnet_puzzle.is_goal(table):
            return True, table
        row, col = self.heuristics.mrv_heuristic(table, assignment)
        if row != None:
            pair = self.magnet_puzzle.get_pair(row, col)
            for num in [1, -1, 0]:
                copy_table = copy.deepcopy(table)
                copy_assignment = copy.deepcopy(assignment)
                if self.magnet_puzzle.is_consistent(table, row, col, num):
                    table[row][col] = num
                    table[pair[0]][pair[1]] = num*-1
                    if num in assignment[row][col]:
                        assignment[row][col].remove(num)
                    flag = self.check_consistency.forward_checking(table, assignment, row, col, num)
                    # self.magnet_puzzle.print_magnet_puzzle(table)
                    if flag:
                        result = self.solve(table, assignment)
                    else:
                        return False
                    if result:
                        return result
                table = copy_table
                assignment = copy_assignment
            # self.print_magnet_puzzle(table)
            # print(row, col, assignment)
            return False
        # else:
        #     return False


if __name__ == "__main__":
    timer = Timer()
    file_path = "D:/Dars/term9/AI/project/PROJECT3/Magnet-Puzzle-Game-CSP/InputFiles/input3_method2.txt"
    bt = Backtrack(file_path)
    ended = timer.endTimer()
    print(ended)