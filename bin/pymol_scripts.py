"""
This is a program written by qianyi cheng in deyonker research group
at university of memphis.
"""
import os, sys
import subprocess

def system_run(cmd):
    print(cmd)
    exit = os.system(cmd)
    if ( exit != 0 ):
        print('failed to run:')
        print(cmd)
        sys.exit()

input = sys.argv[1]
name  = input.split('.')[0]
ouput = name+'_h.pdb'
logf = open('log.pml','w')
if len(sys.argv) == 3:
    logf.write('load %s\ncmd.select("sel","%s and not resi %s")\ncmd.h_add("sel")\ncmd.save("./%s")'%(input,name,sys.argv[2],ouput))
elif len(sys.argv) == 2:
    logf.write('load %s\ncmd.h_add("%s")\ncmd.save("./%s")'%(input,name,ouput))
else:
    print("Something is wrong!")
logf.close()
#print("Please run 'pymol -qc log.pml'")
cmd = '/home/qcheng1/bin/pymol -qc log.pml'
system_run(cmd)
