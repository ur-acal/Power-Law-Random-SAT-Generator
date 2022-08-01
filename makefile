create:
	g++ -std=c++11 -O3 -o CreateSAT CreateSAT.cpp Formula.cpp

clean:
	rm *o all