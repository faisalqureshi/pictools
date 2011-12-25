# Faisal Z. Qureshi
# faisal.qureshi@uoit.ca
#
# Absolutely no warranties, always copy your image files before
# attempting to use this tool to muck around with your files.

#!/usr/bin/python

import sys
import getopt
import os
import shutil
import logging

fileTypesAllowed = [".jpg", ".jpeg", ".JPEG", ".JPG"]
dryrun = True

LOG_FILENAME = 'filename2title.log'
logger = logging.getLogger(LOG_FILENAME)
logger.setLevel(logging.INFO)
sh = logging.StreamHandler()
sh.setLevel(logging.INFO)
formatter = logging.Formatter("%(message)s")
logger.addHandler(sh)


def usage():
  msg =  "This tool sets the title/caption info of jpg images equal to the\
  filenames.  The tool only changes the title/caption of an image if\
  currently the image has no title/caption.\n\n\
  Usage: python filename2title.py --rootdir=<dir> [--commit] [--help]\n\n\
  --commit -- The files are only touched if --commit switch is specified.\n\
  --help   -- Prints this message.\n\
  --rootdir=<> -- specifies the directory to look into.  Rememeber files are changed ind place." 
  
  print msg
 
  
def process_files(srcdir):
  global dryrun

  from iptcinfo import IPTCInfo

  files = os.listdir(srcdir) 
  
  for name in files:
    if not os.path.splitext(name)[1] in fileTypesAllowed:
      logger.info('Ignoring %s' % name)
      continue
    else:
      filepath = os.path.join(srcdir,  name)
      logger.info('Processing %s' % name)
      
      try:
        info = IPTCInfo(filepath, force=True)
      
        caption = info.data['caption/abstract']
        if not caption:
          logger.info('Caption not found.')
          info.data['caption/abstract'] = os.path.splitext(name)[0]
          logger.info('New caption -> %s' % info.data['caption/abstract'])
          if not dryrun:
            logger.info('Overwriting %s' % name)
            info.save()
        else:
          logger.info('Found existing caption. Nothing to do')
      except:
        continue
  
  
def main(argv):
  global subdirList
  global fileTypesAllowed
  global dryrun
  
  rootdir = ""
  dryrun = True
  
  try:
    opts, args = getopt.getopt(argv, "", ["help","rootdir=","fileext=","commit"])
    print opts, args
  except getopt.GetoptError:
    usage()
    sys.exit(1)
  
  for opt, arg in opts:
    print opt, arg
    if opt in ["--help"]:
      usage()
      sys.exit(1)
    elif opt in ["--rootdir"]:
      rootdir = arg
      logger.info('Root directory %s', rootdir)
    elif opt in ["--commit"]:
      dryrun = False
    elif opt in ["--fileext"]:
      ext = arg[0];
      if not ext[0] == '.':
        ext = '.' + ext
      fileTypesAllowed.append(ext)
      logger.info('File type allowed %s', ext)
    
  if rootdir=="":
    logger.info('Must specify root directory.')
    usage()
    sys.exit(1)

  if dryrun:
    logger.info('Dryrun. No files will be touched.')

  
  process_files(rootdir)

  
if __name__ == '__main__':
  main(sys.argv[1:])
