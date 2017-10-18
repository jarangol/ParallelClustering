#!/usr/bin/env

if ! [ -x /usr/bin/nproc ]; then
    echo "nproc is not installed. Please install it."
    exit 1
fi
CORES=$(nproc)

mpiexec -np $CORES python ./paralelo.py
