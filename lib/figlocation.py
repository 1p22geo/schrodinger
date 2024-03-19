import matplotlib
import matplotlib.gridspec


class FigureLocation:
    """
    Describes the location of a subplot in a matplotlib figure
    """
    x: int
    '''
    the width of the figure grid
    '''
    y: int
    '''
    the height of the figure grid
    '''
    num: int
    '''
    which graph is this
    '''

    def __init__(self, x, y, num):
        self.x = x
        self.y = y
        self.num = num

    def spec(self) ->matplotlib.gridspec.SubplotSpec:
        """
        Creates a SubplotSpec which can then be passed to fig.add_subplot
        """
        return matplotlib.gridspec.SubplotSpec(
            matplotlib.gridspec.GridSpec(self.x, self.y), self.num
        )
