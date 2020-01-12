# Positions are used to
#  (1) identify cells on the board
#  (2) dots on blocks relative to the block's anchor.


def is_proper_position(position):
    """
        Check whether the given position is a proper position.
        - True if and only if the given position is a tuple of length 2
          whose elements are both integer numbers.
        ASSUMPTIONS
        - None
    """
    if type(position) == tuple and len(position) == 2:
        if type(position[0]) == int and type(position[1]) == int:
            return True
    else:
        return False


def is_proper_position_for_board(dimension, position):
    """
        Check whether the given position is a proper position for a square
        board with the given dimension.
        - True if and only if (1) the given dimension is a positive integer
          number and (2) if the given position is a proper position within
          the boundaries of a board with the given dimension, i.e not below
          1 nor above the given dimension in both directions.
        ASSUMPTIONS
        - None
    """
    if is_proper_position(position) and type(dimension) == int and dimension > 0:
        if 0 < position[0] <= dimension and 0 < position[1] <= dimension:
            return True
    return False


def left(dimension, position):
    """
        Return the position on any board with the given dimension immediately to
        the left of the given position.
        - None is returned if the generated position is outside the boundaries of
          a board with the given dimension.
        ASSUMPTIONS
        - The given position is a proper position for any board with the
          given dimension.
    """
    if dimension is None or 0 < position[0] - 1 <= dimension:
        return tuple((position[0]-1, position[1]))
    else:
        return None


def right(dimension, position):
    """
       Return the position on any board with the given dimension immediately to
       the right of the given position.
       - None is returned if the generated position is outside the boundaries of
         a board with the given dimension.
       ASSUMPTIONS
       - The given position is a proper position for any board with the
         given dimension.
     """
    if dimension is None or 0 < position[0] + 1 <= dimension:
        return tuple((position[0] + 1, position[1]))
    else:
        return None


def up(dimension, position):
    """
        Return the position on any board with the given dimension immediately
        above the given position.
        - None is returned if the generated position is outside the boundaries of
          a board with the given dimension.
        ASSUMPTIONS
        - The given position is a proper position for any board with the
          given dimension.
     """
    if dimension is None or 0 < position[1] + 1 <= dimension:
        return tuple((position[0], position[1] + 1))
    else:
        return None


def down(dimension, position):
    """
        Return the position on any board with the given dimension immediately
        below the given position.
        - None is returned if the generated position is outside the boundaries of
          a board with the given dimension.
        ASSUMPTIONS
        - The given position is a proper position for any board with the
          given dimension.
     """
    if dimension is None or 0 < position[1] - 1 <= dimension:
        return tuple((position[0], position[1] - 1))
    else:
        return None


def next(dimension, position):
    """
        Return the position on any board with the given dimension next to the
        given position.
        - If the given position is not at the end of a row, the resulting position
          is immediately to the right of the given position.
        - If the given position is at the end of a row, the resulting position is
          the leftmost position of the row above. If that next row does not exist,
          None is returned.
        ASSUMPTIONS
        - The given position is a proper position for any board with the
          given dimension.
     """
    if position[0] < dimension:
        return tuple((position[0] + 1, position[1]))

    if position[0] == dimension and position[1] < dimension:
        return tuple((1, position[1] + 1))

    if position[0] == dimension and position[1] == dimension:
        return None


def translate_over(position, delta_x, delta_y):
    """
        Return the position resulting from translating the given position horizontally
        and vertically over the given delta's.
        ASSUMPTIONS
        - The given position is a proper position.
        - The given delta's are integer numbers.
    """
    return tuple((position[0] + delta_x, position[1] + delta_y))


def get_adjacent_positions(position, dimension=None):
    """
        Return a mutable set of all positions immediately adjacent to the
        given position and within the boundaries of a board with the given
        dimension.
        - Adjacent positions are either at a horizontal distance or at a vertical
          distance of 1 from the given position.
        - If the given dimension is None, no boundaries apply.
        ASSUMPTIONS
        - The given position is a proper position for any board with the
          given dimension, or simply a proper position if no dimension is supplied.
    """
    adjacents = set()
    adjacents.add(up(dimension, position))
    adjacents.add(down(dimension, position))
    adjacents.add(left(dimension, position))
    adjacents.add(right(dimension, position))
    adjacents.discard(None)
    return adjacents


def is_adjacent_to(position, other_positions):
    """
        Check whether the given position is adjacent to at least one of the positions
        in the collection of other positions.
        - True if and only if at least one of the other positions is one of the positions
          adjacent to the given position in an unbounded area.
        ASSUMPTIONS
        - The given position is a proper position
        - All positions in the collection of other positions are proper positions.
    """
    adjacent_positions = get_adjacent_positions(position)
    for other_position in other_positions:
        if other_position in adjacent_positions:
            return True
    return False


