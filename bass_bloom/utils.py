from numba import cuda

def is_cuda_available():
    try:
        cuda.get_current_device()
        return True
    except cuda.cudadrv.error.CudaSupportError:
        return False