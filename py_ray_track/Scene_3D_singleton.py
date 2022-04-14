# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 20:51:30 2022

@author: DB
"""
from Object_3D import *
from Math_3D import *
from Color import *
import numpy as np
'''
用于场景的类,用于储存各种物品以及光源.主要使用字典
'''
_objectDic={}
_lightPosList=[]
_bg_color=Vec_3D([255,255,255])/255#背景颜色
_eye_point=Vec_3D([-1,0,0])
_eye_base=[Vec_3D([0,-1,0]),Vec_3D([0,0,1]),Cross_3D(Vec_3D([0,-1,0]),Vec_3D([0,0,1]))]

#_plane=Plane([0,2,2], [0,-2,-2],[-1,0,0],1)
#计算平面位置
_t=5
_plane_center=Ray_3D(_eye_point, _eye_base[2]).CalcPoint(-1*_t)
_plane_size=[4,4]
_img_size=[400,400]
_R=np.zeros(_img_size)
_G=np.zeros(_img_size)
_B=np.zeros(_img_size)
_RGB=[_R,_G,_B]
#设置eye的位置
def SetEye(e:Vec_3D=(-1,0,0),u:Vec_3D=(0,-1,0),v:Vec_3D=(0,0,1),d=5):
    global _eye_point,_eye_base,_t,_d,_plane_center
    if type(e)!=Vec_3D([]):
        e=Vec_3D(e)
    if type(u)!=Vec_3D([]):
        u=Vec_3D(u)
    if type(v)!=Vec_3D([]):
        v=Vec_3D(v)
    _eye_point=e
    _eye_base=[u,v,Cross_3D(u, v)]
    _t=d
    _plane_center=Ray_3D(_eye_point, _eye_base[2]).CalcPoint(-1*_t)
def SetPalneAndImgSize(pw,ph,Width,Height):
    global _img_size,_plane_size
    _img_size=[Width,Height]
    _plane_size=[pw,ph]
    _UpdateRGB()
def _UpdateRGB():
    global _R,_G,_B
    _R=np.zeros(_img_size)
    _G=np.zeros(_img_size)
    _B=np.zeros(_img_size)
    
def Set_bgColor(color:Vec_3D=Vec_3D([255,255,255])/255):
    global _bg_color
    if type(color)!=Vec_3D([]):
        color=Vec_3D(color)
    _bg_color=color
    
#为场景添加物品
def AddNewObject(shape:Shape_3D):
    _objectDic[shape.id]=shape
#获取物品的法向量
def GetNormalVec(obj:Shape_3D,point:Vec_3D):
    '''
    做成函数,防止接口不同
    '''
    return obj.GetNormalVec(point)
#获取物品在point的颜色
def GetColorAndCoef(obj:Shape_3D,point:Vec_3D):
    return obj.GetColorAndCoef(point)
#添加光源
def AddNewLight(light:Light):
    _lightPosList.append(light)
#删除光源
def DelLight(ind:int):
    _lightPosList.pop(ind)
#计算lam反射
def _DiffuseShading(color_l,color_o,coef,n:Vec_3D,l:Vec_3D):
    newColor=[]
    for _col_l,_col_o,_coe in zip(color_l,color_o,coef):
        newColor.append(_col_l*_col_o*_coe*max(0,dot_3D(n, l)))
    #print('D',newColor)
    return Vec_3D(newColor)
#计算Blin
def _SpecularShading(color_l,color_o,coef,n:Vec_3D,l:Vec_3D,v:Vec_3D,p):
    newColor=[]
    h=(v+l).Norm()
    for _col_l,_col_o,_coe in zip(color_l,color_o,coef):
        c_c=_coe*_col_l*_col_o*max(dot_3D(h,n),0)**p
        #print(c_c)
        newColor.append(c_c)
    #print('S',newColor,coef,"V",v,"L",l,h,n,max(dot_3D(h,n),0)**p)
    return Vec_3D(newColor)
def _AmbientShading(color_l,color_o,coef):
    newColor=[]
    for _col_l,_col_o,_coe in zip(color_l,color_o,coef):
        newColor.append(_coe*_col_l*_col_o)
    #print('A',newColor)
    return Vec_3D(newColor)
        
#计算颜色
def EvalPixelColor(res:tuple,ray:Ray_3D,kk:float=4):
    '''
    假设res是离e最近的交点的物体返回的交点结果,ray是对应的e射出的射线
    '''
    #print('eval')
    object_id=res[1]#物品id
    point=ray.CalcPoint(res[0])#交点
    obj=_objectDic[object_id]#物品
    n_vec=GetNormalVec(obj,point)#获取法向量
    obj_color,pixel_coef=GetColorAndCoef(obj, point)
    pixel_color=Vec_3D([0,0,0])
    v=-1*ray.d.Norm()
    for light_obj in _lightPosList:
        #print(light_obj)
        pixel_color+=_AmbientShading(light_obj.color, obj_color, pixel_coef._a)
        l=light_obj.CalculateLVec(point)
        shadowRay=Ray_3D(point, l)
        #print('S',shadowRay)
        shadow_hit_res=_Intersection(shadowRay,s=0.01,t1=(light_obj.pos-point).Length())
        if shadow_hit_res[1]==-1:
            pixel_color+=_DiffuseShading(light_obj.color, obj_color, pixel_coef._d, n_vec\
                                     ,l )
            #print(_SpecularShading(light_obj.color, obj_color, pixel_coef._s, n_vec, l, v, pixel_coef._s_p))
            pixel_color+=_SpecularShading(light_obj.color, obj_color, pixel_coef._s, n_vec, l, v, pixel_coef._s_p)
    r_vec=ray.d.Norm()-2*(ray.d.Norm()**n_vec)*n_vec
    
    if pixel_color**pixel_color>0.0001 and pixel_coef._km!=0 and (kk-1)!=0:
        #print('ref')
        ref_ray=Ray_3D(point, r_vec.Norm())
        ref_res=_Intersection(ref_ray,s=0.00001,t1=float('inf'))
        if  ref_res[1]!=-1:
            pixel_color+=pixel_coef._km*EvalPixelColor(ref_res, ref_ray,kk-1)
    for i in range(3):
        pixel_color[i]=min(1.,pixel_color[i])
    return pixel_color
# 计算交点
def _Intersection(ray,s=0,t1=float('inf')):
    #t1=float('inf')
    hit=False
    for obj in _objectDic.values():
        '''
        if s==0:
            print('first int')
            print(obj)
            '''
        res=obj.Intersection(ray,Interval(s=s, e=t1))
        if res[0]<t1:#hit
            hit=True
            hit_res=res
            t1=res[0]
    if not hit:
        return (float('inf'),-1)
    return hit_res
#计算Ray
def _CalRayFromEye(i:int,j:int):
    #注意 (i,j)对应的是第i行第j列,也就是说映射到坐标轴上实际是(j,i)第j列*du*u,第i行*dv*v,u对应的是j
    up=(_plane_size[0]/_img_size[0]*(i+.5)-_plane_size[0]/2)*_eye_base[1]
    vp=(_plane_size[1]/_img_size[1]*(j+.5)-_plane_size[1]/2)*_eye_base[0]
    #print(Ray_3D(_eye_point,-1*_t*_eye_base[2]+up+vp))
    return Ray_3D(_eye_point,-1*_t*_eye_base[2]+up+vp)
# 设置RGB
def SetRGB(i:int,j:int,color):
    global _R,_G,_B
    _R[i,j]=color[0]
    _G[i,j]=color[1]
    _B[i,j]=color[2]
    
# 计算图片

def RayTrackImg():
    global _R,_G,_B,_bg_color
    for i in range(_img_size[0]):
        for j in range(_img_size[1]):
            eye_ray=_CalRayFromEye(i, j)
            hit_res=_Intersection(eye_ray)
            if hit_res[1]!=-1:
                color=EvalPixelColor(hit_res,eye_ray)
                SetRGB(i, j, color)
            else:
                SetRGB(i, j, _bg_color)
            print(i,j)
    return RGBChannelToImgArray(_R,_G,_B)
                    
                    
                
            
            
    
        
    
    