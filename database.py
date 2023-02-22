from tkinter.messagebox import showerror
import sqlite3


def get_connection():
    return sqlite3.connect('database.db')


def get_users():
    result = None
    try:
        db = get_connection()
        cursor = db.cursor()
        query = "SELECT username FROM user_keys"
        cursor.execute(query)
        query_result = cursor.fetchall()
        result = [j for i in query_result for j in i]
    except sqlite3.DatabaseError as err:
        showerror(title="خطا", message="خطا در دریافت اطلاعات: "+str(err))
    except Exception as err:
        showerror(
            title="خطا", message="خطای ناشناخته ای رخ داد! لطفا با مدیر تماس بگیرید"+"\n"+str(err))
    finally:
        db.close()
        return result


def create_db_table(conn):
    try:
        cursor = conn.cursor()
        query = "CREATE TABLE IF NOT EXISTS user_keys (username VARCHAR(255) UNIQUE, public_key VARCHAR(255), private_key VARCHAR(255));"
        cursor.execute(query)
        conn.commit()
    except sqlite3.DatabaseError as err:
        showerror(title="خطا", message="خطا در ذخیره اطلاعات: "+str(err))
    except Exception as err:
        showerror(
            title="خطا", message="خطای ناشناخته ای رخ داد! لطفا با مدیر تماس بگیرید"+"\n"+str(err))
