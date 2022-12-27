#!/usr/bin/env python3

'''A simple Python application to display a list of all episodes of a TV series.
This program is complicated by the fact that the class database server is behind a firewall and we are not allowed to
connect directly to the MySQL server running on it. As a workaround, we set up an ssh tunnel (this is the purpose
of the DatabaseTunnel class) and then connect through that. In a more normal database application setting (in
particular if you are writing a database app that connects to a server running on the same computer) you would not
have to bother with the tunnel and could just connect directly.'''

import mysql.connector
import os.path
from db_tunnel import DatabaseTunnel

DB_HOST = "cs.westminstercollege.edu"
DB_SSH_PORT = 2322
DB_SSH_USER = "student"
DB_PORT = 3306

# Default connection information (can be overridden with command-line arguments)
DB_SSH_KEYFILE = "id_rsa.cmpt307"
DB_NAME = "cd0723_books"
DB_USER = "	token_fba2"
DB_PASSWORD = "WwypfCiSUMPv1VVw"

# The query that will be executed
QUERY = """
select Book.title,Book.year,Author.name,Series.title,BookInSeries.number
from Book 
inner join BookInSeries on Book.id = BookInSeries.bookId
inner join Series on Series.id = BookInSeries.seriesId
inner join Author on Book.authorId = Author.id
WHERE Book.title like concat("%",%s,"%")
"""

class BookQuery:
    '''A simple Python application to display a list of all episodes of a TV series.'''

    def __init__(self, dbHost, dbPort, dbName, dbUser, dbPassword):
        '''Creates an IMDbEpisodeQuery with the specified connection information'''
        self.dbHost, self.dbPort = dbHost, dbPort
        self.dbName = dbName
        self.dbUser, self.dbPassword = dbUser, dbPassword

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, *args):
        self.close()

    def connect(self):
        self.connection = mysql.connector.connect(
                host=self.dbHost, port=self.dbPort, database=self.dbName,
                user=self.dbUser, password=self.dbPassword,
                use_pure=True
        )
        self.cursor = self.connection.cursor()

    def close(self):
        self.connection.close()

    def runApp(self):
        while True:
            line = input("\nEnter the name of any book (or hit Enter to quit): ")
            if not line.strip():
                break

            print("Querying database...")
            self.queryBooks(line)


    def queryBooks(self, title):
        # Execute the query with the name of the series we're searching for
        # Note the "(name,)" below - the trailing comma "," is needed to make it a tuple
        # because "(name)" evaluates to the same as just "name"
        self.cursor.execute(QUERY, (title,))

        resultCount = 0
        for (BookTile, year, AuthorName, SeriesTile, Number) in self.cursor:
            resultCount += 1
            print(f"{BookTile} {year} {AuthorName} {Number}")

        print(f"\n{resultCount} books in total.\n")


def main():
    import sys
    '''Entry point of the application. Uses command-line parameters to override database connection settings, then invokes runApp().'''
    # Default connection parameters (can be overridden on command line)
    params = {
        'dbname':       DB_NAME,
        'user':         DB_USER,
        'password':     DB_PASSWORD
    }

    needToPrintHelp = False

    # Parse command-line arguments, overriding values in params
    i = 1
    while i < len(sys.argv) and not needToPrintHelp:
        arg = sys.argv[i]
        isLast = (i + 1 == len(sys.argv))

        if arg in ("-h", "-help"):
            needToPrintHelp = True
            break

        elif arg in ("-dbname", "-user", "-password"):
            if isLast:
                needToPrintHelp = True
            else:
                params[arg[1:]] = sys.argv[i + 1]
                i += 1

        else:
            print("Unrecognized option: " + arg, file=sys.stderr)
            needToPrintHelp = True

        i += 1

    # If help was requested, print it and exit
    if needToPrintHelp:
        printHelp()
        return

    try:
        with \
            DatabaseTunnel() as tunnel, \
            BookQuery(
                dbHost='localhost', dbPort=tunnel.getForwardedPort(),
                dbName=params['dbname'],
                dbUser=params['user'], dbPassword=params['password']
            ) as app:
            app.runApp()
    except mysql.connector.Error as err:
        print("Error communicating with the database (see full message below).", file=sys.stderr)
        print(err, file=sys.stderr)
        print("\nParameters used to connect to the database:", file=sys.stderr)
        print(f"\tDatabase name: {params['dbname']}\n\tUser: {params['user']}\n\tPassword: {params['password']}", file=sys.stderr)
        print("""
(Did you install mysql-connector-python and sshtunnel with pip3/pip?)
(Are the username and password correct?)""", file=sys.stderr)


def printHelp():
    print(f'''
Accepted command-line arguments:
    -help, -h          display this help text
    -dbname <text>     override name of database to connect to
                       (default: {DB_NAME})
    -user <text>       override database user
                       (default: {DB_USER})
    -password <text>   override database password
    ''')


if __name__ == "__main__":
    main()

