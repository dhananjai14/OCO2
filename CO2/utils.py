import netCDF4
import pandas as pd
from CO2.config import kenya_lon_lat
from CO2.logger import logging
from CO2.exception import CO2_Exception
import yaml
import os, sys
import numpy as np
from datetime import datetime


def convert_cdf4_to_csv(complete_folder_path: str):
    """
    Description: This method will convert the cdf4 file format to the csv file format.
    Also, it will extract the data of Kenya.
    =====================================================================
    :param complete_folder_path:
    ======================================================================
    :return: pandas Data frame that combines all the data
    """

    try:
        logging.info('>>>>>>>>>>>>> inside the class Utils <<<<<<<<<<<')
        logging.info(f'Folder path is: {complete_folder_path}')
        list_of_files = os.listdir(complete_folder_path)
        df = pd.DataFrame()
        for file in list_of_files:
            logging.info(f'=======>Processing of File : {file} started')
            path = os.path.join(complete_folder_path, file)
            data0 = netCDF4.Dataset(path)
            latitude_values = list(data0.variables['lat'][:])
            longitude_values = list(data0.variables['lon'][:])
            logging.info('Latitude and longitude value extracted')

            XCO2_values = list(data0.variables['XCO2'][:])[0]
            try:
                XCO2PREC_values = list(data0.variables['XCO2PREC'][:])[0]
            except:
                XCO2PREC_values = np.NaN
            logging.info('CO2 values extracted')

            latitude_values_for_df = np.repeat(latitude_values, len(longitude_values))
            longitude_values_for_df = np.array(longitude_values * len(latitude_values))

            XCO2_values_for_df = XCO2_values.flatten()
            try:
                XCO2PREC_values_for_df = XCO2PREC_values.flatten()
            except:
                XCO2PREC_values_for_df = np.NaN
            logging.info('CO2_precision values extracted')

            format = '%Y-%m-%d'
            month_year = datetime.strptime(data0.RangeBeginningDate, format)
            XCO2_df = pd.DataFrame({'lat': latitude_values_for_df,
                                    'lon': longitude_values_for_df,
                                    'XCO2': XCO2_values_for_df,
                                    'XCO2PREC': XCO2PREC_values_for_df,
                                    'Month': month_year.month,
                                    'Year': month_year.year})
            logging.info('Data Frame Created')

            XCO2_df['DATE'] = pd.to_datetime(XCO2_df[['Year', 'Month']].assign(DAY=1))

            XCO2_df = XCO2_df[(XCO2_df['lat'] >= kenya_lon_lat[2]) & (XCO2_df['lat'] <= kenya_lon_lat[3])]
            XCO2_df = XCO2_df[(XCO2_df['lon'] >= kenya_lon_lat[0]) & (XCO2_df['lon'] <= kenya_lon_lat[1])].reset_index(drop=True)
            logging.info('Filtered the latitude and longitude for kenya')

            df = pd.concat([df, XCO2_df])
            df.reset_index(drop= True, inplace =True)
            logging.info(f'=======>Processing of File: {file} finished')

        cwd = os.getcwd()
        raw_data_path = os.path.join(cwd, 'Raw_data_to_csv_data')
        os.makedirs(raw_data_path, exist_ok=True)
        df.to_csv(rf'{raw_data_path}\XCO2_kenya.csv', index=False)
        logging.info('''XCO2_kenya.csv file created''')
        return df

    except Exception as e:
        raise CO2_Exception(e, sys)


def write_ymal_file(file_path, data:dict):
    try:
        file_dir = os.path.dirname(file_path)
        os.makedirs(file_dir, exist_ok=True)
        with open(file_path,'w') as file_writer:
            yaml.dump(data, file_writer)

    except Exception as e:
        raise CO2_Exception(e, sys)

