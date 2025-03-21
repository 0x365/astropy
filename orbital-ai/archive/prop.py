import matplotlib.pyplot as plt
import numpy as np

from scipy.integrate import solve_ivp


def prop(initial, file_name, time=20, timestep=1000, do_plot=True):
    m1, m2, m3 = initial[:3]

    G = 1 #6.67E-11

    def prop_func(t, y):
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





    t = np.arange(0,time,time/timestep)

    sol = solve_ivp(prop_func, (0, np.amax(t)), y0=initial[3:], t_eval=t, 
                    method="DOP853", rtol=1e-10, atol=1e-13)
    
    print(sol)

    suc = [sol.success, sol.message]

    np.savez("data_big/", t=sol.t, y=sol.y, success=suc)

    


    if sol.success == False:
        print("Unsuccessful?")
        if np.amax(sol.y[6:,-1]) > 3 and np.amin(sol.y[6:,-1]) < -3:
            print("Collision Occured")
            return [], [], []
        else:
            print(sol)
            print(np.swapaxes(sol.y[:,-10:],0,1))

    r1 = np.array([sol.y[0], sol.y[1]])
    r2 = np.array([sol.y[2], sol.y[3]])
    r3 = np.array([sol.y[4], sol.y[5]])

    center_of_mass = (r1+r2+r3)/3

    adj_r1 = r1-center_of_mass
    adj_r2 = r2-center_of_mass
    adj_r3 = r3-center_of_mass

    max_val = np.amax([adj_r1, adj_r2, adj_r3])*1.1

    if do_plot:
        fig = plt.figure(figsize=(5,5))
        plt.plot(adj_r1[0], adj_r1[1], label="Body 1", linewidth=0.1)
        plt.plot(adj_r2[0], adj_r2[1], label="Body 2", linewidth=0.1)
        plt.plot(adj_r3[0], adj_r3[1], label="Body 3", linewidth=0.1)

        plt.legend()
        plt.axis('equal')
        plt.xlim([-max_val, max_val])
        plt.ylim([-max_val, max_val])
        plt.savefig(file_name+".png")
        plt.clf()
        plt.close()

    return adj_r1, adj_r2, adj_r3


    