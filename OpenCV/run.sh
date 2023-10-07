#!/bin/bash
if [ ! -f ./build/ ];
then 
	mkdir build
fi
cd build
cmake ../source
cmake --build  .
./step1
cd ..
