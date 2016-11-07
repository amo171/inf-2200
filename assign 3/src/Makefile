CC = gcc
CFLAGS = -m32 -Wall -Werror -Wno-unused -g -O0 -I.
OBJDIR = obj
PROGRAM = cachesim

OBJS = cpu.o memory.o
HEADERS = byutr.h memory.h

all: $(PROGRAM) $(HEADERS) Makefile

dirs:
	@mkdir -p $(OBJDIR)

$(PROGRAM): $(patsubst %, $(OBJDIR)/%, $(OBJS))
	$(CC) $(CFLAGS) $^ -o $@ -lm

$(OBJDIR)/%.o: %.c dirs
	$(CC) $(CFLAGS) -c $< -o $@ -lm

clean:
	rm -rf *.o *~ $(PROGRAM) $(OBJDIR)
