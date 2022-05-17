all: clean task catcher

task:
	g++ signals.c -o task -ILib --std=c++11

catcher:
	g++ catcher.c -o catcher

clean:
	-rm -f *.o task catcher