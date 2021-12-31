
class Heuristics:
    def __init__(self, magnet_puzzle):
        self.magnet_puzzle = magnet_puzzle
    # input:
    # table -> all values for  each piece
    # assignment -> number of values that remained for each piece
    # output:
    # row and column of selected piece via MRV Heuristic
    def mrv_heuristic(self, table, assignment):
        mrv_row = None
        mrv_col = None
        for y, row in enumerate(assignment):
            for x, item in enumerate(row):
                if (mrv_row == None or len(item) < len(assignment[mrv_row][mrv_col])) and (table[y][x] == None and len(item) > 0):
                    mrv_col = x
                    mrv_row = y
        return mrv_row, mrv_col

    def lcv_heuristic(self, table, assignment, row_index, column_index):
        score_of_pos = 0
        score_of_neg = 0
        ordered_domain = [0]
        pair = self.magnet_puzzle.get_pair(row_index, column_index)
        neighbors = self.magnet_puzzle.get_neighbors(row_index, column_index)
        pair_neighbors = self.magnet_puzzle.get_neighbors(pair[0], pair[1])
        neighbors.remove([pair[0], pair[1]])
        pair_neighbors.remove([row_index, column_index])
        count_1 = 0
        count_minus_1 = 0
        for n in neighbors:
            if 1 in assignment[n[0]][n[1]]:
                count_1 += 1
            if -1 in assignment[n[0]][n[1]]:
                count_minus_1 += 1
        for n in pair_neighbors:
            if -1 in assignment[n[0]][n[1]]:
                count_1 += 1
            if 1 in assignment[n[0]][n[1]]:
                count_minus_1 += 1
        if count_1 < count_minus_1:
            score_of_pos += 1
        elif count_1 > count_minus_1:
            score_of_neg += 1
        num_of_pos_in_row, number_of_neg_in_row\
            , num_of_pos_in_column, number_of_neg_in_column = self.magnet_puzzle.count_of_pos_neg(table, row_index, column_index)
        score_of_pos += (self.magnet_puzzle.PositivePoleEachRow[row_index] - num_of_pos_in_row) + (
                self.magnet_puzzle.PositivePoleEachColumn[column_index] - num_of_pos_in_column)
        score_of_neg += (self.magnet_puzzle.NegativePoleEachRow[row_index] - number_of_neg_in_row) + (
            self.magnet_puzzle.NegativePoleEachColumn[column_index] - number_of_neg_in_column)

        num_of_pos_in_row, number_of_neg_in_row\
            , num_of_pos_in_column, number_of_neg_in_column = self.magnet_puzzle.count_of_pos_neg(table, pair[0], pair[1])

        score_of_pos += (self.magnet_puzzle.PositivePoleEachRow[row_index] - num_of_pos_in_row) + (
                self.magnet_puzzle.PositivePoleEachColumn[column_index] - num_of_pos_in_column)
        score_of_neg += (self.magnet_puzzle.NegativePoleEachRow[row_index] - number_of_neg_in_row) + (
            self.magnet_puzzle.NegativePoleEachColumn[column_index] - number_of_neg_in_column)

        if score_of_pos >= score_of_neg:
            ordered_domain.extend([1, -1])
        else:
            ordered_domain.extend([-1, 1])
        return ordered_domain
