# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 16:45:24 2022

@author: DB
"""
import numpy as np
from  Math_3D  import *
from Object_3D import *
def RGBChannelToImgArray(R,G,B):
    return np.array([R,G,B]).transpose(1,2,0)

class Light():
    def __init__(self,pos:Vec_3D=[0,0,0],color:Vec_3D=Vec_3D([255,255,255])/255):
        if type(pos)!=type(Vec_3D([])):
            pos=Vec_3D(pos)
        if type(color)!=type(Vec_3D([])):
            color=Vec_3D(color)
        
        self.pos=pos
        self.color=color
    def CalculateLVec(self,point:Vec_3D):
        return (self.pos-point).Norm()
    def __str__(self):
        return "Light with pos: "+str(self.pos)+" Color: "+str(self.color)
    def __repr__(self):
        return self.__str__()