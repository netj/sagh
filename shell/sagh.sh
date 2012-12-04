#!/usr/bin/env bash
# sagh -- Social Aspects of GitHub Command-Line Interface
# Usage: sagh [-OPTION] COMMAND [ARG]...
# 
# COMMAND is one of the following forms:
# 
#   sagh init
# 
#   sagh sync-repos
#   sagh compute-global PROPERTY
# 
#   sagh ls-forks REPO
# 
#   sagh hack for-each-repo sh -c 'pwd; cd git; git log --format=%ae | wc -l'
# 
# Global OPTION is one of:
#   -v      for increasing verbosity
# 
#
# Author: Jaeho Shin <netj@cs.stanford.edu>
# Created: 2012-11-14
set -eu

if [ -z "${SAGH_HOME:-}" ]; then
    Self=$(readlink -f "$0" 2>/dev/null || {
        # XXX readlink -f is only available in GNU coreutils
        cd $(dirname -- "$0")
        n=$(basename -- "$0")
        if [ -L "$n" ]; then
            L=$(readlink "$n")
            if [ x"$L" = x"${L#/}" ]; then
                echo "$L"; exit
            else
                cd "$(dirname -- "$L")"
                n=$(basename -- "$L")
            fi
        fi
        echo "$(pwd -P)/$n"
    })
    Here=$(dirname "$Self")

    # Setup environment
    export SAGH_HOME=${Here%/@BINDIR@}
    export BINDIR="$SAGH_HOME/@BINDIR@"
    export TOOLSDIR="$SAGH_HOME/@TOOLSDIR@"
    export DATADIR="$SAGH_HOME/@DATADIR@"

    export PATH="$TOOLSDIR:$PATH"
    export PYTHONPATH="$TOOLSDIR${PYTHONPATH:+:${PYTHONPATH:-}}"
    unset CDPATH
    export SHLVL=0 SAGH_LOGLVL=${SAGH_LOGLVL:-1}
fi


while getopts "v" opt; do
    case $opt in
        v)
            let SAGH_LOGLVL++
            ;;
            # TODO quiet
    esac
done
shift $(($OPTIND - 1))


# Process input arguments
[ $# -gt 0 ] || usage "$0" "No COMMAND given"
Cmd=$1; shift


# Check if it's a valid command
exe=sagh-"$Cmd"
if type "$exe" &>/dev/null; then
    set -- "$exe" "$@"
else
    usage "$0" "$Cmd: invalid COMMAND"
fi


# Run given command under this environment
exec "$@"
