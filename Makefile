PROJ=sp_reader

CC=g++

CFLAGS=-Wall

INC_DIRS=.

LIBS=-lz

$(PROJ): $(PROJ).cpp
	$(CC) $(CFLAGS) -o $@ $^ $(INC_DIRS:%=-I%) $(LIB_DIRS:%=-L%) $(LIBS)

.PHONY: clean

clean:
	rm $(PROJ)
