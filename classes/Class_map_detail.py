class MapDetail:
    """
    Representation of a map detail (polygon)
    ex. beach, park, etc.
    """
    points = []
    color = ""

    def __init__(self, points, color):
        self.points = points
        self.color = color

    def to_dict(self):
        """
        Converts a map_detail object to a dictionary
        """
        return {
            'points': self.points,
            'color': self.color
        }