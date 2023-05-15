class MapColorScheme:
    """
    Color scheme for the map
    """
    # Color Scheme background
    colorLightBG = '#f1f0ed'
    colorDarkBG = '#242424'
    # Color Scheme text
    colorLightText = '#363136'
    colorDarkText = '#c8c8c8'
    # Color Scheme water
    colorLightWater = '#c3e6f9'
    colorDarkWater = '#527b8f'
    # Color Scheme beach
    colorLightBeach = '#f6d897'
    colorDarkBeach = '#f6d897'
    # Color Scheme forest
    colorLightForest = '#6aab73'
    colorDarkForest = '#6aab73'
    # Color Scheme bus station
    colorLightBusStation = '#019ad1'
    colorDarkBusStation = '#019ad1'
    # Color Scheme tram station
    colorLightTramStation = '#eb2827'
    colorDarkTramStation = '#eb2827'
    # Color Scheme train station
    colorLightTrainStation = '#f0cb15'
    colorDarkTrainStation = '#f0cb15'
    # Color Scheme metro station
    colorLightMetroStation = '#be93d4'
    colorDarkMetroStation = '#be93d4'

    def to_dict(self):
        """
        Converts a map_info object to a dictionary
        """
        return {
            'colorLightBG': self.colorLightBG,
            'colorDarkBG': self.colorDarkBG,
            'colorLightText': self.colorLightText,
            'colorDarkText': self.colorDarkText,
            'colorLightWater': self.colorLightWater,
            'colorDarkWater': self.colorDarkWater,
            'colorLightBeach': self.colorLightBeach,
            'colorDarkBeach': self.colorDarkBeach,
            'colorLightForest': self.colorLightForest,
            'colorDarkForest': self.colorDarkForest,
            'colorLightBusStation': self.colorLightBusStation,
            'colorDarkBusStation': self.colorDarkBusStation,
            'colorLightTramStation': self.colorLightTramStation,
            'colorDarkTramStation': self.colorDarkTramStation,
            'colorLightTrainStation': self.colorLightTrainStation,
            'colorDarkTrainStation': self.colorDarkTrainStation,
            'colorLightMetroStation': self.colorLightMetroStation,
            'colorDarkMetroStation': self.colorDarkMetroStation
        }


MapColorSchemeDefault = MapColorScheme()
