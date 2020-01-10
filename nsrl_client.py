# c0ded by zer0_p1k4chu
'''
This script is the Client module of the NSRL_Server_API project.
'''
try:
    import traceback
    import json
    import sqlite3
    import sqlalchemy as sa
    import pandas as pd
    import sys
    from os import path
    import requests
    import argparse
    from termcolor import colored,cprint
    import colorama
    colorama.init()
    parser = argparse.ArgumentParser(description='Client Module arguments')
    parser.add_argument('--input', metavar='i', type=str,
                    help='Input CSV File location')
    parser.add_argument('--output',metavar='o', type=str,
                    help ='Output File Location')
    args = parser.parse_args()
    if(args.input is None or args.output is None):
        parser.print_help()
        exit()
    # arguments assign
    file_location = args.input #location of the input file, right now accepted via arguments
    URL = "http://localhost:5000" #API Server URL

    #Terminal colours
    def prRed(string): 
        cprint(string, 'red')
    def prGreen(string): 
        cprint(string, 'green')
    def prCyan(string):
        cprint(string, 'cyan')

    prGreen("[+] Let's get rolling! Doing some pre-flight checks. [+]")
    prGreen("[+] The input file for analysis is "+ file_location)
    prGreen("[+] Building a dataframe from the CSV, will usually take a minute [+]")
    df = pd.read_csv(file_location)
    prGreen("[+] Pre-Processesing done, Now analysing the file. This might take a while depending on number of hashes [+]")
    hashie = df.columns.get_loc("MD5")
    file_loc = df.columns.get_loc("FileNames")
    file_namei = df.columns.get_loc("FileNames")
    f = open(args.output,"w")
    f.write("MD5,FileName,Path,Found,Priv")
    for i in df.values:
        hash_value = i[hashie]
        file_loca = i[file_loc]
        file_name = i[file_namei]
        PARAMS = {'md5':hash_value}
        r = requests.get(url = URL + "/get_info", params = PARAMS)
        data = r.text
        data = json.loads(data)
        if("Not Found" in data['message'] and ("System32" in file_loca or "Program Files" in file_loca or "Windows" in file_loca )):
            prRed("[-] A hash from a Trustworthy file location: "+ file_loca +" is not found in the NSRL_DB:" + hash_value +"[-]")
            log = str(hash_value) + ","+ str(file_name) +","+ str(file_loca) + ",Not Found,YES"
        elif("Found" in data['message'] and ("System32" in file_loca or "Program Files" in file_loca or "Windows" in file_loca )):
            prGreen("[+] Hash found in NSRL_DB: " + hash_value + ".[+]" )
            log = str(hash_value) + ","+ str(file_name) +","+ str(file_loca) + ",Found,YES"
        elif("Not Found" in data['message']):
            prRed("[-] Hash Not found in NSRL_DB: " + hash_value + ". [-]" )
            log = str(hash_value) + ","+ str(file_name) +","+ str(file_loca) + ",Not Found, NO"
        elif("Found" in data['message']):
            prGreen("[+] Hash found in NSRL_DB: " + hash_value + ". [+]" )
            log = str(hash_value) + ","+ str(file_name) +","+ str(file_loca) + ",Found, NO"
        f.write(log + "\n")
    f.close()
except requests.exceptions.ConnectionError: 
    def prRed(string): 
        cprint(string, 'red')
    def prGreen(string): 
        cprint(string, 'green')
    def prCyan(string):
        cprint(string, 'cyan')
    prRed("[-] Target Server is actively refusing connection. Is the server UP? Maybe try changing the Server URL with --url parameter [-]")
except KeyError:
    def prRed(string): 
        cprint(string, 'red')
    def prGreen(string): 
        cprint(string, 'green')
    def prCyan(string):
        cprint(string, 'cyan')
    prRed("[-] Looks like the format of the input file is wrong. Make sure these columns are present: MD5, Name, Path [-]")

except FileNotFoundError:
    def prRed(string): 
        cprint(string, 'red')
    def prGreen(string): 
        cprint(string, 'green')
    def prCyan(string):
        cprint(string, 'cyan')
    prRed("[-] File not found, Are you sure that's the right location? [-]")
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