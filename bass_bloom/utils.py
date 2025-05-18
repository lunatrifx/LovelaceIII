from numba import cuda
import platform
import os

def is_cuda_available():
    try:
        cuda.get_current_device()
        return True
    except cuda.cudadrv.error.CudaSupportError:
        return False
    
def is_cloud_environment():
    # GitHub Codespaces
    if "CODESPACES" in os.environ or "CODESPACE_NAME" in os.environ:
        return True

    # Replit
    if "REPL_ID" in os.environ:
        return True

    # Google Colab
    if "COLAB_GPU" in os.environ or "COLAB_BACKEND_VERSION" in os.environ:
        return True

    # Headless Linux (usually cloud VM or container)
    if platform.system() == "Linux" and not os.environ.get("DISPLAY"):
        return True

    return False