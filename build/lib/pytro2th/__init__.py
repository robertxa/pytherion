######!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2020 Xavier Robert <xavier.robert@ird.fr>
# SPDX-License-Identifier: GPL-3.0-or-later


from __future__ import  division
# This to be sure that the result of the division of integers is a real, not an integer
from __future__ import absolute_import
from __future__ import print_function

# Import modules
import sys
import os
#import copy
import numpy as np

__version__ = "1.2.0"

# Import all the functions
__all__ = ['vtopotools', 'datathwritetools', 'buildthconfig', 'buildthconfig', 'tro2th.tro2th']

#from .text import joke
#from datathwritetools import writeheader_th, writecenterlineheader, writedata
from .buildparam import *
from .vtopotools import *
from .datathwritetools import *
from .buildthconfig import *
from .tro2th import *
