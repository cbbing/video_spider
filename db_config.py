#coding:utf-8
__author__ = 'cbb'

from sqlalchemy import create_engine
host_mysql = '120.11.1.1'
port_mysql = 3306
user_mysql = 'root'
pwd_mysql = 'root'
db_name_mysql = 'db1'

engine = create_engine('mysql+mysqldb://%s:%s@%s:%d/%s' % (user_mysql, pwd_mysql, host_mysql, port_mysql, db_name_mysql), connect_args={'charset':'utf8'})

host_mysql_j = '120.11.1.1'
port_mysql_j = '3306'
user_mysql_j = 'root'
pwd_mysql_j = 'root'
db_name_mysql_j = 'db2'

engine_ip = create_engine('mysql+mysqldb://%s:%s@%s:%s/%s' % (user_mysql_j, pwd_mysql_j, host_mysql_j, port_mysql_j, db_name_mysql_j), connect_args={'charset':'utf8'})



# Redis config
import redis
# Redis config for Test(Windows Server)
redis_host_test = '10.0.179.124'
redis_port_test = 6379
redis_passwd_test = '111'
redis_db3 = redis.Redis(host=redis_host_test, port=redis_port_test, db=3, password=redis_passwd_test)
