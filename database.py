
class Database:

    def read_database_sqllite3(self, db, table) -> str:
        import sqlite3
        connect = sqlite3.connect(db, check_same_thread=False)
        cursor = connect.cursor()
        try:
            data = cursor.execute(f'SELECT * FROM {table}')
            col = [i[0] for i in data.description]
            row = [f'{i}\n\n' for i in data]
            length = f'Число столбцов - {len(col)}, число строк - {len(row)}'
            zv = "".center(107, '*')
            yield f'\n{col}\n{length}\n' + zv + zv.join(row)
        except Exception as er:
            print(er)
        finally:
            connect.close()

    def read_database_mysql(self, host, port, user, password, db, table):
        import pymysql.cursors
        connecting = pymysql.connect(host=host, port=port, user=user, password=password, db=db,
                                     charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
        try:
            with connecting.cursor() as cursor:
                cursor.execute(f"SELECT * FROM {table}")
                col = [f'{i[0]}' for i in cursor.description]
                row = [f'{i}\n\n' for i in cursor]
                length = f'Число столбцов - {len(col)}, число строк - {len(row)}'
                zv = "".center(107, '*')
                yield f'\n{col}\n{length}\n' + zv + zv.join(row)
        except Exception as er:
            print(er)
        finally:
            connecting.close()

    def read_database_postgresql(self, host, port, user, password, db, table):
        from psycopg2 import connect
        from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
        try:
            connection = connect(user=user, password=password, host=host, port=port, dbname=db)
            connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            with connection.cursor() as cursor:
                cursor.execute(f"SELECT * FROM {table}")
                col = [f'{i[0]}' for i in cursor.description]
                row = [f'{i}\n\n' for i in cursor]
                length = f'Число столбцов - {len(col)}, число строк - {len(row)}'
                zv = "".center(109, '*')
                yield f'\n{col}\n{length}\n' + zv + zv.join(row)
        except Exception as error:
            print("Ошибка при работе с PostgreSQL", error)
        finally:
            cursor.close()
