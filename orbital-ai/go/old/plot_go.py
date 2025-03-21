import csv
import numpy as np
import matplotlib.pyplot as plt
import scipy as sy
import scipy.fftpack as syfp
# from scipy.fft import fft, fftfreq
import math

def csv_input(file_name):
    with open(file_name, "r") as f:
        read_obj = csv.reader(f)
        output = []
        for row in read_obj:
            output.append(row)
    f.close()
    return output

plt.figure(figsize=(10,10))
found = False
c = 0
for j in range(-50,50):

    data = csv_input("data/out_file_name"+str(j)+".csv")

    ender = -1
    for i in range(len(data)):
        vals = np.array(data[i],dtype=float)[500:]
        if len(vals) > 2000 and np.amax(vals) > 15:# and np.amax(vals) > 10:
            # vals = vals/np.amax(vals)
            # vals = 2*(vals-np.amin(vals))/(np.amax(vals)-np.amin(vals)) - 1
            # plt.plot(vals)
            t = np.arange(0,len(vals))
            vals = 1/vals
            vals = vals-np.mean(vals)
            vals = (vals/np.amax(vals))

            peak1 = sy.signal.find_peaks(vals, height=0.1)[0][0]

            # plt.plot(np.linspace(-0.5,0.5,len(vals)),vals/np.amax(vals))


            # vals = sy.ndimage.gaussian_filter(vals, sigma=1000)
            # plt.plot(vals)
            FFT = np.fft.fft(vals, int(len(vals)))
            FFT_freq = np.fft.fftfreq(len(FFT), d=1/len(vals))

            # plt.hist((FFT))

            # print(FFT.real.tolist())

            magnitude = abs(FFT)

            max_frequency = FFT_freq[np.argmax(magnitude)]
            print(np.argmax(magnitude))
            phase = 0
            amplitude = magnitude[np.argmax(magnitude)]
            print(amplitude)

            reconstructed_wave = amplitude * np.sin(2.0 * np.pi * max_frequency * t + phase)
            print(max_frequency)
            magnitude = np.log10(abs(FFT))
            # magnitude[magnitude < 0] = np.nan

            plt.scatter(FFT_freq, magnitude/np.amax(magnitude),alpha=0.1)

            # FFT.real[abs(FFT_freq) < 0.1] = 0

            # magnitude = np.log10(abs(FFT))

            # plt.scatter(FFT_freq, magnitude/np.amax(magnitude),alpha=0.01)
            

            window_size = 500

            stded = np.std(np.lib.stride_tricks.sliding_window_view(magnitude, window_size),axis=1)

            plt.plot(FFT_freq[int(np.floor(window_size/2))-1:-int(np.ceil(window_size/2))], stded)
            # plt.xlim([-0.1,0.1])
            plt.scatter([peak1],[1], c="red")
            plt.savefig("test_fft_"+str(c)+".png")
            plt.clf()

            plt.plot(vals)
            # plt.plot(np.fft.ifft(FFT, len(vals)))
            plt.plot(t,reconstructed_wave)
            plt.scatter([peak1],[0], c="red")
            plt.savefig("test_orbit_"+str(c)+".png")
            plt.clf()

            peaks = sy.signal.find_peaks(vals, height=0.1)[0]
            peak_vals = []
            for k in range(len(peaks)):
                peaks_cut = peaks/peaks[k]
                # print(peaks_cut)
                peak_vals.append(float(np.linalg.norm(peaks_cut-np.round(peaks_cut))))
            # print(peak_vals)
            
            peaks = peaks[peak_vals == np.amin(peak_vals)]
            
            # plt.plot(vals, label=str(i))

            c += 1
            
            break

    if c >= 2:
        break

# plt.legend()
# # plt.xlim([-0.3,0.3])
# plt.savefig("test.png")
# plt.clf()