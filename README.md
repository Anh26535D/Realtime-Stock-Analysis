# Real-time Stock Analysis

## Overview

TODO

## Requirements

This project requires the following dependencies and tools:

- **Python 3.9**: This project uses python 3.9.13, you can use other versions that are similar to.
- **Docker Desktop**: Containerization platform that allows you to build, ship, and run applications in containers.

## Setup

1. **Clone the Repository**
   ```
   git clone https://github.com/Anh26535D/Realtime-Stock-Analysis.git
   cd Realtime-Stock-Analysis
   ```

2. **Install python libraries**
   ```
   python3 -m pip install -r requirements.txt
   ```

3. **Run docker-compose**
   ```
   make docker-up
   ```

4. **Run crawl listing companies [OPTINAL]**
   ```
   make run-list-company
   ```

5. **Run producer and consumer**

   ```
   make run-app
   ```

   The data will be stored in a PostgreSQL database. You can use a tool like DBeaver or psql to inspect the database. For download DBeaver, see [here](https://dbeaver.io/download/). This is the command to use access psql:
   ```
   docker exec -it [container-postgresql-id] psql -U [user_name] -d [database_name]
   ```

   Replace [container-postgresql-id], [user_name], and [database_name] with the appropriate values in the .env file. You can find the PostgreSQL container ID using:
   ```
   docker ps
   ```

## Usage

TODO


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
