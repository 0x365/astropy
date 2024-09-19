import numpy as np
import matplotlib.pyplot as plt

from common import *

data = load_json("data-ga/0_completed.json")

data = data[1:]

x = [xi["x"] for xi in data]
f = [xi["f"] for xi in data]
# f = f*2
f = -np.array(f)
f = f.tolist()

argp = [[xii["argp_i"] for xii in xi] for xi in x]
ecc = [[np.log10(xii["ecc_i"]) for xii in xi] for xi in x]
inc = [[xii["inc_i"] for xii in xi] for xi in x]
raan = [[xii["raan_i"] for xii in xi] for xi in x]
anom = [[xii["anom_i"] for xii in xi] for xi in x]
mot = [[xii["mot_i"] for xii in xi] for xi in x]





colors = plt.cm.viridis_r(np.linspace(0, 1, len(argp)))

fig = plt.figure(figsize=(10,12), layout="tight")
gs = plt.GridSpec(3, 3, height_ratios=[1, 1, 1])

ax1 = fig.add_subplot(gs[0, 0])
ax1.set_title("Argument of Periapsis")
for i in range(len(argp)):
    ax1.scatter(argp[i], f[i], color=colors[i])

ax2 = fig.add_subplot(gs[0, 1])
ax2.set_title("Eccentricity")
for i in range(len(ecc)):
    ax2.scatter((ecc[i]), f[i], color=colors[i])

ax3 = fig.add_subplot(gs[0, 2])
ax3.set_title("Inclination")
for i in range(len(inc)):
    ax3.scatter(inc[i], f[i], color=colors[i])

ax4 = fig.add_subplot(gs[1, 0])
ax4.set_title("RAAN")
for i in range(len(raan)):
    ax4.scatter(raan[i], f[i], color=colors[i])

ax5 = fig.add_subplot(gs[1, 1])
ax5.set_title("Mean Anomoly")
for i in range(len(anom)):
    ax5.scatter(anom[i], f[i], color=colors[i])

ax6 = fig.add_subplot(gs[1, 2])
ax6.set_title("Mean Motion")
for i in range(len(mot)):
    ax6.scatter(np.array(mot[i])/360, f[i], color=colors[i])

ax7 = fig.add_subplot(gs[2, :])
ax7.set_title("Fitness over generations")
ax7.set_xlabel("Generation")
ax7.set_ylabel("Fitness")
for i in range(len(f)):
    ax7.scatter([i]*len(f[i]), f[i], color=colors[i])

plt.savefig("figures/ga/single_learning_orbit_elements.png")
plt.clf()







fig = plt.figure(figsize=(10,12), layout="tight")
gs = plt.GridSpec(3, 3, height_ratios=[1, 1, 1])

colors = plt.cm.viridis_r(np.linspace(0, 1, 50))

ax1 = fig.add_subplot(gs[0, 0])
ax2 = fig.add_subplot(gs[0, 1])
ax3 = fig.add_subplot(gs[0, 2])
ax4 = fig.add_subplot(gs[1, 0])
ax5 = fig.add_subplot(gs[1, 1])
ax6 = fig.add_subplot(gs[1, 2])
ax7 = fig.add_subplot(gs[2, :])

axs = [ax1, ax2, ax3, ax4, ax5, ax6]
titles = ["Argument of Periapsis", "Eccentricity", "Inclination", "RAAN", "Mean Anomoly", "Mean Motion"]
ylabels = ["","Log10 of ","","","",""]

for i in range(len(axs)):
    axs[i].set_title(titles[i])
    axs[i].set_ylabel("Increase in Number of Satellites")
    axs[i].set_xlabel(ylabels[i]+titles[i])

ax7.set_title("Fitness over generations")
ax7.set_xlabel("Generation")
ax7.set_ylabel("Increase in Number of Satellites")


without_data_raw = load_json("with_without.json")
without_data = []
for i in range(20):
    try:
        without_data.append(np.array(without_data_raw["day_"+str(i)]))
    except:
        pass
without_data = np.array(without_data)

