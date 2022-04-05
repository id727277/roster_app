
import sqlite3
from classes import Concierge
import csv
import pandas as pd
import datetime

conn = sqlite3.connect('roster_app/concierges.db')
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
    c.execute("drop table if exists calendars;")
    c.execute("create table if not exists calendars (id integer primary key);")
    c.execute("insert into calendars default values;")
    c.execute("insert into calendars default values;")
    c.execute("insert into calendars select null from calendars d1, calendars d2, calendars d3 , calendars d4;")
    c.execute("insert into calendars select null from calendars d1, calendars d2, calendars d3 , calendars d4;")
    c.execute("alter table calendars add date datetime;")
    c.execute("update calendars set date=date('2022-01-01',(-1+id)||' day');")
    c.execute("create unique index ux_calendars_date on calendars (date);")

def generate_dates(start='2022-01-01 00:00:00', end='2030-01-01 00:00:00'):
    df = pd.DataFrame({"date_time": pd.date_range(start, end, freq='1H')})
    df['date'] = df.date_time.dt.date
    df["year"] = pd.to_datetime(df.date).dt.year
    df["month"] = pd.to_datetime(df.date).dt.month
    df['day'] = df.date_time.dt.day
    df['time'] = df.date_time.dt.time
    df['hour'] = df.date_time.dt.hour
    df['minute'] = df.date_time.dt.minute
    df["quarter"] = pd.to_datetime(df.date).dt.quarter
    df["week_of_year"] = df.date_time.dt.isocalendar().week
    df["day_of_week"] = df.date_time.dt.dayofweek
    df['month_name'] = pd.to_datetime(df.date).dt.month_name()
    df['day_name'] = pd.to_datetime(df.date).dt.day_name()
    df['is_leap_year'] = pd.to_datetime(df.date).dt.is_leap_year
    df['days_in_month'] = pd.to_datetime(df.date).dt.days_in_month
    df['is_month_end'] = df.date_time.apply(lambda x: pd.Timestamp(x).is_month_end)
    df['is_month_start'] = df.date_time.apply(lambda x: pd.Timestamp(x).is_month_start) 
    df['is_year_end'] = df.date_time.apply(lambda x: pd.Timestamp(x).is_year_end)
    df['is_year_start'] = df.date_time.apply(lambda x: pd.Timestamp(x).is_year_start)
    
    return df


def create_table_dates():

    df = generate_dates()
    # print(df.head(2))
    c.execute("drop table if exists dates;")

    df.to_sql('dates', con=conn)

    # c.execute("select count(*) from dates;")
    # print(c.fetchone()[0])


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

            

# insert_concierge_from_csv('roster_app/concierges_sample.csv')
# insert_shift_from_csv('roster_app/shifts.csv')

create_table_dates()


conn.close()

