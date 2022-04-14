# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 20:51:30 2022

@author: DB
"""
from Object_3D import *
from Math_3D import *
from Color import *
class Scene_3D(Object_3D):
    '''
    用于场景的类,用于储存各种物品以及光源.主要使用字典
    '''
    _objectDic={}
    _lightPosList=[]
    _bg_color=[255,255,255]#背景颜色
    _eye_point=Vec_3D([-1,0,0])
    _plane=Plane([0,2,2], [0,-2,-2])
    _img_size=[400,400]
    #设置eye的位置
    def SetEye(e:Vec_3D=(-1,0,0)):
        if type(e)!=Vec_3D([]):
            e=Vec_3D(e)
        Scene_3D._eye_point=e
    def SetPalneAndImgSize(plane:Plane,Width,Height):
        Scene_3D._plane=plane
        Scene_3D._img_size=[Width,Height]
        
        
    def Set_bgColor(color:Vec_3D=[255,255,255]):
        if type(e)!=Vec_3D([]):
            color=Vec_3D(color)
        Scene_3D._bg_color=color
    #为场景添加物品
    def AddNewObject(shape:Shape_3D):
        Scene_3D._objectDic[shape.id]=shape
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
        Scene_3D._lightPosList.append(light)
    #删除光源
    def DelLight(ind:int):
        Scene_3D._lightPosList.pop(ind)
    #计算像素值
    def EvalPixelColor(res:tuple,ray:Ray_3D):
        '''
        假设res是离e最近的交点的物体返回的交点结果,ray是对应的e射出的射线
        '''
        object_id=res[1]#物品id
        point=ray.CalcPoint(res[0])#交点
        obj=Scene_3D._objectDic[object_id]#物品
        n_vec=Scene_3D.GetNormalVec(obj,point)#获取法向量
        pixel_color,pixel_coef=Scene_3D.GetColorAndCoef(obj, point)
        return pixel_color
    # 计算交点
    def _Intersection(ray):
        t1=float('inf')
        hit=False
        for obj in Scene_3D._objectDic.values():
            res=obj.Intersection(ray,Interval(s=0, e=t1))
            if res[0]<t1:#hit
                hit=True
                hit_res=res
                t1=res[0]
        if not hit:
            return (float('inf'),-1)
        return hit_res
    #计算Ray
    def _CalRayFromEye(i:int,j:int):
        
    # 计算图片
    def RayTrackImg():
        pass
        
            
        
        