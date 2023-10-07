@echo off
IF NOT EXIST ".\build" (mkdir build)
cd build
cmake ..\source
cmake --build .
.\Debug\step1.exe
cd ..