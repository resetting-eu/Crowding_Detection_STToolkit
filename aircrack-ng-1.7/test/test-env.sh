#!/bin/sh

abs_builddir="/home/kali/Desktop/aircrack-ng-1.7/test"; export abs_builddir
abs_srcdir="/home/kali/Desktop/aircrack-ng-1.7/test"; export abs_srcdir
top_builddir=".."; export top_builddir
top_srcdir=".."; export top_srcdir

EXEEXT=""; export EXEEXT

EXPECT="/usr/bin//expect"; export EXPECT

AIRCRACK_LIBEXEC_PATH="/home/kali/Desktop/aircrack-ng-1.7/src"; export AIRCRACK_LIBEXEC_PATH

AIRCRACK_NG_ARGS="${AIRCRACK_NG_ARGS:--p 4}"; export AIRCRACK_NG_ARGS

AWK="gawk"; export AWK

GREP="/usr/bin/grep"; export GREP
