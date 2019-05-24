import mysql.connector

def csv_to_database(load_sql, host, username, password, database):
    #connect to mysql 
    connection = mysql.connector.connect(user=username, password=password,
                              host=host,
                              database=database,
                              local_infile=1)
    cursor = connection.cursor()
    cursor.execute(load_sql)
    connection.close()


#load_sql = "LOAD DATA LOCAL INFILE '/assignment/test_utilization.csv' INTO TABLE test_utilization FIELDS TERMINATED BY ',';"
#host = '127.0.0.1'
#user = 'username'
#password = 'password'
#csv_to_database(load_sql, host, user, password)