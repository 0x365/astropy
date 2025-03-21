import numpy as np
import matplotlib.pyplot as plt
import justpy as jp
from propagator import get_orbit
from numpy.linalg import norm


########### SETUP ###########

# Max positive and negative velocities on plot
MAX_V = 1.5
# Type of starting configuration
ORBIT_TYPE = "triangle"     # "triangle" or "line"

# Total number of calculation steps made
CALC_N = 50000
# This isnt really required but works
FREQUENCY = 1/1000

# Number of steps to plot
DISPLAY_N = 20000
# Spacing in main plot
main_plot_spacer = 0.1     # 1 is good for this

###########         ###########

def secondary_plots(v1, v2):
    
    orbit, energy = get_orbit(v1,v2, FREQUENCY, CALC_N, configuration=ORBIT_TYPE)

    energy = np.sum(energy, axis=0)
    energy = energy - np.nanmean(energy)

    FFT = np.fft.fft(energy)

    magnitude = (abs(FFT))
    indx = np.flip(np.argsort(magnitude))
    # print(indx)
    x = np.fft.fftfreq(len(FFT), 0.0075/len(FFT))
    # print(x)
    # freq1 = np.mean(abs(x[indx[0:1]]))
    # freq2 = abs(x[indx[2]])
    # freq3 = abs(x[indx[12]])
    # freq3 = 6200

    # print(abs(x[indx[:30]]))
    indxes = abs(x) < np.amax(x[indx[:30]])
    indxes = abs(x) < 50000
    # print("Number for regression", np.sum(indxes))
    

    # Plot orbit shape
    fig = plt.figure(figsize=(4,4), constrained_layout=True)
    fig.gca().set_aspect('equal')
    plt.plot(orbit[:DISPLAY_N,0], orbit[:DISPLAY_N,1])
    plt.plot(orbit[:DISPLAY_N,2], orbit[:DISPLAY_N,3])
    plt.plot(orbit[:DISPLAY_N,4], orbit[:DISPLAY_N,5])
    # indxes1 = np.array(np.arange(0,ENDER/freq1)*freq1,dtype=int)
    # indxes2 = np.array(np.arange(0,ENDER/freq2)*freq2,dtype=int)
    # indxes3 = np.array(np.arange(0,ENDER/freq3)*freq3,dtype=int)
    # plt.plot(orbit[indxes1,0],orbit[indxes1,1], "x", c="red")
    # plt.plot(orbit[indxes2,0],orbit[indxes2,1], "x", c="orange")
    # plt.plot(orbit[indxes3,0],orbit[indxes3,1], "x", c="yellow")
    plt.title("Orbit Shape")
    d.add(jp.Matplotlib(classes='', name="orbit_map"))
    plt.close(fig)

    # Plot energy and first ffts
    fig = plt.figure(figsize=(6,4), constrained_layout=True)
    plt.plot(energy[:DISPLAY_N], label="Total Energy")
    FFT2 = FFT.copy()
    for i in range(len(FFT)):
        if not i in [*indx[0:1]]:
            FFT2[i] = 0
    y = np.fft.ifft(FFT2, len(FFT2))[:DISPLAY_N]
    size = (np.nanmax(energy[:DISPLAY_N])-np.nanmin(energy[:DISPLAY_N]))
    plt.plot(np.nanmean(energy[:DISPLAY_N]) + size*(-0.5+(y-np.nanmin(y))/(np.nanmax(y)-np.nanmin(y))), label="Largest Fourier Coefficient", alpha=0.3)    
    plt.title("Orbit Energy")
    box = plt.gca().get_position()
    plt.gca().set_position([box.x0, box.y0 + box.height * 0.1,
                    box.width, box.height * 0.9])
    plt.gca().legend(loc='upper center', bbox_to_anchor=(0.5, -0.1),
            fancybox=True, shadow=True, ncol=5)
    d.add(jp.Matplotlib(classes='', name="energy_map"))
    plt.close(fig)

    # Plot fft
    fig = plt.figure(figsize=(10,3), constrained_layout=True)
    magnitude[magnitude < 0.000001] = np.nan
    plt.plot(x[indxes], np.log10(magnitude[indxes]), ".", label="fft")
    plt.title("Fast Fourier Transform of Orbit")
    d.add(jp.Matplotlib(classes='', name="fft_analysis"))
    plt.close(fig)


