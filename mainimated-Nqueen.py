from manim import *
from chess_board import ChessBoard
           
class NqueenVisualization(Scene):
    

    def construct(self):
        board = ChessBoard("3/3/3")
        self.add((board).move_to(ORIGIN))
        self.wait()
        self.solution(3,1)

    def solution(self,N,row):
        threatened_columns_set = set()
        threatened_negative_diagonals_set = set()
        threatened_positive_diagonals_set = set()
        result = []

        if row == N+1:
            return 
        
        for column in range(N):
            
            if column in threatened_columns_set or (row - column) in threatened_negative_diagonals_set or (row + column) in threatened_positive_diagonals_set:
                continue
            self.main(row,column)
            threatened_columns_set.add(column)
            threatened_negative_diagonals_set.add(row - column)
            threatened_positive_diagonals_set.add(row + column)
            self.solution(N,row + 1)
            threatened_columns_set.remove(column)
            threatened_negative_diagonals_set.remove(row - column)
            threatened_positive_diagonals_set.remove(row + column)
            # create function that removes a placed queen

    def main(self,row,column,remove = False):    
        self.N = 3
        for row in range(row,row+1):
            for column in range(column,column+1):
                
                if column == 0 and row < 3:
                    x = f"Q{self.N-(column+1)}/" * row + f"{self.N}/" * (self.N-(row+1)) + str(self.N)
                    if remove == False:
                        self.place_queen(row,column,x)
                    else:
                        self.place_queen(row,column,x,remove = True)    
        
                elif (self.N-(column+1)) == 0 and row < 3:
                    x = f"{column}Q/" * row + f"{self.N}/" * (self.N-(row+1)) + str(self.N)
                    if remove == False:
                        self.place_queen(row,column,x)
                    else:
                        self.place_queen(row,column,x,remove = True) 
    
                elif row >= 3:
                    if column == 0:     
                        x = f"Q{self.N-(column+1)}/" * (row-1) + f"Q{self.N-(column+1)}"
                        if remove == False:
                            self.place_queen(row,column,x)
                        else:
                            self.place_queen(row,column,x,remove = True) 
                        
                    elif (self.N-(column+1)) == 0:
                        x = f"{column}Q/" * (row-1) + f"{column}Q"
                        if remove == False:
                            self.place_queen(row,column,x)
                        else:
                            self.place_queen(row,column,x,remove = True) 
                        
                    else:
                        x = f"{column}Q{self.N-(column+1)}/" * (row-1) + f"{column}Q{self.N-(column+1)}" 
                        if remove == False:
                            self.place_queen(row,column,x)
                        else:
                            self.place_queen(row,column,x,remove = True) 

                else:
                    x = f"{column}Q{self.N-(column+1)}/" * row + f"{self.N}/" * (self.N-(row+1)) + str(self.N)
                    if remove == False:
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
        self.add((board).move_to(ORIGIN))
        self.wait()
        
    def remove_queen(self,row,column,x,board):
        fade_out,movement = board.move_piece(row-1, column, row-1, column)
        self.play(fade_out)
        self.wait()    

    
        

    
        

    
        

        

    


    
        
