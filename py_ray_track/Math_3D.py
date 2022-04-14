# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 17:01:39 2022

@author: DB
"""
# solve quad

def Solve_quad(a,b,c):
    '''
    

    Parameters
    ----------
    a : float/int
        x^2 coefficient
        
    b : float/int
        x ...
        
    c : float/int
        constant ...
        

    Returns
    -------
    solution tuple
         complex solution flag1,with equal roots,x1,x2
        note that x1 is (-b-delta)/2/a. x2 is (-b+delta)/2/a 

    '''
    _delta=b**2-4*a*c
    flag1=False
    flag2=False
    if _delta<0.:
        flag1= True
    if _delta==0:
        flag2=True
    return flag1,flag2,(-b-_delta**(1/2))/2/a,(-b+_delta**(1/2))/2/a
# 区间
class Interval:
    def __init__(self,s:float,e:float):
        '''
        

        Parameters
        ----------
        s : float
            start point
        e : float
            end point

        Returns
        -------
        None.

        '''
        self.s=s
        self.e=e
    def check(self,t):
        if t<self.e and t>=self.s:
            return True
        else:
            return False
        
    
# 三维向量点乘
def dot_3D(vec1,vec2):
    s=0.
    for i,j in zip(vec1,vec2):
        s+=i*j
    return s
from Object_3D import *
def Cross_3D(vec1,vec2):
    x=vec1[1]*vec2[2]-vec1[2]*vec2[1]
    y=vec1[2]*vec2[0]-vec1[0]*vec2[2]
    z=vec1[0]*vec2[1]-vec1[1]*vec2[0]
    return Vec_3D([x,y,z])