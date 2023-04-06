CC:=gcc
CFLAGS:=-Wall -std=c99
DEBUGFLAGS:=-O0 -g

BIN:=cache_sim
SOURCE:=cache_sim.c

.PHONY: clean test $(BIN)

$(BIN): $(SOURCE)
	$(CC) $(CFLAGS) $(DEBUGFLAGS) -o $@ $^

clean:
	rm -f *.o

test/cursemenu.py: cursemenu.py
	cp $< $@

test/diffwin.py: diffwin.py test/cursemenu.py
	cp $< $@

test/testOutput.py: testOutput.py
	cp $< $@

test: $(BIN) test/diffwin.py test/testOutput.py
	python3 ./test/testOutput.py \
--testpath test/cases --exppath test/exp \
--program $<

# vim: noexpandtab
