from player import Player
import random
import math

class AlphaBetaPlayer(Player):
    def get_next_move(self):     
        return self.minimax([], 6, True, -math.inf, math.inf)[1]
        
    def next_moves(self, node, player):
        moves = []
        self.board.start_imagination()
        for (i, j), p in node:
            self.board.imagine_placing_piece(p, i, j)
        for i in range(self.board.get_n()):
            for j in range(self.board.get_n()):
                if self.board.is_imaginary_move_valid(player, i, j):
                    moves.append((i, j))
        return moves

    def score(self, node, player):
        self.board.start_imagination()
        scores = self.board.get_scores()
        for (i, j), p in node:
            c = self.board.imagine_placing_piece(p, i, j)
            scores[p] += c
        opponent = 0 if player else 1
        n = self.board.get_n()
        corners = [(0, 0), (0, n-1), (n-1, 0), (n-1, n-1)]
        s = scores[player] - scores[opponent]
        for corner in corners:
            if (corner[0], corner[1], player) in node:
                s += n
            if (corner[0], corner[1], opponent) in node:
                s -= n
        return s
            
    def minimax(self, node, depth, isMax, alpha, beta):
        player = self.player_number if isMax else self.opponent_number
        moves = self.next_moves(node, player)
        chosen = None
        if len(moves) == 0 or depth == 0:
            return self.score(node, player), chosen
        if isMax :
            bestVal = -math.inf 
            for move in moves:
                value, _ = self.minimax(node + [(move, player)], depth-1, False, alpha, beta)
                if bestVal < value:
                    bestVal = value
                    chosen = move
                alpha = max( alpha, bestVal)
                if beta <= alpha:
                    break
            return bestVal, chosen
        else :
            bestVal = math.inf 
            for move in moves:
                value, _ = self.minimax(node + [(move, player)], depth-1, True, alpha, beta)
                if bestVal > value:
                    bestVal = value
                    chosen = move
                beta = min( beta, bestVal)
                if beta <= alpha:
                    break
            return bestVal, chosen