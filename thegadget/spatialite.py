import sqlite3
import sys
from ctypes import util, cdll

# Verify some of the loaded paths and libraries:
lib = util.find_library('spatialite')

print('loaded spatialite library: ', lib)

for p in sys.path:
    print(p)

SQL = """
        select AsWKT(ST_LineFromText('LINESTRING(540000 220000, 540000 221609)', 32123))
        """
connection = sqlite3.Connection(':memory:')
connection.enable_load_extension(True)
# connection.execute("SELECT load_extension('mod_spatialite')")

try:
    connection.load_extension("mod_spatialite")
except:
    print("load_extension(mod_spatialite) failed, Error: ", sys.exc_info()[1], "occured.")
    print('\n\nTry loading using the name of the dll (spatialite.dll)')
    connection.load_extension("spatialite")

with connection as conn:
    cur = conn.execute(SQL)
    results = cur.fetchall()

    for result in results:
        wkt = result[0]
        print(wkt)