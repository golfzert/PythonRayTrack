# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 15:45:10 2022

@author: DB
"""
from Math_3D import *
from math import sqrt
#from Color import *
# 导入虚函数
from abc import ABC, abstractmethod
import copy
# 3d基类
class Class_3D():
    pass
# 位置
class Position(Class_3D):
    def __init__(self,position=(0,0,0)):
        try:
            self._x,self._y,self._z=position
        except Exception as e:
            raise e

        '''
    def __init__(self,position):
        try:
            self.x,self.y,self.z=position
        except Exception as e:
            raise e 
            '''
    def Get_Position(self):
        return (self._x,self._y,self._z)
# 3D 物品
class Object_3D(Class_3D):
    object_id=0
    @abstractmethod
    def __init__(self):
        self.id=self._GetID()
        self._UpdateID()
        pass
    @abstractmethod
    def Intersection(self):
        pass
    def _UpdateID(self):
        Object_3D.object_id+=1
    def _GetID(self):
        return Object_3D.object_id

# 3维向量
class Vec_3D(Object_3D):
    def __init__(self,vec):
        self.vec=vec
    def __getitem__(self,ind):
        return self.vec[ind]
    def __setitem__(self,ind,value):
        self.vec[ind]=value
    
    def __add__(self,vec2):
        new_vec=[]
        for i,j in zip(self,vec2):
            new_vec.append(i+j)
        return Vec_3D(new_vec)
    #用**代替点乘
    def __pow__(self,vec2):
        return dot_3D(self, vec2)
    # 重载右乘 n*vec
    def __rmul__(self,n):
        new_vec=[]
        for i in self:
            new_vec.append(i*n)
        return Vec_3D(new_vec)
    # 重载左乘
    def __mul__(self,n):
        return n*self
    # 重载减号
    def __sub__(self,vec2):
        return self+-1*vec2
    def __rsub__(self,vec2):
        return vec2+-1*self
    #重载除号
    def __truediv__(self,n):
        return self*(1/n)
    # 重载迭代器
    def __iter__(self):
        return iter(self.vec)
    # 重载next
    def __next__(self):
        return next(iter(self))
    # 重载 str
    def __str__(self):
        return self.vec.__str__()
    def __repr__(self):
        return self.__str__()
    def Intersection(self):
        pass
    #长度
    
    def Length(self):
        return sqrt(self**self)
    #单位向量
    def Norm(self):
        return  self/self.Length()
    
    
#物体的反射系数
class Coefficient(Object_3D):
    def   __init__(self,diffuse_c_vec=Vec_3D([0.4,0.4,0.4]),\
                   specular_c_vec=Vec_3D([1,1,1]),ambient_c_vec=Vec_3D([0.001,0.001,0.001]),p:float=6,k_m:float=0.01):
        if type(diffuse_c_vec)!=type(Vec_3D([])):
            diffuse_c_vec=Vec_3D(diffuse_c_vec)
        if type(specular_c_vec)!=type(Vec_3D([])):
            specular_c_vec=Vec_3D(specular_c_vec)
        if type(ambient_c_vec)!=type(Vec_3D([])):
            ambient_c_vec=Vec_3D(ambient_c_vec)
        self._d=diffuse_c_vec
        self._s=specular_c_vec
        self._a=ambient_c_vec
        self._s_p=p
        self._km=k_m
# ray_3D
class Ray_3D(Object_3D):
    def __init__(self,s:Vec_3D,d:Vec_3D):
        if type(s) != type(Vec_3D([])):
            s=Vec_3D(s)
        if type(d) != type(Vec_3D([])):
            d=Vec_3D(d)
        self.s,self.d=s,d
    def Intersection(self,ray,interval):
        pass
    def CalcPoint(self,t):
        #计算点位置
        return self.s+t*self.d
    def __str__(self):
        return "start point: "+str(self.s)+" direct: "+str(self.d)
    def __repr__(self):
        return self.__str__()
# shape
class Shape_3D(Object_3D):
    pass

# 球
class Sphere(Shape_3D):
    def __init__(self,center=(0,0,0),radius=1.0):
        if type(center)!=type(Vec_3D([])):
            center=Vec_3D(center)
        self._c,self._r=center,radius
        self._color=Vec_3D([123,255,255])/255
        self._coef=copy.deepcopy(Coefficient())
        #self.id=self.GetID()
        #self.UpdateID()
        super().__init__()
    
    def Set_bs_color(self,RGB):
        self._color=RGB
    def Set_light_coefficinet(self,coefficient):
        self._coef=copy.deepcopy(coefficient)
    def __str__(self):
        return "Sphere id:"+str(self.id)+" with center: "+str(self._c)+" radius: "+str(self._r)
    def __repr__(self):
        return self.__str__()
    def Intersection(self,ray:Ray_3D,interval:Interval):
        '''
        返回最小交点t值,以及物品id
        Parameters
        ----------
        ray : Ray_3D
            DESCRIPTION.
        interval : Interval
            DESCRIPTION.

        Returns
        -------
        TYPE
            DESCRIPTION.

        '''
        if not isinstance(ray, Ray_3D):
             print("invalid ray!",type(ray))
        if type(interval)!=type(Interval(0,0)) and type(interval)==type(list()):
            interval=Interval(interval[0], interval[1])
        a=ray.d**ray.d
        b=2*(ray.s-self._c)**ray.d
        c=dot_3D(ray.s-self._c,ray.s-self._c)-self._r**2
        com_flag,equ_flag,x1,x2=Solve_quad(a,b,c)
        #print(x1,x2)
        if com_flag:
            return float("inf"),self.id
        if interval.check(x1):
            return x1,self.id
        if interval.check(x2):
            return x2,self.id
        return float('inf'),self.id
    
    def GetNormalVec(self,point:Vec_3D):
        '''
        point must in the surface of sphere

        Parameters
        ----------
        point : Vec_3D
            DESCRIPTION.

        Returns
        -------
        NormalVec

        '''
        return (point-self._c).Norm()
    def GetColorAndCoef(self,point:Vec_3D):
        return self._color,self._coef
    
        
    
class Triangle(Shape_3D):
    def __init__(self,p1,p2,p3):
        self.p1,self.p2,self.p3=p1,p2,p3
    def Intersection(self,ray,interval):
        pass
    def GetNormalVec(self,*args):
        pass
    
#三维平面 
    
class Plane(Shape_3D):
    def __init__(self,p1:Vec_3D,p4:Vec_3D,n:Vec_3D,ratio:float):
        '''
        ratio是高度比宽度的比值
        '''
        if type(p1)!=Vec_3D([]):
            p1=Vec_3D(p1)
        if type(p4)!=Vec_3D([]):
            p4=Vec_3D(p4)
        if type(n)!=Vec_3D([]):
            n=Vec_3D(n)
        self._p1,self._p4,self._n=p1,p4,n
        self._c=(p1+p4)/2
        l=(p1-p4).Length()
        self.Width=l/(ratio**2+1)**.5
        self.Height=self.Width*ratio
        
    def Intersection(self,ray,interval):
        pass
    def GetNormalVec(self,*args):
        pass
    def __str__(self):
        return "Plane With Center: "+str(self._c)+" with diag point: "+str(self._p1)+" And "+str(self._p4)+" Norm: "+str(self._n)+" W: "+str(self.Width)\
            +" H: "+str(self.Height)
    def __repr__(self):
        return str(self)
#the texture if plane
def DeC1(p):
    return (Vec_3D([1,1,1]) if (int(p[0])%2 == int(p[1])%2) else Vec_3D([0,0,0]))
def DeC2(p):
    return Vec_3D([0.1,0.1,0.1])
class InfinitePlane(Shape_3D):

    def __init__(self,p:Vec_3D=Vec_3D([0,0,0]),n:Vec_3D=[0,0,1],color=None):
        if not isinstance(p, Vec_3D):
            p=Vec_3D(p)
        if not isinstance(n, Vec_3D):
            n=Vec_3D(n)
        self._p=p
        self._n=n.Norm()
        self._coef=copy.deepcopy(Coefficient([0.1,0.1,0.1],[1,1,1],[0.001,0.001,0.001],10,0))

        self._color=color
        super().__init__()
    def Intersection(self,ray:Ray_3D,interval:Interval):
        #print("plane int")
        _dn=ray.d**(self._n)
        if abs(_dn)<1e-6:
            return float('inf'),-1
        _t=(self._p-ray.s)**self._n/_dn
        if interval.check(_t):
            #print('hit',ray,interval,_t,ray.CalcPoint(_t))
            return _t,self.id
        return float('inf'),-1
    def GetNormalVec(self,point:Vec_3D):
        return self._n
    def GetColorAndCoef(self,point:Vec_3D):
        return self._color(point),self._coef
        
        
        
