def read_sqlite3(db: str, table: str, command: str) -> str:
    """ SQLite database"""
    from sqlite3 import connect
    connect = connect(db, check_same_thread=False)
    cursor = connect.cursor()
    try:
        if len(command) > 0:
            data = cursor.execute(command)
            if command.split()[0].lower() in ['create', 'insert', 'delete', 'drop']:
                connect.commit()
                yield f'\nКоманда *{command}* выполнена\n'
        else:
            data = cursor.execute(f'SELECT * FROM {table}')
        col = [i[0] for i in data.description]
        row = [f'{i}\n\n' for i in data]
        length = f'Число столбцов - {len(col)}, число строк - {len(row)}'
        zv = "".center(105, '*') + '\n\n'
        yield f'\nНазвания столбцов - {col}\n{length}\n{zv}{zv.join(row)}'
    except Exception as error:
        yield f'{error}'
    finally:
        connect.close()


def read_mysql(host: str, port: int, user: str, password: str, db: str, table: str,
               command: str) -> str:
    """ MySQL database """
    import pymysql.cursors
    connecting = pymysql.connect(host=host, port=port, user=user, password=password, db=db,
                                 charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    try:
        with connecting.cursor() as cursor:
            import json
            info = {
                'host_info': connecting.__dict__['host_info'],
                'user': f"{connecting.__dict__['user']}"[2:-1],
                'db': f"{connecting.__dict__['db']}"[2:-1],
                'connect_attrs': connecting.__dict__['_connect_attrs'],
                'server_version': connecting.__dict__['server_version']
            }
            output = f'Информация о сервере и соединении:\n{json.dumps(info, indent=4)}'
            dbname = []
            cursor.execute(f"SHOW DATABASES")
            for i in cursor.fetchall():
                for k in i.values():
                    dbname.append(k)
            if db not in dbname and len(command) == 0:
                yield f'\nНазвания баз: {dbname}'
            elif len(table) == 0 == len(command):
                table_name = []
                cursor.execute(f"SHOW TABLES")
                for i in cursor.fetchall():
                    for k in i.values():
                        table_name.append(k)
                yield f'\nНазвания таблиц: {table_name}'
            else:
                if len(command) > 0:
                    cursor.execute(command)
                    if command.split()[0].lower() in ['create', 'insert', 'delete', 'drop']:
                        connecting.commit()
                        yield f'\nКоманда *{command}* выполнена\n'
                else:
                    cursor.execute(f"SELECT * FROM {table}")
                col = [f'{i[0]}' for i in cursor.description]
                row = [f'{i}\n\n' for i in cursor]
                length = f'Число столбцов - {len(col)}, число строк - {len(row)}'
                zv = "".center(105, '*') + '\n'
                yield f'\n{output}\nНазвания столбцов - {col}\n{length}\n{zv}{zv.join(row)}'
    except Exception as error:
        yield f'{error}'
    finally:
        connecting.close()


def read_postgresql(host: str, port: int, user: str, password: str, db: str, table: str,
                    command: str) -> str:
    """ PostgreSQL database """
    from psycopg2 import connect
    from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
    try:
        connection = connect(user=user, password=password, host=host, port=port, dbname=db)
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        with connection.cursor() as cursor:
            import json
            cursor.execute("SELECT version()")
            server_info = json.dumps(connection.get_dsn_parameters(), indent=4)
            output = (f"Информация о сервере PostGreSQL:\n{server_info}\n"
                      f"Вы подключены к - {cursor.fetchone()[0]}")
            if len(command) > 0:
                cursor.execute(command)
                if command.split()[0].lower() in ['create', 'insert', 'delete', 'drop']:
                    connection.commit()
                    yield f'\nКоманда *{command}* выполнена\n'
            else:
                cursor.execute(f"SELECT * FROM {table}")
            col = [f'{i[0]}' for i in cursor.description]
            row = [f'{i}\n\n' for i in cursor]
            length = f'Число столбцов - {len(col)}, число строк - {len(row)}'
            zv = "".center(105, '*') + '\n'
            yield f'\n{output}\n{zv}Названия столбцов - {col}\n{length}\n{zv}{zv.join(row)}'
    except Exception as error:
        yield (f'Соединение не установлено.\nПроверьте данные: host, port, user, password, '
               f'db name, table name.\n{error}')
    finally:
        cursor.close()


def read_mssql(host: str, port: int, user: str, password: str, db: str, table: str,
               command: str) -> str:
    """ MSSQL database """
    from pyodbc import connect
    connecting = connect(f'DRIVER=SQL Server;SERVER={host};DATABASE={db};'
                         f'ENCRYPT=yes;UID={user};PWD={password}')
    cursor = connecting.cursor()
    try:
        cursor.execute("SELECT @@version;")
        row = cursor.fetchone()
        while row:
            print(row[0])
            row = cursor.fetchone()
            yield '{}'.format(row)
    except Exception as error:
        yield '{}'.format(error)
    finally:
        cursor.close()

    """
    ### connector pymssql ###
    import pymssql
    connecting = pymssql.connect(server=host, user=user, password=password, database=db,
                                 port=port)
    cursor = connecting.cursor(as_dict=True)
    try:
        cursor.execute("SELECT @@version;")
        row = cursor.fetchone()
        while row:
            print(row[0])
            row = cursor.fetchone()
            yield '{}'.format(row)
    except Exception as error:
        yield '{}'.format(error)
    finally:
        connecting.close()
    """
