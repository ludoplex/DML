# ==========================================================================
# Copyright (C) 2023 Intel Corporation
#
# SPDX-License-Identifier: MIT
# ==========================================================================

import subprocess
import re

NUMAS    = 'Numas'
DEVICES  = 'Devices'
WQS      = 'WQs'
ENGINES  = 'Engines'

CONFIG      = 'Config'
API         = 'API'
PATH        = 'Path'
EXEC        = 'Execution'
OPERATION   = 'Op'
SRC_MEM     = 'In Mem'
DST_MEM     = 'Out Mem'
TIMING      = 'Timing'
THREADS     = 'Threads'
BATCH_SIZE  = 'BSize'
QDEPTH      = 'QSize'
DATA        = 'Data'
SIZE        = 'Size'
BLOCK_SIZE  = 'Block Size'
BLOCK       = 'Block'
COMP_PARAMS = "Compression Params"
FILT_PARAMS = "Filter Params"
RATIO       = 'Ratio'
THROUGHPUT  = 'Thr (GB/s)'
LATENCY     = 'Lat (ns)'

class DictAttrib(dict):
    def __init__(self, *args, **kwargs):
        super(DictAttrib, self).__init__(*args, **kwargs)
        self.__dict__ = self
        
def get_hostname():
    p = subprocess.run(['hostname'], universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    host = ""
    if not p.returncode:
        lines = p.stdout.splitlines()
        host = "_"+lines[0].split('.')[0]
    return host

def find_alias(name, list):
    return any(name in alias for alias in list)
    
def find_pattern(string, pattern, required, empty = "n/a"):
    if match := re.match(pattern, string):
        return match[1]
    else:
        return "Error" if required else empty
    
def find_param(string, param, required=False, set=False, last=False, delim=":"):
    if not set:
        return find_pattern(string, f".*/{param}{delim}(.+?)/", required)
    result = ""
    value = find_pattern(string, f".*/{param}{delim}(.+?)/", required, empty="")
    if len(value):
        result = f"{param}:{value}"
        if not last:
            result += "/"
    return result

