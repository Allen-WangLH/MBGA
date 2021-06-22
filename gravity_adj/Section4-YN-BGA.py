# -*- coding: utf-8 -*-
"""
Created on Mon Dec  9 10:15:02 2019

@author: DELL
"""

import json
import numpy as np
import graobj as gg
import adjmethods as adj

m1 = gg.Meter('CG5','G169')
# m1.msf = 0.999939   #estimated scale factor
m1.msf = 1.000006   #input scale factor (actual calibration measurement)

m2 = gg.Meter('CG5','G170')
# m2.msf = 0.999911   #estimated scale factor
m2.msf = 1.000031   #input scale factor (actual calibration measurement)

n1 = gg.Network("NorthChina",1)
n1.read_pnts('./input/Section4_data/YNCW1508.DZJ')
print(n1)

s1 = gg.Survey("YNCW", "201508")
s1.add_meter(m1)
s1.add_meter(m2)
s1.net = n1
s1.read_survey_file('./input/Section4_data/YNCW1508.169')
s1.read_survey_file('./input/Section4_data/YNCW1508.170')
s1.corr_aux_effect()
# input scale factors obtained by actual calibration measurement
s1.meter_sf_index = [0, 0]
# estimated scale factors
# s1.meter_sf_index = [1, 1]
print(s1)

gravwork = gg.Campaign("201508", 1)

# read file of absolute gravity stations
# gravwork.add_ag_from_file('./input/Section4_data/AGYNCW1508(a).txt')
# gravwork.add_ag_from_file('./input/Section4_data/AGYNCW1508(b).txt')
# gravwork.add_ag_from_file('./input/Section4_data/AGYNCW1508(c).txt')
gravwork.add_ag_from_file('./input/Section4_data/AGYNCW1508(d).txt')


gravwork.add_surveys(s1)
print(gravwork)

gravwork.adj_method = 2 #1:cls ; 2:Baj; 3:Baj1

gravwork.pre_adj()
gravwork.run_adj('./input/Section4_data/grav_baj.txt', 2)
gravwork.export_station('./output/Section4_output/dz201508.txt') # gravity value
gravwork.export_dc('./output/Section4_output/dc201508.txt')  # gravity difference
gravwork.export_dc_all('./output/Section4_output/d_to_d201508.txt')
grav_dict1 = json.load(open('./input/Section4_data/grav_baj.txt'))