for ii in ["01_", "05_", ""]:

    data_all = []
    for_means = []

    if ii == "01_":
        color_a = "red"
        timer = 0
    elif ii == "05_":
        color_a = "green"
        timer = 4
    elif ii == "":
        color_a = "blue"
        timer = -1
    elif ii == "test_2_":
        color_a = "orange"
        timer = -1

    for i in range(10):
        try:
            data = load_json("data-ga/"+ii+str(i)+"_completed.json")
            data = data[1:]
            data_all.append(data)
        except:
            break

    for j in range(10):
        try:
            x = [xi["x"] for xi in data_all[j]]
            f = [xi["f"] for xi in data_all[j]]
            f = -np.array(f)
            f = f.tolist()
        except:
            continue
        

        argp = [[xii["argp_i"] for xii in xi] for xi in x]
        ecc = [[np.log10(xii["ecc_i"]) for xii in xi] for xi in x]
        inc = [[xii["inc_i"] for xii in xi] for xi in x]
        raan = [[xii["raan_i"] for xii in xi] for xi in x]
        anom = [[xii["anom_i"] for xii in xi] for xi in x]
        mot = [[xii["mot_i"]/360 for xii in xi] for xi in x]

        mean_f = np.mean(f,axis=1)-without_data[j,timer,0,0]
        mean_f_log = np.power(mean_f,50)
        normalised_f = (mean_f_log - np.amin(mean_f_log)) / (np.amax(mean_f_log) - np.amin(mean_f_log))

        ax1.scatter(np.mean(argp,axis=1), mean_f, color=color_a, alpha=normalised_f)

        ax2.scatter(np.mean(ecc,axis=1), mean_f, color=color_a, alpha=normalised_f)
        ax3.scatter(np.mean(inc,axis=1), mean_f, color=color_a, alpha=normalised_f)
        ax4.scatter(np.mean(raan,axis=1), mean_f, color=color_a, alpha=normalised_f)
        ax5.scatter(np.mean(anom,axis=1), mean_f, color=color_a, alpha=normalised_f)
        ax6.scatter(np.mean(mot,axis=1), mean_f, color=color_a, alpha=normalised_f)

        # First zero is day length 0.1, 0.5, 1
        ax7.plot(np.arange(len(mean_f))+1, mean_f, color=color_a, alpha=0.1)
        for_means.append(mean_f)
    if len(for_means) > 0:
        ax7.plot(np.arange(len(for_means[0]))+1, np.mean(for_means, axis=0), color=color_a, alpha=1)

plt.savefig("figures/ga/learning_orbit_elements.png")
plt.clf()











scatter = True

