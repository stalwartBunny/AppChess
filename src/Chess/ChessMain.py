#This file handles user input and current game state object.

import pygame as p
from modules import ChessEngine

WIDTH = HEIGHT = 512 #based on image files
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
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
    p.display.set_caption('Chess App')
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("blue"))
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False
    print(gs.board)
    loadImages()
    running = True
    sqSelected = () #(tuple: (row, col))
    playerClicks = [] #(two tuples: [(row,col), (row,col)] )
    moveUndone = True
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
    #mouse handler below (don't fight the Mouse, the Mouse always wins)
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                if sqSelected == (row, col) or (col >= 8):
                    sqSelected = ()
                    playerClicks = []
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected)
                if len(playerClicks) == 2:
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                    print(move.getChessNotation())
                    print(validMoves)
                    for i in range(len(validMoves)):
                        if move in validMoves:
                            gs.makeMove(move)
                            moveMade = True
                            sqSelected = () #empties player clicks
                            playerClicks = [] #empties player clicks
                if not moveMade:
                    playerClicks = [sqSelected]

        #keyboard inputs
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z: #the key 'z' is pressed
                    gs.undoMove()
                    moveMade = True

        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False

        drawGameState(screen, gs, validMoves, sqSelected)
        clock.tick(MAX_FPS)
        p.display.flip()


#handles all graphic states
def drawGameState(screen, gs, validMoves, sqSelected):
    drawBoard(screen)
    highlightSquares(screen, gs, validMoves, sqSelected)
    drawPieces(screen, gs.board)

def drawBoard(screen):
        colors = [p.Color('white'), p.Color('gray')]
        for r in range(DIMENSION):
            for c in range(DIMENSION):
                color = colors[((r+c)%2)]
                p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def highlightSquares(screen, gs, validMoves, sqSelected):
    if sqSelected != ():
        r, c = sqSelected

        if gs.board[r][c][0] == ("w" if gs.whiteToMove else "b"):
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100)
            s.fill(p.Color("green"))
            screen.blit(s, (c * SQ_SIZE, r * SQ_SIZE))
            s.fill(p.Color("blue"))
            for move in validMoves:
                if (move.startRow == r and move.startCol == c):
                    screen.blit(s, (move.endCol * SQ_SIZE, move.endRow * SQ_SIZE))



def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

if __name__ == "__main__":
    main()

main()
