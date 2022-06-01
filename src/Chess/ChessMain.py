#This file handles user input and current game state object.

import pygame as p
from modules import ChessEngine

WIDTH = HEIGHT = 512 #based on image files
DIMENSION = 8
SQ_SIZE = HEIGHT / DIMENSION
MAX_FPS = 24
IMAGES = {}

def loadImages():
    pieces = ["wp", "bp", "wR", "bR", "wN", "bN", "wB", "bB", "wQ", "bQ", "wK", "bK"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))
    #is accessible from IMAGES["*"]


#Main Driver handles inputs and realtime graphics
def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("blue"))
    gs = ChessEngine.GameState()
    print(gs.board)
    loadImages()
    running = True
    sqSelected = () #(tuple: (row, col))
    playerClicks = [] #(two tuples: [(row,col), (row,col)] )
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                if sqSelected == (row, col):
                    sqSelected = ()
                    playerClicks = []
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected)
                if len(playerClicks) == 2:
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                    print(move.getChessNotation())
                    gs.makeMove(move)
                    sqSelected = () #empties player clicks
                    playerClicks = [] #empties player clicks

        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()

if __name__ == "__main__":
    main()

#handles all graphic states
def drawGameState(screen, gs):
    drawBoard(screen)
    drawPieces(screen, gs.board)

def drawBoard(screen):
        colors = [p.Color('white'), p.Color('gray')]
        for r in range(DIMENSION):
            for c in range(DIMENSION):
                color = colors[((r+c)%2)]
                p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

main()
