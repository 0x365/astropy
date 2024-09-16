import ctypes as ctypes
import os
import numpy as np
from array import array

os.system("go build -buildmode=c-shared -o ./go_fit.so .")

library = ctypes.cdll.LoadLibrary("./go_fit.so")

conn1 = library.consensus_completeness_per
conn1.restype = ctypes.c_int64

conn1.argtypes = [
    ctypes.POINTER(ctypes.c_double),
    ctypes.c_int64,
    ctypes.POINTER(ctypes.c_double),
    ctypes.c_int64,
    ctypes.c_int64
]

combs_arr = array('d', [1, 2, 3, 7, 9, 2])
combs_raw = (ctypes.c_double * len(combs_arr)).from_buffer(combs_arr)


grid_arr = array('d', [1, 2, 4, 5, 2, 3,4, 5])
grid_raw = (ctypes.c_double * len(grid_arr)).from_buffer(grid_arr)

num_sats = 5

print(conn1(combs_raw, len(combs_raw), grid_raw, len(grid_raw), num_sats))