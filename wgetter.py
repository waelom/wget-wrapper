#! /usr/bin/env python
import argparse
import subprocess
import os
import concurrent.futures
#from threading import Lock

def wgetter(command):
    print 'Thread Started'
    #with Lock():
	#print command
    result=subprocess.check_call(command,shell=True)




if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='This is wget_wrapper')

    #Defining arguments
    #Cookies file:
    #URL list
    #No. of threads

    parser.add_argument('--cookie',action='store',help='Use cookies file in wget')
    parser.add_argument('--threads',action='store',default=1,type=int,help='Number of parallel wget downloads, default is 1')
    parser.add_argument('URLS',action='store', type =file, help='File containing urls of files to download')
    args = ''

    ### Parsing command line arguments

    try:
        args = parser.parse_args()
        #print args

    except IOError as e:
        # file doesn't exist
        print e


    #Get urls from file parsed in CLI
    urls = args.URLS.readlines()


    
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.threads) as ex:

        for url in urls:
    
            command = "wget -q  --load-cookies=%s %s" % (args.cookie,url.strip('\n'))
            ex.submit(wgetter, command)
