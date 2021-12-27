from MapReader import MapReader
import copy

class MagnetPuzzle:
    def __init__(self, input_path):
        self.NumberOfRows, self.NumberOfColumns, self.PositivePoleEachRow, \
        self.NegativePoleEachRow, self.PositivePoleEachColumn, self.NegativePoleEachColumn, \
        self.pairs = MapReader(input_path).read_map()

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
    def get_all_pairs(self):
        self.all_pairs = set()
        for i in range(self.NumberOfRows):
            for j in range(self.NumberOfColumns):
                self.all_pairs.add(((i, j), self.get_pair(i, j)))
        all_pairs_copy = copy.deepcopy(self.all_pairs)
        for pairs in all_pairs_copy:
            if pairs in self.all_pairs and (pairs[1], pairs[0]) in self.all_pairs:
                self.all_pairs.remove((pairs[1], pairs[0]))
        return self.all_pairs
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