def get_surrounding_positions(position, dimension=None):
    """
        Return a mutable set of all positions immediately surrounding the
        given position and within the boundaries of a board with the given
        dimension.
        - Surrounding positions are at a horizontal distance and/or a vertical
          distance of 1 from the given position.
        - If the given dimension is None, no boundaries apply.
        ASSUMPTIONS
        - The given position is a proper position for any board with the
          given dimension, or simply a proper position if no dimension is supplied.
    """
    # get the adjacents first, add corners later
    surrounding_positions = get_adjacent_positions(position, dimension)

    if left(dimension, position) is not None:
        surrounding_positions.add(up(dimension, left(dimension, position)))
        surrounding_positions.add(down(dimension, left(dimension, position)))
    if right(dimension, position) is not None:
        surrounding_positions.add(up(dimension, right(dimension, position)))
        surrounding_positions.add(down(dimension, right(dimension, position)))

    surrounding_positions.discard(None)

    return surrounding_positions


def are_chained(positions):
    """
        Check whether the given collection of positions make up a chain.
        - True if and only if each position in the given collection of positions
          can be reached from each other position in that collection.
          A position P1 can be reached from another position P2 if
            (1) P1 and P2 are adjacent to each other, or
            (2) there exists at least one position P3 in the given collection
                of positions that can be reached from both P1 and P2.
       ASSUMPTIONS
       - Each position in the collection of positions is a proper position.
       NOTE
       - This version of the function must be worked out in an iterative way.
         The body may use while statements and/or for statements.
    """

    neighbours_of_each_dot = dict()
    positions_copy = list(set(positions))
    for position in positions_copy:
        adjacent_positions = get_adjacent_positions(position)
        neighbours = list()
        for adjacent_position in adjacent_positions:
            if adjacent_position in positions_copy:
                neighbours.append(adjacent_position)
        neighbours_of_each_dot[position] = neighbours

    if len(neighbours_of_each_dot) == 1:  # als block bestaat uit 1 dot
        return True

    for values in neighbours_of_each_dot.values():  # als een dot geen enkele buur heeft
        if len(values) == 0:
            return False

    total_amount_of_neighbours = 0
    for neighbour_of_each_dot in neighbours_of_each_dot.values():
        total_amount_of_neighbours += len(neighbour_of_each_dot)

    if total_amount_of_neighbours < 2*len(positions_copy)-2:
        return False
    else:
        return True


def adjacent_positions_in_block(positions, block):
    adjacent_and_in_block = set()
    for position in positions:
        adjacents = get_adjacent_positions(position)
        for pos in adjacents:
            if pos in block and pos not in adjacent_and_in_block and pos not in positions:
                adjacent_and_in_block.add(pos)
    return adjacent_and_in_block


def are_chained_rec(positions, chained_positions=[], non_chained_positions=set()):
    """
        Check whether the given collection of positions make up a chain.
        - True if and only if each position in the given collection of positions
          can be reached from each other position in that collection.
          A position P1 can be reached from another position P2 if
            (1) P1 and P2 are adjacent to each other, or
            (2) there exists at least one position P3 in the given collection
                of positions that can be reached from both P1 and P2.
       ASSUMPTIONS
       - Each position in the collection of positions is a proper position.
       NOTE
       - This version of the function must be worked out in a recursive way. The body
         may not use while statements nor for statements.
       TIP
       - Extend the heading of the function with two additional parameters:
          - chained_positions: a frozen set of positions that already form a chain.
          - non_chainable_positions: a frozen set of positions that are not
            adjacent to any of the positions in the set of chained positions.
         Assign both extra parameters the empty frozen set as their default value.
    """
    positions = set(positions)
    if len(positions) == 0:
        # print("True 1")
        return True

    positions_copy = positions.copy()
    #print(positions_copy)
    if len(chained_positions) == 0:
        chained_positions.append(positions_copy.pop())
        non_chained_positions = positions_copy
        # print("oorspronkelijke positions = ",positions)
        # print("chained_positions = ",chained_positions," non_chained (de rest)= ",non_chained_positions)

    if len(chained_positions) == len(positions) or len(non_chained_positions) == 0:
        # print("positions =",positions)
        # print("True 2")
        return True

    adjacent_positions = adjacent_positions_in_block(chained_positions, positions)
    # print("adjacent positions = ", adjacent_positions)
    for adjacent_position in adjacent_positions:
        if adjacent_position not in chained_positions:
            chained_positions.append(adjacent_position)
            non_chained_positions.remove(adjacent_position)
            # print("check")

    if len(adjacent_positions) == 0:
        if len(chained_positions) < len(positions):
            return False
    return are_chained_rec(positions, chained_positions, non_chained_positions)

















