# Author : Chris Ranc
# Date : March 31, 2018
# Description : Makefile to compile python scripts into micropython byte code
#               and to load them to a micropython compatible esp device

# Toolchain and Path Configuratio
MC=./tools/mpy-cross
UL=$(shell whereis ampy | sed -e "s/ampy: //")
RM=rm -f


# File locations
SRCDIR=src
OBJDIR=obj
SRC=$(wildcard $(SRCDIR)/*.py)
OBJ=$(patsubst $(SRCDIR)/%.py, $(OBJDIR)/%.mpy, $(SRC))
RMSRC=$(patsubst $(SRCDIR)/%.py, %.py, $(SRC)) 
RMOBJ=$(patsubst $(OBJDIR)/%.mpy, %.mpy, $(OBJ))

# Build flags
BF=-v

# Upload flags
UF=-p /dev/ttyUSB0 -b 115200


# Makefile rules
all: build
load: build
build: $(OBJ)

# Clean up byte code files
clean:
	$(RM) $(OBJ)

# Compiling each source file
$(OBJDIR)/%.mpy: $(SRCDIR)/%.py
	$(MC) -v -o $@ $<


# Upload function
# Upload all byte code files
load:
	@echo Loading
	@for file in $(OBJ) ; do \
		$(UL) $(UF) put $$file ; \
		sync ; \
		echo $$file loaded ; \
	done
	@echo Done

loadpy:
	@echo Loading
	@for file in $(SRC) ; do \
		$(UL) $(UF) put $$file ; \
		sync ; \
		echo $$file loaded ; \
	done
	@echo Done

# Upload main python script
loadmain:
	$(UL) $(UF) put main.py

loadlib:
	$(UL) $(UF) put $(OBJDIR)/lib

loadlibpy:
	$(UL) $(UF) put $(SRCDIR)/lib

# Remove byte code
rmbulk:
	@echo Loading
	@for file in $(ls $(OBJDIR)/*.mpy) ; do \
		$(UL) $(UF) rm $$file ; \
		echo $$file removed ; \
	done
	@echo Done

# Remove scripts
rmbulkpy:
	@echo Loading
	@for file in $(RMSRC) ; do \
		$(UL) $(UF) rm $$file ; \
		echo $$file removed; \
	done
	@echo Done

# ampy helper functions
espls:
	$(UL) $(UF) ls

espput:
	$(UL) $(UF) put $(input)

espget:
	$(UL) $(UF) get $(input)

esprm:
	$(UL) $(UF) rm $(input)
