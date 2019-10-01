# !/usr/bin/python
from csp import *
import sys
from timeit import default_timer as timer


class kakuro(CSP):

    def __init__(self, board):

        self.rows = len(board)
        self.columns = len(board[0])

        self.horizontal_entries = []
        self.vertical_entries = []

        self.value_cells = None
        blank_cells = []
        value_cells = []
        constraint_cells = []
        domains = {}
        domain = list(range(1, 10))
        self.consistency_check_counter = 0

        for row, mylist in enumerate(board):
            for col, value in enumerate(mylist):
                if value == -1:
                    coord = 'x' + str(row) + str(col)
                    blank_cells.append(coord)
                elif value == 0:
                    coord = 'x' + str(row) + str(col)
                    value_cells.append(coord)
                elif dict == type(value):
                    coord = 'x' + str(row) + str(col)
                    constraint_cells.append(coord)

        self.value_cells = value_cells
        for var_pos, var in enumerate(value_cells):

            domains.update({value_cells[var_pos]: domain})

        neighbors = {}

        for var in value_cells:
            var_neighbors = []
            row = var[1]
            col = var[2]
            # ==================== now add the neighbors on the same horizontal_entry ===================

            # first we add the left boxes in the specific horizontal_entry from our box
            previous_col = int(col) - 1
            while True:  # add all the neighbors in horizontal_entry from the left for the specific variable in value_cells
                previous_var_in_row = 'x' + row + str(previous_col)
                if previous_var_in_row not in value_cells or previous_col < 0:
                    break  # it means has no other neighbor in row(horizontal_entry)

                var_neighbors.append(previous_var_in_row)
                neighbors.update({var: var_neighbors})
                previous_col -= 1

            # now we  add the right boxes in the specific horizontal_entry from our box
            next_col = int(col) + 1
            while True:  # add all the neighbors in horizontal_entry from the right for the specific variable in value_cells
                next_var_in_row = 'x' + row + str(next_col)
                if next_var_in_row not in value_cells:
                    break  # it means has no other neighbor in row(horizontal_entry)

                var_neighbors.append(next_var_in_row)
                neighbors.update({var: var_neighbors})
                next_col += 1

            # ==================== now add the neighbors on the same vertical_entry ===================
            # first we  add the upper boxes in the specific vertical_entry from our box
            previous_row = int(row) - 1
            while True:  # add all the neighbors in vertical_entry for the specific variable in value_cells
                previous_var_in_col = 'x' + str(previous_row) + col
                if previous_var_in_col not in value_cells:
                    break  # it means has no other neighbor in column(vertical_entry)

                var_neighbors.append(previous_var_in_col)
                neighbors.update({var: var_neighbors})
                previous_row -= 1

            # now we add the down boxes in the specific vertical_entry from our box
            next_row = int(row) + 1
            while True:  # add all the neighbors in vertical_entry for the specific variable in value_cells
                next_var_in_col = 'x' + str(next_row) + col
                if next_var_in_col not in value_cells:
                    break  # it means has no other neighbor in column(vertical_entry)

                var_neighbors.append(next_var_in_col)
                neighbors.update({var: var_neighbors})
                next_row += 1

        ######      HERE I WILL MAKE A LIST OF ALL THE horizontal_entries AND vertical_entries IN THE BOARD      ######

        # firstly I  will take all the constraint boxes and then I will make the lists for the horizontal_entries and vertical_entries
        for black_box in constraint_cells:

            black_box_row = int(black_box[1])
            black_box_col = int(black_box[2])

            if board[black_box_row][black_box_col]['R'] != -1:  # it means we have a horizontal_entry-sum constraint
                # then find the horizontal_entry and put it in the horizontal_entries list
                certain_horizontal_entry = []
                next_col = black_box_col + 1
                while True:
                    next_var_in_horizontal_entry = 'x' + str(black_box_row) + str(next_col)
                    if next_var_in_horizontal_entry not in value_cells:
                        break  # it means we reached the end of the horizontal_entry
                    certain_horizontal_entry.append(next_var_in_horizontal_entry)
                    next_col += 1
                certain_horizontal_entry.append(board[black_box_row][black_box_col]['R'])
                self.horizontal_entries.append(certain_horizontal_entry)

            if board[black_box_row][black_box_col]['C'] != -1:  # it means we have a vertical_entry-sum constraint
                # then fins the vertical_entry and put it in the vertical_entries list
                certain_vertical_entry = []
                next_row = black_box_row + 1
                while True:
                    next_var_in_vertical_entry = 'x' + str(next_row) + str(black_box_col)
                    if next_var_in_vertical_entry not in value_cells:
                        break
                    certain_vertical_entry.append(next_var_in_vertical_entry)
                    next_row += 1
                certain_vertical_entry.append(board[black_box_row][black_box_col]['C'])
                self.vertical_entries.append(certain_vertical_entry)

        # #initialize csp
        CSP.__init__(self, value_cells, domains, neighbors, self.kakuro_constraints)

    def display(self, solution):
        print("\n -----Now printing solution-----\n")
        if solution is None:
            print("No solution was found \n")
        else:
            print("Solution was found with succes!")
            assigned_vars = self.infer_assignment()
            for x in sorted(assigned_vars):
                print(x, assigned_vars[x])

    def kakuro_constraints(self, A, a, B, b):
        self.consistency_check_counter += 1

        if A == B:  # if A,B are the same variable
            return False

        A_neighbors = self.neighbors[A]
        B_neighbors = self.neighbors[B]

        # get a dictionary with all assigned variables and their corresponding values
        assigned_vars = self.infer_assignment()

        if A in B_neighbors or B in A_neighbors:  # redundancy the 2nd statement
            # and have the same value
            if a == b:
                return False

        # checking neighbors constraint (only 1 same symbol in horizontal_entry and vertical_entry) for  A
        for neighbor in A_neighbors:
            if neighbor in assigned_vars.keys():  # if  A's neighbor has been assigned to a value

                # check if the value of A-->a is the same with the assigned neighbor's value
                if a == assigned_vars[neighbor]:
                    return False

        ###same technique for B###
        # checking neighbors constraint (only 1 same symbol in horizontal_entry and vertical_entry) for  B
        for neighbor in B_neighbors:
            if neighbor in assigned_vars.keys():  # if  B's neighbor has been assigned to a value
                # check if the value of B-->b is the same with the assigned neighbor's value
                if b == assigned_vars[neighbor]:
                    return False

        A_horizontal_entry_checked = 0
        A_vertical_entry_checked = 0
        B_horizontal_entry_checked = 0
        B_vertical_entry_checked = 0

        found_horizontal_entry_A = 0
        found_vertical_entry_A = 0
        found_horizontal_entry_B = 0
        found_vertical_entry_B = 0

        for horizontal_entry_A in self.horizontal_entries:
            if A in horizontal_entry_A:
                found_horizontal_entry_A = 1
                break
        if found_horizontal_entry_A == 0:
            horizontal_entry_A = []
        for vertical_entry_A in self.vertical_entries:
            if A in vertical_entry_A:
                found_vertical_entry_A = 1
                break
            if found_vertical_entry_A == 0:
                vertical_entry_A = []
        for horizontal_entry_B in self.horizontal_entries:
            if B in horizontal_entry_B:
                found_horizontal_entry_B = 1
                break
        if found_horizontal_entry_B == 0:
            horizontal_entry_B = []
        for vertical_entry_B in self.vertical_entries:
            if B in vertical_entry_B:
                found_vertical_entry_B = 1
                break
        if found_vertical_entry_B == 0:
            vertical_entry_B = []

        if (horizontal_entry_A != horizontal_entry_B) and (vertical_entry_A != vertical_entry_B):

            # check A horizontal & vertical entry if it's consistent
            if all(neighbor in assigned_vars for neighbor in A_neighbors):

                if found_horizontal_entry_A != 0:
                    entry_constraint_check, A_horizontal_entry_checked = self.entry_constraint(
                        horizontal_entry_A, assigned_vars, A, a)
                    if entry_constraint_check == -1:
                        return False
                else:
                    A_horizontal_entry_checked = 1

                if found_vertical_entry_A != 0:
                    entry_constraint_check, A_vertical_entry_checked = self.entry_constraint(
                        vertical_entry_A, assigned_vars, A, a)
                    if entry_constraint_check == -1:
                        return False
                else:
                    A_vertical_entry_checked = 1

            else:
                return True

            # same for B

            if all(neighbor in assigned_vars for neighbor in B_neighbors):

                if found_horizontal_entry_B != 0:
                    entry_constraint_check, B_horizontal_entry_checked = self.entry_constraint(
                        horizontal_entry_B, assigned_vars, B, b)

                    if entry_constraint_check == -1:
                        return False
                else:
                    B_horizontal_entry_checked = 1

                if found_vertical_entry_B != 0:
                    entry_constraint_check, B_vertical_entry_checked = self.entry_constraint(
                        vertical_entry_B, assigned_vars, B, b)
                    if entry_constraint_check == -1:
                        return False
                else:
                    B_vertical_entry_checked = 1
            else:
                return True

        elif horizontal_entry_A == horizontal_entry_B:

            if found_horizontal_entry_A != 0:  # it would be same as  if found_horizontal_entry_B != 0
                # this list is needed to check if all the neighbors beyond A,B in the horizontal entry have been assigned
                horizontal_entry_beyond_A_B = [
                    x for x in horizontal_entry_A[:-1] if x not in A and x not in B]

                if all(var in assigned_vars for var in horizontal_entry_beyond_A_B):

                    entry_constraint_check, A_B_horizontal_entry_checked = self.entry_constraint(
                        horizontal_entry_A, assigned_vars, A, a, B, b)
                    if entry_constraint_check == -1:
                        return False
                    if A_B_horizontal_entry_checked == 1:
                        A_horizontal_entry_checked = 1
                        B_horizontal_entry_checked = 1
                else:
                    return True
            else:
                A_horizontal_entry_checked = 1
                B_horizontal_entry_checked = 1

            # check A vertical entry if it's consistent
            if found_vertical_entry_A != 0:
                if all(neighbor in assigned_vars for neighbor in A_neighbors):

                    entry_constraint_check, A_vertical_entry_checked = self.entry_constraint(
                        vertical_entry_A, assigned_vars, A, a)
                    if entry_constraint_check == -1:
                        return False
                else:
                    return True
            else:
                A_vertical_entry_checked = 1

            # same for B

            if found_vertical_entry_B != 0:
                if all(neighbor in assigned_vars for neighbor in B_neighbors):
                    entry_constraint_check, B_vertical_entry_checked = self.entry_constraint(
                        vertical_entry_B, assigned_vars, B, b)
                    if entry_constraint_check == -1:
                        return False
                else:
                    return True

            else:
                B_vertical_entry_checked = 1

        elif vertical_entry_A == vertical_entry_B:
            if found_vertical_entry_A != 0:  # it would be same as  if found_vertical_entry_B != 0

                vertical_entry_beyond_A_B = [
                    x for x in vertical_entry_A[:-1] if x not in A and x not in B]

                if all(var in assigned_vars for var in vertical_entry_beyond_A_B):

                    entry_constraint_check, A_B_vertical_entry_checked = self.entry_constraint(
                        vertical_entry_A, assigned_vars, A, a, B, b)
                    if entry_constraint_check == -1:
                        return False
                    if A_B_vertical_entry_checked == 1:
                        A_vertical_entry_checked = 1
                        B_vertical_entry_checked = 1
                else:
                    return True
            else:
                A_vertical_entry_checked = 1
                B_vertical_entry_checked = 1

            if found_horizontal_entry_A != 0:
                if all(neighbor in assigned_vars for neighbor in A_neighbors):

                    entry_constraint_check, A_horizontal_entry_checked = self.entry_constraint(
                        horizontal_entry_A, assigned_vars, A, a)
                    if entry_constraint_check == -1:
                        return False
                else:
                    return True
            else:
                A_horizontal_entry_checked = 1

            if found_horizontal_entry_B != 0:
                if all(neighbor in assigned_vars for neighbor in B_neighbors):

                    entry_constraint_check, B_horizontal_entry_checked = self.entry_constraint(
                        horizontal_entry_B, assigned_vars, B, b)
                    if entry_constraint_check == -1:
                        return False
                else:
                    return True
            else:
                B_horizontal_entry_checked = 1

        if (A_horizontal_entry_checked == 1 and A_vertical_entry_checked == 1 and B_horizontal_entry_checked == 1 and B_vertical_entry_checked == 1):
            return True
        else:
            return False

    def entry_constraint(self, entry, assigned_vars, var1, x, var2=None, y=0):
        constraint_entry_sum = entry[-1]
        sum = 0
        for var in entry[:-1]:

            if var2 != None:
                if var == var1 or var == var2:
                    pass
                else:
                    sum += assigned_vars[var]

            else:

                if var == var1:
                    pass
                else:

                    sum += assigned_vars[var]

        if var2 != None:
            if sum + x + y == constraint_entry_sum:

                return 0, 1
            else:
                return -1, 0
        else:
            if sum + x == constraint_entry_sum:
                return 0, 1
            else:
                return -1, 0


