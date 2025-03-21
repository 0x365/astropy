import matplotlib.pyplot as plt
import numpy as np

from scipy.integrate import solve_ivp
from scipy.optimize import leastsq
import scipy as sy
import scipy.fftpack as syfp

def propagated(v_1, v_2, m3, file_name, time=20, timestep=1000):
    m1 = 1
    m2 = 1
    # m3 = 1

    r1x = -1
    r1y = 0
    r2x = 1
    r2y = 0
    r3x = 0
    r3y = 0
    v1x = v_1
    v1y = v_2
    v2x = v_1
    v2y = v_2
    v3x = -2*v_1/m3
    v3y = -2*v_2/m3

    G = 1 #6.67E-11

    def prop(t, y):
        r1x,r1y,r2x,r2y,r3x,r3y,v1x,v1y,v2x,v2y,v3x,v3y = y
        r1 = np.array([r1x,r1y])
        r2 = np.array([r2x,r2y])
        r3 = np.array([r3x,r3y])
        r12 = np.linalg.norm(r1-r2)
        r13 = np.linalg.norm(r1-r3)
        r23 = np.linalg.norm(r2-r3)
        F1 = -G*m2*(r1-r2)/((r12)**3) + -G*m3*(r1-r3)/((r13)**3)
        F2 = -G*m1*(r2-r1)/((r12)**3) + -G*m3*(r2-r3)/((r23)**3)
        F3 = -G*m1*(r3-r1)/((r13)**3) + -G*m2*(r3-r2)/((r23)**3)
        return [v1x,v1y,v2x,v2y,v3x,v3y,F1[0],F1[1],F2[0],F2[1],F3[0],F3[1]]

    t = np.linspace(0,time,timestep)

    sol = solve_ivp(prop, (0, np.amax(t)), y0=[r1x,r1y,r2x,r2y,r3x,r3y,v1x,v1y,v2x,v2y,v3x,v3y], t_eval=t, 
                    method="DOP853", rtol=1e-10, atol=1e-13)

    print(sol)

    plt.plot(sol.y[0],sol.y[1], label="Body 1")
    plt.plot(sol.y[2],sol.y[3], label="Body 2")
    plt.plot(sol.y[4],sol.y[5], label="Body 3")

    plt.legend()
    plt.axis('equal')
    plt.savefig(file_name+".png")
    plt.clf()




