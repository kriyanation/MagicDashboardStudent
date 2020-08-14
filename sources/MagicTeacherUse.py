import logging
import sqlite3, random

import bcrypt as bcrypt
import sys, platform

from getmac import get_mac_address
from tkinter import messagebox, simpledialog

logger = logging.getLogger("MagicLogger")
class MagicTeacherUse():
    def __init__(self,parent,gp,*args,**kwargs):

        status = self.get_activation_status()
        if status == 1:
            gp.withdraw()
            pin_string = simpledialog.askstring("Enter PIN", "Please Enter the 6 Letter PIN",parent=parent)

            self.validate_pin(pin_string)
            self.insertclass_id()
            self.insertuser()
            gp.deiconify()
        else:
            self.validate_mac()

    def validate_mac(self):
        try:
            connection = sqlite3.connect("MagicCheck")
            cur = connection.cursor()
            sql = "select MAC from Check_Teacher"
            cur.execute(sql)
            mac = cur.fetchone()[0]
            cur.connection.close()
            mac_address = platform.node()
            if mac != mac_address:
                messagebox.showerror("Installation Moved","The application will close now")
                sys.exit()
            else:
                return

        except sqlite3.OperationalError:
            messagebox.showerror("Database Issue", "Issue with database connection")
            logger.exception("Activation Check met with an error")
            sys.exit()

    def get_activation_status(self):
        try:
            connection = sqlite3.connect("MagicCheck")
            cur = connection.cursor()
            sql = "select Activation from Check_Teacher"
            cur.execute(sql)
            status = cur.fetchone()[0]
            cur.connection.close()
            return status
        except sqlite3.OperationalError:
            messagebox.showerror("Database Issue", "Issue with database connection")
            logger.exception("Activation Check met with an error")
            sys.exit()

    def validate_pin(self,pin):
        try:
            connection = sqlite3.connect("MagicCheck")
            cur = connection.cursor()
            sql = "select PIN from Check_Teacher"
            cur.execute(sql)
            PIN = cur.fetchone()[0]
            cur.connection.close()
            if bcrypt.checkpw(pin.encode("utf-8"),PIN):
                activated_status = 0
                mac_address = platform.node()
                connection = sqlite3.connect("MagicCheck")
                cur = connection.cursor()
                sql = "update Check_Teacher set Activation=?,MAC = ?"
                cur.execute(sql,(activated_status,mac_address))
                messagebox.showinfo("Success","PIN successfully validated")
                connection.commit()
                connection.close()
            else:
                messagebox.showwarning("Invalid PIN","Invalid PIN, exiting application")
                sys.exit()



        except sqlite3.OperationalError:
            messagebox.showerror("Database Issue", "Issue with database connection")
            logger.exception("PIN Check met with an error")
            sys.exit()

    def insertclass_id(self):
        try:
            connection = sqlite3.connect("../MagicRoom.db")
            cur = connection.cursor()
            number = random.randint(10000,99999)
            sql ="update Magic_Teacher_Data set class_id=? where Class_No=1"
            cur.execute(sql, (number, ))
            connection.commit()
            connection.close()

        except sqlite3.OperationalError:
            messagebox.showerror("Database Issue", "Issue with database connection")
            logger.exception("Data setup met with an error")

    def insertuser(self):
        try:
            connection = sqlite3.connect("MagicCheck")
            cur = connection.cursor()
            sql = "select EMAIL from Check_Teacher"
            cur.execute(sql)
            user = cur.fetchone()[0]
            cur.connection.close()
            connection = sqlite3.connect("../MagicRoom.db")
            cur = connection.cursor()
            sql = "update Magic_Teacher_Data set User=? where Class_No=1"
            cur.execute(sql, (user,  ))
            connection.commit()
            connection.close()
        except sqlite3.OperationalError:
            messagebox.showerror("Database Issue", "Issue with database connection")
            logger.exception("Data setup met with an error")
