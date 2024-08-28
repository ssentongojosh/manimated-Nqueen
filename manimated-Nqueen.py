from manim import *
from chess_board import ChessBoard
           
class NqueenVisualization(Scene):
    boardStatus = {}
    threatened_columns_set = set()
    threatened_negative_diagonals_set = set()
    threatened_positive_diagonals_set = set()

    def construct(self):
        N = 3
        board = ChessBoard("3/3/3")
        self.add((board).move_to(ORIGIN))
        self.wait()
        self.solution(N,1)

    def solution(self,N,row):
        
        result = []

        if row == N+1:
            return 
        
        for column in range(N):
            if column in NqueenVisualization.threatened_columns_set or (row - column) in NqueenVisualization.threatened_negative_diagonals_set or (row + column) in NqueenVisualization.threatened_positive_diagonals_set:
                continue
            #place queen and update sets
            self.main(row,column)
            NqueenVisualization.threatened_columns_set.add(column)
            NqueenVisualization.threatened_negative_diagonals_set.add(row - column)
            NqueenVisualization.threatened_positive_diagonals_set.add(row + column)

            #recursive call function to place next queen
            self.solution(N,row + 1)

            # backtrack: remove queen and update sets
            NqueenVisualization.threatened_columns_set.remove(column)
            NqueenVisualization.threatened_negative_diagonals_set.remove(row - column)
            NqueenVisualization.threatened_positive_diagonals_set.remove(row + column)
            
            # create function that removes a placed queen
            self.main(row,column,remove=True)
    def main(self,row,column,remove = False):    
        self.N = 3
        for row in range(row,row+1):
            for column in range(column,column+1):
                
                if column == 0 and row < self.N:
                    x = f"Q{self.N-(column+1)}/" * row + f"{self.N}/" * (self.N-(row+1)) + str(self.N)
                    if not remove:
                        self.place_queen(row,column,x)
                    else:
                        self.place_queen(row,column,x,remove = True)    
        
                elif (self.N-(column+1)) == 0 and row < self.N:
                    x = f"{column}Q/" * row + f"{self.N}/" * (self.N-(row+1)) + str(self.N)
                    if not remove:
                        self.place_queen(row,column,x)
                    else:
                        self.place_queen(row,column,x,remove = True) 
    
                elif row >= self.N:
                    if column == 0:     
                        x = f"Q{self.N-(column+1)}/" * (row-1) + f"Q{self.N-(column+1)}"
                        if not remove:
                            self.place_queen(row,column,x)
                        else:
                            self.place_queen(row,column,x,remove = True) 
                        
                    elif (self.N-(column+1)) == 0:
                        x = f"{column}Q/" * (row-1) + f"{column}Q"
                        if not remove:
                            self.place_queen(row,column,x)
                        else:
                            self.place_queen(row,column,x,remove = True) 
                        
                    else:
                        x = f"{column}Q{self.N-(column+1)}/" * (row-1) + f"{column}Q{self.N-(column+1)}" 
                        if not remove:
                            self.place_queen(row,column,x)
                        else:
                            self.place_queen(row,column,x,remove = True) 

                else:
                    x = f"{column}Q{self.N-(column+1)}/" * row + f"{self.N}/" * (self.N-(row+1)) + str(self.N)
                    if not remove:
                        self.place_queen(row,column,x)
                    else:
                        self.place_queen(row,column,x,remove = True) 
                        

    def fenstring_generator(self,row,x):
        list2 = x.split("/")
        square = list2[0]
        for   i in range(row-1):
            list2.remove(square)
            list2.insert(i,"3") 
        fenstring = "/".join(list2)
        return fenstring

    def place_queen(self,row,column,x,remove = False):
        board = ChessBoard(self.fenstring_generator(row,x))
        if not remove:
            self.add(board.move_to(ORIGIN))
            self.wait()
            NqueenVisualization.boardStatus[x] = board
        else:
            y = list(NqueenVisualization.boardStatus.items())[-1][0]
            boardy = list(NqueenVisualization.boardStatus.items())[-1][1]
            self.remove_queen(row,column,y,boardy) 
        
    def remove_queen(self,row,column,x,board):
        fade_out,movement = board.move_piece(row-1, column, row-1, column)
        self.add((board).move_to(ORIGIN))
        self.play(fade_out)
        self.wait()
        NqueenVisualization.boardStatus.popitem()
            

    
        

    
        

        

    


    
        
