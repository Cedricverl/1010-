import Position


def make_block(dot_positions):
    """
       Create a new block involving the given mutable set of dot positions.
       ASSUMPTIONS
       - The given set of dot positions is not empty and each of its
         elements is a proper position.
       - The given dot positions are chained together.
    """
    return set(dot_positions)


def get_all_dot_positions(block):
    """
        Return a mutable set of all the dot positions of the given block.
        - Dot positions are relative towards the block's anchor.
        ASSUMPTIONS
        - The given block is a proper block.
    """
    return set(block)


def is_proper_block(block):
    """
        Check whether the given block is a proper block.
        - True if and only if the set of dot positions of the given block is not empty,
          if each of its elements is a proper position, and if the dot positions of the
          given block are chained together.
        ASSUMPTIONS:
        - None
    """
    if len(block) == 0:
        return False
    if type(block) != set:
        return False
    for dot in block:
        if not Position.is_proper_position(dot):
            return False
    if not Position.are_chained_rec(block):
        return False
    else:
        return True


def add_dot(block, dot_position):
    """
        Add the given dot position to the given block.
        - Nothing happens if the given block already has a dot at the given position, or
          if the given dot cannot be chained with existing dots of the given block.
        ASSUMPTIONS
        - The given block is a proper block.
        - The given position is a proper position.
    """
    # Block is a set so no double dots will be added
    if Position.is_adjacent_to(dot_position, block):
        block.add(dot_position)


def remove_dot(block, dot_position):
    """
        Remove the given dot position from the given block.
        - Nothing happens if the given dot is not part of the given block, if the
          given block only has the dot to be removed as its single dot, or if the dots
          in the resulting block can no longer be chained.
        ASSUMPTIONS
        - The given block is a proper block.
        - The given position is a proper position.
    """
    if len(block) > 1:
        if Position.are_chained(block.difference({dot_position})):
            block.discard(dot_position)


def get_horizontal_offsets_from_anchor(block):
    """
        Return the horizontal offsets from the anchor of this block.
        - The function returns a tuple involving the smallest horizontal offset
          to the left of the anchor, followed by the largest horizontal offset
          to the right the anchor.
          More formally, if the function returns the tuple (L,R), then for each dot
          position (x,y) of the given block, L <= x <= R
        ASSUMPTIONS
        - The given block is a proper block.
    """
    most_right_element = None
    most_left_element = None
    for dot in block:
        if most_left_element is None or dot[0] < most_left_element:
            most_left_element = dot[0]
        if most_right_element is None or dot[0] > most_right_element:
            most_right_element = dot[0]
    return most_left_element, most_right_element


def get_vertical_offsets_from_anchor(block):
    """
        Return the vertical offsets from the anchor of this block.
        - The function returns a tuple involving the smallest vertical offset
          below the anchor, followed by the largest vertical offset above the anchor.
          More formally, if the function returns the tuple (B,A), then for each dot
          position (x,y) of the given block, B <= y <= A
        ASSUMPTIONS
        - The given block is a proper block.
    """
    most_up_element = None
    most_down_element = None
    for dot in block:
        if most_up_element is None or dot[1] > most_up_element:
            most_up_element = dot[1]
        if most_down_element is None or dot[1] < most_down_element:
            most_down_element = dot[1]
    return most_down_element, most_up_element


def get_most_central_dot(block):
    """returns the most central dot in a block wich is always the same for each block no matter the anchor"""
    sum_x = 0
    sum_y = 0
    for dot in block:
        sum_x += dot[0]
        sum_y += dot[1]
    average_x = sum_x//len(block)
    average_y = sum_y//len(block)
    return average_x, average_y


def are_equivalent(block, other_block):
    """
       Check whether the given blocks are equivalent, i.e. cover equivalent
       chains of dots.
       - A block is equivalent with some other block , if there exists a position
         for the anchor of the one block such that the set of dots covered by that
         block relative towards that anchor position, is identical to the set of
         dots covered by the other block.
        ASSUMPTIONS
        - Both given blocks are proper blocks.
    """
    other_block_edit = other_block.copy()
    other_block_moved = set()
    # if block positions are equivalent:
    if block == other_block:
        return True

    # if block positions are not equivalent (but relatively the same):
    elif len(block) == len(other_block):
        central_dot, central_other_dot = get_most_central_dot(block), get_most_central_dot(other_block)
        x_offset, y_offset = central_other_dot[0] - central_dot[0], central_other_dot[1] - central_dot[1]

        # translate other_block until both central_dots matches
        for dot in other_block_edit:
            other_block_moved.add((dot[0] - x_offset, dot[1] - y_offset),)

        if other_block_moved == block:
            return True
        else:
            return False


def is_normalized(block):
    """
       Check whether the given block is normalized.
       - True if and only if the anchor of the given block is one of the dot positions
         of that block.
       ASSUMPTIONS
       - The given block is a proper block.
    """
    if (0, 0) in block:
        return True
    return False


def normalize(block):
    """
       Return a new block that is a normalized version of the given block.
       - The resulting block must be equivalent with the given block.
       - The function is free to choose a proper anchor for the normalized
         block.
       ASSUMPTIONS
       - The given block is a proper block.
    """
    if is_normalized(block):
        return block

    else:
        block_editable = block.copy()
        new_block = {(0, 0), }
        # Pick a dot from block to be the new anchor
        new_anchor = block_editable.pop()

        # translate the other dots in block so block has the same shape relative to anchor
        for dot in block_editable:
            new_block.add((dot[0] - new_anchor[0], dot[1] - new_anchor[1]),)

    return new_block


