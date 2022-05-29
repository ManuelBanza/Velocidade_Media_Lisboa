import json
import requests
import pandas as pd
import numpy as np
import holidays
from datetime import datetime
import googlemaps

# Import origins and destinations
od = pd.read_csv('../data_sources/data_raw/origin_destination.csv')


#Perform request to use the Google Maps API web service
API_key = 'AIzaSyA9GXCsCRFCU0kNsrczDdveIQlYGXTStLk'#enter Google Maps API key
gmaps = googlemaps.Client(key=API_key)

df_result = pd.DataFrame()


for i in range(len(od)) :
    origin = od.loc[i, 'Origin']
    destination = od.loc[i, 'Destination']
    result = gmaps.distance_matrix(origin, destination, mode = 'driving')
    # To dataframe
    df = pd.DataFrame.from_dict(result)
    # Get distance and duration
    df['distance_km'] = df['rows'][0]['elements'][0]['distance']['text']
    df['distance_meters'] = df['rows'][0]['elements'][0]['distance']['value']
    df['distance_km'] = df['distance_km'].str.replace(' km', '')
    df['distance_km'] = df['distance_km'].astype(float)
    df['duration_seconds'] = df["rows"][0]["elements"][0]["duration"]["value"]
    df['duration_minutes'] = df["rows"][0]["elements"][0]["duration"]["text"]
    # Get average speed
    df['duration_hours'] = df['duration_seconds'] / 3600
    df['average_speed'] = df['distance_km'] / df['duration_hours']
    # Get date and hour
    df['date'] = pd.Timestamp.today().strftime('%Y-%m-%d')
    df['hour'] = pd.Timestamp.today().strftime('%H:%M')
    df['date'] = pd.to_datetime(df['date'])
    df['dayofweek'] = df['date'].dt.day_name()
    # Append to dataframe
    df_result = df_result.append(df)



# Order columns and drop others

df_result = df_result[
    [
        "date",
        "hour",
        "dayofweek",
        "origin_addresses",
        "destination_addresses",
        "distance_km",
        "distance_meters",
        "duration_hours",
        "duration_minutes",
        "duration_seconds",
        "average_speed",
    ]
]


# Get today date now to file name when export to csv or excel with encoding utf8
df_result.to_csv(datetime.now().strftime('../data_sources/data_transformed/velocidade_media_lisboa-%Y-%m-%d-%H-%M-%S.csv'), encoding='utf8', index=False)
