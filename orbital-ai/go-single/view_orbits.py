import numpy as np
import matplotlib.pyplot as plt
import justpy as jp
from propagator import prop
from numpy.linalg import norm

which_orbit = 1
num_loops = 20
per_loop = 1000
SQRT3 = np.sqrt(3)

def get_orbit(v_1,v_2, total_time, configuration="triangle"):
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
    time = total_time/per_loop
    timestep = total_time

    orbit = prop(initial, time=time, timestep=timestep)["y"]

    r1x, r1y, r2x, r2y, r3x, r3y = orbit[0], orbit[1], orbit[2], orbit[3], orbit[4], orbit[5]
    v1x, v1y, v2x, v2y, v3x, v3y = orbit[6], orbit[7], orbit[8], orbit[9], orbit[10], orbit[11]

    r12 = norm([r1x-r2x, r1y-r2y], axis=0)**3
    r13 = norm([r1x-r3x, r1y-r3y], axis=0)**3
    r23 = norm([r2x-r3x, r2y-r3y], axis=0)**3

    pe1, pe2, pe3 = - 2/r12 - 2/r13, - 2/r12 - 2/r23, - 2/r13 - 2/r23
    ke1 = 0.5*norm([v1x, v1y], axis=0)**2
    ke2 = 0.5*norm([v2x, v2y], axis=0)**2
    ke3 = 0.5*norm([v3x, v3y], axis=0)**2

    orbit = np.swapaxes(orbit,0,1)

    energy = np.array([pe1, ke1, pe2, ke2, pe3, ke3])

    return orbit, energy


def secondary_plots(v1, v2):

    ender = 20000
    
    orbit, energy = get_orbit(v1,v2,ender)

    energy = np.sum(energy, axis=0)

    FFT_b1 = np.fft.fft(energy)

    magnitude = (abs(FFT_b1))
    indx = np.flip(np.argsort(magnitude))
    # print(indx)
    x = np.fft.fftfreq(len(FFT_b1), 0.0075/len(FFT_b1))
    # print(x)
    # freq1 = np.mean(abs(x[indx[0:1]]))
    # freq2 = abs(x[indx[2]])
    # freq3 = abs(x[indx[12]])
    # freq3 = 6200

    # print(abs(x[indx[:30]]))
    indxes = abs(x) < np.amax(x[indx[:30]])
    indxes = abs(x) < 50000
    # print("Number for regression", np.sum(indxes))
    for i in range(len(FFT_b1)):
        if not i in [*indx[0:1]]:
            FFT_b1[i] = 0


    fig = plt.figure(figsize=(4,4), constrained_layout=True)
    plt.plot(orbit[:ender,0], orbit[:ender,1])
    plt.plot(orbit[:ender,2], orbit[:ender,3])
    plt.plot(orbit[:ender,4], orbit[:ender,5])
    
    # indxes1 = np.array(np.arange(0,ender/freq1)*freq1,dtype=int)
    # indxes2 = np.array(np.arange(0,ender/freq2)*freq2,dtype=int)
    # indxes3 = np.array(np.arange(0,ender/freq3)*freq3,dtype=int)

    # plt.plot(orbit[indxes1,0],orbit[indxes1,1], "x", c="red")
    # plt.plot(orbit[indxes2,0],orbit[indxes2,1], "x", c="orange")
    # plt.plot(orbit[indxes3,0],orbit[indxes3,1], "x", c="yellow")
    
    d.add(jp.Matplotlib(classes='', name="orbit_map"))
    plt.close(fig)


    fig = plt.figure(figsize=(6,4), constrained_layout=True)
    # f = plt.figure(figsize=(2, 2))
    plt.plot(energy[:ender])
    plt.plot(np.fft.ifft(FFT_b1, len(FFT_b1))[:ender])    
    d.add(jp.Matplotlib(classes='', name="energy_map"))
    plt.close(fig)

    fig = plt.figure(figsize=(10,3), constrained_layout=True)
    magnitude[magnitude == 0] = np.nan
    plt.plot(x[indxes], np.log10(magnitude[indxes]), ".", label="fft")
    # plt.ylim([0, 1.1*np.amax(np.log10(magnitude[indxes]))])
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
        
        # print('x:', pageX-left)
        # print('y:', pageY-top)
    
        d.components = [d.components[0]]

        # print(left, right, top, bottom)
        v1 = ((pageX-left)-((right-left)*0.05))/((right-left)-(0.1*(right-left)))
        v2 = ((pageY-top)-((bottom-top)*0.05))/((bottom-top)-(0.1*(bottom-top)))

        fidelity = 200
        max_v = 1.5
        scale = np.linspace(-max_v,max_v,fidelity)
        print("Velocity", scale[int(fidelity*v1)], -scale[int(fidelity*v2)])
        secondary_plots(scale[int(fidelity*v1)],-scale[int(fidelity*v2)])









    
def click_image(self, msg):

    # f-string needs `{{ }}` to put string `{ }` in `({{image: rect}});`
    js_code = "var image = document.querySelector('[name="+str(self.name)+"]'); var rect = image.getBoundingClientRect(); console.log(rect.top, rect.right, rect.bottom, rect.left); ({image: rect, mouse:{ pageX:"+str(msg.pageX)+", pageY:"+str(msg.pageY)+", screenX: "+str(msg.screenX)+", screenY: "+str(msg.screenY)+" } });"


    jp.run_task(wp.run_javascript(js_code, request_id='image_data'))





def plot_fft():
    global wp
    # Build web app
    wp = jp.WebPage()
    wp.debug = True
    wp.on('result_ready', result_ready)

    global d
    d = jp.Div(classes='flex flex-wrap m-1 p-2', a=wp)
    

    ender = 20000

    np.load()

    fig = plt.figure(figsize=(10,10))
    plt.imshow()
    plt.subplots_adjust(left=0.05, bottom=0.05, top=0.95, right=0.95)
    fig.gca().yaxis.tick_right()
    fig.gca().set_aspect('equal')
    # fig.gca().spines['left'].set_visible(False)
    # fig.gca().spines['top'].set_visible(False)
    plt.xlim([-1.5,1.5])
    plt.ylim([-1.5,1.5])
    
    # fig.canvas.mpl_connect('button_press_event',lambda event: onclick(event))
    chart = jp.Matplotlib(classes='rounded', name="big_plot")
    chart.on('click', click_image)
    chart.additional_properties = ['pageX', 'pageY', 'screenX', 'screenY']
    d.add(chart)
    plt.close(fig)


    secondary_plots(0.5,0.5)

    return wp




jp.justpy(plot_fft)
