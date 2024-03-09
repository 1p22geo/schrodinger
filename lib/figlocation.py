import matplotlib


class FigureLocation:
    """
    Describes the location of a subplot in a matplotlib figure

    Attributes:
        int x: the width of the figure grid
        int y: the height of the figure grid
        int num: which graph is this
    """

    def __init__(self, x, y, num):
        self.x = x
        self.y = y
        self.num = num

    def spec(self):
        """
        Creates a SubplotSpec which can then be passed to fig.add_subplot

        Returns: matplotlib.gridspec.SubplotSpec
        """
        return matplotlib.gridspec.SubplotSpec(
            matplotlib.gridspec.GridSpec(self.x, self.y), self.num
        )
