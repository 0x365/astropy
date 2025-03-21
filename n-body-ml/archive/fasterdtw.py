import torch
import numbers
from collections import defaultdict

def fastdtw(x, y, radius=1, dist=None):
    ''' return the approximate distance between 2 time series with O(N)
        time and memory complexity (with GPU support using PyTorch)

        Parameters
        ----------
        x : array_like
            input tensor 1 (can be a numpy array or PyTorch tensor)
        y : array_like
            input tensor 2 (can be a numpy array or PyTorch tensor)
        radius : int
            size of neighborhood when expanding the path.
        dist : function or int
            Distance calculation method.

        Returns
        -------
        distance : float
            the approximate distance between the 2 time series
        path : list
            list of indexes for the inputs x and y
    '''
    # Prepare inputs as PyTorch tensors
    x, y, dist = __prep_inputs(x, y, dist)
    
    return __fastdtw(x, y, radius, dist)


def __difference(a, b):
    # GPU-compatible difference calculation using absolute value
    return torch.abs(a - b)

def __norm(p):
    return lambda a, b: torch.norm(a - b, p=p)

def __fastdtw(x, y, radius, dist):
    min_time_size = radius + 2

    if len(x) < min_time_size or len(y) < min_time_size:
        return dtw(x, y, dist=dist)

    x_shrinked = __reduce_by_half(x)
    y_shrinked = __reduce_by_half(y)
    distance, path = __fastdtw(x_shrinked, y_shrinked, radius=radius, dist=dist)
    window = __expand_window(path, len(x), len(y), radius)
    
    return __dtw(x, y, window, dist=dist)

def __prep_inputs(x, y, dist):
    # Convert inputs to PyTorch tensors if they are not already
    if not torch.is_tensor(x):
        x = torch.tensor(x, dtype=torch.float32)
    if not torch.is_tensor(y):
        y = torch.tensor(y, dtype=torch.float32)

    # Move to GPU if available
    if torch.cuda.is_available():
        x = x.cuda()
        y = y.cuda()

    # Set distance metric
    if x.ndim == y.ndim > 1 and x.shape[1] != y.shape[1]:
        raise ValueError('Second dimension of x and y must be the same')
    if isinstance(dist, numbers.Number) and dist <= 0:
        raise ValueError('dist cannot be a negative integer')

    if dist is None:
        if x.ndim == 1:
            dist = __difference
        else: 
            dist = __norm(p=1)
    elif isinstance(dist, numbers.Number):
        dist = __norm(p=dist)

    return x, y, dist

def dtw(x, y, dist=None):
    ''' Exact dynamic time warping calculation with GPU support. '''
    x, y, dist = __prep_inputs(x, y, dist)
    return __dtw(x, y, None, dist)

def __dtw(x, y, window, dist):
    len_x, len_y = len(x), len(y)
    if window is None:
        window = [(i, j) for i in range(len_x) for j in range(len_y)]
    window = ((i + 1, j + 1) for i, j in window)
    
    D = defaultdict(lambda: (float('inf'),))
    D[0, 0] = (0, 0, 0)
    
    # Iterate over the window and compute distances
    for i, j in window:
        dt = dist(x[i-1], y[j-1])
        D[i, j] = min(
            (D[i-1, j][0] + dt, i-1, j),
            (D[i, j-1][0] + dt, i, j-1),
            (D[i-1, j-1][0] + dt, i-1, j-1),
            key=lambda a: a[0]
        )
    
    path = []
    i, j = len_x, len_y
    while not (i == j == 0):
        path.append((i-1, j-1))
        i, j = D[i, j][1], D[i, j][2]
    
    path.reverse()
    return (D[len_x, len_y][0], path)

def __reduce_by_half(x):
    # Reduce by half operation
    x_reshaped = (x[:-1:2] + x[1::2]) / 2
    return x_reshaped

def __expand_window(path, len_x, len_y, radius):
    path_ = set(path)
    for i, j in path:
        for a, b in ((i + a, j + b)
                     for a in range(-radius, radius + 1)
                     for b in range(-radius, radius + 1)):
            path_.add((a, b))

    window_ = set()
    for i, j in path_:
        for a, b in ((i * 2, j * 2), (i * 2, j * 2 + 1),
                     (i * 2 + 1, j * 2), (i * 2 + 1, j * 2 + 1)):
            window_.add((a, b))

    window = []
    start_j = 0
    for i in range(0, len_x):
        new_start_j = None
        for j in range(start_j, len_y):
            if (i, j) in window_:
                window.append((i, j))
                if new_start_j is None:
                    new_start_j = j
            elif new_start_j is not None:
                break
        start_j = new_start_j

    return window
