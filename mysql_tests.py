import MySQLdb
from sql import destroy_dbs, build_dbs, rebuild_tables
import sys, traceback

def migration():
    try:
        conn = MySQLdb.connect(host="localhost",user="rich",
                                passwd="some_pass")
        destroy_dbs(conn)
        print "Successfully dropped dbs"
        build_dbs(conn)
        print "Successfully built dbs"
    except Exception as e:
        # disconnect from server
        conn.close()
        print(traceback.print_exc(file=sys.stdout))
        print e

    else:
        print "Successfully ran migration"
        conn.close()
