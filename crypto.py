from database import get_connection, create_db_table
from tkinter.filedialog import asksaveasfile
from tkinter.messagebox import showerror, showinfo
import rsa
from sanity import normalize_string


def save_key_file(name, content):
    f = asksaveasfile(mode='w', initialfile=f'{name}.pem', defaultextension=".pem", filetypes=[
                      ("Key Files", "*.pem")])
    if f is None:
        return
    f.write(str(content))
    f.close()


def generateKeys(username: str):
    try:
        public_key, private_key = rsa.newkeys(1024)

        db = get_connection()
        cursor = db.cursor()

        create_db_table(db)

        query = "INSERT INTO user_keys VALUES (?, ?, ?);"
        cursor.execute(query, [normalize_string(
            username), public_key.save_pkcs1(), private_key.save_pkcs1()])

        db.commit()

        save_key_file('public', public_key.save_pkcs1())
        save_key_file('private', private_key.save_pkcs1())
        showinfo(title='عملیات موفقیت آمیز',
                 message='عملیات با موفقیت انجام شد')
    except sqlite3.DatabaseError as err:
        showerror(title="خطا", message="خطا در ذخیره اطلاعات: "+str(err))
    except ValueError as err:
        showerror(title="خطا", message="خطا در ذخیره اطلاعات: "+str(err))
    except Exception as err:
        showerror(
            title="خطا", message="خطای ناشناخته ای رخ داد! لطفا با مدیر تماس بگیرید"+"\n"+str(err))
    finally:
        db.close()
        set_screen('home')


def encrypt(text, reciver_username):
    result = None
    try:
        db = get_connection()
        cursor = db.cursor()

        create_db_table(db)

        query = "SELECT * FROM user_keys WHERE username = ?"
        cursor.execute(query, [reciver_username])
        result = cursor.fetchone()

        if result:
            f = asksaveasfile(mode='w', defaultextension=".txt", filetypes=[
                              ("Text Documents", "*.txt")])
            if f is None:
                return
            encrypted_txt = rsa.encrypt(text.encode(
                'utf8'), rsa.PublicKey.load_pkcs1(result[1]))
            f.write(str(encrypted_txt))
            f.close()
            showinfo(title='عملیات موفقیت آمیز',
                     message='عملیات با موفقیت انجام شد')
        else:
            showerror(title="خطا", message="خطا در دریافت اطلاعات" +
                      "\n"+"کاربری با این نام وجود ندارد")

    except sqlite3.DatabaseError as err:
        showerror(title="خطا", message="خطا در دریافت اطلاعات: "+str(err))
        db.close()
    except Exception as err:
        showerror(
            title="خطا", message="خطای ناشناخته ای رخ داد! لطفا با مدیر تماس بگیرید"+"\n"+str(err))
    finally:
        db.close()


def decrypt(text, private_key):
    print(private_key)
    try:
        decryptedText = rsa.decrypt(text.encode(
            'utf8'), rsa.PrivateKey.load_pkcs1(private_key))

        return decryptedText.decode('utf8')
    except Exception as err:
        showerror(
            title="خطا", message="خطای ناشناخته ای رخ داد! لطفا با مدیر تماس بگیرید"+"\n"+str(err))
        return ''