def propagated2(v_1, v_2, m3, file_name, time=20, timestep=1000):
    m1 = 1
    m2 = 1
    # m3 = 1

    r1x = -1
    r1y = 0
    r2x = 1
    r2y = 0
    r3x = 0
    r3y = 0
    v1x = v_1
    v1y = v_2
    v2x = v_1
    v2y = v_2
    v3x = -2*v_1/m3
    v3y = -2*v_2/m3

    G = 1 #6.67E-11

    def prop(t, y):
        r1x,r1y,r2x,r2y,r3x,r3y,v1x,v1y,v2x,v2y,v3x,v3y = y
        r1 = np.array([r1x,r1y])
        r2 = np.array([r2x,r2y])
        r3 = np.array([r3x,r3y])
        r12 = np.linalg.norm(r1-r2)
        r13 = np.linalg.norm(r1-r3)
        r23 = np.linalg.norm(r2-r3)
        F1 = -G*m2*(r1-r2)/((r12)**3) + -G*m3*(r1-r3)/((r13)**3)
        F2 = -G*m1*(r2-r1)/((r12)**3) + -G*m3*(r2-r3)/((r23)**3)
        F3 = -G*m1*(r3-r1)/((r13)**3) + -G*m2*(r3-r2)/((r23)**3)
        return [v1x,v1y,v2x,v2y,v3x,v3y,F1[0],F1[1],F2[0],F2[1],F3[0],F3[1]]

    t = np.linspace(0,time,timestep)

    sol = solve_ivp(prop, (0, np.amax(t)), y0=[r1x,r1y,r2x,r2y,r3x,r3y,v1x,v1y,v2x,v2y,v3x,v3y], t_eval=t, 
                    method="DOP853", rtol=1e-10, atol=1e-13)

    print(sol)

    plt.plot(sol.y[0],sol.y[1], label="Body 1")
    plt.plot(sol.y[2],sol.y[3], label="Body 2")
    plt.plot(sol.y[4],sol.y[5], label="Body 3")

    plt.legend()
    plt.axis('equal')
    plt.savefig(file_name+".png")
    plt.clf()

    print()

    rel_12 = np.linalg.norm([sol.y[[0,1]]-sol.y[[2,3]]], axis=1)[0]
    rel_13 = np.linalg.norm([sol.y[[0,1]]-sol.y[[4,5]]], axis=1)[0]
    rel_23 = np.linalg.norm([sol.y[[2,3]]-sol.y[[4,5]]], axis=1)[0]

    rel_rel = (rel_12+rel_13+rel_23)/3
    # print(rel_12)

    # optimize_func = lambda x: x[0]*np.sin(x[1]*t+x[2]) + x[3] - rel_rel
    # est_amp, est_freq, est_phase, est_mean = leastsq(optimize_func, [1, 1, 1, 1])[0]

    # fine_t = np.arange(0,max(t),0.1)
    # data_fit=est_amp*np.sin(est_freq*fine_t+est_phase)+est_mean

    rel_rel = rel_rel - np.mean(rel_rel)

    window_size = 200

    plotter = np.lib.stride_tricks.sliding_window_view(rel_rel, window_size)
    plotter2 = 0.707*np.amax(plotter,axis=1)
    x_plotter = t[round(window_size/2):][:len(plotter2)]



    plt.scatter(sol.t, rel_rel, s=0.1)
    plt.plot(x_plotter, plotter2)
    # plt.plot(fine_t, data_fit)
    # plt.plot(sol.t, rel_13)
    # plt.plot(sol.t, rel_23)
    plt.savefig("data/distances.png")
    plt.clf()






