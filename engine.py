import os
import numpy as np

LENGTH = 3 # Board Length, currently supports only 3


class AgentEval:
    def __init__(self, sym, value_sym):
        self.V = value_sym
        self.sym = sym

    def take_action(self, env):
        best_state = None
        pos2value = {}
        next_move = None
        best_value = -1
        for i in range(LENGTH):
            for j in range(LENGTH):
                if env.is_empty(i, j):
                    env.board[i, j] = self.sym
                    state = env.get_state()
                    env.board[i, j] = 0
                    pos2value[(i, j)] = self.V[state]
                    if self.V[state] > best_value:
                        best_value = self.V[state]
                        best_state = state
                        next_move = (i, j)
        env.board[next_move[0], next_move[1]] = self.sym
        return next_move
    
    
class Environment:
    def __init__(self):
        self.board = np.zeros((LENGTH, LENGTH))
        self.x = -1
        self.o = 1
        self.winner = None
        self.ended = False
        self.num_states = 3 ** (LENGTH * LENGTH)

    def is_empty(self, i, j):
        return self.board[i, j] == 0

    def set_state(self, state):
        self.board = np.reshape(state, (LENGTH, LENGTH))
        self.game_over()
        if self.ended:
          print("Please enter a Non terminal state")

    def reward(self, sym):

        if not self.game_over():
            return 0

        return 1 if self.winner == sym else 0

    def get_state(self):

        k = 0
        h = 0
        for i in range(LENGTH):
            for j in range(LENGTH):
                if self.board[i, j] == 0:
                    v = 0
                elif self.board[i, j] == self.x:
                    v = 1
                elif self.board[i, j] == self.o:
                    v = 2
                h += (3 ** k) * v
                k += 1
        return h

    def game_over(self, force_recalculate=False):

        if not force_recalculate and self.ended:
            return self.ended

        # check rows
        for i in range(LENGTH):
            for player in (self.x, self.o):
                if self.board[i].sum() == player * LENGTH:
                    self.winner = player
                    self.ended = True
                    return True

        # check columns
        for j in range(LENGTH):
            for player in (self.x, self.o):
                if self.board[:, j].sum() == player * LENGTH:
                    self.winner = player
                    self.ended = True
                    return True

        # check diagonals
        for player in (self.x, self.o):
            # top-left -> bottom-right diagonal
            if self.board.trace() == player * LENGTH:
                self.winner = player
                self.ended = True
                return True
            # top-right -> bottom-left diagonal
            if np.fliplr(self.board).trace() == player * LENGTH:
                self.winner = player
                self.ended = True
                return True

        if np.all((self.board == 0) == False):
            # winner stays None
            self.winner = None
            self.ended = True
            return True

        self.winner = None
        return False

    def is_draw(self):
        return self.ended and self.winner is None


    def draw_board(self, emt_cell = "   |"):
        for i in range(LENGTH):
            print("-------------------")
            print("|", end="")
            for j in range(LENGTH):
                print("  ", end="")
                if self.board[i, j] == self.x:
                    print("x  |", end="")
                elif self.board[i, j] == self.o:
                    print("o  |", end="")
                else:
                    print(emt_cell, end="")
            print("")
        print("-------------------")


# Example Usage

if __name__ == '__main__':
    
    # Provide a State
    # Symbols X: represented by -1 and O: represented by +1
    state = [[-1, -1, 1],
             [-1, -1, 1],
             [1, 0, 0]]
    
    # Provide a Player
    # Symbols X: represented by 'x' and O: represented by 'o'
    current_player = 'x'

    # Provide path to common folder enclosing 'vx.npy' and 'vo.npy'
    sv_path = ''
    
    env = Environment()
    env.set_state(np.array(state))

    def get_next_action(env, symbol='x', sv_path=''):
        vx_val = np.load(os.path.join(sv_path, 'vx.npy'))
        vo_val = np.load(os.path.join(sv_path, 'vo.npy'))
        x_agent = AgentEval(env.x, vx_val)
        o_agent = AgentEval(env.o, vo_val)
        if symbol == 'x':
            return x_agent.take_action(env)
        else:
            return o_agent.take_action(env)

    best_move = get_next_action(env, symbol=current_player, sv_path=sv_path)
    env.draw_board()
    game_over = env.game_over()
    print(game_over)
    is_draw = env.is_draw()
    print("is_draw", is_draw)