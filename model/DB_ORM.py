import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import pooling

# 載入 .env 檔案
load_dotenv()

## 讀取環境變數
AWS_db_name = os.getenv("db_name")
AWS_db_user = os.getenv("db_user")
AWS_db_password = os.getenv("db_password")
AWS_host = os.getenv("AWS_host")
AWS_port = os.getenv("AWS_port")

dbconfig = {
            "database": AWS_db_name,
            "user": AWS_db_user,
            "password": AWS_db_password,
            "host": AWS_host,
            "port": "3306"
            }

pool = mysql.connector.pooling.MySQLConnectionPool(pool_name="wehelp_stage3_DB_pool",
                                            pool_size=5,
                                            pool_reset_session=True,
                                            **dbconfig)


class DBfunction:

    def __init__(self):
        pass

    def MessageSearch(self):
        sql = "select * from message_table"
        connection = pool.get_connection()
        cursor = connection.cursor()
        cursor.execute(sql)#依據頁數查詢資料
        Messagesearch_result = cursor.fetchall()
        cursor.close()
        connection.close() # return connection to the pool.

        return Messagesearch_result


    def MessageInsertToDB(self, message, upload_img_url=None):
        """
        1. 先判斷有沒有圖片
        2. 有,先上傳到S3取得S3的圖片網址
        3. 將訊息和圖片網址存到DB
        """
        
        sql = "insert into message_table (message_text, message_img) values (%s,%s)"
        connection = pool.get_connection()
        cursor = connection.cursor()
        cursor.execute(sql,(message, upload_img_url,))#依據頁數查詢資料
        connection.commit()
        cursor.close()
        connection.close()

        return {"ok":True}

