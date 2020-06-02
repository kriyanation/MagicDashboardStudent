import logging
import sqlite3
import sys

from getmac import get_mac_address
from tkinter import messagebox, simpledialog

logger = logging.getLogger("MagicLogger")
class MagicTeacherUse():
    def __init__(self,parent,*args,**kwargs):

        status = self.get_activation_status()
        if status == 1:
            pin_string = simpledialog.askstring("Enter PIN", "Please Enter the 6 Letter PIN")
            self.validate_pin(pin_string)
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
            mac_address = get_mac_address()
            if mac != mac_address:
                messagebox.showerror("Installation Moved","The application will close now")
                sys.exit()
            else:
                return

        except sqlite3.OperationalError:
            messagebox.showerror("Database Issue", "Issue with database connection")
            logger.exception("Activation Check met with an error")

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

    def validate_pin(self,pin):
        try:
            connection = sqlite3.connect("MagicCheck")
            cur = connection.cursor()
            sql = "select PIN from Check_Teacher"
            cur.execute(sql)
            PIN = cur.fetchone()[0]
            cur.connection.close()
            if pin == PIN:
                activated_status = 0
                mac_address = get_mac_address()
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