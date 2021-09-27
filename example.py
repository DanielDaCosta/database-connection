from database import DataBaseConn, get_query

if __name__ == '__main__':
    with DataBaseConn() as db:
        # Execute Select Query
        sql_query = get_query('select_helloworld')
        db.execute(sql_query)
        output = db.fetchone()[0]

        # Insert Values
        sql_query = get_query('insert_helloworld')
        db.execute(sql_query, {'column_value': 'Hello World'})