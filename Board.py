import Block
import Position
import random


def make_board(dimension=10, positions_to_fill=frozenset()):
    """
        Return a new board of the given dimension for which all cells at the
        given positions are already filled.
        ASSUMPTIONS
        - The given dimension is a positive integer number.
        - The filled positions is a collection of proper positions. Positions
          outside the boundaries of the new board have no impact on the content
          of the new board.
    """
    # Board is a dict with a key "dim"(value = dimension) and other keys are the filled positions (value = True)
    board = dict()
    for position in positions_to_fill:
        if 0 < position[0] <= dimension and 0 < position[1] <= dimension:
            board[position] = True
    board["dim"] = dimension
    return board


def copy_board(board):
    """
        Return a copy of the given board.
        ASSUMPTIONS
        - The given board is a proper board.
    """
    return board.copy()


def is_proper_board(board):
    """
        Check whether the given board is a proper board.
        - The board type is a dictionary
        - Each key in the dictionary is a tuple except for the "dim" key
        - The length of the board is not bigger than #elements + 1 (the "dim" key)
        ASSUMPTIONS
        - None
        NOTE
        - You need to complete the conditions
        (as they depend on the internal representation you have chosen for the board)
    """
    if type(board) != dict:
        return False
    if not 0 < board["dim"]:
        return False
    if len(board) > board["dim"]**2+1:
        return False
    for elem in board:
        if elem == "dim":
            if type(board[elem]) is not int:
                return False
        else:
            if type(elem) != tuple:
                return False
            if board[elem] is not True:
                return False
    else:
        return True


def dimension(board):
    return board["dim"]


def is_filled_at(board, position):
    """
        Return a boolean indicating whether or not the cell at the given position
        on the given board is filled.
        - Returns false if the given position is outside the boundaries of the
          given board.
        ASSUMPTIONS
        - The given board is a proper board.
        - The given position is a proper position.
    """

    if position in board and board[position] is True:
        return True
    # When position is outside board boundaries or position is not valid
    return False


def get_all_filled_positions(board):
    """
        Return a set of all the positions of filled cells on the given board.
        ASSUMPTIONS
        - The given board is a proper board.
    """
    filled_positions = set()

    for pos in board:
        if is_filled_at(board, pos):
            filled_positions.add(pos)

    return filled_positions


def is_filled_row(board, row):
    """
        Return a boolean indicating whether or not all the cells of the given
        row on the given board are filled.
        - Returns false if the given row is not an integer number or if it is
          outside the boundaries of the given board.
        ASSUMPTIONS
        - The given board is a proper board.
        NOTE
        - You are not allowed to use for statements in the body of this function.
    """
    col = 1
    while col <= dimension(board):
        if not is_filled_at(board, (col, row)):
            return False
        col += 1
    return True


def is_filled_column(board, column):
    """
        Return a boolean indicating whether or not all the cells of the given
        column on the given board are filled.
        - Returns false if the given column is not an integer number or if it is
          outside the boundaries of the given board.
        ASSUMPTIONS
        - The given board is a proper board.
        NOTE
        - You are not allowed to use while statements in the body of this function.
    """
    for row in range(1, dimension(board) + 1):
        if not is_filled_at(board, (column, row)):
            return False
    return True


def get_all_filled_rows(board):
    """
        Return all the rows on the given board that are completely filled.
        - The function returns a list of the numbers in ascending order of
          all the rows that are completely filled.
        ASSUMPTIONS
        - The given board is a proper board.
        NOTE
        - You are not allowed to use for statements in the body of this function.
    """
    filled_rows = []
    row = 1
    while row <= dimension(board):
        if is_filled_row(board, row):
            filled_rows.append(row)
        row += 1

    return filled_rows


def get_all_filled_columns(board):
    """
        Return all the columns on the given board that are completely filled.
        - The function returns a tuple of the numbers in descending order of
          all the columns that are completely filled.
        ASSUMPTIONS
        - The given board is a proper board.
        NOTE
        - You are not allowed to use while statements in the body of this function.
    """
    filled_columns = tuple()
    for col in range(1, dimension(board)+1):
        if is_filled_column(board, col):
            filled_columns = (col,) + filled_columns

    return filled_columns


def inside_board(board, position):
    if 0 < position[0] <= dimension(board) and 0 < position[1] <= dimension(board):
        return True
    return False


def fill_cell(board, position):
    """
        Fill the cell at the given position on the given board.
        - Nothing happens if the given position is outside the
          boundaries of the given board or if the given cell is
          already filled.
        ASSUMPTIONS
        - The given board is a proper board.
        - The given position is a proper position.
    """
    if not is_filled_at(board, position) and inside_board(board, position):
        board[position] = True


