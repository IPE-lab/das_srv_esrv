# -*- coding: UTF-8 -*-
import os
import sys
import pandas as pd
import numpy as np
from descartes import PolygonPatch
import matplotlib.pyplot as plt
import alphashape as ap
import mpl_toolkits.mplot3d as a3
from scipy.spatial import Delaunay
from sklearn.cluster import KMeans, OPTICS, cluster_optics_dbscan, DBSCAN
sys.path.insert(0, os.path.dirname(os.getcwd()))

plt.rcParams['font.sans-serif'] = ['Microsoft Yahei'] 
plt.rcParams['font.family'] = ['sans-serif']
plt.rcParams['axes.unicode_minus'] = False

def tetrahedron_volume(a, b, c, d):
    # Use the determinant to find the tetahedron volume.
    return np.abs(np.einsum('ij,ij->i', a-d, np.cross(b-d, c-d))) / 6

def find_tri(points_3d, alpha):
    # Generate the envelope of the 3D point set points_3d with alpha as radius
    
    '''

    Available upon request
    
    '''    

def alpha_cal(points_3d, alpha):
    # Calculate the volume of the envelope that generates the 3D point set points_3d with alpha as radius

    '''

    Available upon request
    
    '''  

    return alpha_shape, vol
def stagesrv(df_stagex, alpha, ax):
    # Generate an envelope body of a microseismic coordinate df_stagex with alpha as the radius and calculate SRV to visualize it on the ax axis.
    try:
        alpha_shape, vol = alpha_cal(df_stagex, alpha)
        if alpha_shape != 0:
            ax.plot_trisurf(*zip(*alpha_shape.vertices), triangles=alpha_shape.faces, color='skyblue',
                        edgecolor='k', linewidth=0.5, alpha=0.6)
    except IndexError:
            t = ap.optimizealpha(df_stagex)
            alpha_shape, vol = alpha_cal(df_stagex, t)
            if alpha_shape != 0:
                ax.plot_trisurf(*zip(*alpha_shape.vertices), triangles=alpha_shape.faces, color='skyblue',
                            edgecolor='k', linewidth=0.5, alpha=0.6)
    return alpha_shape, vol

def srv(df, alpha, estimator, ax):
    # For the whole well micro-seismic coordinates df, calculate the SRV with alpha as the radius estimator as the clustering algorithm, and finally visualize it on the ax axis.
    ax = ax
    alpha = alpha
    # Remove the number of segments.
    df_stage = list(df['stage'].drop_duplicates().sort_values()) 
    dict={}
    # Segmented calculation
    for i in range(len(df_stage)):
        df_stagei = df.drop(df[df['stage']!=df_stage[i]].index)
        df_stagex = np.array(df_stagei.drop(['stage', 'date', 'time', 'mag'], axis=1))
        if df_stagex.shape[0] >=4:
            estimator.fit_predict(df_stagex)
            label_pred = estimator.labels_
            
            stage_vol_sum = []
            for j in range(len(tuple(set(label_pred)))):
                
                if j != -1:
                    exec('df_stagex%d = df_stagex[label_pred == %d]'%(j, j))
                    exec('alpha_shape%d, volstage%d = stagesrv(df_stagex%d, alpha, ax)'%(j, j, j))
                    exec('stage_vol_sum.append(volstage%d)'%j)
                    
            dict.update({df_stage[i]:sum(stage_vol_sum)})
        else:dict.update({df_stage[i]:0})
    return dict
    
if __name__ == '__main__':
    df = pd.read_excel('D:/wellA.xls')
    df.columns=['stage', 'date', 'time', 'north', 'east', 'down', 'mag']

    fig = plt.figure(1, figsize=(8, 8), dpi=300)
    ax = fig.add_subplot(111, projection='3d')
    plt.tick_params(labelsize=15)
    ax.invert_zaxis()
    ax.set_xlabel('X', fontsize=16)
    ax.set_ylabel('Y', fontsize=16)
    ax.set_zlabel('Z', fontsize=16)
    ax.scatter(df['north'], df['east'], df['down'], c=df['stage'], cmap='rainbow', s=5)

    dbscan = DBSCAN(eps=200, min_samples=5)  
    srv = srv(df, 0.001, dbscan, ax)
    
    fig.savefig('D:/dbsrv.jpg')
    print(srv)

    plt.show()
