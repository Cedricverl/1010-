import Position
import Block
import Board
import random
import itertools
def highest_score(board, blocks, start=0):
    """
        Return the highest possible score that can be obtained by dropping
        all the blocks in the given sequence of blocks starting from the given
        start index in the order from left to right on the given board.
        - If a solution is possible, the function actually returns a tuple
          consisting of the highest score followed by a list of all positions
          at which the successive blocks must be dropped.
        - If the highest score can be reached in several possible ways, the
          function will give preference to the smallest position in the sense of
          the standard tuple comparison in Python (see section 6.7 of the book).
          For example, if there are two solutions s1 and s2 and s1 < s2, s1 will
          be returned.
        - If no solution is possible, the function returns the tuple (None,None).
        - At the end of the function, the board must still be in the same
          state it was in at the start of the function.
        ASSUMPTIONS
        - The given board is a proper board.
        - Each block in the given sequence of blocks is a proper block.
        - The given start index is not negative, but may be beyond the last element
          in the sequence of blocks.
        NOTE
        - You are allowed to take a copy of the given board.
        - You are not allowed to extend the heading of the function with
          additional parameters, nor to introduce an auxiliary function
          to be able to pass additional information.
        - The function should be worked out in a recursive way.
    """
    # base case
    if start == len(blocks):
        return 0, []

    droppable_positions = Board.get_droppable_positions(board, blocks[start])

    max_score = 0
    max_result = None, None

    for droppable_position in droppable_positions:
        # use a copy board
        board_try = Board.copy_board(board)

        # Get the score of droppable position
        score = game_move(board_try, blocks[start], droppable_position)

        # recursion step until base case
        result = highest_score(board_try, blocks, start+1)

        # add result to previous result if not None
        if result is not (None, None):
            result = (result[0] + score, [droppable_position] + result[1])

        # if score of result is greater than max_score, change max_score
        if result[0] is not None and result[0] > max_score:
            max_score = result[0]
            max_result = result

    return max_result


def turn_in_triplets(blocks):
    """returns a list into a list of lists consisting of triplets"""
    triplet_list = []
    if len(blocks) <= 3:
        return [blocks]
    for i in range(2,len(blocks)+1,3):
        triplet = blocks[i-2:i+1]
        triplet_list.append(triplet)
    return triplet_list

def turn_in_lists(permutations):
    """turns the list with tuples into list with lists (highest_score needs lists)"""
    permutations_list = []
    for permutation in permutations:
        permutations_list.append(list(permutation))
    return permutations_list

def play_greedy(board, blocks):
    """
        Drop the given sequence of blocks in the order from left to right on
        the given board in a greedy way.
        - The function will take blocks in triplets (groups of 3) in the order from
          left tot right, and drop them on the given board in the best possible way
          (i.e yielding the highest possible score) not taking into account blocks
          that still need to be dropped further on.
        - If the number of blocks is not a multiple of 3, the function will take the
          remaining blocks (1 or 2) in the last step.
        - The function will search for the best possible positions to drop each
          of the 3 blocks in succession. If several positions yield the same highest
          score, the function will give preference to positions closest to the bottom
          left corner.
        - If a solution is possible, the function returns the total score obtained
          from dropping all the blocks.
        - If no solution is possible, the function returns None. All the blocks that
          could be dropped are effectively dropped on the given board.
        ASSUMPTIONS
        - The given board is a proper board.
        - The number of blocks in the given sequence of blocks is a multiple of 3.
    """
    if len(blocks) == 0:
        return 0

    triplets = turn_in_triplets(blocks)
    # print("triplets = ",triplets)
    final_max_result = 0

    for triplet in triplets:
        # Store the information of the max score and how to get it (for game_move later on)
        max_result = {"max_score": None,"max_positions": None,"max_block_permutation": None}

        # get a list of tuples with all possible permutations (this length max 3!)
        all_triplet_permutations = list(itertools.permutations(triplet))

        # get a list of lists with all possible permutations (highest_score wants a list)
        all_triplet_permutations = turn_in_lists(all_triplet_permutations)

        # try each permutation of a triplet and see which permutation yeelds the highest score
        for triplet_permutation in all_triplet_permutations:

            highest_score_result = highest_score(board, triplet_permutation)

            if max_result["max_score"] is None:
                # print("max_result['max_score'] is none so replace it with highest score")
                max_result["max_score"] = highest_score_result[0]
                max_result["max_positions"] = highest_score_result[1]
                max_result["max_block_permutation"] = triplet_permutation

            elif highest_score_result[0] is not None and highest_score_result[0] > max_result["max_score"]:
                max_result["max_score"] = highest_score_result[0]
                max_result["max_positions"] = highest_score_result[1]
                max_result["max_block_permutation"] = triplet_permutation

        # add the max_score to final_max_result and make all the game_moves for the permutation that yeelds max score
        if max_result["max_score"] is not None:
            # print("max_score of max_result is not None...")
            for i in range(0, len(max_result["max_positions"])):
                game_move(board, max_result["max_block_permutation"][i], max_result["max_positions"][i])
            final_max_result += max_result["max_score"]
        # if max score is None, no score will be achieved and no blocks will be placed
        else:
            # print("return None")
            return None
    return final_max_result


def game_move(board, block, position):
    """
        Drop the given block at the given position on the given board, and
        clear all full rows and columns, if any, after the drop.
        - The function returns the score obtained from the give move.
        ASSUMPTIONS
        - The given board is a proper board
        - The given block is a proper block.
        - The given position is a proper position.
        - The given block can be dropped at the given position on the given
          board.
    """
    Board.drop_at(board, block, position)
    nb_filled_seqs = \
        len(Board.get_all_filled_columns(board)) + \
        len(Board.get_all_filled_rows(board))
    Board.clear_full_rows_and_columns(board)
    return \
        len(Block.get_all_dot_positions(block)) + \
        10 * ((nb_filled_seqs + 1) * nb_filled_seqs) // 2


def play_game():
    """
        Play the game.
    """
    the_board = Board.make_board(5)
    score = 0
    current_block = Block.select_standard_block()
    print("Score: ", score)
    print()
    print("Next block to drop:")
    Block.print_block(current_block)
    print()
    Board.print_board(the_board)
    print()

    while len(Board.get_droppable_positions(the_board, current_block)) > 0:

        position = input("Enter the position to drop the block: ")
        if position == "":
            position = \
                random.choice(Board.get_droppable_positions(the_board, current_block))
            print("   Using position: ", position[0], ",", position[1])
        else:
            position = eval(position)
            if not isinstance(position, tuple):
                print("Not a valid position")
                continue

        if not Board.can_be_dropped_at(the_board, current_block, position):
            print("Block cannot be dropped at the given position")
            continue

        score += game_move(the_board, current_block, position)

        current_block = Block.select_standard_block()
        print("Score: ", score)
        print()
        print("Next block to drop:")
        Block.print_block(current_block)
        print()
        Board.print_board(the_board)
        print()

    print("End of game!")
    print("   Final score: ", score)


if __name__ == '__main__':
    play_game()