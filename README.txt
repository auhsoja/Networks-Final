Explanation of each file in this folder:

oeis.py - The oeis scraping program. Depends on the "requests" nonstandard library (pip install requests). *Note: cannot be run through command prompt. Instead, run the function "create_xrefs_dict()" in a shell.
 
output.csv - The output after running the oeis program. This contains the first 304236 sequences, which took about 13 hours to fetch.

log.txt - The shell output of oeis.py when making output.csv. Gives detailed information about the rate sequences were fetched.

raw.txt - Contains the python dictionary format of the network. Can be read with a python program to easily retrieve the network in dictionary format.
