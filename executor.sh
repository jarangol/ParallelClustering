#!/usr/bin/env

if ! [ -x /usr/bin/nproc ]; then
    echo "nproc is not installed. Please install it."
    exit 1
fi
CORES=$(nproc)

TEST=1
#mpiexec -np ${CORES} python ./hello_world${EXAMPLE}.py
# mpiexec -np 4 python ./test${TEST}.py
python ./serial.py
# mpiexec -np 4 python ./paralelo.py
