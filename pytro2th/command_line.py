######!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2020 Xavier Robert <xavier.robert@ird.fr>
# SPDX-License-Identifier: GPL-3.0-or-later

import argparse

from ._version import __version__
from .tro2th import tro2th


def main(**kwargs):
    ap = argparse.ArgumentParser()
    ap.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    ap.add_argument(
        "--fle-tro-fnme",
        default=None,
        help="Path and name of the .tro file to convert",
    )
    ap.add_argument(
        "--fle-tro-encoding",
        default=None,
        help="Force encoding of the .tro file to convert, for instance iso-8859-1. Default is utf-8",
    )
    ap.add_argument(
        "--fle-th-fnme",
        default=None,
        help="Path and name of the .th file to create from the .tro file.",
    )
    ap.add_argument(
        "--thlang", default="fr", help="String that set the language. 'fr' by default"
    )
    ap.add_argument("--cavename", default=None, help="Name of the cave")
    ap.add_argument(
        "--no-icomments",
        default=True,
        action="store_const",
        const=False,
        dest="icomments",
        help="Disable comments in the produced files",
    )
    ap.add_argument(
        "--no-icoupe",
        default=True,
        action="store_const",
        const=False,
        dest="icoupe",
        help="Disable the extended-elevation layout in the .thconfig file",
    )
    ap.add_argument(
        "--ithconfig",
        default=True,
        action="store_const",
        const=False,
        dest="ithconfig",
        help="Disable creation of the thconfig file",
    )
    ap.add_argument(
        "--thconfigfnme", default=None, help="Path and name of the thconfig file"
    )
    ap.add_argument(
        "--no-ithc",
        default=True,
        action="store_const",
        const="False",
        dest="ithc",
        help="Disable creation of a config file config.thc",
    )
    ap.add_argument(
        "--thcpath",
        default=None,
        help="Path to the directory that contains the config file called in the cave.thconfig file",
    )
    ap.add_argument("--thcfnme", default="config.thc", help="Name of the config.thc")
    ap.add_argument(
        "--sourcefile",
        nargs="*",
        help="Define the source files declared in the cave.thconfig",
    )
    ap.add_argument(
        "--xviscale", default=1000, type=float, help="Scale of the xvi file"
    )
    ap.add_argument(
        "--xvigrid",
        default=10.0,
        type=float,
        help="Spacing of the grid for the xvi, in meters",
    )
    ap.add_argument("--scale", default=500, type=float, help="Scale of the map")
    ap.add_argument(
        "--no-error-files",
        default=True,
        action="store_const",
        const=False,
        dest="Errorfiles",
        help="Do not raise en error if output files exists in the folder",
    )
    args = ap.parse_args(**kwargs)
    tro2th(**vars(args))
