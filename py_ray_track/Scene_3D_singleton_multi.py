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
class Scene:
    def __init__(self):
        self._objectDic={}
        self._lightPosList=[]
        self._bg_color=Vec_3D([255,255,255])/255#背景颜色
        self._eye_point=Vec_3D([-1,0,0])
        self._eye_base=[Vec_3D([0,-1,0]),Vec_3D([0,0,1]),Cross_3D(Vec_3D([0,-1,0]),Vec_3D([0,0,1]))]
        
        #_plane=Plane([0,2,2], [0,-2,-2],[-1,0,0],1)
        #计算平面位置
        self._t=5
        self._plane_center=Ray_3D(self._eye_point, self._eye_base[2]).CalcPoint(-1*self._t)
        self._plane_size=[4,4]
        self._img_size=[400,400]
        self._R=np.zeros(self._img_size)
        self._G=np.zeros(self._img_size)
        self._B=np.zeros(self._img_size)
        self._RGB=[self._R,self._G,self._B]
    #设置eye的位置
    def SetEye(self,e:Vec_3D=(-1,0,0),u:Vec_3D=(0,-1,0),v:Vec_3D=(0,0,1),d=5):
        #global _eye_point,_eye_base,_t,_d,_plane_center
        if type(e)!=Vec_3D([]):
            e=Vec_3D(e)
        if type(u)!=Vec_3D([]):
            u=Vec_3D(u)
        if type(v)!=Vec_3D([]):
            v=Vec_3D(v)
        self._eye_point=e
        self._eye_base=[u,v,Cross_3D(u, v)]
        self._t=d
        self._plane_center=Ray_3D(self._eye_point, self._eye_base[2]).CalcPoint(-1*self._t)
    def SetPalneAndImgSize(self,pw,ph,Width,Height):
        global _img_size,_plane_size
        self._img_size=[Width,Height]
        self._plane_size=[pw,ph]
        self._UpdateRGB()
    def _UpdateRGB(self):
        #global _R,_G,_B
        self._R=np.zeros(self._img_size)
        self._G=np.zeros(self._img_size)
        self._B=np.zeros(self._img_size)
        
    def Set_bgColor(self,color:Vec_3D=Vec_3D([255,255,255])/255):
        global _bg_color
        if type(color)!=Vec_3D([]):
            color=Vec_3D(color)
        self._bg_color=color
        
    #为场景添加物品
    def AddNewObject(self,shape:Shape_3D):
        self._objectDic[shape.id]=shape
    #获取物品的法向量
    def GetNormalVec(self,obj:Shape_3D,point:Vec_3D):
        '''
        做成函数,防止接口不同
        '''
        return obj.GetNormalVec(point)
    #获取物品在point的颜色
    def GetColorAndCoef(self,obj:Shape_3D,point:Vec_3D):
        return obj.GetColorAndCoef(point)
    #添加光源
    def AddNewLight(self,light:Light):
        self._lightPosList.append(light)
    #删除光源
    def DelLight(self,ind:int):
        self._lightPosList.pop(ind)
    #计算lam反射
    def _DiffuseShading(self,color_l,color_o,coef,n:Vec_3D,l:Vec_3D):
        newColor=[]
        for _col_l,_col_o,_coe in zip(color_l,color_o,coef):
            newColor.append(_col_l*_col_o*_coe*max(0,dot_3D(n, l)))
        #print('D',newColor)
        return Vec_3D(newColor)
    #计算Blin
    def _SpecularShading(self,color_l,color_o,coef,n:Vec_3D,l:Vec_3D,v:Vec_3D,p):
        newColor=[]
        h=(v+l).Norm()
        for _col_l,_col_o,_coe in zip(color_l,color_o,coef):
            c_c=_coe*_col_l*_col_o*max(dot_3D(h,n),0)**p
            #print(c_c)
            newColor.append(c_c)
        #print('S',newColor,coef,"V",v,"L",l,h,n,max(dot_3D(h,n),0)**p)
        return Vec_3D(newColor)
    def _AmbientShading(self,color_l,color_o,coef):
        newColor=[]
        for _col_l,_col_o,_coe in zip(color_l,color_o,coef):
            newColor.append(_coe*_col_l*_col_o)
        #print('A',newColor)
        return Vec_3D(newColor)
            
    #计算颜色
    def EvalPixelColor(self,res:tuple,ray:Ray_3D,kk:int=4):
        '''
        假设res是离e最近的交点的物体返回的交点结果,ray是对应的e射出的射线
        '''
        #print('eval')
        object_id=res[1]#物品id
        point=ray.CalcPoint(res[0])#交点
        obj=self._objectDic[object_id]#物品
        n_vec=self.GetNormalVec(obj,point)#获取法向量
        obj_color,pixel_coef=self.GetColorAndCoef(obj, point)
        pixel_color=Vec_3D([0,0,0])
        v=-1*ray.d.Norm()
        for light_obj in self._lightPosList:
            #print(light_obj)
            pixel_color+=self._AmbientShading(light_obj.color, obj_color, pixel_coef._a)
            l=light_obj.CalculateLVec(point)
            shadowRay=Ray_3D(point, l)
            #print('S',shadowRay)
            shadow_hit_res=self._Intersection(shadowRay,s=0.0001,t1=(light_obj.pos-point).Length())
            if shadow_hit_res[1]==-1:
                pixel_color+=self._DiffuseShading(light_obj.color, obj_color, pixel_coef._d, n_vec\
                                         ,l )
                #print(_SpecularShading(light_obj.color, obj_color, pixel_coef._s, n_vec, l, v, pixel_coef._s_p))
                pixel_color+=self._SpecularShading(light_obj.color, obj_color, pixel_coef._s, n_vec, l, v, pixel_coef._s_p)
        r_vec=ray.d.Norm()-2*(ray.d.Norm()**n_vec)*n_vec
        kk-=1
        if (pixel_color**pixel_color)>0.01 and pixel_coef._km!=0 and kk!=0:
            #print(kk)
            #print('ref')
            ref_ray=Ray_3D(point, r_vec.Norm())
            ref_res=self._Intersection(ref_ray,s=0.00001,t1=float('inf'))
            if  ref_res[1]!=-1:
                pixel_color+=pixel_coef._km*self.EvalPixelColor(ref_res, ref_ray,kk)
        for i in range(3):
            pixel_color[i]=min(1.,pixel_color[i])
        return pixel_color
    # 计算交点
    def _Intersection(self,ray,s=0,t1=float('inf')):
        #t1=float('inf')
        hit=False
        for obj in self._objectDic.values():
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
    def _CalRayFromEye(self,i:int,j:int):
        #注意 (i,j)对应的是第i行第j列,也就是说映射到坐标轴上实际是(j,i)第j列*du*u,第i行*dv*v,u对应的是j
        up=(self._plane_size[0]/self._img_size[0]*(i+.5)-self._plane_size[0]/2)*self._eye_base[1]
        vp=(self._plane_size[1]/self._img_size[1]*(j+.5)-self._plane_size[1]/2)*self._eye_base[0]
        #print(Ray_3D(_eye_point,-1*_t*_eye_base[2]+up+vp))
        return Ray_3D(self._eye_point,-1*self._t*self._eye_base[2]+up+vp)
    # 设置RGB
    def SetRGB(self,i:int,j:int,color):
        #global _R,_G,_B
        self._R[i,j]=color[0]
        self._G[i,j]=color[1]
        self._B[i,j]=color[2]
        
    # 计算图片
    
    def RayTrackImg(self):
        for i in range(self._img_size[0]):
            for j in range(self._img_size[1]):
                eye_ray=self._CalRayFromEye(i, j)
                hit_res=self._Intersection(eye_ray)
                if hit_res[1]!=-1:
                    color=self.EvalPixelColor(hit_res,eye_ray)
                    self.SetRGB(i, j, color)
                else:
                    self.SetRGB(i, j, _bg_color)
                print(i,j)
        return RGBChannelToImgArray(_R,_G,_B)
    
    
    def RayTrackImg_mt(self):
        from multiprocessing import Pool
        #global _img_size,_bg_color,_R,_G,_B
        '''
        并行版
        '''
        set_data=RGBChannelToImgArray(self._R, self._G,self._B)
        size_of_set=np.array(self._img_size)
        #size_of_tbl=len(tbl_data)
        
        x_size=size_of_set[0]
        y_size=size_of_set[1]
        
        x_job_size=int(x_size/3)
        x_job_end=x_size-2*x_job_size
        
        x_start_list=[0,x_job_size,2*x_job_size]
        x_size_list=[x_job_size]*2+[x_job_end]
        
        y_job_size=int(y_size/2)
        y_job_end=y_size-y_job_size
        y_start_list=[0,y_job_size]
        y_size_list=[y_job_size]*1+[y_job_end]
        
        pool=Pool(6)
        
        arg_list=[]
        jobs_tbl={None:None}
        for i in range(3):
            for j in range(2):
                
                x_start=x_start_list[i]
                x_end=x_start+x_size_list[i] #注意 numpy中的切片是左闭右开 如果都是闭合那该减一
                y_start=y_start_list[j]
                y_end=y_start+y_size_list[j]
                
                
                arg_list.append(
                    [   
                        (x_start,x_end),
                        (y_start,y_end),
                        (i,j),
                        self._bg_color
                        ]
                    )
                jobs_tbl[(i,j)]=(x_start,x_end,y_start,y_end)
        jobs_done=pool.map(self._convert,arg_list)
        
        for i in jobs_done:
            job=i[1]
            xxyy=jobs_tbl[job]
            set_data[xxyy[0]:xxyy[1],xxyy[2]:xxyy[3]]=i[0]
        del arg_list
        return set_data
    def _convert(self,var):
        size=[var[0][1]-var[0][0],var[1][1]-var[1][0]]
        _R=np.zeros(size)
        _G=np.zeros(size)
        _B=np.zeros(size)
        jobsid=var[2]
        _bg_color=var[3]
        print('job'+str(jobsid)+'start')
        for i in range(size[0]):
            for j in range(size[1]):
                eye_ray=self._CalRayFromEye(i+var[0][0], j+var[1][0])
                hit_res=self._Intersection(eye_ray)
                if hit_res[1]!=-1:
                    color=self.EvalPixelColor(hit_res,eye_ray)
                    _R[i,j]=color[0]
                    _G[i,j]=color[1]
                    _B[i,j]=color[2]
                    #print(color)
                else:
                    _R[i,j]=_bg_color[0]
                    _G[i,j]=_bg_color[1]
                    _B[i,j]=_bg_color[2]
                    #print(_bg_color)
                #print(i+var[0][0], j+var[1][0])
                #print('job'+str(jobsid),i/size[0]*100,'done')
        print('job'+str(jobsid)+'done')
        del var
        return RGBChannelToImgArray(_R,_G,_B),jobsid
                        
                        
                    
                
                
        
            
        
        