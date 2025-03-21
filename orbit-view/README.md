# Orbit View

### About

A tool to visualise the stability of 3-body orbits.

The stability is given as standard distribution of the euclidean distance from the first orbit over all other orbits. The period of the first orbit is calculated by looking at the euclidean distance from the intial positions of the 3-bodys and using scipy.signal.find_peaks to identify close contacts with the intial positions.

Calculating the period and stability for all the 200x200 orbits in the grid is computationally expensive and is done with a different repository and is therefore not shown here currently.

This is just a tool to visualise and shouldn't be used as an official way to calculate orbit stability or orbit periods.

### Map of standard distribution of energy of each orbit
<img src="https://github.com/0x365/orbit-view/blob/main/data/line/energies_std.png" width="300" height="300"></img>
<img src="https://github.com/0x365/orbit-view/blob/main/data/triangle/energies_std.png" width="300" height="300"></img>

### Map of Correlation between FFT of Neighbouring Orbits
<img src="https://github.com/0x365/orbit-view/blob/main/data/line/fft_map_close.png" width="300" height="300"></img>
<img src="https://github.com/0x365/orbit-view/blob/main/data/triangle/fft_map_close.png" width="300" height="300"></img>

### Setup
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Run
```bash
python main.py
```
Then open `localhost:8000` in the browser of your choice.

Then just click on the plot to view the orbit at that specific cell. You can switch between energy standard distribution and neighbourhood fft correlation with the buttons at the bottom of the page.

To change between line and triangular initial configuration change orbit type in the main file:
```python
########### SETUP ###########

# Max positive and negative velocities on plot
MAX_V = 1.5
# Type of starting configuration
ORBIT_TYPE = "triangle"     # "triangle" or "line"
```
