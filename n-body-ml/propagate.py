import numpy as np
from scipy.integrate import solve_ivp
from numpy.linalg import norm

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



def get_orbit(v_1,v_2, frequency, total_time, configuration="triangle"):
    SQRT3 = np.sqrt(3)
    v_1 = float(v_1)
    v_2 = float(v_2)
    m1,m2,m3 = 1,1,1
    if configuration == "line":
        r1x, r1y, r2x, r2y, r3x, r3y = -1, 0, 1, 0, 0, 0
        v1x, v1y, v2x, v2y, v3x, v3y = v_1, v_2, v_1, v_2, -2*v_1/m3, -2*v_2/m3
    elif configuration == "triangle":
        r1x, r1y, r2x, r2y, r3x, r3y = -SQRT3/2, -0.5, SQRT3/2, -0.5, 0, 1
        v1x, v1y, v2x, v2y, v3x, v3y = v_1/2, v_2*(-SQRT3/2), v_1/2, v_2*(SQRT3/2), -v_1, 0
    initial = [m1,m2,m3,r1x,r1y,r2x,r2y,r3x,r3y,v1x,v1y,v2x,v2y,v3x,v3y]
    time = total_time*frequency
    timestep = total_time
    orbit = prop(initial, time=time, timestep=timestep)["y"]
    r1x, r1y, r2x, r2y, r3x, r3y = orbit[0], orbit[1], orbit[2], orbit[3], orbit[4], orbit[5]
    v1x, v1y, v2x, v2y, v3x, v3y = orbit[6], orbit[7], orbit[8], orbit[9], orbit[10], orbit[11]
    r12 = norm([r1x-r2x, r1y-r2y], axis=0)**2
    r13 = norm([r1x-r3x, r1y-r3y], axis=0)**2
    r23 = norm([r2x-r3x, r2y-r3y], axis=0)**2
    pe1, pe2, pe3 = - 2/r12 - 2/r13, - 2/r12 - 2/r23, - 2/r13 - 2/r23
    ke1 = 0.5*norm([v1x, v1y], axis=0)**2
    ke2 = 0.5*norm([v2x, v2y], axis=0)**2
    ke3 = 0.5*norm([v3x, v3y], axis=0)**2
    orbit = np.swapaxes(orbit,0,1)
    energy = np.array([pe1, ke1, pe2, ke2, pe3, ke3])
    return orbit, energy
