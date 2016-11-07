# Makefile for compiling and linking .C files with asm files

# -m32 compiles .C to 32bit assembly
# -masm=att Compiles .C with at&t assembly systax

CC = gcc
CFLAGS = -m32 -masm=att -g -pg

all: program

# To change optimization levels on .C file change -O0 to either -O1, -O2, -O3
# Optimization levels GCC https://gcc.gnu.org/onlinedocs/gnat_ugn/Optimization-Levels.html
main: main.c Makefile
	$(CC) $(CFLAGS) -O0 -S -o $@.s $<

# asm.S and main has to exist before executing compilation targets
program: asm.S main
	$(CC) $(CFLAGS) -E $< > $@_pp.s
	$(CC) $(CFLAGS) main.s $@_pp.s -o $@
