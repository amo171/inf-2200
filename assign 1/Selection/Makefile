# Author: Erlend Graff <erlend.h.graff@uit.no>

CC = gcc
CFLAGS = -m32 -masm=att

all: selection

main: main.c Makefile
	$(CC) $(CFLAGS) -O0 -S -o $@.s $<  

selection: selection.S main
	$(CC) $(CFLAGS) -E $< > $@_pp.s
	$(CC) $(CFLAGS) main.s $@_pp.s -o $@

clean:
	rm -rf *_pp.s selection selection.exe main.s