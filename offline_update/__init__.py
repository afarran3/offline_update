
__version__ = '1.0.0'

VERSION = "1.0.0"
PROJECT_NAME = "offline_update"
FRAPPE_VERSION = None
current_path = None
updated_path = None
LOG_BUFFER = []
from frappe.utils import get_bench_path
import os

dirs = {
	'pip_dir': os.path.join(get_bench_path(), "pip_lib"),
	'yarn_dir': os.path.join(get_bench_path(), "yarn_lib")
}

def set_frappe_version(bench_path=get_bench_path()):
    
    from .utils.app import get_current_frappe_version

    global FRAPPE_VERSION
    if not FRAPPE_VERSION:
        FRAPPE_VERSION = get_current_frappe_version(bench_path=bench_path)
