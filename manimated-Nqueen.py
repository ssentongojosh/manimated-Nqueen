from manim import *
from chess_board import ChessBoard

# To find ALL solutions instead of just the first one:
# Change self.find_all_solutions = True in the __init__ method
           
class NqueenVisualization(Scene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.N = 4
        self.board = None
        self.queen_positions = []
        self.highlight_squares = []
        self.queen_pieces = {}  # Track queen pieces by their positions
        self.threatened_columns_set = set()
        self.threatened_negative_diagonals_set = set()
        self.threatened_positive_diagonals_set = set()
        self.find_all_solutions = False  # Set to True to find all solutions
        self.solutions_found = 0

    def construct(self):
        self.board = ChessBoard("4/4/4/4")
        self.add(self.board.move_to(ORIGIN))
        self.wait()
        
        # Add title to show mode
        if self.find_all_solutions:
            title = Text("N-Queens: Finding All Solutions", font_size=24)
            title.to_edge(UP)
            self.add(title)
        
        self.solution(0)  # Start from row 0, not 1
        
        # Show final summary
        if self.find_all_solutions:
            summary = Text(f"Total Solutions Found: {self.solutions_found}", font_size=20)
            summary.to_edge(DOWN)
            self.play(Write(summary))
            self.wait(3)

    def solution(self, row):
        if row == self.N:
            # Found a complete solution
            self.solutions_found += 1
            
            # Clear any existing highlights
            self.clear_highlights()
            
            # Highlight the entire board green to show solution
            self.highlight_solution_board()
            
            if self.find_all_solutions:
                # Show solution number
                solution_text = Text(f"Solution #{self.solutions_found}", font_size=18, color=GREEN)
                solution_text.next_to(self.board, RIGHT, buff=1)
                self.play(Write(solution_text), run_time=0.5)
                self.wait(2)  # Show solution longer
                self.play(FadeOut(solution_text), run_time=0.3)
                
                # Remove green highlights before continuing
                self.clear_solution_highlights()
                
                # Continue searching for more solutions
                return False  # Don't stop, continue the search
            else:
                # Show single solution and stop
                solution_text = Text("Solution Found!", font_size=24, color=GREEN, weight=BOLD)
                solution_text.next_to(self.board, UP, buff=1)
                self.play(Write(solution_text), run_time=0.8)
                self.wait(3)  # Show complete solution longer
                return True
        
        for column in range(self.N):
            if self.is_safe(row, column):
                # Place queen first (or move existing queen)
                self.place_or_move_queen(row, column)
                
                # Then show threatened squares
                self.highlight_threatened_squares(row, column)
                
                # Recursive call
                if self.solution(row + 1):
                    # Only return True if we're not finding all solutions
                    if not self.find_all_solutions:
                        return True
                    
                # If we reach here, the recursive call failed or we're finding all solutions
                # Clear highlights before trying next position
                self.clear_highlights()
        
        # If we exit the loop, no safe column was found in this row
        # Show "No Safe Squares" feedback
        if row > 0:  # Don't show for the first row
            self.show_no_safe_squares_feedback(row)
        
        # Remove the queen from this row before backtracking
        if self.queen_positions and any(pos[0] == row for pos in self.queen_positions):
            # Find the queen in this row
            for pos_row, pos_col in self.queen_positions:
                if pos_row == row:
                    self.remove_queen(row, pos_col)
                    break
        
        return False

    def is_safe(self, row, col):
        """Check if placing a queen at (row, col) is safe"""
        for queen_row, queen_col in self.queen_positions:
            if (queen_col == col or 
                queen_row - queen_col == row - col or 
                queen_row + queen_col == row + col):
                return False
        return True

    def highlight_threatened_squares(self, row, col):
        """Highlight squares that would be threatened by placing a queen at (row, col)"""
        # Clear previous highlights first
        self.clear_highlights()
        
        threat_squares = []
        
        # Same row
        for c in range(self.N):
            if c != col:
                threat_squares.append((row, c))
        
        # Same column
        for r in range(self.N):
            if r != row:
                threat_squares.append((r, col))
        
        # Diagonal (top-left to bottom-right)
        for i in range(1, self.N):
            # Upper diagonal
            if row - i >= 0 and col - i >= 0:
                threat_squares.append((row - i, col - i))
            # Lower diagonal
            if row + i < self.N and col + i < self.N:
                threat_squares.append((row + i, col + i))
        
        # Diagonal (top-right to bottom-left)
        for i in range(1, self.N):
            # Upper diagonal
            if row - i >= 0 and col + i < self.N:
                threat_squares.append((row - i, col + i))
            # Lower diagonal
            if row + i < self.N and col - i >= 0:
                threat_squares.append((row + i, col - i))
        
        # Create highlight squares using board's square_size
        highlights_to_add = []
        for threat_row, threat_col in threat_squares:
            highlight = Square(
                side_length=self.board.square_size,
                fill_color=RED,
                fill_opacity=0.3,
                stroke_opacity=0
            )
            # Position the highlight at the correct square using board's square positions
            target_square = self.board.squares[threat_row][threat_col]
            highlight.move_to(target_square.get_center())
            
            self.highlight_squares.append(highlight)
            highlights_to_add.append(highlight)
        
        # Animate all highlights appearing at once for better performance
        if highlights_to_add:
            self.play(*[FadeIn(highlight) for highlight in highlights_to_add], run_time=0.3)
        
        self.wait(0.5)

    def clear_highlights(self):
        """Remove all highlight squares"""
        if self.highlight_squares:
            self.play(*[FadeOut(highlight) for highlight in self.highlight_squares], run_time=0.2)
            self.highlight_squares = []

    def highlight_solution_board(self):
        """Highlight the entire board green to show a solution"""
        green_highlights = []
        for row in range(self.N):
            for col in range(self.N):
                highlight = Square(
                    side_length=self.board.square_size,
                    fill_color=GREEN,
                    fill_opacity=0.4,
                    stroke_opacity=0
                )
                target_square = self.board.squares[row][col]
                highlight.move_to(target_square.get_center())
                green_highlights.append(highlight)
        
        # Store green highlights separately
        self.solution_highlights = green_highlights
        
        # Animate all green highlights appearing
        self.play(*[FadeIn(highlight) for highlight in green_highlights], run_time=0.5)

    def clear_solution_highlights(self):
        """Remove green solution highlights"""
        if hasattr(self, 'solution_highlights') and self.solution_highlights:
            self.play(*[FadeOut(highlight) for highlight in self.solution_highlights], run_time=0.3)
            self.solution_highlights = []

    def show_no_safe_squares_feedback(self, row):
        """Show feedback when no safe squares are found"""
        feedback_text = Text(f"No safe squares in row {row}", font_size=16, color=RED)
        feedback_text.next_to(self.board, DOWN, buff=0.5)
        
        # Flash the feedback message
        self.play(Write(feedback_text), run_time=0.4)
        self.wait(0.8)
        self.play(FadeOut(feedback_text), run_time=0.3)

    def place_or_move_queen(self, row, col):
        """Place a new queen or move existing queen to the specified position"""
        # Check if there's already a queen in this row
        existing_queen_col = None
        for pos_row, pos_col in self.queen_positions:
            if pos_row == row:
                existing_queen_col = pos_col
                break
        
        if existing_queen_col is not None:
            # Move existing queen to new position
            self.move_queen(row, existing_queen_col, row, col)
        else:
            # Place new queen
            self.place_queen(row, col)

    def place_queen(self, row, col):
        """Place a queen at the specified position"""
        self.queen_positions.append((row, col))
        
        # Create and animate a new queen piece directly
        queen = self.create_queen_piece()
        target_square = self.board.squares[row][col]
        queen.move_to(target_square.get_center())
        
        # Store reference to the queen piece
        self.queen_pieces[(row, col)] = queen
        
        # Animate the queen appearing
        self.play(FadeIn(queen), run_time=0.5)
        self.wait(0.3)

    def move_queen(self, from_row, from_col, to_row, to_col):
        """Smoothly move a queen from one position to another"""
        # Clear highlights first
        self.clear_highlights()
        
        # Update queen_positions list
        if (from_row, from_col) in self.queen_positions:
            self.queen_positions.remove((from_row, from_col))
        self.queen_positions.append((to_row, to_col))
        
        # Get the queen piece and target square
        queen = self.queen_pieces.get((from_row, from_col))
        if queen:
            target_square = self.board.squares[to_row][to_col]
            
            # Animate smooth movement
            self.play(queen.animate.move_to(target_square.get_center()), run_time=0.8)
            
            # Update queen piece reference
            del self.queen_pieces[(from_row, from_col)]
            self.queen_pieces[(to_row, to_col)] = queen
            
        self.wait(0.3)

    def remove_queen(self, row, col):
        """Remove the queen from the specified position"""
        if (row, col) in self.queen_positions:
            self.queen_positions.remove((row, col))
        
        # Clear highlights first
        self.clear_highlights()
        
        # Find and remove the queen piece at this position
        queen = self.queen_pieces.get((row, col))
        if queen:
            # Animate removal
            self.play(FadeOut(queen), run_time=0.5)
            # Remove from tracking dictionary
            del self.queen_pieces[(row, col)]
        
        self.wait(0.3)

    def create_queen_piece(self):
        """Create a queen piece using the actual chess piece image"""
        import os
        try:
            # Try to load the actual queen image
            dir_path = os.path.dirname(os.path.realpath(__file__))
            queen_path = os.path.join(dir_path, "png_pieces/wQ.png")
            queen = ImageMobject(queen_path)
            queen.scale(0.3)  # Scale down to fit better on the squares
        except:
            # Fallback to geometric shape if image loading fails
            queen = Circle(
                radius=0.25,  # Smaller radius for better fit
                fill_color=WHITE, 
                fill_opacity=1.0, 
                stroke_color=BLACK, 
                stroke_width=2
            )
            # Add yellow center to distinguish queens
            inner = Circle(
                radius=0.1,  # Smaller inner circle
                fill_color=YELLOW, 
                fill_opacity=1.0, 
                stroke_color=BLACK, 
                stroke_width=1
            )
            queen.add(inner)
            queen.scale(0.6)  # Smaller overall scale
        
        return queen

    def is_queen_piece(self, mobject):
        """Check if a mobject is a queen piece"""
        # Check for both ImageMobject (actual queen image) and Circle (fallback)
        return (isinstance(mobject, ImageMobject) or 
                (hasattr(mobject, 'submobjects') and 
                 len(mobject.submobjects) > 0 and
                 isinstance(mobject, Circle)))

    def generate_fen(self):
        """Generate FEN string for current queen positions"""
        board_array = [['.' for _ in range(self.N)] for _ in range(self.N)]
        
        for row, col in self.queen_positions:
            board_array[row][col] = 'Q'
        
        fen_rows = []
        for row in board_array:
            fen_row = ""
            empty_count = 0
            for cell in row:
                if cell == '.':
                    empty_count += 1
                else:
                    if empty_count > 0:
                        fen_row += str(empty_count)
                        empty_count = 0
                    fen_row += cell
            if empty_count > 0:
                fen_row += str(empty_count)
            fen_rows.append(fen_row)
        
        return "/".join(fen_rows)
            

    
        

    
        

        

    


    
        
