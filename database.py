import sqlite3
import sys


con = sqlite3.connect('todo.db')
cur = con.cursor()


def loadTask(activity, email, priority):
    create_table = """CREATE TABLE [IF NOT EXISTS] todo (id INTEGER PRIMARY KEY, activity TEXT, email TEXT, proority text)"""
    insert = f"insert into todo (activity, email, priority) values({activity}, {email}, {priority})"
    sql = f"{create_table} {insert}"
    cur.executescript(sql)
    con.commit()


    
