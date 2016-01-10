#! /usr/bin/env python
import argparse
import subprocess
import concurrent.futures
import logging

def wgetter(wget_args):
    #pass wget command to shell

    command = "wget -q %(passed_args)s %(cookie_file)s %(url)s" % wget_args
    print "Thread Started: ", command
    result=subprocess.check_call(command,shell=True)
    logging.info(command)
    return result,wget_args['url']




if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='This script wraps wget and creates threads as needed')

    #Defining arguments
    #cookie:Cookies file
    #No. of threads
    #Wget arguments: passed as is
    #logfile: log all downloaded files
    #URLs: file with a list of urls to download



    parser.add_argument('--cookie',action='store',help='Use cookies file in wget')
    parser.add_argument('--threads',action='store',default=1,type=int,help='Number of parallel wget downloads, default is 1')
    parser.add_argument('--towget', action='store',help='pass following arguments to wget as is')
    parser.add_argument('--log',action='store',help='log file path')
    parser.add_argument('URLS',action='store', type =file, help='File containing urls of files to download')
    args = ''

    ### Parsing command line arguments

    try:
        args = parser.parse_args()


    except IOError as e:
        # file doesn't exist
        print "URLs file error:", e
        quit()

    logfile= args.log
    logformat="%(asctime)s : %(levelname)s :%(message)s"
    try:
        logging.basicConfig(filename=logfile,level=logging.INFO,format=logformat)
    except IOError as e:
        print "log file error:", e
        quit()


    #Get urls from file parsed in CLI
    urls = args.URLS.readlines()


    
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.threads) as ex:

        futures = []
        wget_args = {}
        wget_args['passed_args']= args.towget if args.towget else ''
        wget_args['cookie_file']= "--load-cookies="+args.cookie if args.cookie else ''


        for url in urls:

            url = url.strip("\n")      #remove newline feed if it exist
            # if url is not empty
            if url:
                wget_args['url']= url

                #logging.info(url)
                f=ex.submit(wgetter, wget_args)
                futures.append(f)


        for f in futures:

            if f.result()[0]==0:
                logging.info(f.result()[1] + " Successfully Downloaded")
            else:
               logging.info(f.result()[1] + " Error: " + f.result()[0])






