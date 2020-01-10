# c0ded by zer0_p1k4chu
'''
This script is the server module of the NSRL_Server_API project.
'''
try:
    import traceback
    import psutil
    import sqlite3
    import sqlalchemy as sa
    import pandas as pd
    from os import path
    from flask import Flask
    from flask import request
    from flask import jsonify
    from flask_api import status
    import argparse
    from termcolor import colored, cprint
    import colorama
    colorama.init()
    app = Flask(__name__)
    # DB_Location = os.getcwd() + '/nsrl.db' # By default Database will be stored in the current folder
    parser = argparse.ArgumentParser(description='Server Module arguments')
    parser.add_argument('--input', metavar='i', type=str,
                    help='Input CSV File location')
    parser.add_argument('--dir',metavar='d', type=str,
                    help='Directory for storing/checking the database')
    args = parser.parse_args()
    if(args.input is None or args.dir is None):
        parser.print_help()
        exit()
    NSRLFile_Location = args.input
    DB_Location = args.dir + '/nsrl.db'
    @app.route('/',methods=['GET'])
    def index():
        return "Nothing over here, Endpoint for quering: [GET] /get_info with URL-parameter name: md5"


    @app.route('/get_info',methods=['GET'])
    def get_hashinfo():
        conn = sqlite3.connect(DB_Location)
        cur = conn.cursor()
        print(request.args.get)
        if(len(request.args) == 1):
            rows = cur.execute("Select * FROM NSRL_Hashes where MD5 = upper('" + request.args.get('md5') +"');").fetchall()
            if(len(rows) > 0):
                rows = rows[0]
                conn.close()
                return jsonify(message="Found",
                                index=rows[0],
                                sha1=rows[1],
                                md5=rows[2],
                                file_name=rows[3])
            else:
                return (jsonify(message="Not Found in NSRL_DB"),status.HTTP_404_NOT_FOUND)
        else:
            return (jsonify(message="Malformed Request"),status.HTTP_400_BAD_REQUEST)

    # The following function will create a Database and dump in it.
    def create_database():
        df_sample = pd.read_csv(NSRLFile_Location, nrows=10)
        mem_count = df_sample.memory_usage(index=True).sum()
        con = sa.create_engine('sqlite:///'+DB_Location)
        dcs = int((2000000000 / mem_count)/10)
        chunks = pd.read_csv(NSRLFile_Location, chunksize=dcs,encoding='latin-1')
        prCyan("[+] Started dumping database.. Please be patient [+] ")
        for chunk in chunks:
            chunk.to_sql(name='NSRL_Hashes', if_exists='append', con=con)

        prGreen("[+] Database dumping completed. [+]")
        prGreen("[+] Creating index for faster searching. [+]")
        conn = sqlite3.connect(DB_Location)
        cur = conn.cursor()
        cur.execute('CREATE INDEX index_hash ON NSRL_Hashes(MD5)')
        conn.close()
        prGreen("[+] Index creation complete. [+]")
        
     #Terminal colours
    def prRed(string): 
        cprint(string, 'red')
    def prGreen(string): 
        cprint(string, 'green')
    def prCyan(string):
        cprint(string, 'cyan')

    def check_database():
        if path.exists(DB_Location) == False:
            prRed("[-] Database not found, Creating one. Please wait..  [-]")
            create_database()
        else:
            prGreen("[+] Looks like database is already there. [+]")

    prCyan("[+] Checking for database. [+]")
    check_database()
    if __name__ == '__main__':
        app.run(debug=True)


except ModuleNotFoundError:
    def prRed(string): 
        cprint(string, 'red')
    def prGreen(string): 
        cprint(string, 'green')
    def prCyan(string):
        cprint(string, 'cyan')
    prRed("[-] Please install all dependecies using 'pip install -r requirements.txt' [-]")

except Exception as e:
    def prRed(string): 
        cprint(string, 'red')
    def prGreen(string): 
        cprint(string, 'green')
    def prCyan(string):
        cprint(string, 'cyan')
    with open('log.txt', 'a') as f:
        f.write(str(e))
        f.write(traceback.format_exc())
    prRed("[-] Some unknown issue occured. Please check the log file. [-]")
    
except KeyboardInterrupt:
    def prRed(string): 
        cprint(string, 'red')
    def prGreen(string): 
        cprint(string, 'green')
    def prCyan(string):
        cprint(string, 'cyan')
    prRed("[-] CTRL+C detected, Gracefully shutting down. Bye .. Bye .. [-]")