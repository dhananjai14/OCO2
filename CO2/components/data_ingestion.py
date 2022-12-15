from dataclasses import dataclass
import pandas as pd
from CO2 import utils
from CO2.entity import config_entity
from CO2.entity import artifact_entity
from CO2.exception import CO2_Exception
import sys, os

from sklearn.model_selection import train_test_split
from CO2.logger import logging


class DataIngestion:
    def __init__(self, data_ingestion_config: config_entity.DataIngestionConfig):
        try:
            logging.info('================== Data Ingestion Class =========================')
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise CO2_Exception(e, sys)

    def initiate_data_ingestion(self) -> artifact_entity.DataIngestionArtifact:
        try:
            # Exporting the data as pandas DataFrame
            logging.info('================== Initiate Data Ingestion =========================')

            df: pd.DataFrame = utils.convert_cdf4_to_csv(complete_folder_path=self.data_ingestion_config.raw_data_file_path)
            logging.info(f'Folder path is {self.data_ingestion_config.raw_data_file_path}')

            # Create a feature store folder
            feature_store_dir = os.path.dirname(self.data_ingestion_config.feature_store_file_path)
            os.makedirs(feature_store_dir, exist_ok=True)
            logging.info(f'Created folder {feature_store_dir}')

            # Save data to the feature store folder
            df.to_csv(path_or_buf=self.data_ingestion_config.feature_store_file_path, index = False)
            logging.info(f'Data compiled and stored to {self.data_ingestion_config.feature_store_file_path} ')


            # splitting the data into train and test
            logging.info(f'Split size is {self.data_ingestion_config.test_size}')
            train_df, test_df = train_test_split(df , test_size= self.data_ingestion_config.test_size)

            # create the dataset directory
            dataset_dir = os.path.dirname(self.data_ingestion_config.train_file_path)
            os.makedirs(dataset_dir, exist_ok=True)
            logging.info(f'Directory created {self.data_ingestion_config.train_file_path}')

            train_df.to_csv(path_or_buf=self.data_ingestion_config.train_file_path, index = False)
            test_df.to_csv(path_or_buf=self.data_ingestion_config.test_file_path, index = False)
            logging.info('Train and Test file created.')

            # prepare the artifact
            data_ingestion_artifact = artifact_entity.DataIngestionArtifact(
                                                    feature_store_file_path=self.data_ingestion_config.feature_store_file_path,
                                                    train_file_path= self.data_ingestion_config.train_file_path,
                                                    test_file_path= self.data_ingestion_config.test_file_path)
            logging.info('============= Data Ingestion completed =========================')

            return data_ingestion_artifact

        except Exception as e:
            raise CO2_Exception(e, sys)


@dataclass
class DataValidationArtifact:
    report_file_path: str


class DataTransformationArtifact: ...


class ModelTrainerArtifact: ...


class ModelEvaluationArtifact: ...


class ModelPusherArtifact: ...
