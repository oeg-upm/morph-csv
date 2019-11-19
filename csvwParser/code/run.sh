#!/bin/bash

head -20 tmp/gene_info_bk > tmp/gene_info
time python3 main.py