def propagated3(v_1, v_2, m3, file_name, time=20, timestep=1000):
    m1 = 1
    m2 = 1
    # m3 = 1

    r1x = -1
    r1y = 0
    r2x = 1
    r2y = 0
    r3x = 0
    r3y = 0
    v1x = v_1
    v1y = v_2
    v2x = v_1
    v2y = v_2
    v3x = -2*v_1/m3
    v3y = -2*v_2/m3

    G = 1 #6.67E-11

    def prop(t, y):
        r1x,r1y,r2x,r2y,r3x,r3y,v1x,v1y,v2x,v2y,v3x,v3y = y
        r1 = np.array([r1x,r1y])
        r2 = np.array([r2x,r2y])
        r3 = np.array([r3x,r3y])
        r12 = np.linalg.norm(r1-r2)
        r13 = np.linalg.norm(r1-r3)
        r23 = np.linalg.norm(r2-r3)
        F1 = -G*m2*(r1-r2)/((r12)**3) + -G*m3*(r1-r3)/((r13)**3)
        F2 = -G*m1*(r2-r1)/((r12)**3) + -G*m3*(r2-r3)/((r23)**3)
        F3 = -G*m1*(r3-r1)/((r13)**3) + -G*m2*(r3-r2)/((r23)**3)
        return [v1x,v1y,v2x,v2y,v3x,v3y,F1[0],F1[1],F2[0],F2[1],F3[0],F3[1]]

    t = np.linspace(0,time,timestep)

    sol = solve_ivp(prop, (0, np.amax(t)), y0=[r1x,r1y,r2x,r2y,r3x,r3y,v1x,v1y,v2x,v2y,v3x,v3y], t_eval=t, 
                    method="DOP853", rtol=1e-10, atol=1e-13)




    dis_x = sol.y[0]-sol.y[0,sol.t == 0]
    dis_y = sol.y[1]-sol.y[1,sol.t == 0]
    val_1 = np.linalg.norm([dis_x, dis_y],axis=0)
    mini_1 = []
    for i in range(1, len(val_1)-1):
        if val_1[i-1] >= val_1[i] and val_1[i] <= val_1[i+1]:
            mini_1.append(i)
    plt.plot(sol.t, val_1, label="Body 1")

    dis_x = sol.y[2]-sol.y[2,sol.t == 0]
    dis_y = sol.y[3]-sol.y[3,sol.t == 0]
    val_2 = np.linalg.norm([dis_x, dis_y],axis=0)
    mini_2 = []
    for i in range(1, len(val_2)-1):
        if val_2[i-1] >= val_2[i] and val_2[i] <= val_2[i+1]:
            mini_2.append(i)
    plt.plot(sol.t, val_2, label="Body 2")

    dis_x = sol.y[4]-sol.y[4,sol.t == 0]
    dis_y = sol.y[5]-sol.y[5,sol.t == 0]
    val_3 = np.linalg.norm([dis_x, dis_y],axis=0)
    mini_3 = []
    for i in range(1, len(val_3)-1):
        if val_3[i-1] >= val_3[i] and val_3[i] <= val_3[i+1]:
            mini_3.append(i)
    plt.plot(sol.t, val_3, label="Body 3")

    min_all = []
    for i in range(len(mini_1)):
        if mini_1[i] in mini_2 and mini_1[i] in mini_3:
            min_all.append(mini_1[i])

    plt.scatter(sol.t[min_all], [0]*len(min_all))

    plt.legend()
    # plt.axis('equal')
    plt.savefig(file_name+"_data.png")
    plt.clf()



    
    from scipy.signal import argrelmin
    from scipy.interpolate import interp1d

    min_dis = np.empty((0,3))
    dis_time = np.empty((0,3))

    for i in min_all:
        larger = round(timestep/(10*time/np.pi))

        t = np.linspace(sol.t[i-1], sol.t[i+1], 1000)

        fx1 = interp1d(sol.t[i-larger:i+larger], sol.y[0,i-larger:i+larger])
        fy1 = interp1d(sol.t[i-larger:i+larger], sol.y[1,i-larger:i+larger])
        fx2 = interp1d(sol.t[i-larger:i+larger], sol.y[2,i-larger:i+larger])
        fy2 = interp1d(sol.t[i-larger:i+larger], sol.y[3,i-larger:i+larger])
        fx3 = interp1d(sol.t[i-larger:i+larger], sol.y[4,i-larger:i+larger])
        fy3 = interp1d(sol.t[i-larger:i+larger], sol.y[5,i-larger:i+larger])

        x1, y1 = fx1(t), fy1(t)
        x2, y2 = fx2(t), fy2(t)
        x3, y3 = fx3(t), fy3(t)

        dis1 = np.linalg.norm([x1-sol.y[0,sol.t == 0], y1-sol.y[1,sol.t == 0]],axis=0)
        dis2 = np.linalg.norm([x2-sol.y[2,sol.t == 0], y2-sol.y[3,sol.t == 0]],axis=0)
        dis3 = np.linalg.norm([x3-sol.y[4,sol.t == 0], y3-sol.y[5,sol.t == 0]],axis=0)

        dis = np.array([dis1, dis2, dis3])
        # print(dis)
        # print(np.shape(min_dis), np.shape([np.amin(dis,axis=1)]))
        min_vals = np.amin(dis,axis=1)
        min_dis = np.append(min_dis, [min_vals],axis=0)
        # print(t[dis[0] == min_vals[0]][0])
        dis_time = np.append(dis_time,[[t[dis[0] == min_vals[0]][0], t[dis[1] == min_vals[1]][0], t[dis[2] == min_vals[2]][0]]], axis=0)
            
    def moving_average(a, n=7):
        ret = np.cumsum(a, dtype=float)
        ret[n:] = ret[n:] - ret[:-n]
        return ret[n - 1:] / n
    
    plt.plot(np.mean(dis_time,axis=1),np.sum(min_dis,axis=1))

    plt.plot(np.mean(dis_time,axis=1)[3:-3],moving_average(np.sum(min_dis,axis=1)))

    # plt.scatter(dis_time, min_dis, s=3)


    # plt.legend()
    # plt.title("Deviation from initial position")
    # plt.axis('equal')
    # plt.xlim([-0.008,0.008])
    # plt.ylim([-0.008,0.008]) 
    plt.savefig(file_name+"_deviation.png")
    plt.clf()