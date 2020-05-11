
import sqlite3
import configparser, os
from tkinter import StringVar,messagebox
import traceback
import logging

TEST_ROW = 16
logger = logging.getLogger("MagicLogger")

file_root = os.path.abspath(os.getcwd())
db = file_root+os.path.sep+".."+os.path.sep+"MagicRoom.db"




def class_info():
    try:
        list_names = []
        connection = sqlite3.connect(db)
        cur = connection.cursor()
        sql = "select * from Magic_Class_Info"
        cur.execute(sql)
        rows = cur.fetchall()
        for element in rows:
            list_names.append(element)

        connection.commit()
        connection.close()
        return list_names
    except:
        logger.info("Exception in retrieving class information")
        logger.info(traceback.print_exc())



def get_Lessons_count():
    try:
        print (db)
        connection = sqlite3.connect(db)
        cur = connection.cursor()
        sql = "select count(*) from Magic_Science_Lessons"
        cur.execute(sql)
        count = cur.fetchone()
        print(count)
        connection.commit()
        connection.close()
        return count
    except:
        logger.info("Exception in retrieving lessons information")
        logger.info(traceback.print_exc())


def get_participants_count():
    try:
        print (db)
        connection = sqlite3.connect(db)
        cur = connection.cursor()
        sql = "select count(*) from Magic_Class_Info"
        cur.execute(sql)
        count = cur.fetchone()
        print(count)
        connection.commit()
        connection.close()
        return count
    except:
        logger.info("Exception in retrieving lessons information")
        logger.info(traceback.print_exc())


def get_skill_steps_count():
    try:
        print (db)
        connection = sqlite3.connect(db)
        cur = connection.cursor()
        sql = "select sum(Application_Steps_Number) from Magic_Science_Lessons"
        cur.execute(sql)
        sum = cur.fetchone()
        print(sum)
        connection.commit()
        connection.close()
        return sum
    except:
        logger.info("Exception in retrieving lessons information")
        logger.info(traceback.print_exc())

def get_badge_1_count():
    try:
        print (db)
        connection = sqlite3.connect(db)
        cur = connection.cursor()
        sql = "select Name from Magic_Class_Info where Badge = 'a'"
        cur.execute(sql)
        names = cur.fetchall()
        print(sum)
        connection.commit()
        connection.close()
        return names
    except:
        logger.info("Exception in retrieving lessons information")
        logger.info(traceback.print_exc())