def main(argv):
    board0 = [[-1, {'C': 5, 'R': -1}, {'C': 16, 'R': -1}],
              [-1, 0, 0],
              [{'C': -1, 'R': 12}, 0, 0]]

    board1 = [[-1, -1, -1, {'R': -1, 'C': 6}, {'R': -1, 'C': 3}],
              [-1, {'R': -1, 'C': 4}, {'R': 3, 'C': 3}, 0, 0],
              [{'R': 10, 'C': -1}, 0, 0, 0, 0],
              [{'R': 3, 'C': -1}, 0, 0, -1, -1]]

    board2 = [[-1, {'C': 7, 'R': -1}, {'C': 6, 'R': -1}, -1, -1],
              [{'C': -1, 'R': 6}, 0, 0, {'C': 7, 'R': -1}, {'C': 24, 'R': -1}],
              [{'C': -1, 'R': 15}, 0, 0, 0, 0],
              [{'C': -1, 'R': 13}, 0, 0, 0, 0],
              [-1, -1, {'C': -1, 'R': 10}, 0, 0]]

    board3 = [[-1, {'R': -1, 'C': 23}, {'R': -1, 'C': 30}, -1, -1, {'R': -1, 'C': 27}, {'R': -1, 'C': 12}, {'R': -1, 'C': 16}],
              [{'R': 16, 'C': -1}, 0, 0, -1, {'R': 24, 'C': 17}, 0, 0, 0],
              [{'R': 17, 'C': -1}, 0, 0, {'R': 29, 'C': 15}, 0, 0, 0, 0],
              [{'R': 35, 'C': -1}, 0, 0, 0, 0, 0, {'R': -1, 'C': 12}, -1],
              [-1, {'R': 7, 'C': -1}, 0, 0, {'R': 8, 'C': 7}, 0, 0, {'R': -1, 'C': 7}],
              [-1, {'R': -1, 'C': 11}, {'C': 10, 'R': 16}, 0, 0, 0, 0, 0],
              [{'C': -1, 'R': 21}, 0, 0, 0, 0, {'C': -1, 'R': 5}, 0, 0],
              [{'C': -1, 'R': 6}, 0, 0, 0, -1, {'C': -1, 'R': 3}, 0, 0]]

    test = kakuro(board0)

    # BT:
    # start = timer()
    # x = backtracking_search(test)
    # duration = timer() - start

    # BT + MRV:
    # start = timer()
    # x = backtracking_search(test, select_unassigned_variable=mrv)
    # duration = timer() - start

    # FC:
    # start = timer()
    # x = backtracking_search(test, inference=forward_checking)
    # duration = timer() - start

    # FC + MRV:
    # start = timer()
    # x = backtracking_search(test, select_unassigned_variable=mrv, inference=forward_checking)
    # duration = timer() - start

    # MAC:
    start = timer()
    x = backtracking_search(test, inference=mac)
    duration = timer() - start

    # test.display(x)
    test.display(x)

    print("duration:", duration)
    print("number of assignments:", test.nassigns)
    print("number of consistency checks:", test.consistency_check_counter)


if __name__ == "__main__":
    main(sys.argv)
