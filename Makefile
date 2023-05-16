CC:=g++
CFLAGS:=-std=c++11
DEBUGFLAGS:=-O0 -g

BIN:=cache_sim
SRC:=$(wildcard *.cpp)
OBJ:=$(SRC:.cpp=.o)

all: $(BIN)

.PHONY: clean test $(BIN)

$(BIN): $(OBJ)
	$(CC) $(CFLAGS) $(DEBUGFLAGS) -o $@ $^
	rm -f *.o

%.o: %.cpp
	$(CC) $(CFLAGS) $(DEBUGFLAGS) -c -o $@ $<

clean:
	rm -f $(BIN) *.o

test: $(BIN)
	python3 test/testOutput.py \
--testpath test/cases --exppath test/exp \
--program $<

# vim: noexpandtab
