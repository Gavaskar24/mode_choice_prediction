import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

def convert_csv_to_shapefile(file_name, input_path, output_file_name):
    # Construct full input path
    full_input_path = input_path + file_name
    
    # Read CSV file
    df = pd.read_csv(full_input_path)
    
    # Create geometry column from lat and long
    geometry = [Point(xy) for xy in zip(df['D_LONG'], df['D_LAT'])]
    crs = {'init': 'epsg:4326'}  # Assuming WGS84
    
    # Keep other columns as they are
    columns_to_keep = ['ID', 'RENT_BICYCLE']  # Specify the names of columns you want to keep
    for col in columns_to_keep:
        if col in df.columns:
            df[col] = df[col]
    
    # Create GeoDataFrame
    gdf = gpd.GeoDataFrame(df, crs=crs, geometry=geometry)
    
    # Save as shapefile
    full_output_path = input_path + output_file_name
    gdf.to_file(full_output_path)

# Example usage
# convert_csv_to_shapefile('egress_data.csv', 'E:/Metro1/artifacts//', 'destination_points_fetched.shp')
