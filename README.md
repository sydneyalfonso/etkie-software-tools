# ekie-software-tools- 
Tools around Shopify and SOS inventory used to simplify generation of list of materials for each artisan to take on the work orders.


## Getting started 
To install everything (if you are working on a mac)

Open a terminal on mac (cmd + space and type terminal) 

install brew : 
Copy the line on the page and paste it the terminal  
https://brew.sh/

once brew is installed, type 

brew install python
pip install pandas
pip install numpy


## Run the script 
- Click on Clone or Download ( on the github page) 
- Download as ZIP
- UNZIP the file and place it in your work Folder
- Download BOMS from SOS inventory and place in the folder called BOM  (do not change the name of the downloaded file)
- Download the weekly work order and place it in the work order folder
- in the terminal run : python generate_raw_materials.py
