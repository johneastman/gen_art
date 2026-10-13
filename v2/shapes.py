class Shape:
    def __init__(self, x, y, size, fill_color=None, border_color=None, border_width=1):
        """
        X and Y represent the top-left corner of the shape.
        """
        self.x = x
        self.y = y
        self.size = size

        self.display_kwargs = {
            "fill": fill_color,
            "outline": border_color,
            "width": border_width
        }
    
    @property
    def center(self):
        return self.x + (self.size // 2), self.y + (self.size // 2)

    def box(self):
        return (
            self.x,
            self.y,
            self.x + self.size,
            self.y + self.size
        )
