#!/usr/bin/env python
#-*- coding:utf-8 -*-

###############################################################
# CLAM: Computational Linguistics Application Mediator
# -- CLAM Wrapper script Template --
#       by Maarten van Gompel (proycon)
#       https://proycon.github.io/clam
#       Centre for Language and Speech Technology
#       Radboud University Nijmegen
#
#       (adapt or remove this header for your own code)
#
#       Licensed under GPLv3
#
###############################################################

#This is a template wrapper which you can use a basis for writing your own
#system wrapper script. The system wrapper script is called by CLAM, it's job it
#to call your actual tool.

#This script will be called by CLAM and will run with the current working directory set to the specified project directory

#This wrapper script uses Python and the CLAM Data API.
#We make use of the XML settings file that CLAM outputs, rather than
#passing all parameters on the command line.


#If we run on Python 2.7, behave as much as Python 3 as possible
from __future__ import print_function, unicode_literals, division, absolute_import

#import some general python modules:
import sys

#import CLAM-specific modules. The CLAM API makes a lot of stuff easily accessible.
import clam.common.data
import clam.common.status
import os
import shutil
import glob
import errno

#When the wrapper is started, the current working directory corresponds to the project directory, input files are in input/ , output files should go in output/ .

#make a shortcut to the shellsafe() function
shellsafe = clam.common.data.shellsafe

#this script takes three arguments from CLAM: $DATAFILE $STATUSFILE $OUTPUTDIRECTORY
#(as configured at COMMAND= in the service configuration file, there you can
#reconfigure which arguments are passed and in what order.
datafile = sys.argv[1]
statusfile = sys.argv[2]
outputdir = sys.argv[3]

#If you make use of CUSTOM_FORMATS, you need to import your service configuration file here and set clam.common.data.CUSTOM_FORMATS
#Moreover, you can import any other settings from your service configuration file as well:

#from yourserviceconf import CUSTOM_FORMATS

#Obtain all data from the CLAM system (passed in $DATAFILE (clam.xml)), always pass CUSTOM_FORMATS as second argument if you make use of it!
clamdata = clam.common.data.getclamdata(datafile)

#You now have access to all data. A few properties at your disposition now are:
# clamdata.system_id , clamdata.project, clamdata.user, clamdata.status , clamdata.parameters, clamdata.inputformats, clamdata.outputformats , clamdata.input , clamdata.output

clam.common.status.write(statusfile, "Starting...")


#=========================================================================================================================

try:
    os.makedirs("input/images", exist_ok=True);
except OSError as e:
    if e.errno != errno.EEXIST:
        raise

images_tbl_path=''  
header_template_path=''
for inputfile in clamdata.input:
  inputtemplate = inputfile.metadata.inputtemplate
  inputfilepath = str(inputfile)
  ext = os.path.splitext(inputfilepath)[1]
  if (ext == '.fits'):
      newPath = shutil.move(inputfilepath, "input/images");
      clam.common.status.write(statusfile, "Moved: "+inputfilepath);
  if (ext == '.tbl'):
      images_tbl_path = inputfilepath
      clam.common.status.write(statusfile, "images_tbl_path: "+images_tbl_path);      
  if (ext == '.hdr'):
      header_template_path = inputfilepath
      clam.common.status.write(statusfile, "header_template_path: "+header_template_path); 

#========================================================================================

# Below is an example of how to read global parameters and how to invoke your
# actual system. You may want to integrete these into one of the solution
# examples A,B or C above.

#-- Read global parameters? --

# Global parameters are accessed by addressing the clamdata instance as-if were a simple dictionary.

#parameter = clamdata['parameter_id']

#-- Invoke your actual system? --

# note the use of the shellsafe() function that wraps a variable in the
# specified quotes (second parameter) and makes sure the value doesn't break
# out of the quoted environment! Can be used without the quote too, but will be
# do much stricter checks then to ensure security.

cmd=''
if (clamdata['q']):
    cmd+='-q -p input/images'
else:
    cmd+='-p input/images'
if (clamdata['d']):
    cmd+=' -d'
if (clamdata['e']):
    cmd+=' -e'
if (clamdata['X']):
    cmd+=' -X'
if (clamdata['b']):
    cmd+=' -b '+shellsafe(clamdata['b'])
if (clamdata['r']):
    cmd+=' -r '+shellsafe(clamdata['r'])
if (clamdata['X']):
    cmd+=' -X '+shellsafe(clamdata['X'])
    
try:
    os.makedirs("output/images", exist_ok=True);
except OSError as e:
    if e.errno != errno.EEXIST:
        raise    
    
os.system("mProjExec " + cmd +" "+ shellsafe(images_tbl_path)+" "+shellsafe(header_template_path)+" "+shellsafe("output/images")+" "+shellsafe("stats.tbl"));

# Rather than execute a single system, call you may want to invoke it multiple
# times from within one of the iterations.

#A nice status message to indicate we're done
clam.common.status.write(statusfile, "Done",100) # status update

sys.exit(0) #non-zero exit codes indicate an error and will be picked up by CLAM as such!