def result_ready(self, msg):
    
    if msg.request_id == 'image_data':
    

        left = msg.result.image.left
        top = msg.result.image.top
        right = msg.result.image.right
        bottom = msg.result.image.bottom
        
        pageX = msg.result.mouse.pageX
        pageY = msg.result.mouse.pageY
    
        d.components = [d.components[0]]

        v1 = ((pageX-left)-((right-left)*main_plot_spacer))/((right-left)-(2*main_plot_spacer*(right-left)))
        v2 = ((pageY-top)-((bottom-top)*main_plot_spacer))/((bottom-top)-(2*main_plot_spacer*(bottom-top)))

        fidelity = 200
        max_v = MAX_V
        scale = np.linspace(-max_v,max_v,fidelity)
        print("Velocity", scale[int(fidelity*v1)], -scale[int(fidelity*v2)])
        secondary_plots(scale[int(fidelity*v1)],-scale[int(fidelity*v2)])



    
def click_image(self, msg):
    js_code = "var image = document.querySelector('[name="+str(self.name)+"]'); var rect = image.getBoundingClientRect(); console.log(rect.top, rect.right, rect.bottom, rect.left); ({image: rect, mouse:{ pageX:"+str(msg.pageX)+", pageY:"+str(msg.pageY)+", screenX: "+str(msg.screenX)+", screenY: "+str(msg.screenY)+" } });"
    jp.run_task(wp.run_javascript(js_code, request_id='image_data'))


def set_std(self, msg):
    grid = np.array(np.load("data/"+ORBIT_TYPE+"/background_energy_std.npy"),dtype=float)

    fig = plt.figure(figsize=(10,10))

    plt.imshow(np.log10(np.flip(grid,axis=1)), interpolation=None, extent=[-MAX_V,MAX_V,-MAX_V,MAX_V])
    plt.subplots_adjust(left=main_plot_spacer, bottom=main_plot_spacer, top=1-main_plot_spacer, right=1-main_plot_spacer)
    fig.gca().yaxis.tick_right()
    fig.gca().yaxis.set_label_position("right")
    fig.gca().set_aspect('equal')
    plt.xlabel("V1")
    plt.ylabel("V2")

    self.chart.set_figure(fig)
    plt.close(fig)

def set_fft(self, msg):
    grid = np.array(np.load("data/"+ORBIT_TYPE+"/background_fft.npy"),dtype=float)

    fig = plt.figure(figsize=(10,10))

    plt.imshow((np.flip(grid,axis=1)), interpolation=None, extent=[-MAX_V,MAX_V,-MAX_V,MAX_V])
    plt.subplots_adjust(left=main_plot_spacer, bottom=main_plot_spacer, top=1-main_plot_spacer, right=1-main_plot_spacer)
    fig.gca().yaxis.tick_right()
    fig.gca().yaxis.set_label_position("right")
    fig.gca().set_aspect('equal')
    plt.xlabel("V1")
    plt.ylabel("V2")

    self.chart.set_figure(fig)
    plt.close(fig)


def main():
    global wp

    # Build web app
    wp = jp.WebPage()
    wp.debug = True
    wp.on('result_ready', result_ready)

    wp = generate(wp, ORBIT_TYPE)

    return wp
    
def generate(wp, config="triangle"):

    global d
    d = jp.Div(classes='flex flex-wrap m-1 p-2', a=wp)

    grid = np.array(np.load("data/"+config+"/background_energy_std.npy"),dtype=float)

    

    fig = plt.figure(figsize=(10,10))
    im = plt.imshow(np.log10(grid), interpolation=None, extent=[-MAX_V,MAX_V,MAX_V,-MAX_V])
    plt.subplots_adjust(left=main_plot_spacer, bottom=main_plot_spacer, top=1-main_plot_spacer, right=1-main_plot_spacer)
    fig.gca().yaxis.tick_right()
    fig.gca().yaxis.set_label_position("right")
    fig.gca().set_aspect('equal')
    plt.xlabel("V1")
    plt.ylabel("V2")
    plt.xlim([-MAX_V,MAX_V])
    plt.ylim([-MAX_V,MAX_V])
    
    chart = jp.Matplotlib(classes='rounded', name="big_plot")
    chart.on('click', click_image)
    chart.additional_properties = ['pageX', 'pageY', 'screenX', 'screenY']
    d.add(chart)
    plt.close(fig)

    b = jp.Button(text='Change to Standard Deviation of Energy map', a=wp,
                  classes='m-2 bg-transparent hover:bg-blue-500 text-blue-700 font-semibold hover:text-white py-2 px-4 border border-blue-500 hover:border-transparent rounded')
    b.chart = chart
    b.on('click', set_std)

    b2 = jp.Button(text='Change to FFT proximity map', a=wp,
                  classes='m-2 bg-transparent hover:bg-blue-500 text-blue-700 font-semibold hover:text-white py-2 px-4 border border-blue-500 hover:border-transparent rounded')
    b2.chart = chart
    b2.on('click', set_fft)

    secondary_plots(0.5,0.5)    # Just arbitrary starting values before clicking on graph

    return wp




jp.justpy(main)
