# Supplementary Feeder Unit

## Dependencies
 - ampy
    - Used for loading python scripts
    - Installed with pip
        -  pip install adafruit-ampy
 - mpy-cross
    - Micropython byte code cross compiler
        - This is done to reduce RAM consumption during initialization
    - Included in repo but can be built from source from micropython git repo
        - https://github.com/micropython/micropython/mpy-cross
 - GNU Make
    - Used for quickly automating byte code builds and loading and removing files onto and off of the esp8266
 - An esp8266 development board with micropython
    - Adafruit dev board
        - https://www.adafruit.com/product/2821
    - Acrobotic dev board
        - https://acrobotic.com/products/acr-00018
    - Flash instructions
        - https://docs.micropython.org/en/latest/esp8266/esp8266/tutorial/intro.html

## Quickstart 

To load the project right away run:
    
    make loadmain
    make load

The first will load the main.py script and then proceed to build the 
dependencies as byte code files and load them onto the board.

The are a handful of other make targets that can be used for adding and 
removing files quickly.  As well as helper targets for using ampy functions
