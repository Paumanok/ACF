# Author : Chris Ranc
# Date : March 31, 2018
# Description : Makefile to compile python scripts into micropython byte code
#               and to load them to a micropython compatible esp device

# Toolchain and Path Configuratio
MC=./tools/mpy-cross
UL=$(shell whereis ampy | sed -e "s/ampy:  //")
RM=rm -f


# File locations
SRCDIR=src
OBJDIR=obj
SRC=$(wildcard $(SRCDIR)/*.py)
OBJ=$(patsubst $(SRCDIR)/%.py, $(OBJDIR)/%.mpy, $(SRC))

# Build flags
BF=-v

# Upload flags
UF=-p /dev/ttyUSB0 -b 115200 put

# Makefile rules
all: build
build: $(OBJ)

clean:
	$(RM) $(OBJ)

#Compiling each source file
$(OBJDIR)/%.mpy: $(SRCDIR)/%.py
	$(MC) -v -o $@ $<



