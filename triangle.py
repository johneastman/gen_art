"""An implementation of Game Chaos.

MIT License

Copyright (c) 2018 John Eastman

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import pygame
import random
import sys

WIDTH = 800   # Pygame window width
HEIGHT = 600  # Pygame window height
FRAMES = 25   # FPS

class Point:
    def __init__(self, pos, radius=9):
        self.pos = pos
        self.radius = radius


class LabeledPoint(Point):

    def __init__(self, pos, rolls, label_text, label_pos_id, radius=9, offset=30):
        """Initialize a point.
        
        Required Parameters:
        pos:            Position of point on screen.
        rolls:          What dice rolls will make the random dots go toward 
                        this point.
        label_text:     Display text for point's label.
        label_pos_id:   Specifying what side (top, bottom, left, right, etc.) of 
                        the point the label should be on.
        
        Optional Parameters:
        radius: Radius of the point
        offset: How much the Point's label position is offset from the point.
        """
        # Initialize Parent Point
        super().__init__(pos, radius)

        self.position_offsets = {"top":  (0, -offset), "bottom": (0, offset),
                                 "left": (-offset, 0), "right": (offset, 0)}
        
        self.rolls = rolls
        self.label_text = label_text  
        self.label_pos = self._get_label_pos(label_pos_id, pos)
        
    def _get_label_pos(self, label_pos_id, pos):
        """Returns the position of the label."""
        if label_pos_id not in self.position_offsets:
            raise Exception(f"'{label_pos_id}' is an invalid position identifier. Valid identifiers include: {', '.join(self.position_offsets.keys())}")
        
        # Add the offset values to the given position to get the label's position
        x1, y1 = pos
        x2, y2 = self.position_offsets[label_pos_id]
        return (x1 + x2, y1 + y2)
        
    def get_label(self, text_color):
        """Create a label to be drawn on the screen."""
        text_font = pygame.font.Font("freesansbold.ttf", 40)

        text_surface = text_font.render(self.label_text, True, text_color)
        text_rect = text_surface.get_rect()
        text_rect.center = (self.label_pos)
        
        return text_surface, text_rect

if __name__ == "__main__":

    # Pygame initializations
    pygame.init()
    display = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Chaos Game")
    clock = pygame.time.Clock()
    
    starting_point = Point((400, 300))  # Initial starting position for the dots
    current_position = starting_point.pos
    
    # Color Definitions
    black = (0, 0, 0)
    white = (255, 255, 255)
    red = (255, 0, 0)
    green = (0, 255, 0)

    dots = []
    dot_size = 1  # In pixels

    # Three points that comprise the triangle.
    points = [LabeledPoint((400, 67), (1, 2), "A", "top"), 
              LabeledPoint((89, 533), (3, 4), "B", "left"),
              LabeledPoint((711, 533), (5, 6), "C", "right")]

    while True:

        # Handle Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Roll the die
        random_number = random.randint(1, 6)
        
        display.fill(white)
        
        # Draw all the generated dots on the screen.
        for dot in dots:
            pygame.draw.circle(display, black, dot, dot_size)
        
        for point in points:
            if random_number in point.rolls:
                point_x, point_y = point.pos
                
                # The new point is halfway between the current dot and the point 
                # selected from the die roll.
                new_x = round((point_x + current_position[0]) / 2)
                new_y = round((point_y + current_position[1]) / 2)

                current_position = (new_x, new_y)  # Update the current position
                dots.append(current_position)
            
            # Draw the point's label.
            label_surface, label_rect = point.get_label(black)
            display.blit(label_surface, label_rect)

            # Draw the point.
            pygame.draw.circle(display, red, point.pos, point.radius)
            
        # Draw the starting position
        pygame.draw.circle(display, green, starting_point.pos, starting_point.radius)

        pygame.display.update()
        clock.tick(FRAMES)
