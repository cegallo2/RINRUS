"""
This is a program written by qianyi cheng in deyonker research group
at university of memphis.
Version 1.0
"""
import os, sys, re
from read_write_pdb import *
from read_probe import *
from copy import *

##############   Example   ########################################
#pdb = read_pdb('../comt2/3bwm_h_mg.ent')
#probe = '../comt2/3bwm_h.probe'
#freqf = 'freq_per_res.dat'
#idx_list = ['A',300;'A',301;'A',302]
###################################################################


pdb, res_info, tot_charge = read_pdb(sys.argv[1])
probe = sys.argv[2]
freqf = sys.argv[3]
list4 = sys.argv[4]

#idx_list = []
#for parts in list4.split(','):
#    v = parts.split(':')
#    print v
#    for i in v:
#        idx_list.append(v[0])
#        idx_list.append(int(v[1]))
#c = list4.split(',')
#for i in range(0,len(c),2):
#    idx_list.append(c[i])
#    idx_list.append(int(c[i+1]))
#print('Seeds are:', idx_list)

res_name = {}
res_atom = {}
res_cout = {}
res_info = {}
pdb_res_name = {}
cres_atom = {}

### get key residues ###
res_atom, res_name, res_info, pdb_res_name = get_sel_atoms(pdb,list4,res_atom,res_name,res_info,pdb_res_name)
sel_key = list(res_name.keys())   ### sel_key = [('A',300),('A',301),('A',302)]
print('Seeds are:', sel_key)

### Sort residue by frequency ###
qf = {}
qf[len(sel_key)] = {}
for i in sel_key:
    try:
        qf[len(sel_key)][i[0]].append(i[1])
    except:
        qf[len(sel_key)][i[0]] = [i[1]]
with open(freqf) as f:
    lines = f.readlines()
sm = len(lines)
j = len(sel_key)
for i in range(sm):
#    print(lines[i].split())
    c = lines[i].split()
    Alist = [chr(i) for i in range(ord('A'),ord('Z')+1)]
    if c[0] in Alist:
        cha = c[0]
        res = int(c[1])
        freq = int(c[2])
        if (cha,res) in sel_key: continue
        j += 1
        qf[j] = deepcopy(qf[j-1])
        try:
            qf[j][cha].append(res)
        except:
            qf[j][cha] = [res]
    else:
        cha = ' '
        res = int(c[0])
        freq = int(c[1])
        if (cha,res) in sel_key: continue
        j += 1
        qf[j] = deepcopy(qf[j-1])
        try:
            qf[j][cha].append(res)
        except:
            qf[j][cha] = [res]

### read in probe file ###
res_atom, res_name, res_cout = get_probe_atoms(probe,res_name,res_atom,res_cout)

#res_list = get_res_list(res_atom)
#nres_list = get_res_list(res_atom)
res_detailf = open('model_detail.dat', 'w')
for nm_res in sorted(qf.keys()):
    res_detailf.write("%s residue model\n"%nm_res)
    res_list = qf[nm_res]
    print(nm_res, qf[nm_res])
    for key_sub in sorted(qf[nm_res].keys()):
        res_detailf.write("Chain %s, "%key_sub)
        for res_ids in sorted(qf[nm_res][key_sub]):
            res_detailf.write(" %d"%res_ids)
    res_detailf.write('\n')    
    for key in res_list.keys():
        for res in sorted(res_list[key]):
            if (key,res) in sel_key or res_name[(key,res)] in ['HOH','WAT'] or res_name[(key,res)][:2] == 'WT':
                cres_atom[(key,res)] = res_atom[(key,res)]
            else:
                cres_atom[(key,res)] = get_res_parts(res_name[(key,res)],res_atom[(key,res)])


    nres_atom = {}
    for key in res_list.keys():
        for res in sorted(res_list[key]):
            key1 = (key,res)
#            print(key1)
            if res_name[key1] == 'HOH': 
                res_info[key1] = []
                nres_atom[key1] = cres_atom[key1]
            else:
                nres_atom, res_info, res_name = check_b(key,res,cres_atom[key1],res_info,nres_atom,res_name,pdb_res_name)
                nres_atom, res_info = check_s(key,res,cres_atom[key1],res_info,nres_atom)
                nres_atom, res_info, res_name = check_a(key,res,cres_atom[key1],res_info,nres_atom,res_name,pdb_res_name)
    
    
    for key in sorted(nres_atom.keys()):
        nres_atom = check_bb(key[0],key[1],nres_atom)
    
    res_pick = final_pick(pdb,nres_atom,res_info)
    outf = 'res_%s.pdb'%str(nm_res)
    write_pdb(outf,res_pick)
res_detailf.close()    
