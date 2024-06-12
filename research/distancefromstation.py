import pandas as pd
import numpy as np
from geopy.distance import geodesic
import argparse

def distance_from_station(df):
    # Define a function to calculate distance from the station
    station_latitude = 12.975943265903705
    station_longitude = 77.57107685224518
    def calculate_distance(row):
        return geodesic((row['D_LAT'], row['D_LONG']), (station_latitude, station_longitude)).km

    # Apply the function to each row in the DataFrame
    df['CBD'] = df.apply(calculate_distance, axis=1)
    
    return df

def main(input_file, output_file):
    # Read the input CSV file
    df = pd.read_csv(input_file)
    
    # Calculate the distance from the station
    df = distance_from_station(df)
    
    # Save the DataFrame to a CSV file
    df.to_csv(output_file, index=False)
    print(f'Data saved to {output_file}')

if __name__ == '__main__':
    # Set up argument parsing
    parser = argparse.ArgumentParser(description='Calculate distances from a station and save the results.')
    parser.add_argument('input_file', type=str, help='Path to the input CSV file')
    parser.add_argument('output_file', type=str, help='Path to save the output CSV file')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Run the main function
    main(args.input_file, args.output_file)