def print_block(block):
    """
        Print the given block on the standard output stream.
        - The anchor of the given block will be revealed in the print-out.
        ASSUMPTIONS
        - The given block is a proper block.
    """
    horizontal_offsets = get_horizontal_offsets_from_anchor(block)
    width = max(horizontal_offsets[1], 0) - min(horizontal_offsets[0], 0) + 1
    vertical_offsets = get_vertical_offsets_from_anchor(block)
    height = max(vertical_offsets[1], 0) - min(vertical_offsets[0], 0) + 1
    printout = [[" " for column in range(1, width + 1)]
                for row in range(1, height + 1)]
    dot_positions = get_all_dot_positions(block)
    for (column, row) in dot_positions:
        printout[row - min(vertical_offsets[0], 0)]\
            [column - min(horizontal_offsets[0], 0)] = "\u25A9"
    if (0, 0) in dot_positions:
        anchor_symbol = "\u25A3"
    else:
        anchor_symbol = "\u25A2"
    printout[-min(vertical_offsets[0], 0)][-min(horizontal_offsets[0], 0)] = anchor_symbol
    for row in range(len(printout) - 1, -1, -1):
        for col in range(0, len(printout[0])):
            print(printout[row][col], end=" ")
        print()


# collection of standard blocks used to play the game.


standard_blocks = \
    (  # Single dot
        make_block({(0, 0)}),
        # Horizontal line of length 2
        make_block({(0, 0), (1, 0)}),
        # Horizontal line of length 3
        make_block({(-1, 0), (0, 0), (1, 0)}),
        # Horizontal line of length 4
        make_block({(-3, 0), (-2, 0), (-1, 0), (0, 0)}),
        # Horizontal line of length 5
        make_block({(0, 2), (1, 2), (2, 2), (3, 2), (4, 2)}),
        # Vertical line of length 2
        make_block({(0, 0), (0, 1)}),
        # Vertical line of length 3
        make_block({(0, -1), (0, 0), (0, 1)}),
        # Vertical line of length 4
        make_block({(-2, 2), (-2, 3), (-2, 4), (-2, 5)}),
        # Vertical line of length 5
        make_block({(0, -6), (0, -5), (0, -4), (0, -3), (0, -2)}),
        # T-squares 1x1
        make_block({(-1, 0), (0, 0), (0, 1)}),
        make_block({(0, 0), (0, 1), (1, 0)}),
        make_block({(0, 0), (0, -1), (1, 0)}),
        make_block({(-1, 0), (0, 0), (0, -1)}),
        # T-squares 2x2
        make_block({(-2, 0), (-1, 0), (0, 0), (0, 1), (0, 2)}),
        make_block({(0, 2), (1, 2), (2, 2), (2, 1), (2, 0)}),
        make_block({(2, 0), (1, 0), (0, 0), (0, -1), (0, -2)}),
        make_block({(-2, -2), (-1, -2), (0, -2), (-2, -1), (-2, 0)}),
        # Square block 2x2
        make_block({(0, 0), (1, 0), (0, 1), (1, 1)}),
        # Square block 3x3
        make_block({(0, 0), (1, 0), (2, 0), (0, 1), (1, 1), (2, 1), (0, 2), (1, 2), (2, 2)}),
        # T 3x2
        make_block({(-1,0),(0,0),(1,0),(0,1)}),
        make_block({(-1, 0), (0, 0), (1, 0), (0, -1)}),
        make_block({(-1,0),(0,0),(0,1),(0,-1)}),
        make_block({(1, 0), (0, 0), (0, 1), (0, -1)}),
        # L 3x2
        make_block({(-1, 0), (-2, 0), (0, 0), (0, 1)}),
        make_block({(-1, 0), (-2, 0), (0, 0), (0, -1)}),
        make_block({(-1, 0), (-2, 0), (0, 0), (-2, -1)}),
        make_block({(-1, 0), (-2, 0), (0, 0), (-2, 1)}),
        make_block({(-1, 0), (0, 1), (0, 0), (0, 2)}),
        make_block({(1, 0), (0, 1), (0, 0), (0, 2)}),
        make_block({(1, 2), (0, 1), (0, 0), (0, 2)}),
        make_block({(-1, 2), (0, 1), (0, 0), (0, 2)}),

        # # Dick
        #  make_block({(-1,0), (-1,1), (-2,0), (-2, 1), (0,0),(0,1),(0,2),(0,3),(1,0),(1,1),(1,2),(1,3),(2,0),(2,1),(3,0),(3,1),(0,4),(1,4),(1,5),(0,5)}),
        # # Nazi
        #  make_block({(-2,2), (0,2), (1,2), (2,2), (-2,1), (0,1), (-2,0), (-1,0), (0,0), (1,0), (2,0), (0,-1), (2,-1), (-2,-2), (-1,-2), (0, -2), (2,-2)})
    )


def select_standard_block():
    """
        Return one of the standard blocks.
        - The resulting block is selected randomly.
    """
    import random

    return random.choice(standard_blocks)
