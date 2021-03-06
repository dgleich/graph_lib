# A python wrapper for sweep cut procedure
# A - the sparse matrix representing the symmetric graph
# ids - the order of vertices given
# results - the best set with the smallest conductance
# actual_length - the number of vertices in the best set
# num - the number of vertices given
# values - A vector scoring each vertex (e.g. pagerank value). 
#          This will be sorted and turned into one of the other inputs.
# flag - 0 for sweepcut_with_sorting and 1 for sweepcut_without_sorting
# degrees - user defined degrees, set it to be [] if not provided
# min_cond - minimum conductance

from operator import itemgetter
import numpy as np
from numpy.ctypeslib import ndpointer
import ctypes
import platform

def wrapped_ndptr(*args, **kwargs):
    base = ndpointer(*args, **kwargs)
    def from_param(cls, obj):
        if obj is None:
            return obj
        return base.from_param(obj)
    return type(base.__name__, (base,), {'from_param': classmethod(from_param)})

def sweepcut(n,ai,aj,a,ids,num,values,flag,degrees = None):
    
    if platform.architecture() == ('64bit', ''):
        float_type = np.float64
    else:
        float_type = np.float32

    dt = np.dtype(ai[0])
    (itype, ctypes_itype) = (np.int64, ctypes.c_int64) if dt.name == 'int64' else (np.uint32, ctypes.c_uint32)
    dt = np.dtype(aj[0])
    (vtype, ctypes_vtype) = (np.int64, ctypes.c_int64) if dt.name == 'int64' else (np.uint32, ctypes.c_uint32)

    #load library
    lib=ctypes.cdll.LoadLibrary("../../lib/graph_lib_test/./libgraph.dylib")
    
    if (vtype, itype) == (np.int64, np.int64):
        fun = lib.sweepcut_with_sorting64 if flag == 0 else lib.sweepcut_without_sorting64
    elif (vtype, itype) == (np.uint32, np.int64):
        fun = lib.sweepcut_with_sorting32_64 if flag == 0 else lib.sweepcut_without_sorting32_64
    else:
        fun = lib.sweepcut_with_sorting32 if flag == 0 else lib.sweepcut_without_sorting32

    #call C function
    ids=np.array(ids,dtype=vtype)
    values=np.array(values,dtype=float_type)
    results=np.zeros(num,dtype=vtype)
    fun.restype=ctypes_vtype
    min_cond = np.array([0.0],dtype=float_type)
    if degrees is not None:
        degrees = np.array(degrees,dtype=float_type)
    if flag == 0:
        fun.argtypes=[ndpointer(ctypes.c_double, flags="C_CONTIGUOUS"),
                      ndpointer(ctypes_vtype, flags="C_CONTIGUOUS"),
                      ndpointer(ctypes_vtype, flags="C_CONTIGUOUS"),
                      ctypes_vtype,ctypes_vtype,
                      ndpointer(ctypes_itype, flags="C_CONTIGUOUS"),
                      ndpointer(ctypes_vtype, flags="C_CONTIGUOUS"),
                      ndpointer(ctypes.c_double, flags="C_CONTIGUOUS"),
                      ctypes_vtype,
                      ndpointer(ctypes.c_double, flags="C_CONTIGUOUS"),
                      wrapped_ndptr(dtype=ctypes.c_double,ndim=1,flags="C_CONTIGUOUS")
                      ]
        actual_length=fun(values,ids,results,num,n,ai,aj,a,0,min_cond,degrees)
    else:
        fun.argtypes=[ndpointer(ctypes_vtype, flags="C_CONTIGUOUS"),
                      ndpointer(ctypes_vtype, flags="C_CONTIGUOUS"),
                      ctypes_vtype,ctypes_vtype,
                      ndpointer(ctypes_itype, flags="C_CONTIGUOUS"),
                      ndpointer(ctypes_vtype, flags="C_CONTIGUOUS"),
                      ndpointer(ctypes.c_double, flags="C_CONTIGUOUS"),
                      ctypes_vtype,
                      ndpointer(ctypes.c_double, flags="C_CONTIGUOUS"),
                      wrapped_ndptr(dtype=ctypes.c_double,ndim=1,flags="C_CONTIGUOUS")
                      ]
        actual_length=fun(ids,results,num,n,ai,aj,a,0,min_cond,degrees)

    actual_results=np.empty(actual_length,dtype=vtype)
    actual_results[:]=[results[i] for i in range(actual_length)]
    min_cond = min_cond[0]

    return (actual_length,actual_results,min_cond)
