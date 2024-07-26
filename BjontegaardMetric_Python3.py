#!/usr/bin/python3

#################################################################################################################################
# Bjontegaard metric
#
# This code is a Python-3.x version of the matlab code: http://www.mathworks.com/matlabcentral/fileexchange/27798-bjontegaard-metric/content/bjontegaard.m
#
#
# Copyright (c) Feb. 2015, Zhongwei Xu, Gici group, DEIC, Universitat Autònoma de Barcelona 
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in
#      the documentation and/or other materials provided with the distribution
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#################################################################################################################################

# include modules MATH and NUMPY
import math  
import numpy 


#################################################
############### Read User Inputs ################
#################################################

print("\n  Read data from a text file. \n  Inside the text file, Please put the Rate in Column 1 and 3, and their corresponding PSNR in Column2 and 4.")

# module INPUT is a built-in function in Python 3.x
filename = input("Please enter filename with path: ")
mode = float(input("Please enter mode (0 or 1 ?): "))



#################################################
############### Compute BDPSNR ##################
#################################################

f = open(filename, 'r')

# define arrays to store the data
Rate1 = []
Rate2 = []
Psnr1 = []
Psnr2 = []

# Loop over lines and extract variables of interest
for line in f:
	if line in ['\n', '\r\n']:
		break
	line = line.strip()
	columns = line.split()
	Rate1.append(math.log(float(columns[0])))
	Rate2.append(math.log(float(columns[2])))
	Psnr1.append(float(columns[1]))
	Psnr2.append(float(columns[3]))
	
#print(Rate1) 	
#print()
#f.close()

if mode == 0:
	# compute PSNR differences
	rates1 = numpy.array(Rate1)
	psnrs1 = numpy.array(Psnr1)
	z_poly1 = numpy.polyfit(rates1,psnrs1,3)

	rates2 = numpy.array(Rate2)
	psnrs2 = numpy.array(Psnr2)
	z_poly2 = numpy.polyfit(rates2,psnrs2,3) 
	
	stack_rate = []
	stack_rate.append(Rate1)
	stack_rate.append(Rate2)
	min_int = numpy.amax(stack_rate)
	max_int = numpy.amin(stack_rate)

	#compute integral
	z_poly_integral1 = numpy.polyint(numpy.poly1d(z_poly1))	
	z_poly_integral2 = numpy.polyint(numpy.poly1d(z_poly2))

	integral1 = numpy.polyval(z_poly_integral1, max_int) - numpy.polyval(z_poly_integral1, min_int)
	integral2 = numpy.polyval(z_poly_integral2, max_int) - numpy.polyval(z_poly_integral2, min_int)

	#compute average differences
	avg_diff = (integral2-integral1)/(max_int-min_int)
	print(avg_diff)

elif mode == 1:	
	# compute Rate differences
	rates1 = numpy.array(Rate1)
	psnrs1 = numpy.array(Psnr1)
	z_poly1 = numpy.polyfit(psnrs1,rates1,3)

	rates2 = numpy.array(Rate2)
	psnrs2 = numpy.array(Psnr2)
	z_poly2 = numpy.polyfit(psnrs2,rates2,3) 

	stack_psnr = []
	stack_psnr.append(Psnr1)
	stack_psnr.append(Psnr2)
	min_int = numpy.amax(stack_psnr)
	max_int = numpy.amin(stack_psnr)

	#compute integral
	z_poly_integral1 = numpy.polyint(numpy.poly1d(z_poly1))	
	z_poly_integral2 = numpy.polyint(numpy.poly1d(z_poly2))

	integral1 = numpy.polyval(z_poly_integral1, max_int) - numpy.polyval(z_poly_integral1, min_int)
	integral2 = numpy.polyval(z_poly_integral2, max_int) - numpy.polyval(z_poly_integral2, min_int)

	#compute average differences
	avg_exp_diff = (integral2-integral1)/(max_int-min_int)
	#avg_diff = 100*(math.pow(10,avg_exp_diff)-1)
	avg_diff = 100*(math.pow(math.exp(1),avg_exp_diff)-1)	
	print(avg_diff,'%')







