#!/usr/local/bin/python
import sys

import psycopg2
from tabulate import tabulate
from prettytable import PrettyTable
from config import config


def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        # print('PostgreSQL database version:')
        # cur.execute('SELECT version()')
        query1 = '''
        select * from newness.brand where id=(%s)
        '''

        query2 = '''
        select distinct b.name,bsm.merchandise_market_id,mh.name 
        from newness.merchandise_hierarchy mh
        join newness.brand_sub_brand_mapping bsm on mh.id = bsm.merchandise_market_id
        join newness.brand b on bsm.brand_id = b.id
        where b.id in (%s)
        '''
        brand_id = sys.argv[1:][0]
        cur.execute(query2, (brand_id,))
        rows = cur.fetchall()
        # print(tabulate(rows, headers=["Brand", "Mrkt Id", "Market"], tablefmt="fancy_grid"))
        # mytable = PrettyTable()
        # mytable.field_names=["Brand", "Market ID", "Market"]
        #  for row in rows:
        #     mytable.add_row(rows[0])
        # print(mytable)
        query3 = '''
        select 
	um.username, 
	o."name" as organization, 
	array_agg(distinct m.market) as markets, 
	array_agg(distinct b."name") as brands  
from 
	newness.user u,
	newness.organization o, 
	newness.user_market um, 
	newness.market m , 
	newness.user_brand ub, 
	newness.brand b 
where 
	um.username = u.username and 
	ub.username = u.username and
	u.organization = o.id and
	um.market = m.id and 
	ub.brand  = b.id  and 
	um.username = ub.username
group by um.username, o."name"
having um.username = (%s)
order by um.username
        '''
        cur.execute(query3, ('xho@sephora.sg',))
        rows = cur.fetchall()
        print(tabulate(rows, headers=["Username", "Org", "Markets", "Brands"], tablefmt="fancy_grid"))

        # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            # print('Database connection closed.')


if __name__ == '__main__':
    connect()
