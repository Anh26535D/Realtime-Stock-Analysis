# Real-time Stock Analysis

## Overview

TODO

## Requirements

This project requires the following dependencies and tools:

- **Make**: [download here](https://gnuwin32.sourceforge.net/packages/make.htm)
- **Python 3.9**: This project uses python 3.9.13, you can use other versions that are similar to.
- **Docker Desktop**: Containerization platform that allows you to build, ship, and run applications in containers.

## Setup

1. **Clone the Repository**
   ```
   git clone https://github.com/Anh26535D/Realtime-Stock-Analysis.git
   cd Realtime-Stock-Analysis
   ```

2. **Run crawl listing companies [OPTIONAL]**
   ```
   mkdir data
   make run-list-company
   ```

3. **Run app**

   ```
   docker compose up
   ```

   After run app, waiting for containers starting.
   You can access:
    - kafka-ui via port 8080, 
    - spark master ui via port 8888
    - influxdb via port 8086

4. **Restart docker container [OPTIONAL]**
   ```
   make restart
   ```

## Note

Docker Desktop for Windows v2, which uses WSL2, stores all image and container files in a separate virtual volume (vhdx). This virtual hard disk file can automatically grow when it needs more space (to a certain limit). Unfortunately, if you reclaim some space, i.e. by removing unused images, vhdx doesn't shrink automatically. You can try to reduce its size manually by calling this command in PowerShell (as Administrator). Assume your path to (vhdx) file is "C:\Users\{user_name}\AppData\Local\Docker\wsl\data\ext4.vhdx":
   ```
   Optimize-VHD -Path "YOUR_PATH" -Mode Full
   ```
Or trying this
   ```
   wsl --shutdown
   diskpart
   select vdisk file="YOURPATH"
   attach vdisk readonly
   compact vdisk
   detach vdisk
   exit
   ```


## Contributing

TODO

## License

TODO

## Acknowledgments

TODO

## Contact

For any inquiries or issues, please contact:

- Dam Viet Anh 
- anh.dv204627@sis.hust.edu.vn
