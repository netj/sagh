# Makefile for Social Aspects of GitHub

export BINDIR         := bin
export TOOLSDIR       := tools
export DATADIR        := data

PACKAGENAME := sagh
PACKAGEEXECUTES := bin/sagh

STAGEDIR := @prefix@
include buildkit/modules.mk