def fill_all_cells(board, positions):
    """
        Fill all the cells at each position in the given collection of
        positions on the given board.
        - Positions outside the boundaries of the given board are ignored.
        - Positions that are already filled are left untouched.
        ASSUMPTIONS
        - The given board is a proper board.
        - Each position in the collection of positions is a proper position.
    """
    for position in positions:
        fill_cell(board, position)


def free_cell(board, position):
    """
        Free the cell at the given position of the given board.
        - Nothing happens if the cell is already free or if the given
          position is outside the boundaries of the given board.
        ASSUMPTIONS
        - The given board is a proper board.
        - The given position is a proper position.
    """
    if position in board:
        if board[position] is True:
            del board[position]


def free_all_cells(board, positions):
    """
        Fill all the cells at each position in the tuple of positions on
        the given board.
        - Positions outside the boundaries of the given board are ignored.
        - Positions that are already filled are left untouched.
        ASSUMPTIONS
        - The given board is a proper board.
        - Each position in the tuple of positions is a proper position.
        NOTE
        - This function must be worked out in a recursive way.
    """
    if len(positions) == 1:
        free_cell(board, positions[0])
    else:
        return free_all_cells(board, positions[1:])


def free_row(board, row):
    """
        Free all the cells of the given row on the given board.
        - Nothing happens if the given row is not an integer number or if
          it is outside the boundaries of the given board.
        ASSUMPTIONS
        - The given board is a proper board.
    """
    if type(row) == int and 0 < row <= dimension(board):
        for col in range(1, dimension(board) + 1):
            free_cell(board, (col, row))


def free_column(board, column):
    """
        Free all the cells of the given column on the given board.
        - Nothing happens if the given column is not an integer number or if
          it is outside the boundaries of the given board.
        ASSUMPTIONS
        - The given board is a proper board.
    """
    if type(column) == int and 0 < column <= dimension(board):
        for row in range(1, dimension(board) + 1):
            free_cell(board, (column, row))


def can_be_dropped_at(board, block, position):
    """
        Check whether the given block can be dropped at the given position.
        - The given position determines the position for the anchor of the
          given block.
        - True if and only if for each of the dot positions D of the given block
          there is a FREE cell at a position within the boundaries of the given
          board and at the same horizontal- and vertical distance from the
          given position as the horizontal- and vertical distance of the dot
          position D from the anchor of the given block.
        ASSUMPTIONS
        - The given board is a proper board.
        - The given block is a proper block.
        - The given position is a proper position.
    """
    # get the positions of the dots in the board with given position
    block_in_board = list()
    for dot in block:
        block_in_board.append((dot[0] + position[0], dot[1] + position[1]))

    for dot_in_board in block_in_board:
        if dot_in_board in get_all_filled_positions(board):  # checks if pos is already filled
            return False
        if not inside_board(board, dot_in_board):  # check if pos in board
            return False
    return True


def get_droppable_positions(board, block):
    """
        Return a list of all positions at which the given block can be dropped
        on the given board.
        - The positions in the resulting list are in ascending order.
        ASSUMPTIONS
        - The given board is a proper board.
        - The given block is a proper block.
        NOTE
        - The function should only examine positions at which the given block
          fully fits within the boundaries of the given board.
    """
    block_copy = block.copy()
    droppable_positions = []

    horizontal_offsets = Block.get_horizontal_offsets_from_anchor(block_copy)
    vertical_offsets = Block.get_vertical_offsets_from_anchor(block_copy)

    # check every position where block fully fits within the boundaries of the given board
    for x_value in range(1-horizontal_offsets[0], dimension(board)-horizontal_offsets[1] + 1):
        for y_value in range(1-vertical_offsets[0], dimension(board)-vertical_offsets[1] + 1):
            possible_position = (x_value, y_value)
            if can_be_dropped_at(board, block, possible_position):
                droppable_positions.append(possible_position)
    return droppable_positions


def block_pos_in_board(block, position):
    """assumes the block can be placed in the board, returns the coordinates of block dots in board
    (self made)
    """
    block_in_board = set()
    for dot in block:
        block_in_board.add((dot[0] + position[0], dot[1] + position[1]))
    return block_in_board


