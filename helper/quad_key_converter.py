from pygeotile.tile import Tile


def converter(latitude, longitude, zoom):
    tile = Tile.for_latitude_longitude(latitude=latitude, longitude=longitude, zoom=zoom)
    return tile.quad_tree

