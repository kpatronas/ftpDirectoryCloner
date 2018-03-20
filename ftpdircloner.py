#!/usr/bin/env python
import os
import argparse
from ftplib import FTP

def get_args():
	'''
	Get command line arguments
	'''
	parser = argparse.ArgumentParser(description="Reads a file with directories structure, re-creates the structure on an FTP server")
	parser.add_argument('-s','--server',	 type=str,	help='FTP Server',				required = True)
	parser.add_argument('-u','--username',	 type=str,	help='FTP Username',			required = True)
	parser.add_argument('-p','--password',	 type=str,	help='FTP Password',			required = True)
	parser.add_argument('-f','--prefix',	 type=str,	help='FTP directory prefix',	required = False)
	parser.add_argument('-v','--verbose',	 help='Verbose',	action='store_true', default = False)
	parser.add_argument('-d','--directories',type=str,	help='directories file to read',required = True)
	args = parser.parse_args()
	return args.server,args.username,args.password,args.prefix,args.directories,args.verbose

if __name__ == '__main__':

	ftp_server, ftp_username, ftp_password,ftp_prefix, ftp_directories, verbose = get_args()
	ftp = FTP(ftp_server,ftp_username,ftp_password)	
	dir_append = ftp_prefix

	dir_exists_counter = 0
	dir_created_counter = 0
	with open(ftp_directories) as f:
		for line in f:
			line = line.replace('\n','')
			if dir_append:
				line = dir_append+line
			try:
				ftp.cwd(line)
				dir_exists_counter +=1
				if verbose:
					print("Exists: %s"%(line))
			except Exception as ex:
				ftp.mkd(line)
				dir_created_counter +=1
				if verbose:
					print("Creating: %s"%(line))
	print("directories created: %s "%(dir_created_counter))
	print("directories exist: %s "%(dir_exists_counter))
