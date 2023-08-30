from dotenv import dotenv_values

from database_functions import get_db_connection

if __name__ == '__main__':
    configuration = dotenv_values()
    connection = get_db_connection(configuration)
