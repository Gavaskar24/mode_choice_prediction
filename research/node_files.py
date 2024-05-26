import geopandas as gpd
from shapely.geometry import Point
from shapely.ops import transform
from functools import partial
import pyproj
import os
import argparse

def node_file(filename, path, buffer_radius):
    # Load node shapefile
    node_gdf = gpd.read_file(os.path.join(path, filename))
    
    # Define a function to create a buffer of specified radius around a point
    def create_buffer(point, buffer_radius):
        if point is None:
            return None
        proj_wgs84 = pyproj.Proj(init='epsg:4326')
        proj_merc = pyproj.Proj(init='epsg:3857')
        lon, lat = point.x, point.y
        lon, lat = pyproj.transform(proj_wgs84, proj_merc, lon, lat)
        point_merc = Point(lon, lat)
        buffer_merc = point_merc.buffer(buffer_radius) # buffer in meters
        return transform(partial(pyproj.transform, proj_merc, proj_wgs84), buffer_merc)
    
    # Apply the function to each node point to create buffers
    node_gdf['buffer'] = node_gdf['geometry'].apply(lambda point: create_buffer(point, buffer_radius))
    
    # Convert buffers to a new GeoDataFrame
    buffer_gdf = gpd.GeoDataFrame(node_gdf[['buffer']], geometry='buffer')
    
    # Construct the output filename by removing the last two words from the input filename
    base_filename = os.path.splitext(filename)[0]
    filename_parts = base_filename.split('_')
    if len(filename_parts) > 2:
        base_filename = '_'.join(filename_parts[:-2])
    output_filename = f'output_{base_filename}_{buffer_radius}m_radius.shp'
    
    # Save the buffer shapefile
    buffer_gdf.to_file(os.path.join(path, output_filename))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create buffers around points in a shapefile")
    parser.add_argument("filename", type=str, help="Name of the input shapefile")
    parser.add_argument("path", type=str, help="Path to the directory containing the shapefile")
    parser.add_argument("buffer_radius", type=int, help="Radius of the buffer in meters")

    args = parser.parse_args()
    node_file(args.filename, args.path, args.buffer_radius)
