from random import random

class CSP:
    def __init__(self, neighbors, colors):
        self.neighbors = neighbors
        self.colors = colors
        self.assignments = {}
    
    def is_valid(self, coordinate, color):
        """Iterate over all neighbors and check if any have the same color.
    
        Return False if any share the same color; True otherwise.
        """
        for neighbor in self.neighbors[coordinate]:
            if self.assignments.get(neighbor) == color:
                return False
        return True

    def backtrack(self):
        # Have all cells been colored?
        if len(self.assignments) == len(self.neighbors):
            return True

        # Find a cell that hasn't been colored yet
        coordinate = next(
            cell for cell in self.neighbors
            if cell not in self.assignments
        )

        random_colors = sorted(self.colors, key=lambda _: random())

        # Try each available color
        for color in random_colors:
            if self.is_valid(coordinate, color):
                # Make the assignment
                self.assignments[coordinate] = color

                # Recursively color the remaining cells
                if self.backtrack():
                    return True

                # Dead end! Undo the assignment and try another color
                del self.assignments[coordinate]

        # No color worked for this cell
        return False
