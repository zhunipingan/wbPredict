from sqlalchemy import create_engine
import pandas as pd

# MySQLUtil include:
# df_write_mysql -> DataFrame write into mysql xx database xx table function
class MySQLUtil:
    # param：ip、port、username、password、database、tableName
    def __init__(self, host, port, username, password, db, table):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.db = db
        self.table = table
        self.write_mode = 'append'
        self.connect_url = 'mysql+pymysql://' + username + ':' + password + '@' + host + ':' + port + '/' + db + '?charset=utf8mb4' #charset=utf8'
        self.mysql_connect = create_engine(self.connect_url)

    def df_write_mysql(self, data):
        pd.io.sql.to_sql(data, self.table, self.mysql_connect, schema=self.db, if_exists=self.write_mode)
        print("write into mysql finish")