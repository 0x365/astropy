import csv
import numpy as np
import matplotlib.pyplot as plt
import scipy as sy
import scipy.fftpack as syfp
# from scipy.fft import fft, fftfreq
import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import freqz
from scipy.signal import butter, lfilter

def csv_input(file_name):
    with open(file_name, "r") as f:
        read_obj = csv.reader(f)
        output = []
        for row in read_obj:
            output.append(row)
    f.close()
    return output


from scipy.signal import butter, lfilter
from scipy import signal
from scipy.signal import find_peaks, peak_prominences

def butter_bandpass(lowcut, highcut, fs, order=5):
    return butter(order, [lowcut, highcut], fs=fs, btype='band')

def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y


plt.figure(figsize=(5,5))
found = False
c = 0
for j in range(-50,50):

    data = csv_input("data/out_file_name"+str(j)+".csv")

    ender = -1
    for i in range(len(data)):
        vals = np.array(data[i],dtype=float)[500:]
        # plt.plot()
        if len(vals) >= 95000 and np.amax(vals) < 15:# and np.amax(vals) > 10:
            # vals = vals/np.amax(vals)
            # vals = 2*(vals-np.amin(vals))/(np.amax(vals)-np.amin(vals)) - 1
            # plt.plot(vals)

            vals = vals
            vals = ((vals-np.amin(vals))/(np.amax(vals)-np.amin(vals)))
            # vals = vals/np.amax(vals)

            t = np.linspace(0,len(vals)/1000, len(vals))

            sos = signal.butter(10, 0.2, 'lowpass', fs=1000, output='sos')
            filtered = signal.sosfilt(sos, vals)
            # plt.plot(t-5, filtered, label="filtered")

            x = vals
            peaks, _ = find_peaks(x, prominence=0.001)
            prominences = peak_prominences(x, peaks)[0]

            indx = np.flip(np.argsort(prominences))
            peaks = peaks[indx]
            prominences = prominences[indx]
            prominences2 = prominences.copy()
            # print(prominences)


            tol = 500
            c2 = 0

            lesser_peaks = peaks[prominences < prominences[0]]
            # print(lesser_peaks)
            numbers = np.arange(2,len(lesser_peaks)+1)
            numbers = peaks[0]/numbers
            # print(numbers)
            least = []
            if len(numbers) > 0:
                for lesser in lesser_peaks:
                    if np.amin(abs(numbers-lesser)) < tol:
                        least.append(lesser)
            if len(least) == 0:
                freq = peaks[0]
            else:
                freq = np.amin(least)
            print(freq)

            prominences[peaks != freq] = 0
            plt.scatter([freq/1000], [0.2])
            # print(p)
            # for i in range(1,len(prominences)):
            #     if peaks[i] < peaks[c2]:
            #         numbers = np.arange(1,10)
            #         # numbers = np.logspace(0, 10, num=11, base=2)
            #         numbers = peaks[c2]/numbers
            #         min_val = np.amin(abs((peaks[i]/numbers)-1))

            #         if min_val < tol:
            #             c2 = i
            #         else:
            #             prominences[i] = 0
            #     else:
            #         prominences[i] = 0


            # for i in range(1,len(prominences)):
            #     if peaks[i] < peaks[c2]:
            #         # if peaks[i] and peaks[0] are multiples of a number
            #         print(i, abs((peaks[c2] / peaks[i]) - 2), peaks[c2], peaks[i])
            #         # print(i)
            #         if abs((peaks[c2] / peaks[i]) - 2) < tol:
            #             # print(i)
            #             print("Change")
            #             c2 = i
            #         else:
            #             prominences[i] = 0
            #     else:
            #         prominences[i] = 0
                # print(np.std(peaks[:i]/peaks[0]))

            # plt.plot([13611/1000,13611/1000],[0,1])
            # prominences[prominences < np.mean(prominences)] = 0
            contour_heights = x[peaks] - prominences
            contour_heights2 = x[peaks] - prominences2
            # print(prominences)
            
            
            # plt.plot((peaks/1000), x[peaks], "x")
            plt.vlines(x=(peaks/1000), ymin=contour_heights2, ymax=x[peaks], color="green")
            plt.vlines(x=(peaks/1000), ymin=contour_heights, ymax=x[peaks], color="red")

            refined_peaks = peaks[prominences > 0]
            # print(refined_peaks)
            # print(refined_peaks/refined_peaks[0])
            print()
            print()
            print()
            print()
            print("next")

            # # Plot the frequency response for a few different orders.
            # plt.figure(1)
            # plt.clf()
            # for order in [3, 6, 9]:
            #     b, a = butter_bandpass(lowcut, highcut, fs, order=order)
            #     w, h = freqz(b, a, fs=fs, worN=2000)
            #     plt.plot(w, abs(h), label="order = %d" % order)

            # plt.plot([0, 0.5 * fs], [np.sqrt(0.5), np.sqrt(0.5)],
            #         '--', label='sqrt(0.5)')
            # plt.xlabel('Frequency (Hz)')
            # plt.ylabel('Gain')
            # plt.grid(True)
            # plt.legend(loc='best')

            # y = butter_bandpass_filter(vals, lowcut, highcut, fs, order=12)
            # plt.plot(y)
            plt.plot(t, vals, label="input")
            plt.legend()
            plt.savefig("test_"+str(c)+".png")
            plt.clf()
                    
            # plt.plot(vals, label=str(i))

            c += 1
            
            break


    if c >= 2:
        break

# plt.legend()
# # plt.xlim([-0.3,0.3])
# plt.savefig("test.png")
# plt.clf()