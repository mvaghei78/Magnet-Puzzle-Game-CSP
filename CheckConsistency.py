import copy


class CheckConsistency:
    def __init__(self, magnet_puzzle):
        self.magnet_puzzle = magnet_puzzle

    def forward_checking(self, table, assignment, row_index, col_index, new_value):
        neighbors = self.magnet_puzzle.get_neighbors(row_index, col_index)
        pair = self.magnet_puzzle.get_pair(row_index, col_index)
        pair_neighbors = self.magnet_puzzle.get_neighbors(pair[0], pair[1])
        neighbors.remove([pair[0], pair[1]])
        pair_neighbors.remove([row_index, col_index])
        for neighbor_pos in neighbors:
            if new_value in assignment[neighbor_pos[0]][neighbor_pos[1]]:
                assignment[neighbor_pos[0]][neighbor_pos[1]].remove(new_value)
                if len(assignment[neighbor_pos[0]][neighbor_pos[1]]) == 0 and table[neighbor_pos[0]][neighbor_pos[1]] == None:
                    return False
        for neighbor_pos in pair_neighbors:
            if new_value in assignment[neighbor_pos[0]][neighbor_pos[1]]:
                assignment[neighbor_pos[0]][neighbor_pos[1]].remove(new_value)
                if len(assignment[neighbor_pos[0]][neighbor_pos[1]]) == 0 and table[neighbor_pos[0]][neighbor_pos[1]] == None:
                    return False
        return True

    def ac3(self, assignment, row_index, col_index):
        csp_list = self.magnet_puzzle.csp(row_index, col_index)
        while csp_list:
            (xi, xj) = csp_list.pop(0)
            pair = self.magnet_puzzle.get_pair(xi[0], xi[1])
            if self.remove_inconsistent_values(assignment, xi, xj):
                if len(assignment[xi[0]][xi[1]]) == 0:
                    return False
                xi_neighbors = self.magnet_puzzle.get_neighbors(xi[0], xi[1])
                xi_neighbors.remove([pair[0], pair[1]])
                for xk in xi_neighbors:
                    csp_list.append((xk, xi))
            if self.remove_inconsistent_values(assignment, pair, xj):
                if len(assignment[pair[0]][pair[1]]) == 0:
                    return False
                pair_neighbors = self.magnet_puzzle.get_neighbors(pair[0], pair[1])
                pair_neighbors.remove([xi[0], xi[1]])
                for xk in pair_neighbors:
                    csp_list.append((xk, pair))
        return True

    def remove_inconsistent_values(self, assignment, xi, xj):
        removed = False
        first_pair_domain_copy = copy.deepcopy(assignment[xi[0]][xi[1]])
        for x in first_pair_domain_copy:
            if x == 1 or x == -1:
                if x*-1 not in assignment[xj[0]][xj[1]] and 0 not in assignment[xj[0]][xj[1]]:
                    assignment[xi[0]][xi[1]].remove(x)
                    removed = True
        return removed

    # def ac3(self, assignment):
    #     all_pairs = self.magnet_puzzle.get_all_pairs()
    #     for first_pair, second_pair in all_pairs:
    #         first_pair_neighbors = self.magnet_puzzle.get_neighbors(first_pair[0], first_pair[1])
    #         second_pair_neighbors = self.magnet_puzzle.get_neighbors(second_pair[0], second_pair[1])
    #         first_pair_neighbors.remove([second_pair[0], second_pair[1]])
    #         second_pair_neighbors.remove([first_pair[0], first_pair[1]])
    #         for n in first_pair_neighbors:
    #             if self.remove_inconsistent_values(assignment, first_pair, n):
    #                 if len(assignment[first_pair[0]][first_pair[1]]) == 0:
    #                     return False
    #
    #         for n in second_pair_neighbors:
    #             if self.remove_inconsistent_values(assignment, second_pair, n):
    #                 if len(assignment[second_pair[0]][second_pair[1]]) == 0:
    #                     return False
    #     return True