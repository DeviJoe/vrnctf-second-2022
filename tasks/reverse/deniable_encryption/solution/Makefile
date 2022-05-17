all: clean encrypt do_not_launch

encrypt:
	gcc encrypt.c -o encrypt

do_not_launch:
	gcc decrypt.c -o do_not_launch

clean:
	-rm -f *.o encrypt do_not_launch