def drop_at(board, block, position):
    """
        Drop the given block at the given position on the given board.
        - Each of the cells on the given board at a position with the same
          horizontal- and vertical distance from the given position as a dot
          position of the given block from the block's anchor, is filled.
        - Nothing happens if the given block can not be dropped at the given
          position on the given board.
        ASSUMPTIONS
        - The given board is a proper board.
        - The given position is a proper position.
        - The given block is a proper block.
    """
    if can_be_dropped_at(board, block, position):
        block_in_board = block_pos_in_board(block, position)
        for dot_in_board in block_in_board:
            board[dot_in_board] = True


def clear_full_rows_and_columns(board):
    """
        Clear all full rows and all full columns on the given board.
        ASSUMPTIONS
        - The given board is a proper board.
    """
    full_columns = get_all_filled_columns(board)
    full_rows = get_all_filled_rows(board)

    for full_column in full_columns:
        free_column(board, full_column)

    for full_row in full_rows:
        free_row(board, full_row)


def adjacent_positions_in_block(positions, block):
    """
        returns the adjacent positions that are in the block itself.
        Note: it does not return the positions in the block itself.
    """
    adjacent_and_in_block = set()
    for position in positions:
        adjacents = Position.get_adjacent_positions(position)
        for pos in adjacents:
            if pos in block and pos not in adjacent_and_in_block and pos not in positions:
                adjacent_and_in_block.add(pos)
    return adjacent_and_in_block


def is_subset_of(bigset, subset):
    """
        Returns true if 'subset' is a subset of 'bigset', else False.
    """
    for elem in subset:
        if elem not in bigset:
            return False
    return True


def invert_board(board):
    """
        Inverts the board: frees filled cells and fills free cells
    """
    all_positions_in_board = list()
    non_filled_positions_in_board = set()
    for x_value in range(1, dimension(board)+1):
        for y_value in range(1, dimension(board)+1):
            all_positions_in_board.append(tuple((x_value, y_value),))

    for position in all_positions_in_board:
        if not is_filled_at(board, position):
            non_filled_positions_in_board.add(position)

    inverted_board = make_board(dimension(board), frozenset(non_filled_positions_in_board))
    return inverted_board


def are_chainable(board, positions, current_chain=tuple(), unchained_positions=tuple()):
    """
        Check whether the given collection of positions is chained on the
        given board.
        - True if and only if at least one collection of chained positions exists
          on the given board that includes all given positions and for which all
          the cells in that collection are either all filled or all empty.
        ASSUMPTIONS
        - The given board is a proper board.
        - Each of the given positions is a proper position for the given board.
        - All the cells on the given board at the given positions all have the
          same state, i.e. they are all filled or all empty.
        NOTE
        - This function should be worked out in a recursive way
    """
    positions = set(positions)
    if len(positions) <= 1:
        return True

    # Invert board if position is not filled and continue function
    if not is_filled_at(board, random.choice(tuple(positions))):
        board = invert_board(board)

    positions_copy = positions.copy()
    filled_positions = get_all_filled_positions(board)  # Get all the filled positions of board and positions

    # Only for the first iteration:
    if len(current_chain) == 0:
        first_pos = positions_copy.pop()
        current_chain += (first_pos,)
        unchained_positions = set(tuple(positions_copy) + tuple(filled_positions))
        unchained_positions.discard(first_pos)
        # Now you have a current_chain, and a set of (yet) unchained positions which are yet to be tested

    # If all filled positions are in the current_chain, return True
    if is_subset_of(current_chain, positions):
        return True

    adjacent_positions = adjacent_positions_in_block(current_chain, filled_positions)

    # add adjacent dots of current chain which are in the block to the current chain, and remove from unchained_pos
    for adjacent_position in adjacent_positions:
        if adjacent_position not in current_chain:
            unchained_positions.remove(adjacent_position)
            current_chain += (adjacent_position,)

    # If no adjacent positions are left in current_chain and not all positions are in current chain, return False
    if len(adjacent_positions) == 0:
        if not is_subset_of(current_chain, positions):
            return False

    # restart with new current_chain and new unchained_positions
    return are_chainable(board, positions, current_chain, unchained_positions)


def print_board(board):
    """
        Print the given board on the standard output stream.
        ASSUMPTIONS
        - The given board is a proper board.
    """
    for row in range(dimension(board), 0, -1):
        print('{:02d}'.format(row), end="  ")
        for column in range(1, dimension(board) + 1):
            if is_filled_at(board, (column, row)):
                print(" \u25A9 ", end=" ")
            else:
                print("   ", end=" ")
        print()
    print("    ", end="")
    for column in range(1, dimension(board) + 1):
        print('{:02d}'.format(column), end="  ")
    print()
