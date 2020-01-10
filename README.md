# NSRLAPI
A server client architecture for querying the NSRL database of known Hashes. [Not affiliated to NSRL or nist.gov in any way]

# Usage
### For Installing all dependecies.
```
git clone github.com/pbssubhash/NSRRLAPI
cd NSRLAPI
pip3 install -r requirements.txt
```
### For starting the server: 
```
python3 nsrl_server.py --input test.csv --dir dir/
```
The Input is a CSV file. Current format only supports hashes extracted from FTKImager in CSV format. If done manually, the CSV format has to comply with the CSV file uploaded as sample_csv.csv. The dir is the directory where the Database is stored. It'll be the current directory unless changed.

Improvement: Add EnCase or arbitary CSV format maybe? (Enhancement) 
### For starting the client:
```
python3 nsrl_client.py --input test.csv --output out.csv
```
The Server API is hardcoded, can be modified in nsrl_client.py file.

# Frequently asked questions?
#### Q. How is it different from other packages providing an API interface? 
A. It's just another package, built to be lightweight and use a DB to store the contents of the NSRLFile.txt for faster quering.

#### Q. How does it work? 
A. In a nutshell, it takes the NSRLFile.txt, carves a database out of it and then uses that database to initialize a Flask API interface which can then be used to query. 

#### Q. What's the use? 
A. It can used in multitude of ways where automation of verifying hashes of multiple systems is required. Like in Massive threat hunting across the network.

#### Q. Need help!!
A. Open an issue. 
