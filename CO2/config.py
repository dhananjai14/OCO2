import pymongo
import pandas as pd
import json
import os
from dataclasses import dataclass


# provide the mongo DB local host url to connect with python

@dataclass
class EnvironmentVariable:
    mongo_db_url: str = os.getenv('Mongo_db_url')


env_var = EnvironmentVariable()
mongo_client = pymongo.MongoClient(env_var.mongo_db_url)