for iii in ["01_","05_", "", "test_2_"]:
    fig = plt.figure(figsize=(15,10), layout="tight")
    gs = plt.GridSpec(2, 3, height_ratios=[1, 1])
    ax1 = fig.add_subplot(gs[0, 0])
    ax2 = fig.add_subplot(gs[0, 1])
    ax3 = fig.add_subplot(gs[0, 2])
    ax4 = fig.add_subplot(gs[1, 0])
    ax5 = fig.add_subplot(gs[1, 1])
    ax6 = fig.add_subplot(gs[1, 2])

    axs = [ax1, ax2, ax3, ax4, ax5, ax6]
    titles = ["Argument of Periapsis", "Eccentricity", "Inclination", "RAAN", "Mean Anomoly", "Mean Motion"]
    ylabels = ["","","","","",""]

    for i in range(len(axs)):
        axs[i].set_title(titles[i])
        axs[i].set_xlabel("Generation")
        axs[i].set_ylabel(ylabels[i]+titles[i])

    data_all = []
    for i in range(10):
        try:
            data = load_json("data-ga/"+iii+str(i)+"_completed.json")
            if iii != "test_2_":
                data = data[1:]
            data_all.append(data)
        except:
            break

    for j in range(10):
        try:
            x = [xi["x"] for xi in data_all[j]]
            f = [xi["f"] for xi in data_all[j]]
            f = -np.array(f)
            f = f.tolist()
        except:
            continue
        print(iii)

        argp = [[xii["argp_i"] for xii in xi] for xi in x]
        ecc = [[np.log10(xii["ecc_i"]) for xii in xi] for xi in x]
        inc = [[xii["inc_i"] for xii in xi] for xi in x]
        raan = [[xii["raan_i"] for xii in xi] for xi in x]
        anom = [[xii["anom_i"] for xii in xi] for xi in x]
        mot = [[xii["mot_i"]/360 for xii in xi] for xi in x]

        if iii == "test_2_":
            for i in range(len(argp)):
                ax1.scatter([i]*len(argp[i]), argp[i], alpha=0.01)
            for i in range(len(ecc)):
                ax2.scatter([i]*len(ecc[i]), ecc[i], alpha=0.01)
            for i in range(len(inc)):
                ax3.scatter([i]*len(inc[i]), inc[i], alpha=0.01)
            for i in range(len(raan)):
                ax4.scatter([i]*len(raan[i]), raan[i], alpha=0.01)
            for i in range(len(anom)):
                ax5.scatter([i]*len(anom[i]), anom[i], alpha=0.01)
            for i in range(len(mot)):
                ax6.scatter([i]*len(mot[i]), mot[i], alpha=0.01)
        elif scatter:
            for i in range(len(argp)):
                ax1.scatter([i]*len(argp[i]), argp[i], alpha=0.005, c="black")
            for i in range(len(ecc)):
                ax2.scatter([i]*len(ecc[i]), np.power(10,ecc[i]), alpha=0.005, c="black")
            for i in range(len(inc)):
                ax3.scatter([i]*len(inc[i]), inc[i], alpha=0.005, c="black")
            for i in range(len(raan)):
                ax4.scatter([i]*len(raan[i]), raan[i], alpha=0.005, c="black")
            for i in range(len(anom)):
                ax5.scatter([i]*len(anom[i]), anom[i], alpha=0.005, c="black")
            for i in range(len(mot)):
                ax6.scatter([i]*len(mot[i]), mot[i], alpha=0.005, c="black")
        else:
            stuff = []
            for i in range(len(argp)):
                stuff.append([i, np.mean(argp[i]), np.std(argp[i])])
            stuff = np.array(stuff)
            ax1.plot(stuff[:,0], stuff[:,1])
            ax1.fill_between(stuff[:,0], stuff[:,1]-stuff[:,2], stuff[:,1]+stuff[:,2], alpha=0.2)

            stuff = []
            for i in range(len(ecc)):
                stuff.append([i, np.mean(ecc[i]), np.std(ecc[i])])
            stuff = np.array(stuff)
            ax2.plot(stuff[:,0], stuff[:,1])
            ax2.fill_between(stuff[:,0], stuff[:,1]-stuff[:,2], stuff[:,1]+stuff[:,2], alpha=0.2)

            stuff = []
            for i in range(len(ecc)):
                stuff.append([i, np.mean(inc[i]), np.std(inc[i])])
            stuff = np.array(stuff)
            ax3.plot(stuff[:,0], stuff[:,1])
            ax3.fill_between(stuff[:,0], stuff[:,1]-stuff[:,2], stuff[:,1]+stuff[:,2], alpha=0.2)

            stuff = []
            for i in range(len(ecc)):
                stuff.append([i, np.mean(raan[i]), np.std(raan[i])])
            stuff = np.array(stuff)
            ax4.plot(stuff[:,0], stuff[:,1])
            ax4.fill_between(stuff[:,0], stuff[:,1]-stuff[:,2], stuff[:,1]+stuff[:,2], alpha=0.2)

            stuff = []
            for i in range(len(ecc)):
                stuff.append([i, np.mean(anom[i]), np.std(anom[i])])
            stuff = np.array(stuff)
            ax5.plot(stuff[:,0], stuff[:,1])
            ax5.fill_between(stuff[:,0], stuff[:,1]-stuff[:,2], stuff[:,1]+stuff[:,2], alpha=0.2)

            stuff = []
            for i in range(len(ecc)):
                stuff.append([i, np.mean(mot[i]), np.std(mot[i])])
            stuff = np.array(stuff)
            ax6.plot(stuff[:,0], stuff[:,1])
            ax6.fill_between(stuff[:,0], stuff[:,1]-stuff[:,2], stuff[:,1]+stuff[:,2], alpha=0.2)

    plt.savefig("figures/ga/"+iii+"trend_learning_orbit_elements.png")
    plt.clf()