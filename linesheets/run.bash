#!/bin/bash
python linesheet.py 

cd output
for filename in *.tex; do
    pdflatex "$filename" -interaction=nonstopmode
done
cd ..
mkdir pdfs
mv output/*.pdf pdfs/
rm output/*.log 
rm output/*.aux