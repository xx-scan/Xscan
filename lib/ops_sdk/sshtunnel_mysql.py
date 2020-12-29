# coding:utf-8
# Author   : actanble
# DateTime : 2018/6/15 15:19
# SoftWare : PyCharm
import paramiko
import pymysql

from sshtunnel import SSHTunnelForwarder


class StunnelConnectMysql:

    def __init__(self,
                 ssh_host='127.0.0.1',
                 ssh_uname='root',
                 ssh_pass='111111',
                 ssh_port=22,
                 ssh_pkey_path='/root/.ssh/id_rsa',
                 use_key=False,
                 mysql_user='root',
                 mysql_pass='test@1q2w2e4R',
                 mysql_db='test',
                 local_bind_port=57320
                 ):
        self.ssh_host = ssh_host
        self.ssh_uname = ssh_uname
        self.ssh_pass = ssh_pass
        self.ssh_port = ssh_port
        self.ssh_pkey_path = ssh_pkey_path
        self.use_key = use_key
        self.mysql_config = dict(
            db=mysql_db,
            user=mysql_user,
            passwd=mysql_pass,
            host='127.0.0.1',
            port=local_bind_port
        )

    def conn(self):
        if self.use_key:
            # 获取密钥
            private_key = paramiko.RSAKey.from_private_key_file(self.ssh_pkey_path)
        with SSHTunnelForwarder(
                ('*.*.*.*', 11690),
                ssh_username="***",
                ssh_pkey="/Users/.ssh/id_rsa",
                ssh_private_key_password="***",
                remote_bind_address=('127.0.0.1', 3306)) as server:
            conn = pymysql.connect(host='127.0.0.1',
                                   port=server.local_bind_port,
                                   user='**',
                                   passwd='**',
                                   db='**')

            cursor = conn.cursor()
            # 使用 execute()  方法执行 SQL 查询
            cursor.execute("SELECT VERSION()；")

            # 使用 fetchone() 方法获取单条数据.
            data = cursor.fetchone()

            print("Database version : %s " % data)
            # 关闭数据库连接
            cursor.close()