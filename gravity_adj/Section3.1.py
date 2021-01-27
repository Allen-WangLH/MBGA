# -*- coding: utf-8 -*-
"""
Created on Mon Dec  9 10:15:02 2019

@author: DELL
"""

import json
import numpy as np
import graobj as gg
import adjmethods as adj
# Initialize the relative gravimeter
# G1 relative gravimeter
m1 = gg.Meter('CG5','C097')   #Type and ID of relative gravimeter
#Calibration table for LCR relative gravimeter
# m1.read_table('./input/benchmark_data/table.DAT')  
# m1.msf = 0.999995  #estimated scale factor
m1.msf = 1.000000  #true scale factor
# G2 relative gravimeter
m2 = gg.Meter('CG5','C098')  #Type and ID of relative gravimeter
 #Calibration table for LCR relative gravimeter
# m2.read_table('./input/benchmark_data/table.DAT') 
# m2.msf = 0.999991  #estimated scale factor
m2.msf = 1.0001   #scale factor with a deviation of 1E-4
# m2.msf = 0.9999   #scale factor with a deviation of -1E-4

#network name and type
n1 = gg.Network("NorthChina1",1)  
#ID, name and coordinates of measuring point
n1.read_pnts('./input/Section3.1_data/QSCW912017.DZJ')  
print(n1) 

# Initialize survey
s1 = gg.Survey("benchmark", "201708")  
s1.add_meter(m1)
s1.add_meter(m2)
s1.net = n1
# Read observation file of relative gravimeter
s1.read_survey_file('./input/Section3.1_data/simG1.C097')  
s1.read_survey_file('./input/Section3.1_data/simG2.C098')  
s1.corr_aux_effect()  # Get earthtide and atomsphere effect
# 0 : use the input scale factor 
# 1 : estimated the scale factor
# [0,0] : BGA method
# [1,1] : MBGA method, estimate scale factor of two instruments
s1.meter_sf_index = [1, 1]
# for Section 3.3
# [0,1],[1,0] : MBGA method, use the scale factor of one instrument to estimate the other instrument
# s1.meter_sf_index = [0, 1]  # use G1 (l=1.000000) to estimate G2
# s1.meter_sf_index = [1, 0]  # use G2 (l=1.000100) to estimate G1 
print(s1)

# Initialize the adjustment object
gravwork = gg.Campaign("201708", 1)

# add information of absolute gravity stations 
gravwork.add_ag_from_file('./input/Section3.1_data/Section3.1_AG.txt')

# Add measurement to adjustment task
gravwork.add_surveys(s1) 
print(gravwork)

#Selection of adjustment methods 
# cls : initial adjustment class
# Baj : Bayesian gravity adjustment
# Baj1 : Modified Bayesian gravity adjustment
gravwork.adj_method = 3 #1:cls ; 2:Baj; 3:Baj1

# checking survey information and generated matrix    
gravwork.pre_adj()
# Running adjustment
# 1 : Nelder-Mead simplex method used for optimization
# 2 : BFGS method used for optimization
gravwork.run_adj('./input/Section3.1_data/grav_baj.txt', 2)
# Output adjustment results
gravwork.export_station('./output/Section3.1_output/dz201708.txt') #gravity value
gravwork.export_dc('./output/Section3.1_output/dc201708.txt')  # gravity difference (unique)
gravwork.export_dc_all('./output/Section3.1_output/d_to_d201708.txt') # gravity difference (back "-" and forth "+")
# export all parameters
grav_dict1 = json.load(open('./input/Section3.1_data/grav_baj.txt'))
