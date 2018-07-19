from django.db import connection


def run_custom_sql(sql, args, is_many=False):
    c = connection.cursor()
    result = None
    rowcount = 0
    try:
        if is_many:
            c.executemany(sql, args)
            connection.commit()
        else:
            c.execute(sql, args)
            result = c.fetchall()
    finally:
        c.close()

    return result, rowcount
