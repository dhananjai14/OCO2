import os
import logging
from datetime import datetime

# Creating log directory
log_file_directory = os.path.join(os.getcwd(), 'logs')
os.makedirs(log_file_directory, exist_ok=True)

# creating log file name
log_file_name = f"{datetime.now().strftime('%m-%d-%Y__%H:%M:%S')}.log"
log_file_path = os.path.join(log_file_directory, log_file_name)

# Writing the info to log file
logging.basicConfig(
    filename=log_file_path,
    format = '[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s',
    level = logging.INFO)