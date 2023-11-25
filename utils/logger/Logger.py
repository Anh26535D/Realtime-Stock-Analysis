import logging
from datetime import datetime


class Logger:

    DEFAULT_START_TIME = '01/01/2020'
    
    def __init__(self, log_file_path) -> None:
        logging.basicConfig(
            filename=log_file_path, 
            format='[%(levelname)s]: Mapping from [%(asctime)s] to [%(message)s]',
            datefmt='%m/%d/%Y',
            level=logging.INFO
        )

        try:
            with open(log_file_path, 'r') as file:
                lines = file.readlines()
                if lines:
                    last_log_message = lines[-1].strip()
                    latest_system_time = last_log_message.split()[-1][1:-1]
                else:
                    latest_system_time = self.DEFAULT_START_TIME
        except FileNotFoundError:
            latest_system_time = self.DEFAULT_START_TIME

        latest_system_time = datetime.strptime(latest_system_time, '%m/%d/%Y')
        self.latest_system_time = latest_system_time
    
    def log_time_system(self) -> None:
        self.latest_system_time = self.latest_system_time.strftime('%m/%d/%Y')
        logging.info(f'{self.latest_system_time}')