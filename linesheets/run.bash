#!/bin/bash
python3 linesheet.py 

rm -r pdfs
cp -r photos output/photos
cd output
for filename in *.tex; do
    pdflatex "$filename" --interaction=nonstopmode
done
cd ..
mkdir pdfs
mv output/*.pdf pdfs/
rm output/*.log 
rm output/*.aux

mv pdfs/Blush.pdf . 
pdftk front.pdf Blush.pdf pdfs/*.pdf output linesheet.pdf