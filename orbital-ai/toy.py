import matplotlib.pyplot as plt
import numpy as np

from prop_simple import prop


plot_1_orbit = False

loops = 50
per_loop = 1000
total_steps = loops*per_loop


grid = np.load("data_big/orbit_deviation_std.npy")
grid[grid == np.inf] = np.nan
grid = 1-np.sqrt(1/grid)

period = np.load("data_big/periods.npy")


def get_orbit_data(v_1,v_2):

    v_1 = float(v_1)
    v_2 = float(v_2)

    m1,m2,m3 = 1,1,1

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
    initial = [m1,m2,m3,r1x,r1y,r2x,r2y,r3x,r3y,v1x,v1y,v2x,v2y,v3x,v3y]

    time = loops
    timestep = loops*per_loop
    file_name = ""

    return prop(initial, file_name, time=time, timestep=timestep, save=False)


def onclick(event):
    
    if event.xdata != None and event.ydata != None:
        counters = np.linspace(-1,1, np.shape(grid)[0])
        ii = np.argsort(np.square(counters - event.ydata))[0]
        jj = np.argsort(np.square(counters - event.xdata))[0]

        try:
            print("Plot", ii, jj)

            orbit_data = get_orbit_data(counters[ii],counters[jj])

            t = orbit_data["t"]
            r1x, r1y, r2x, r2y, r3x, r3y, v1x, v1y, v2x, v2y, v3x, v3y = orbit_data["y"]
            success = orbit_data["success"]


            fig2, axs2 = plt.subplots(1,1, figsize=(16,10))

            if np.isnan(period[ii,jj]) or np.isinf(period[ii,jj]) or not plot_1_orbit:
                ender = -1
            else:
                ender = int(period[ii,jj]*per_loop)

            axs2.plot(r1x[:ender],r1y[:ender])
            axs2.plot(r2x[:ender],r2y[:ender])
            axs2.plot(r3x[:ender],r3y[:ender])

            axs2.set_xlabel("X")
            axs2.set_ylabel("Y")

            if len(t) != total_steps:
                collisional = "True"
                per = np.nan
                std = np.nan
            else:
                collisional = "False"
                if np.isnan(period[ii,jj]):
                    per = np.inf
                    std = np.inf
                else:
                    per = period[ii,jj]
                    std = 1/((1-grid[ii,jj])**2)
            
            textstr = ""
            textstr += "V1=%.9f\n"%(counters[ii])
            textstr += "V2=%.9f\n"%(counters[jj])
            textstr += "\n"
            textstr += "Predicted Period=%.3f\n"%(per)
            textstr += "STD in Euclidean Distance=%.0f\n"%(std)
            textstr += "\n"
            textstr += "Collisional Orbit="+collisional+"\n"
            textstr += "Total ODE Steps=%.0f\n"%(len(t))
            
            plt.text(-0.5, 0.5, textstr, transform=axs2.transAxes,va='center', ha="center", fontsize=20)
            plt.subplots_adjust(left=0.44)
            
            plt.title("Propagated Orbit for 1 of the predicted period")
            

            plt.axis('equal')
            
            fig2.savefig("data_big/chosen_orbit.png") #redraw
            plt.clf()
            plt.close()
        except:
            print("File does not exist for", ii, jj)



def main_map():

    fig, axs = plt.subplots(1,1, figsize=(12,10))
    # colors = axs.contourf(np.linspace(-1,1,np.shape(grid)[0]), np.linspace(-1,1,np.shape(grid)[0]), grid, levels=40, cmap="BuPu_r")
    colors = plt.imshow(grid, extent=[-1,1,1,-1], cmap="BuPu_r")
    axs.invert_yaxis()

    # ticker = np.arange(0,0.07)
    ticker = np.arange(0, np.nanmax(grid), 0.01)
    cbar = plt.colorbar(colors, ticks=[*ticker, np.nanmax(grid)])
    cbar.ax.set_yticklabels([*np.array(np.around((1/(np.square(1-ticker))),decimals=-2), dtype=str), "inf"])

    plt.axis('equal')

    # plt.xlim([-1,1])
    # plt.ylim([-1,1])

    plt.xlabel("V2")
    plt.ylabel("V1")

    plt.savefig("data_big/stability.png",dpi=1000)

    fig.canvas.mpl_connect('button_press_event',onclick)

    plt.show()
    plt.clf()
    plt.close()


main_map()
