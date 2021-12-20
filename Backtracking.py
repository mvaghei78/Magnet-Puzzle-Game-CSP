from MapReader import MapReader
import numpy as np
import copy
from Timer import Timer
import sys
class Backtrack:
    def __init__(self, input_path):
        self.x = 0
        self.NumberOfRows, self.NumberOfColumns, self.PositivePoleEachRow, \
        self.NegativePoleEachRow, self.PositivePoleEachColumn, self.NegativePoleEachColumn, \
        self.pairs = MapReader(input_path).read_map()
        Pieces = np.full((self.NumberOfRows, self.NumberOfColumns), None)
        assignment = np.zeros(shape=(self.NumberOfRows, self.NumberOfColumns, 3), dtype=np.int)
        for i in range(self.NumberOfRows):
            for j in range(self.NumberOfColumns):
                Pieces[i][j] = None
                assignment[i][j][0] = 1
                assignment[i][j][1] = -1
                assignment[i][j][2] = 0
        Pieces = Pieces.tolist()
        assignment = assignment.tolist()
        result = self.solve(Pieces, assignment)
        if result:
            self.print_magnet_puzzle(result[1])
        else:
            print("magnet puzzle with this information has no answer.")

    # input:
    # table -> all values for  each piece
    # assignment -> number of values that remained for each piece
    # output:
    # row and column of selected piece via MRV Heuristic
    def mrv_heuristic(self, table, assignment):
        self.x += 1
        mrv_row = None
        mrv_col = None
        for y, row in enumerate(assignment):
            for x, item in enumerate(row):
                if (mrv_row == None or len(item) < len(assignment[mrv_row][mrv_col])) and (table[y][x] == None and len(item) > 0):
                    mrv_col = x
                    mrv_row = y
        return mrv_row, mrv_col
    def lcv_heuristic(self, assignment, row_index, column_index):
        ordered_domain = [0]
        pair = self.get_pair(row_index, column_index)
        neighbors = self.get_neighbors(row_index, column_index)
        pair_neighbors = self.get_neighbors(pair[0], pair[1])
        count_1 = 0
        count_minus_1 = 0
        for n in neighbors:
            if not (n[0] == pair[0] and n[1] == pair[1]):
                if 1 in assignment[n[0]][n[1]]:
                    count_1 += 1
                if -1 in assignment[n[0]][n[1]]:
                    count_minus_1 += 1
        for n in pair_neighbors:
            if not (n[0] == row_index and n[1] == column_index):
                if -1 in assignment[n[0]][n[1]]:
                    count_1 += 1
                if 1 in assignment[n[0]][n[1]]:
                    count_minus_1 += 1
        if count_1 <= count_minus_1:
            ordered_domain.extend([1, -1])
        else:
            ordered_domain.extend([-1, 1])
        return ordered_domain


    def forward_checking(self, table, assignment, row_index, col_index, new_value):
        neighbors = self.get_neighbors(row_index, col_index)
        pair = self.get_pair(row_index, col_index)
        pair_neighbors = self.get_neighbors(pair[0], pair[1])
        for neighbor_pos in neighbors:
            if not(neighbor_pos[0] == pair[0] and neighbor_pos[1] == pair[1]) and new_value in assignment[neighbor_pos[0]][neighbor_pos[1]]:
                assignment[neighbor_pos[0]][neighbor_pos[1]].remove(new_value)
                if len(assignment[neighbor_pos[0]][neighbor_pos[1]]) == 0 and table[neighbor_pos[0]][neighbor_pos[1]] == None:
                    return False

        for neighbor_pos in pair_neighbors:
            if not(neighbor_pos[0] == row_index and neighbor_pos[1] == col_index) and new_value in assignment[neighbor_pos[0]][neighbor_pos[1]]:
                assignment[neighbor_pos[0]][neighbor_pos[1]].remove(new_value)
                if len(assignment[neighbor_pos[0]][neighbor_pos[1]]) == 0 and table[neighbor_pos[0]][neighbor_pos[1]] == None:
                    return False
        return True

    # input:
    # row_index -> row_index of piece that we want to find it's pair
    # column_index -> column_index of piece that we want to find it's pair
    # output:
    # row_index and column_index of piece that is pair of input piece
    def get_pair(self, row_index, column_index):
        # up , left , down, right
        if row_index != 0:
            # up
            if self.pairs[row_index-1][column_index] == self.pairs[row_index][column_index]:
                return row_index-1, column_index

        if column_index != 0:
            # left
            if self.pairs[row_index][column_index-1] == self.pairs[row_index][column_index]:
                return row_index, column_index-1

        if row_index != self.NumberOfRows-1:
            # down
            if self.pairs[row_index+1][column_index] == self.pairs[row_index][column_index]:
                return row_index+1, column_index

        if column_index != self.NumberOfColumns:
            # right
            if self.pairs[row_index][column_index + 1] == self.pairs[row_index][column_index]:
                return row_index, column_index + 1

    # input:
    # table , table, row_index, column_index
    # new_value: new value for selected piece
    # output:
    # check that neighbors don't have it's value and when we put this value the number of positive and negative poles
    # in each row and column don't become grather than specified value
    def is_consistent_for_one_piece(self, table, row_index, column_index, new_value):
        neighbors = self.get_neighbors(row_index, column_index)
        pair = self.get_pair(row_index, column_index)
        for neighbor_position in neighbors:
            if table[neighbor_position[0]][neighbor_position[1]] == new_value and new_value != 0:
                if not (neighbor_position[0] == pair[0] and neighbor_position[1] == pair[1]):
                    return False

        number_of_positives = 0
        number_of_negatives = 0
        if new_value == 1:
            number_of_positives += 1
        if number_of_negatives == -1:
            number_of_negatives += 1
        for i in range(self.NumberOfColumns):
            if i != column_index and table[row_index][i] == 1:
                number_of_positives += 1
            if i != column_index and table[row_index][i] == -1:
                number_of_negatives += 1
        if number_of_positives > self.PositivePoleEachRow[row_index] or number_of_negatives > self.NegativePoleEachRow[row_index]:
            return False

        number_of_positives = 0
        number_of_negatives = 0
        if new_value == 1:
            number_of_positives += 1
        if number_of_negatives == -1:
            number_of_negatives += 1
        for i in range(self.NumberOfRows):
            if i != row_index and table[i][column_index] == 1:
                number_of_positives += 1
            if i != row_index and table[i][column_index] == -1:
                number_of_negatives += 1
        if number_of_positives > self.PositivePoleEachColumn[column_index] or number_of_negatives > self.NegativePoleEachColumn[column_index]:
            return False
        return True

    # input:
    # table, row_index, column_index, new_value
    # output:
    # check consistency for selected piece and it's neighbor. for selected piece check new_value and for its pair
    # check new_value*-1
    def is_consistent(self, table, row_index, column_index, new_value):
        if self.is_consistent_for_one_piece(table, row_index, column_index, new_value) and self.is_consistent_for_one_piece(table, row_index, column_index, new_value):
            return True
        else:
            return False

    # input:
    # row_index, column_index
    # output:
    # get all neighbors of selected piece
    def get_neighbors(self, row_index, column_index):
        neighbors = []
        if row_index != 0:
            neighbors.append([row_index-1, column_index])
        if column_index != 0:
            neighbors.append([row_index, column_index-1])
        if row_index != self.NumberOfRows-1:
            neighbors.append([row_index+1, column_index])
        if column_index != self.NumberOfColumns-1:
            neighbors.append([row_index, column_index+1])
        return neighbors
    def solve2(self, table, assignment):
        self.x += 1
        print(self.x)
        if self.is_goal(table):
            return True, table
        row, col = self.mrv_heuristic(table, assignment)
        if row != None:
            pair = self.get_pair(row, col)
            ordered_domain = self.lcv_heuristic(assignment, row, col)
            for num in ordered_domain:
                copy_table = copy.deepcopy(table)
                copy_assignment = copy.deepcopy(assignment)
                if self.is_consistent(table, row, col, num):
                    table[row][col] = num
                    table[pair[0]][pair[1]] = num*-1
                    if num in assignment[row][col]:
                        assignment[row][col].remove(num)
                    flag = self.forward_checking(table, assignment, row, col, num)
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
        if self.is_goal(table):
            return True, table
        row, col = self.mrv_heuristic(table, assignment)
        if row != None:
            pair = self.get_pair(row, col)
            for num in [1, -1, 0]:
                copy_table = copy.deepcopy(table)
                copy_assignment = copy.deepcopy(assignment)
                if self.is_consistent(table, row, col, num):
                    table[row][col] = num
                    table[pair[0]][pair[1]] = num*-1
                    if num in assignment[row][col]:
                        assignment[row][col].remove(num)
                    flag = self.forward_checking(table, assignment, row, col, num)
                    # self.print_magnet_puzzle(table)
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

    def is_goal(self, table):
        for i in range(self.NumberOfRows):
            number_of_positives = 0
            number_of_negatives = 0
            for j in range(self.NumberOfColumns):
                if table[i][j] == 1:
                    number_of_positives += 1
                if table[i][j] == -1:
                    number_of_negatives += 1
            if number_of_positives != self.PositivePoleEachRow[i] or number_of_negatives != self.NegativePoleEachRow[i]:
                return False
        for i in range(self.NumberOfColumns):
            number_of_positives = 0
            number_of_negatives = 0
            for j in range(self.NumberOfRows):
                if table[j][i] == 1:
                    number_of_positives += 1
                if table[j][i] == -1:
                    number_of_negatives += 1
            if number_of_positives != self.PositivePoleEachColumn[i] or number_of_negatives != self.NegativePoleEachColumn[i]:
                return False
        return True
    def count_of_pos_neg(self, table, row_index, column_index):
        num_of_pos_in_row = 0
        number_of_neg_in_row = 0
        num_of_pos_in_column = 0
        number_of_neg_in_column = 0
        row_data = table[row_index]
        for i in row_data:
            if i == 1:
                num_of_pos_in_row += 1
            if i == -1:
                number_of_neg_in_row += 1
        column_data = table[:][column_index]
        for i in column_data:
            if i == 1:
                num_of_pos_in_column += 1
            if i == -1:
                number_of_neg_in_column += 1
        return num_of_pos_in_row, number_of_neg_in_row, num_of_pos_in_column, number_of_neg_in_column
    def print_magnet_puzzle(self, table):
        x = self.PositivePoleEachColumn.tolist()
        y = self.NegativePoleEachColumn.tolist()
        print("+  ", *x)
        print("  -", *y)
        for i in range(self.NumberOfRows):
            str1 = ""
            for j in range(self.NumberOfColumns):
                if table[i][j] == 1:
                    str1 += "+ "
                elif table[i][j] == -1:
                    str1 += "- "
                else:
                    str1 += "0 "
            print(self.PositivePoleEachRow[i], self.NegativePoleEachRow[i], str1)

if __name__ == "__main__":
    timer = Timer()
    file_path = "D:/Dars/term9/AI/project/PROJECT3/Magnet-Puzzle-Game-CSP/InputFiles/input1_method2.txt"
    bt = Backtrack(file_path)
    ended = timer.endTimer()
    print(ended)