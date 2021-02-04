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
m1 = gg.Meter('CG5','C098')  #Type and ID of relative gravimeter
#network name and type
n1 = gg.Network("NorthChina1",1)  
#ID, name and coordinates of measuring point
n1.read_pnts('./input/Section3.4_data/QSCW912017.DZJ')  
print(n1) 
# Initialize survey
s1 = gg.Survey("benchmark", "201708")  
s1.add_meter(m1)
s1.net = n1
# Read observation file of relative gravimeter
s1.read_survey_file('./input/Section3.4_data/simG2.C098')   
s1.corr_aux_effect()  # Get earthtide and atomsphere effect
# 1 : estimated the scale factor
s1.meter_sf_index = [1]
print(s1)
# Initialize the adjustment object
gravwork = gg.Campaign("201708", 1)

# add information of absolute gravity stations 
# greater than the range of the gravity values in the survey network
# >60%
gravwork.add_ag_from_file('./input/Section3.4_data/Section3.4_AG1.txt')
# gravwork.add_ag_from_file('./input/Section3.4_data/Section3.4_AG2.txt')
# gravwork.add_ag_from_file('./input/Section3.4_data/Section3.4_AG3.txt')
# gravwork.add_ag_from_file('./input/Section3.4_data/Section3.4_AG4.txt')
# <60%
# gravwork.add_ag_from_file('./input/Section3.4_data/Section3.4_AG5.txt')
# gravwork.add_ag_from_file('./input/Section3.4_data/Section3.4_AG6.txt')
# gravwork.add_ag_from_file('./input/Section3.4_data/Section3.4_AG7.txt')
# gravwork.add_ag_from_file('./input/Section3.4_data/Section3.4_AG8.txt')
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
gravwork.run_adj('./input/Section3.4_data/grav_baj.txt', 2)
# Output adjustment results
gravwork.export_station('./output/Section3.4_output/dz201708.txt') #gravity value
gravwork.export_dc('./output/Section3.4_output/dc201708.txt')  # gravity difference (unique)
gravwork.export_dc_all('./output/Section3.4_output/d_to_d201708.txt') # gravity difference (back "-" and forth "+")
# export all parameters
grav_dict1 = json.load(open('./input/Section3.4_data/grav_baj.txt'))
