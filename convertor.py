from convertor_class import attribute
from convertor_class import foreignkey
from convertor_class import table
from convertor_class import relation
from convertor_class import tree
from convertor_class import output
import xml.etree.ElementTree as ET
from copy import deepcopy
import os
import signal
import time
from eralchemy import render_er
from sqlalchemy import create_engine
import subprocess
from PIL import Image
from query_func import *


###
def import_sql(_conn, _file):
    # Open the .sql file
    sql_file = open(_file, 'r')
    # Create an empty command string
    sql_command = ''
    # Iterate over all lines in the sql file
    for line in sql_file:
        # Ignore commented lines
        if not line.startswith('--') and line.strip('\n'):
            # Append line to the command string
            sql_command += line.strip('\n')

            # If the command string ends with ';', it is a full statement
            if sql_command.endswith(';'):
                # Try to execute statement and commit it
                try:
                    _conn.execute(str(sql_command))

                # Assert in case of error
                except:
                    _conn.execute(str(sql_command))
                    _conn.commit()
                    print(str(sql_command))
                    print('Ops')

                # Finally, clear command string
                finally:
                    sql_command = ''
###


if __name__ == '__main__':
    dbms = []
    while (True):
        commands = input('YTDB> ').split()
        if (commands[0] == 'exit'):
            break
        if (commands[0] == 'parse'):
            if (os.path.isfile(commands[1])):
                db = tree(commands[1])
                dbms.append(db)
                print('\nNew Database Successfully Added\n')
            else:
                print('\nInvalid Path\n')

        elif (commands[0] == 'showtables'):
            for db in dbms:
                for table in db.tables.values():
                    print(table.name)
                    for att in table.attlist.values():
                        print('->', att.name)
                    print('\n')

        elif (commands[0] == 'transql'):
            if dbms:
                db = dbms[-1]
                ###
                output(commands[1], db).export()
                ###
                print('\nNew SQL file Successfully Added\n')
            else:
                print('\nplease construct at least one database\n')
         # create ERD png
        ###
        elif (commands[0] == 'tranERD'):
            # TODO
            if dbms:
                # select query result as db
                if len(commands) == 1:
                    db = dbms[-1]
                    output('demo.er', db).export_ERD()
                # select orgin result as db
                else:
                    db = dbms[0]
                    output(commands[1], db).export_ERD()
                bashCommand = "/Users/apple/.local/bin/erd -i ./demo.er -o ./demo.png"
                process = subprocess.Popen(
                    bashCommand.split(), stdout=subprocess.PIPE)
                # output, error = process.communicate()
                time.sleep(1)
                print('\nNew ER file Successfully Added\n')
                image = Image.open('demo.png')
                image.show()
                # os.killpg(os.getpgid(process.pid), signal.SIGINT)
                process.terminate()

            else:
                print('\nplease construct at least one database\n')
        ###

        elif (commands[0] == 'sqlschema'):

            if (os.path.isfile(commands[1])):
                engine = create_engine(
                    "mysql+mysqlconnector://root:qqwe@localhost/db?charset=utf8")
                conn = engine.connect()
                conn.execute("commit")
                try:
                    conn.execute("create database tmp")
                except:
                    conn.execute("drop database tmp")
                    conn.execute("create database tmp")

                engine = create_engine(
                    "mysql+mysqlconnector://<username>:<password>@localhost/tmp?charset=utf8")
                conn = engine.connect()
                import_sql(conn, commands[1])
                render_er(
                    "mysql+mysqlconnector://root:qqwe@localhost/tmp?charset=utf8", 'erd_from_sqlite.png')
                conn.execute("drop database tmp")
                conn.close()
                image = Image.open('erd_from_sqlite.png')
                image.show()
            else:
                print('\nInvalid Path\n')

        elif (commands[0] == 'query'):
            if not dbms:
                print('\nthere is no database yet\n')
            elif (commands[1] == '-e'):
                ###
                query_db = deepcopy(dbms[0])
                ###
                query_db = queryEntity(commands[2], query_db)
                if (query_db == None):
                    print('\nCan not find entity\n')
                else:
                    dbms.append(query_db)
                    print('\nSuccessfully Query\n')
            elif (commands[1] == '-a'):
                ###
                query_db = deepcopy(dbms[0])
                ###
                query_db = queryAttribute(commands[2], query_db)
                if (query_db == None):
                    print('\nCan not find attribute\n')
                else:
                    dbms.append(query_db)
                    print('\nSuccessfully Query\n')

            elif (commands[1] == '-r'):
                ###
                query_db = dbms[0]
                ###
                query_db = queryRelation(commands[2], query_db)
                if (query_db == None):
                    print('\nCan not find relation\n')
                else:
                    dbms.append(query_db)
                    print('\nSuccessfully Query\n')
            else:
                print('\nwrong query command\n')
        elif (commands[0] == 'HELP'):
            print('\nexit       - exit the program')
            print('parse -x   - parse xml file (x) into database')
            print('showtables - show all tables in database')
            print('transql -x - export database into sql file (x)\n')
            print(
                'tranERD -x - export ER diagram into .er file (x) and export .png file\n')
            print('sqlschema -x - export sql database schema .png file\n')
        else:
            print('\nInvalid Command. Check HELP for more information\n')

    print('bye.')
