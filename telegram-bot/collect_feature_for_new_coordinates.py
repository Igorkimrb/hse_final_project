import pandas as pd
import geopandas as gpd
import numpy as np
import sys
import os
from catboost import CatBoostRegressor
import ssl
import certifi
import geopy.geocoders


ctx = ssl.create_default_context(cafile=certifi.where())
geopy.geocoders.options.default_ssl_context = ctx
app = geopy.geocoders.Nominatim(user_agent="igorkim")
ssl._create_default_https_context = ssl._create_stdlib_context


def  return_index(lat, lon, atm_group):
    data = pd.read_csv('https://storage.yandexcloud.net/for-tg-bot-serverless/expanded_data_with_OSM_v3.csv', sep = ',')
    data_with_points = pd.read_csv('https://storage.yandexcloud.net/for-tg-bot-serverless/all_object.csv', sep = ',')
    df_regions = pd.read_csv('https://storage.yandexcloud.net/for-tg-bot-serverless/regions_data.csv', sep = ';')

    point = pd.DataFrame([[lon], [lat], ]).T.rename(columns={0:'lon',1:'lat'})
    point['atm_group'] =atm_group
    point['geometry']='POINT ('+str(lon)+' '+str(lat)+')'
    point = gpd.GeoDataFrame(point, geometry=gpd.points_from_xy(point.lon, point.lat))
    point.geometry=point.geometry.set_crs('EPSG:4326').to_crs('EPSG:3857')

    data_with_points= gpd.GeoDataFrame(data_with_points[['bulding_type', 'lon', 'lat']], geometry=gpd.points_from_xy(data_with_points.lon, data_with_points.lat))
    data_with_points.geometry=data_with_points.geometry.set_crs('EPSG:4326').to_crs('EPSG:3857')

    objects = data_with_points.bulding_type.unique()

    for i in objects:
      col_name = 'distance_to_'+i
      point[col_name]= point.\
      sjoin_nearest(data_with_points[data_with_points['bulding_type']==i], how = 'inner', max_distance=10000, distance_col='distance')\
      ['distance'].min()

    point = point.fillna(10000)

    d = list(zip(point['lat'], point['lon']))

    id = []
    id_r = []

    cities, regions, states = [], [], []
    for i, item in enumerate(d):
        coordinates = f"{lat}, {lon}"
        address = app.reverse(coordinates, language='en').raw
        try:
            cities.append(address['address']['city'])
        except KeyError:
            try:
                cities.append(address['address']['town'])
            except KeyError:
                try:
                    cities.append(address['address']['village'])
                except:
                    try:
                        cities.append(address['address']['hamlet'])
                    except:
                        try:
                            cities.append(address['address']['municipality'])
                        except:
                            cities.append(address['address']['county'])
                            id.append(i)

        try:
            regions.append(address['address']['region'])
        except:
            regions.append(np.nan)
            id_r.append(i)

        states.append(address['address']['state'])

    point['city'], point['regions'], point['states'] = cities, regions, states

    point= point.merge(df_regions, how = 'inner', left_on = 'regions', right_on = 'Unnamed: 0').drop('Unnamed: 0', axis =1)

    X_test = (
    point.drop(['lat', 'lon','geometry'], axis = 1)
    .merge(data[['regions','avgR']].groupby('regions', as_index=False).max('avgR'), how = 'inner', on = 'regions')
    .merge(data[['states','avgS']].groupby('states', as_index=False).max('avgS'), how = 'inner', on = 'states')
    .merge(data[['cities','avgC']].groupby('cities', as_index=False).max('avgC'), how = 'inner', left_on = 'city',right_on = 'cities')
    .merge(data[['atm_group','avgA']].groupby('atm_group', as_index=False).max('avgA'), how = 'inner', on = 'atm_group')
    ).drop(['city'], axis = 1)

    X_test['capital'] = np.where((X_test['cities'] == 'Moscow') | (X_test['cities'] == 'Saint Petersburg'), 1, 0)
    X_test['atm_group']=X_test['atm_group'].astype('int64')

    X_test = X_test[['atm_group', 'distance_to_retail', 'distance_to_apartments',
           'distance_to_commercial', 'distance_to_office',
           'distance_to_train_station', 'distance_to_residential',
           'distance_to_house', 'distance_to_detached', 'distance_to_supermarket',
           'distance_to_cinema', 'distance_to_pharmacy', 'distance_to_cafe',
           'distance_to_bank', 'distance_to_sber_bank', 'distance_to_restaurant',
           'distance_to_sber_atm', 'distance_to_atm', 'distance_to_fast_food',
           'distance_to_vtb_bank', 'distance_to_convenience',
           'distance_to_clothes', 'distance_to_mobile_phone_shop',
           'distance_to_shoe_shop', 'distance_to_vending_any',
           'distance_to_alfa_bank', 'distance_to_vtb_atm', 'distance_to_ros_bank',
           'distance_to_alfa_atm', 'distance_to_ros_atm',
           'distance_to_vending_parking', 'distance_to_bus_stop',
           'distance_to_railway_station', 'distance_to_tram_stop',
           'distance_to_railway_halt', 'distance_to_airport',
           'distance_to_parking', 'distance_to_parking_underground', 'cities',
           'regions', 'states', 'population', 'salary', 'population_density',
           'happy_index', 'avgC', 'avgR', 'avgS', 'avgA', 'capital']]
    model = CatBoostRegressor()
    model.load_model('catboost_model',format='cbm')
    y_pred = model.predict(X_test)[0]
    return y_pred


