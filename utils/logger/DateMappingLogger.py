import datetime

class DateMappingLogger:

    DEFAULT_START_TIME = '01/01/2020'
    DEFAULT_DATE_FORMAT = '%m/%d/%Y'

    def __init__(self, log_file_path) -> None:
        self.log_file_path = log_file_path
        self.latest_system_time = self.read_latest_time_system(log_file_path)
        self.logger = open(log_file_path, 'a')

    def read_latest_time_system(self, log_file_path) -> datetime.datetime:
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

        latest_system_time = datetime.datetime.strptime(latest_system_time, self.DEFAULT_DATE_FORMAT)
        return latest_system_time        

    def log_time_system(self):
        str_date = self.latest_system_time.strftime(self.DEFAULT_DATE_FORMAT)
        current_date = datetime.datetime.now().strftime(self.DEFAULT_DATE_FORMAT)
        self.logger.write(f'[{current_date}] [{str_date}]\n')
        self.logger.flush()

    def close(self):
        self.logger.close()