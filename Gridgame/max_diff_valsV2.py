#!/usr/bin/env python

from Agent import MaxAgent
from interestingBoards import findInterestingBoards, playGame

def find_max_diff_vals_idx(optimal_rollout, human_rollout, optimal_scores, human_scores, min_t, min_y, value_fn):
    # Finds index (after min_t) where the corresponding states in the two rollouts
    # have the maximum difference in value
    statePairs = {} #optimal, human states
    for t in range(min_t+1, len(optimal_rollout)):
        for y in range(min_y + 1, len(human_rollout)):
            diff_rewards_sofar = optimal_scores[t] - human_scores[y]
            if abs(diff_rewards_sofar) <= 10:
                diff_val = value_fn(optimal_rollout[t]) - value_fn(human_rollout[y]) - diff_rewards_sofar
                statePairs[(t, y)] = diff_val
    if not statePairs:
        return None, None
    tup = max(statePairs, key = lambda x: statePairs[x]) #TODO: pick later
    # if statePairs[tup] <= 0:
    #     return None, None
    return tup
def value(scores, index, depth):
    return scores[index + depth] - scores[index]


def print_max_diff_vals(optimal_rollout, human_rollout, value_fn, \
                        optimal_scores, human_scores):
    #assert len(optimal_rollout) == len(human_rollout)
    curr_t = 0
    y = 0
    chosen_t = []
    while curr_t+1 < len(optimal_rollout):
        t, y = find_max_diff_vals_idx(optimal_rollout, human_rollout, optimal_scores, human_scores, curr_t, -1, value_fn)
        if t is None:
            break
        print("At human timestep " + str(y) + " and optimal timestep " + str(t) + ":")
        print("From human rollout:\t\t\tFrom optimal rollout:")
        human_board = human_rollout[y].printBoard(print_to_screen=False)
        optimal_board = optimal_rollout[t].printBoard(print_to_screen=False)
        for i in range(len(human_board)):
            print(" ".join(human_board[i]) + "\t\t" + " ".join(optimal_board[i]))
        print("holding: " + str(human_rollout[y].holding) + "\t\t\t\t" + \
              "holding: " + str(optimal_rollout[t].holding))
        print("(score: " + formatScore(human_scores[y]) + ")\t\t\t\t" + \
              "(score: " + formatScore(optimal_scores[t]) + ")")
        print("depth 2 value: " + formatScore(value_fn(human_rollout[y])) + ")\t\t\t\t" + \
              "depth 2 value: " + formatScore(value_fn(optimal_rollout[t])) + ")")
        print()
        curr_t = t
        chosen_t.append(t)
    return chosen_t

def print_whole_rollout(rollout, chosen_t, value_fn, scores):
    for t in range(len(rollout)):
        if t in chosen_t:
            print("[important]")
        rollout[t].printBoard()
        print("(score: " + formatScore(scores[t]) + ")")
        print("(value: " + formatScore(value_fn(rollout[t])) + ")")
        print()

def formatScore(score):
    return format(score, '.2f')

def print_whole_rollouts(rollout1, rollout2, chosen_t, value_fn, scores1, scores2):
    for t in range(max(len(rollout1), len(rollout2))):
        if t in chosen_t:
            print("[important]")
        if t < len(rollout1) and t < len(rollout2):
            board1 = rollout1[t].printBoard(print_to_screen=False)
            board2 = rollout2[t].printBoard(print_to_screen=False)
            for i in range(len(board1)):
                print(" ".join(board1[i]) + "\t\t" + " ".join(board2[i]))
            print("holding: " + str(rollout1[t].holding) + "\t\t\t\t" + \
                  "holding: " + str(rollout2[t].holding))
            print("(score: " + formatScore(scores1[t]) + ")\t\t\t\t" + \
                  "(score: " + formatScore(scores2[t]) + ")")
            print("(value: " + formatScore(value_fn(rollout1[t])) + ")\t\t\t\t" + \
                  "(value: " + formatScore(value_fn(rollout2[t])) + ")")
            print()
        elif t < len(rollout1):
            board1 = rollout1[t].printBoard(print_to_screen=False)
            for i in range(len(board1)):
                print(" ".join(board1[i]))
            print("holding: " + str(rollout1[t].holding))
            print("(score: " + formatScore(scores1[t]) + ")")
            print("(value: " + formatScore(value_fn(rollout1[t])) + ")")
        else:
            board2 = rollout2[t].printBoard(print_to_screen=False)
            for i in range(len(board1)):
                print("                               " + "\t\t" + " ".join(board2[i]))
            print("holding: " + str(rollout2[t].holding))
            print("(score: " + formatScore(scores2[t]) + ")")
            print("(value: " + formatScore(value_fn(rollout2[t])) + ")")



def max_diff_vals_explanation(game=None):
    if game is None:
        game = findInterestingBoards(threshold=30, n_boards=1, numpieces = 4)[0]
    
    k10agent = MaxAgent(depth=10)
    k2agent = MaxAgent(depth=2)
    k1agent = MaxAgent(depth=1)

    scoreK10, rolloutK10, scoresK10 = playGame(game, k10agent, return_rollout=True)
    scoreK2, rolloutK2, scoresK2 = playGame(game, k2agent, return_rollout=True)
    scoreK1, rolloutK1, scoresK1 = playGame(game, k1agent, return_rollout=True)

    value_fn = lambda s: k2agent.value(s)[0]

    print("Comparing against human with k=1")
    print("Starting state:")
    start_board = rolloutK10[0].printBoard(print_to_screen=False)
    for i in range(len(start_board)):
        print(" ".join(start_board[i]))
    k10action = k10agent.getAction(game)
    print("Optimal action:", k10action, "K1 action", k1agent.getAction(game))
    print()
    chosen_t = print_max_diff_vals(rolloutK10, rolloutK1, value_fn, scoresK10, scoresK1)

    # print("Entire human (k=1) rollout:\t\t\tEntire optimal rollout:")
    # print_whole_rollouts(rolloutK1, rolloutK10, chosen_t, value_fn, scoresK1, scoresK10)

    # print("-----")
    print("Comparing against human with k=2")
    print("Starting state:")
    start_board = rolloutK10[0].printBoard(print_to_screen=False)
    for i in range(len(start_board)):
        print(" ".join(start_board[i]))
    print("Optimal action:", k10action, "K2 action", k2agent.getAction(game))
    print()
    # chosen_t = print_max_diff_vals(rolloutK2, rolloutK10, value_fn, scoresK2, scoresK10)
    # print("Entire human (k=2) rollout:\t\t\tEntire optimal rollout:")
    # print_whole_rollouts(rolloutK2, rolloutK10, chosen_t, value_fn, scoresK2, scoresK10)

def main():
    max_diff_vals_explanation()

if __name__ == "__main__":
    main()
