# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 15:44:55 2022

@author: DB
"""
#测试 Vec_3D
import time
from Math_3D import *
from Object_3D import *
from Color import *
import Scene_3D_singleton_multi as Scene_3D
import matplotlib.pyplot as plt

#%%
if __name__=='__main__':
    print(1111)
    vec1=Vec_3D([1,2,3])
    vec2=Vec_3D([5,6,7])
    vec3=vec2-vec1
    vec4=vec1-vec2
    #测试 Ray_3D
    ray=Ray_3D([1,2,3], [1,1,1])
    c=Vec_3D([0,0,0])
    a=ray.d**ray.d
    b=2*(ray.s-c)**ray.d
    cc=dot_3D(ray.s-c,ray.s-c)
    #测试sphere
    s1=Sphere()
    s2=Sphere(1,2)
    #测试Sphere.Intersection 即相交
    ray=Ray_3D([-5,0,0], [1,0,0])
    interval=Interval(0, float('inf'))
    res=s1.Intersection(ray, interval)
    ray.CalcPoint(res[0])
    ray2=Ray_3D([-5,0,0],[0,1,0])
    res2=s1.Intersection(ray2, interval)
    res2=s1.Intersection(ray2, [0,float('inf')])
    #%%测试Scene
    
    sc=Scene_3D.Scene()
    sc._img_size=[500,500]
    sc._plane_size=[2,2]
    #刷新图片大小
    sc._UpdateRGB()
    sc.SetEye([20,0,3],u=Vec_3D([0,1,0]),v=Vec_3D([0,0,1]),d=7)
    #添加光源
    #sc.AddNewLight(Light())
    #sc.AddNewLight(Light(Vec_3D([50,-70,90]),Vec_3D([124,124,255])/255))
    sc.AddNewLight(Light(Vec_3D([100,4,11]),Vec_3D([1,1,1])))
    sc.AddNewLight(Light(Vec_3D([10,0,8]),Vec_3D([.7,.7,.7])))
    sc.AddNewLight(Light(Vec_3D([20,-100,5]),Vec_3D([.2,.3,1])))
    #sc.AddNewLight(Light(Vec_3D([-100,-20,10]),Vec_3D([.7,.7,.7])))
    sc.AddNewLight(Light(Vec_3D([6,0,10]),Vec_3D([0.3,0,0])))
    #设置背景 颜色
    sc.Set_bgColor(Vec_3D([0,0,0])/255)
    #球
    sphere1=Sphere([2,2,4],4)
    #添加物品
    sc.AddNewObject(sphere1)
    #修改物品 的shading系数
    sphere1.Set_bs_color(Vec_3D([255,255,255])/255)
    coef1=sphere1._coef
    coef1._d=Vec_3D([.1,0.1,.1])
    coef1._s=Vec_3D([.6,.5,.5])
    coef1._s_p=3
    sphere1.Set_light_coefficinet(coef1)
    sphere2=Sphere([1,0,5],5)
    sc.AddNewObject(sphere2)
    
    
    sphere3=Sphere([4,4,3],3)
    sphere3.Set_bs_color(Vec_3D([200,12,125])/255)
    coef2=sphere3._coef
    coef2._d=Vec_3D([0.5,0.1,0.1])
    coef2._s=Vec_3D([0.3,0.1,0.1])
    coef2._s_p=30
    sphere3.Set_light_coefficinet(coef2)
    sc.AddNewObject(sphere3)
    
    sphere4=Sphere([7,0,8],2)
    sphere4._coef._km=1
    sphere4._coef._s_p=16
    sphere4.Set_bs_color(Vec_3D([1,1,1]))
    sc.AddNewObject(sphere4)

    p1=InfinitePlane(color=DeC1)
    p1._coef._km=0

    #p1._color=DeC
    sc.AddNewObject(p1)

    p2=InfinitePlane(p=Vec_3D([-5,0,0]),n=Vec_3D([1,0,-0.5]).Norm(),color=DeC2)
    p2._coef._km=1

    sc.AddNewObject(p2)

    '''
    sphere4=Sphere([6,1,1],.5)
    sphere4.Set_bs_color(Vec_3D([1,1,1]))
    sc.AddNewObject(sphere4)
    '''
    #%% 测试 Intersection
    ray=Ray_3D(s=[-1,0,0], d=[1,0,0])
    res=sc._Intersection(ray)
    print("交点: ",ray.CalcPoint(res[0]))
    #print("视平面: ",sc._plane)
    print("映射的图像大小: ",sc._img_size)
    #%%
    #del Scene_3D
    #%% 测试eye_ray计算
    print(sc._CalRayFromEye(0, 0))
    #%% 测试图片
    sc._img_size=[4000,4000]
    sc._plane_size=[10,10]
    sphere1._c=Vec_3D([1,-5,4])
    sc._UpdateRGB()
    plt.close('all')
    img=np.flip(sc.RayTrackImg_mt(),0)
    plt.figure(figsize=(20,20))
    plt.imshow(img)#左上角为坐标原点,而追踪是以左下角为原点
    #%%
    plt.axis('off')
    
    plt.savefig(fname=str(time.time())+'img.jpg', bbox_inches='tight')
    plt.show()
    '''
    #%% 测试图片
    #sc.SetEye(Vec_3D([1,1,1]),Vec_3D([0,,]).Norm(),Vec_3D([0,1,0]).Norm(),3)
    sc._img_size=[900,900]
    sc._plane_size=[2,2]
    sc._UpdateRGB()
    img_list=[]
    frames=200
    for i in range(frames):
        print(i)
        sphere1._c=Vec_3D([6,-3+6*i/frames,1])
        img_list.append(np.flip(sc.RayTrackImg(),0))
        
    
    #%%动画
    fig = plt.gcf()
    im=plt.imshow(img_list[0])
    plt.show()
    from matplotlib import animation
    def func(i):
        im.set_data(img_list[i])
        return [im]
    def init():
        return plt.imshow(img_list[0])
    
    ani = animation.FuncAnimation(fig=fig,
                                  func=func,
                                  frames=frames,
                                  interval=100,
                                  blit=True)
    #%%图片
    '''
    
    #%% 
    '''
    plt.figure()
    for i in range(20):
        sc._img_size=[90,90]
        sc._plane_size=[2,2]
        #刷新图片大小
        sc._UpdateRGB()
        coef1._d=Vec_3D([i/20,0.1,.1])
        sphere1.Set_light_coefficinet(coef1)
        img=sc.RayTrackImg()
        plt.subplot(4,5,i+1)
        plt.imshow(np.flip(img,0))#左上角为坐标原点,而追踪是以左下角为原点
    '''
        