#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 27 18:12:12 2021

@author: edisonsalazar
"""

import numpy as np
import pandas as pd
import os

"""
Script to generate a file with the distance between C12-C4 and the energies 
of S0, S1, S2 and S3 for each optimized PES structure in S1.

The number of roots is 5 for each PES output file and 10 for each VEE file. 
"""
roots_vee = 10 
roots_pes = 5
atom1 = 4
atom2 = 12
em_df = pd.DataFrame()
for filename in os.listdir("SF_VEE_Open_Closed"):
    states = []
    states_op = []
    if filename.endswith(".out"):
        with open(os.path.join("SF_VEE_Open_Closed",filename), 'r+') as file: 
            for line in file:
                if 'Standard Nuclear Orientation' in line:
                    C12_C4 = []
                    for _ in range(atom1 + 1): file.readline() # locate the carbon 4
                    C_4 = file.readline().split()
                    C_4 = [float(C_4[2]),float(C_4[3]),float(C_4[4])]
                    for _ in range(atom2-atom1-1): file.readline() # locate the carbon 12
                    C_12 = file.readline().split()
                    C_12 = [float(C_12[2]),float(C_12[3]),float(C_12[4])]
                    dist_C12_C4 = np.sqrt((C_12[0]-C_4[0])**2+(C_12[1]-C_4[1])**2\
                                          +(C_12[2]-C_4[2])**2)
                elif 'Total energy for state' in line:
                    state = int(line.split()[4].split(':')[0]) -1
                    energy = float(line.split()[5])   
                elif '<S**2>' in line:  
                    s2 = float(line.split()[-1])
                    if s2 < 1.6:     
                        states.append([state,energy])
            long = len(states)
            if states[long-roots_vee +1][0] != 1:
                states_op.append([dist_C12_C4,states[long-roots_vee +1][1], \
                                  states[long-roots_vee +2][1], states[long-roots_vee +3][1],\
                                      states[long-roots_vee +4][1]])
            else: 
                states_op.append([dist_C12_C4,states[long-roots_vee][1], \
                                  states[long-roots_vee +1][1], states[long-roots_vee +3][1],\
                                      states[long-roots_vee +4][1]])
    """
    Making Dataframe 
    """
    lt1_df = pd.DataFrame(states_op)
    em_df = em_df.append(lt1_df)                

                
for filename in os.listdir("PES_S1_DTE"):
    states = []
    states_op = [] 
    if filename.endswith(".out"):
        with open(os.path.join("PES_S1_DTE",filename), 'r+') as file: 
            for line in file:  
                if 'Total energy for state' in line:
                    state = int(line.split()[4].split(':')[0]) -1
                    energy = float(line.split()[5])   
                elif '<S**2>' in line:  
                    s2 = float(line.split()[-1])
                    if s2 < 1.6:     
                        states.append([state,energy])
                elif 'OPTIMIZATION CONVERGED' in line:
                    C12_C4 = []
                    for _ in range(atom1 + 3): file.readline() # locate the carbon 4
                    C_4 = file.readline().split()
                    C_4 = [float(C_4[2]),float(C_4[3]),float(C_4[4])]
                    for _ in range(atom2-atom1-1): file.readline() # locate the carbon 12
                    C_12 = file.readline().split()
                    C_12 = [float(C_12[2]),float(C_12[3]),float(C_12[4])]
                    dist_C12_C4 = np.sqrt((C_12[0]-C_4[0])**2+(C_12[1]-C_4[1])**2\
                                          +(C_12[2]-C_4[2])**2)
                    long = len(states)
                    if states[long-roots_pes +1][0] != 1:
                        states_op.append([dist_C12_C4,states[-roots_pes +1][1], \
                                          states[long-roots_pes +2][1], states[long-roots_pes +3][1],\
                                              states[long-roots_pes +4][1]])
                    else: 
                        states_op.append([dist_C12_C4,states[long-roots_pes][1], \
                                          states[long-roots_pes +1][1], states[long-roots_pes +3][1],\
                                              states[long-roots_pes +4][1]])
    """
    Making Dataframe 
    """
    lt2_df = pd.DataFrame(states_op)
    em_df = em_df.append(lt2_df)
"""
Processing Dataframe 
"""
em_df.columns = ["#C1-C4", "S0", "S1", "S2", "S3"]
em_df = em_df.sort_values(by="#C1-C4")
em_df = em_df.drop_duplicates(subset=["#C1-C4"])
em_df.to_csv("DATA_PY/VEE_PES_S1", index = False, sep='\t')
print(em_df)

    

        

                
         
            

                          