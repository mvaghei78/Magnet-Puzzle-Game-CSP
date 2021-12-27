from MagnetPuzzle import MagnetPuzzle
class CheckConsistency:
    def __init__(self, magnet_puzzle):
        self.magnet_puzzle = magnet_puzzle
    def forward_checking(self, table, assignment, row_index, col_index, new_value):
        neighbors = self.magnet_puzzle.get_neighbors(row_index, col_index)
        pair = self.magnet_puzzle.get_pair(row_index, col_index)
        pair_neighbors = self.magnet_puzzle.get_neighbors(pair[0], pair[1])
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

    def ac3(self, table, assignment, row_index, col_index, new_value):
        all_pairs = self.magnet_puzzle.get_all_pairs()
        for first_pair, second_pair in all_pairs:
            print(first_pair, second_pair)