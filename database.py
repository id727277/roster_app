
import sqlite3
from classes import Concierge
import csv
import pandas as pd

conn = sqlite3.connect('./concierges.db')
c = conn.cursor()

def create_table_concierges():

    c.execute("drop table if exists concierges;")
    c.execute("""
        create table concierges (
            id integer primary key,
            first text,
            last text,
            user_id text,
            phone text,
            tg_account text,
            dept text,
            remote int
        );""" )

def create_table_shifts():
    c.execute("drop table if exists shifts;")

    c.execute("""
        create table shifts (
            id integer primary key,
            shift text,
            time_start text,
            time_end text,
            description text,
            hours real
        );""" )

def create_table_calendar():
    c.execute("drop table if exists dates;")
    c.execute("create table if not exists dates (id integer primary key);")
    c.execute("insert into dates default values;")
    c.execute("insert into dates default values;")
    c.execute("insert into dates select null from dates d1, dates d2, dates d3 , dates d4;")
    c.execute("insert into dates select null from dates d1, dates d2, dates d3 , dates d4;")
    c.execute("alter table dates add date datetime;")
    c.execute("update dates set date=date('2022-01-01',(-1+id)||' day');")
    c.execute("create unique index ux_dates_date on dates (date);")










def get_concierge_by_lastname(lastname):
    c.execute("select * from concierges where last= :last", {'last':lastname})
    return c.fetchall()

def insert_concierge(concierge):
    with conn:
        c.execute("insert into concierges values (null, :first, :last, :user_id, :phone, :tg_account, :dept, :remote)", 
                    {'first':concierge.first, 
                    'last':concierge.last, 
                    'user_id':concierge.user_id, 
                    'phone':concierge.phone,
                    'tg_account':concierge.tg_account, 
                    'dept':concierge.dept, 
                    'remote':concierge.remote
                    })

def remove_concierge(concierge):
    with conn:
        c.execute("delete from employee where first = :first and last = :last",
                  {'first':concierge.first, 'last':concierge.last})

def strip_phone(phone):
    return phone.strip("'").replace(' ', '').lstrip('8')

def insert_concierge_from_csv(file):
    
    create_table_concierges()

    with open(file, 'r') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            first,last,user_id,phone,tg_account,dept,remote = row
            
            if user_id == '' and remote != '1':
                user_id = first.lower().strip() + '.' + last.lower().strip()
            elif user_id == '' and remote == '':
                user_id = ''
            else:
                pass
            
            insert_concierge(Concierge(first,last,user_id,strip_phone(phone),tg_account,dept,remote))

def insert_shift_from_csv(file):

    create_table_shifts()

    with open(file, 'r') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            shift, time_start, time_end, description, hours = row
            with conn:
                c.execute("insert into shifts values (null, :shift, :time_start, :time_end, :description, :hours)", 
                            {'shift':shift, 
                            'time_start':time_start, 
                            'time_end':time_end, 
                            'description':description,
                            'hours':hours
                            })

            

insert_concierge_from_csv('roster_app/concierges_sample.csv')
insert_shift_from_csv('roster_app/shifts.csv')
create_table_calendar()





conn.close()

