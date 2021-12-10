from MapReader import MapReader
import numpy as np

class MagnetPuzzle:
    def __init__(self):
        self.NumberOfRows, self.NumberOfColumns, self.PositivePoleEachRow, \
        self.NegativePoleEachRow, self.PositivePoleEachColumn, self.NegativePoleEachColumn, \
        self.pairs = MapReader("D:/Dars/term9/AI/project/PROJECT3/Magnet-Puzzle-Game-CSP/InputFiles/input1_method2.txt").read_map()
        print(self.NumberOfRows, self.NumberOfColumns)
        print(self.PositivePoleEachRow)
        print(self.NegativePoleEachRow)
        print(self.PositivePoleEachColumn)
        print(self.NegativePoleEachColumn)
        print(self.pairs)
        self.poles_sign = np.zeros((self.NumberOfRows, self.NumberOfColumns))
        self.possible_values = np.empty((self.NumberOfRows, self.NumberOfColumns, 3))
        self.possible_values[:,:] = np.array([1, -1, 0])

    def number_of_rows_and_columns(self):
        return self.NumberOfRows, self.NumberOfColumns

    def number_of_positive_in_row(self, row_index):
        return self.PositivePoleEachRow[row_index]

    def number_of_negative_in_row(self, row_index):
        return self.NegativePoleEachRow[row_index]

    def number_of_positive_in_column(self, column_index):
        return self.PositivePoleEachColumn[column_index]

    def number_of_negative_in_column(self, column_index):
        return self.NegativePoleEachColumn[column_index]

    def is_consistent(self, row_index, column_index, pole_sign):
        pass
    def get_neighbors(self, row_index, column_index):
        # up , left , down, right
        is_block = np.zeros((self.NumberOfRows, self.NumberOfColumns, 4), dtype=bool)
        for i in range(self.NumberOfRows):
            for j in range(self.NumberOfColumns):
                if i == 0:
                    is_block[i, :, 0] = True
                if j == 0:
                    is_block[:, j, 1] = True
                if i == self.NumberOfRows-1:
                    is_block[i, :, 2] = True
                if j == self.NumberOfColumns-1:
                    is_block[:, j, 3] = True

        blocked_around = is_block[row_index, column_index]
        if not blocked_around[0]:
            # up
            if self.pairs[row_index-1][column_index] == self.pairs[row_index][column_index]:
                return (row_index-1, column_index)
        if not blocked_around[1]:
            # left
            if self.pairs[row_index][column_index-1] == self.pairs[row_index][column_index]:
                return (row_index, column_index-1)
        if not blocked_around[2]:
            # down
            if self.pairs[row_index+1][column_index] == self.pairs[row_index][column_index]:
                return (row_index+1, column_index)
        if not blocked_around[3]:
            # right
            if self.pairs[row_index][column_index + 1] == self.pairs[row_index][column_index]:
                return (row_index, column_index + 1)

    def is_goal(self):
        for i in range(self.NumberOfRows):
            row_list = self.poles_sign[i]
            number_of_positives = 0
            number_of_negatives = 0
            for j in row_list:
                if j == 1:
                    number_of_positives += 1
                if j == -1:
                    number_of_negatives += 1
            if number_of_positives != self.PositivePoleEachRow[i] or number_of_negatives != self.NegativePoleEachRow[i]:
                return False

        for i in range(self.NumberOfColumns):
            column_list = self.poles_sign[:, i]
            number_of_positives = 0
            number_of_negatives = 0
            for j in column_list:
                if j == 1:
                    number_of_positives += 1
                if j == -1:
                    number_of_negatives += 1
            if number_of_positives != self.PositivePoleEachColumn[i] or number_of_negatives != self.NegativePoleEachColumn[i]:
                return False
        return True

if __name__ == "__main__":
    print(MagnetPuzzle().get_neighbors(5, 0))