import netCDF4
import pandas as pd
from CO2.config import kenya_lon_lat
# from CO2.logger import logging
from CO2.exception import CO2_Exception
import yaml
import os, sys
import numpy as np
from datetime import datetime


def get_data_as_dataframe(complete_folder_path: str):
    list_of_files = os.listdir(complete_folder_path)
    for file in list_of_files:
        path = os.path.join(complete_folder_path, file)
        data0 = netCDF4.Dataset(path)
        latitude_values = list(data0.variables['lat'][:])
        longitude_values = list(data0.variables['lon'][:])

        XCO2_values = list(data0.variables['XCO2'][:])[0]
        try:
            XCO2PREC_values = list(data0.variables['XCO2PREC'][:])[0]
        except:
            XCO2PREC_values = np.NaN

        latitude_values_for_df = np.repeat(latitude_values, len(longitude_values))
        longitude_values_for_df = np.array(longitude_values * len(latitude_values))

        XCO2_values_for_df = XCO2_values.flatten()
        try:
            XCO2PREC_values_for_df = XCO2PREC_values.flatten()
        except:
            XCO2PREC_values_for_df = np.NaN
        format = '%Y-%m-%d'
        month_year = datetime.strptime(data0.RangeBeginningDate, format)
        XCO2_df = pd.DataFrame({'lat': latitude_values_for_df,
                                'lon': longitude_values_for_df,
                                'XCO2': XCO2_values_for_df,
                                'XCO2PREC': XCO2PREC_values_for_df,
                                'Month': month_year.month,
                                'Year': month_year.year})

        XCO2_df['DATE'] = pd.to_datetime(XCO2_df[['Year', 'Month']].assign(DAY=1))

        XCO2_df = XCO2_df[(XCO2_df['lat'] >= kenya_lon_lat[2]) & (XCO2_df['lat'] <= kenya_lon_lat[3])]
        XCO2_df = XCO2_df[(XCO2_df['lon'] >= kenya_lon_lat[0]) & (XCO2_df['lon'] <= kenya_lon_lat[1])].reset_index(drop=True)
        os.makedirs(r'C:\Users\preet\Desktop\DS\Project\OCO2\Raw_data_to_csv_data', exist_ok= True)
        XCO2_df.to_csv(rf'C:\Users\preet\Desktop\DS\Project\OCO2\Raw_data_to_csv_data\XCO2_{month_year.month}_{month_year.year}.csv', index=False)

    return None


get_data_as_dataframe(r'C:\Users\preet\Desktop\DS\Project\OCO2\Raw_data')
