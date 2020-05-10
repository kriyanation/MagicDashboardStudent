
import sqlite3
import configparser, os
from tkinter import StringVar,messagebox
import traceback

TEST_ROW = 16


file_root = os.path.abspath(os.getcwd())
db = file_root+os.path.sep+".."+os.path.sep+"MagicRoom.db"




def class_info():
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



def get_Lessons_count():
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

def get_participants_count():
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

def get_skill_steps_count():
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

def get_badge_1_count():
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



