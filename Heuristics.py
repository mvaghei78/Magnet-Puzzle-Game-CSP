
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

    def lcv_heuristic(self, assignment, row_index, column_index):
        ordered_domain = [0]
        pair = self.magnet_puzzle.get_pair(row_index, column_index)
        neighbors = self.magnet_puzzle.get_neighbors(row_index, column_index)
        pair_neighbors = self.magnet_puzzle.get_neighbors(pair[0], pair[1])
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
