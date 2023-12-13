import os

current_folder = os.getcwd()

datapath = os.path.join(current_folder, 'data')
if not os.path.exists(datapath):
    os.mkdir(datapath)

logpath = os.path.join(current_folder, 'logs', 'date_logs', 'datemapping.log')
if not os.path.exists(logpath):
    os.mkdir(logpath)