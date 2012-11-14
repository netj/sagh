# Makefile for GitHub analysis tools

export BINDIR         := bin
export TOOLSDIR       := tools
export DATADIR        := data

PACKAGENAME := gha
PACKAGEEXECUTES := bin/gha

STAGEDIR := @prefix@
include buildkit/modules.mk
