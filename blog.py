#!/usr/bin/env python3

'''A template for a simple app that interfaces with a database on the class server.
This program is complicated by the fact that the class database server is behind a firewall and we are not allowed to
connect directly to the MySQL server running on it. As a workaround, we set up an ssh tunnel (this is the purpose
of the DatabaseTunnel class) and then connect through that. In a more normal database application setting (in
particular if you are writing a database app that connects to a server running on the same computer) you would not
have to bother with the tunnel and could just connect directly.'''

import mysql.connector
import os.path
from db_tunnel import DatabaseTunnel
from uuid import UUID

# Default connection information (can be overridden with command-line arguments)
# Change these as needed for your app. (You should create a token for your database and use its username
# and password here.)
DB_NAME = "cd0723_blogs"
DB_USER = "token_28dc"
DB_PASSWORD = "BN03DTnHdLCZfbjW"

# If you change the name of this class (and you should) you also need to change it in main() near the bottom
class Blogs:
    '''A simple Python application that interfaces with a database.'''

    def __init__(self, dbHost, dbPort, dbName, dbUser, dbPassword):
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
                use_pure=True,
                autocommit=True,
        )
        self.cursor = self.connection.cursor()

    def close(self):
        self.connection.close()

    def runApp(self):
        username = input("Username: ")
        password = input("Password: ")

        LOGIN_QUERY = f"""
    SELECT id
    FROM User
    WHERE username = '{username}'
    AND password_hash = UNHEX(SHA2('{password}', 256))
        """
        
        self.cursor.execute(LOGIN_QUERY)
        
        userId = None
        for (id,) in self.cursor:
            userId = id
        
        userId = str(UUID(bytes=bytes(userId))).replace('-', '')
        
        POSTS_QUERY = f"""
    SELECT id, title
    FROM BlogPost
    WHERE user_id = UNHEX('{userId}')
        """
        
        print(POSTS_QUERY)
        
        while True:
            print("\nBlog posts:")
            self.cursor.execute(POSTS_QUERY)
            
            for (postId, title) in self.cursor:
                print(f'[{postId:04d}] {title}')
            
            postId = input("\nEnter a post number to delete (or hit Enter to exit): ")
            
            if postId == '':
                break
            
            DELETE_QUERY = f"""
    DELETE FROM BlogPost
    WHERE user_id = UNHEX('{userId}')
    AND id = '{postId}'
            """
            
            self.cursor.execute(DELETE_QUERY)
            print("Post deleted.")


    # Add one method here for each database operation your app will perform, then call them from runApp() above


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
            Blogs(
                dbHost='localhost', dbPort=tunnel.getForwardedPort(),
                dbName=params['dbname'],
                dbUser=params['user'], dbPassword=params['password']
            ) as app:
            
            try:
                app.runApp()
            except mysql.connector.Error as err:
                print("\n\n=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-", file=sys.stderr)
                print("SQL error when running database app!\n", file=sys.stderr)
                print(err, file=sys.stderr)
                print("\n\n=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-", file=sys.stderr)
                
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

