#############################################
##         average precision              ###
##      Packaged by Xiaojun Chang         ###
##			cxj273@gmail.com			  ###
#############################################

CC = g++

all : ap

ap : main.o calcap.o
	$(CC) -o ap main.o calcap.o

main.o : main.cpp calcap.h
	$(CC) -c main.cpp

calcap.o : calcap.cpp calcap.h
	$(CC) -c calcap.cpp

clean :
	rm -rf ap
	rm -rf *.o
