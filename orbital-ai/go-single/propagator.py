import numpy as np
from scipy.integrate import solve_ivp


def prop(initial, time=20, timestep=1000):

    initial = np.array(initial)

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

    return sol    