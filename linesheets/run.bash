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

mv pdfs/Dark\ Skies.pdf DarkSkies.pdf
#pdftk front.pdf Golden.pdf pdfs/*.pdf output linesheet.pdf
gs -q -dNOPAUSE -dBATCH -sDEVICE=pdfwrite -sOutputFile=linesheet.pdf front.pdf DarkSkies.pdf pdfs/*.pdf
gs -sDEVICE=pdfwrite -dPDFSETTINGS=/ebook -q -o linesheet_small.pdf linesheet.pdf