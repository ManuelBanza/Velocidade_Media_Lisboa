import requests
import pandas as pd
from datetime import datetime, timedelta
import io
from pandas.io.json import json_normalize

# Import origins and destinations
od = pd.read_csv('data_sources/data_raw/origin_destination.csv')

# Get data
df_result = pd.DataFrame()


for i in range(len(od)) :
    Origin = od.loc[i, 'Origin']
    Destination = od.loc[i, 'Destination']
    Rua = od.loc[i, 'Rua']
    url = od.loc[i, 'url']

    data = requests.get(url)
    json = data.json()

    # Pass to dataframe
    df = pd.DataFrame(json['routes'])
    df = json_normalize(df['summary'])

    # Get average speed
    df['duration_minutes'] = df['travelTimeInSeconds'] / 60
    df['duration_hours'] = df['travelTimeInSeconds'] / 3600
    df['distance_km'] = df['lengthInMeters'] / 1000
    df['average_speed'] = df['distance_km'] / df['duration_hours']

    # Get date and hour
    df['date'] = pd.Timestamp.today().strftime('%Y-%m-%d')
    df['hour'] = pd.Timestamp.today().strftime('%H:%M')
    df['date'] = pd.to_datetime(df['date'])
    df['dayofweek'] = df['date'].dt.day_name()
    
    df['Rua'] = Rua
    df['Origin'] = Origin
    df['Destination'] = Destination
    
    # Append to dataframe
    df_result = df_result.append(df)



# Order columns and drop others

df_result = df_result[
    [
        "Rua",
        "Origin",
        "Destination",
        "date",
        "hour",
        "dayofweek",
        "lengthInMeters",
        "distance_km",
        "travelTimeInSeconds",
        "duration_minutes",
        "duration_hours",
        "average_speed",
        "departureTime",
        "arrivalTime",
        "trafficDelayInSeconds",
        "trafficLengthInMeters"       
    ]
]


# Get today date now to file name when export to csv or excel with encoding utf8
df_result.to_csv((datetime.now()+timedelta(hours=1)).strftime('data_sources/data_transformed/velocidade_media_lisboa-%Y-%m-%d-%H-%M-%S.csv'), encoding='utf8', index=False)
