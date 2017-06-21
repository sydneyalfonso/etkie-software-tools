import os
import importlib
import sys
import traceback
import math


path_wo = 'work_orders'
root_wo = 'work_orders/work_orders_'
path_bom = 'bom'
root_bom = 'bom/boms_'


def error(str):
    print "##########################"
    print "There was an error, don't panick !"
    print "Here is some info : ", str
    print "If this does not make any sense copy and paste everything between the lines ### and send it to clem.jambou@gmail.com"
    print traceback.print_exc()
    print "##########################"
    sys.exit()


def nice_import(lib):
    try:
        importlib.import_module(lib)
    except:
        error("You need to install another library, type: pip install {}".format(lib))


nice_import("pandas")
import pandas as pd


def get_last_file_date(path):
    l = os.listdir(path)
    dates = sorted([name[-12:-4] for name in l if name[-4:] == '.csv'])
    try:
        return dates[-1]
    except:
        error("Files for the work order of the BOM were not found ! Make sure that a file namedwork_orders_YYYYMMDD ( where YYYY is the year, MM is the month and DD is the day is in the work_orders folder, similarly a file like boms_20170409.csv is in the bom folder. Tips : Use the default filename used when downloading from SOSInventory")


def load_last_file(path, root):
    """load the last file (alphabetically) of a folder in a pandas table,
    @input path to the folder
    @input root : root name of the file"""
    d = get_last_file_date(path)
    file_path = root + str(d) + '.csv'
    print "loading file : ", file_path
    return pd.read_csv(file_path)


def generate_wo_boms(wo, bom):
    work_orders_boms = {}
    work_order_numbers = list(set(wo.WorkOrderNumber))
    for w in work_order_numbers:
        wo_temp = wo[wo.WorkOrderNumber == w].copy()
        bom_items = []
        for id_r, row in wo_temp.iterrows():
            name = row['Item']
            qt = row['Quantity']
            bom_item = bom[bom.Assembly == name].copy()
            bom_item['Exact Quantity'] = bom_item['Quantity']
            bom_item = bom_item[['Component', 'Exact Quantity']].copy()
            bom_item['Exact Quantity'] *= qt
            bom_item['Recommended'] = bom_item['Exact Quantity']

            bom_items.append(bom_item)
        
        # concat by component
        wob = pd.concat(bom_items).groupby('Component').sum()

        ind_str = pd.Series(wob.index).astype(str)
        bool = ind_str.str.contains("Leather|Thread|Glue|Labor")
        wob.loc[wob.index[~bool], 'Recommended'] *= 1.05
        wob.Recommended = wob.Recommended.map(math.ceil)
        wob.Recommended.astype(int)

        work_orders_boms[w] = wob
        
    return work_orders_boms


def start_html(f):

  f.write("""
    <!DOCTYPE html>
    <html>
    <style>
    tr:nth-child(even) {background-color: #f2f2f2}

    td, th {
        border: 1px solid #ddd;
        padding: 8px;
    }

    tr:nth-child(even){background-color: #f2f2f2;}

    tr:hover {background-color: #ddd;}

    customers th {
        padding-top: 12px;
        padding-bottom: 12px;
        text-align: left;
        background-color: #4CAF50;
        color: white;
    }

    </style>
    <body>
    """)


def end_html(f):

    f.write(""" </body> 
    </html> """)


def write_file(f, w, wo, df):
    start_html(f)
   
    f.write('<h1> Work Order {} </h1>'.format(w))
    f.write('<h2> Raw material &#9633 | Finished Goods &#9633 </h2>')

    f.write('<h2> Artisan : {}  </h2>'.format(w.split("_")[-1]))
    f.write('<h3> Raw materials </h2>'.format(w))
    f.write(df.to_html())
    f.write('<h3> Summary, Checked by __________ </h3>')
    df_summary = wo[wo.WorkOrderNumber == w][['Date', 'Item', 'Quantity']].fillna('__').groupby('Item').first().copy()
    df_summary['Received ? '] = '' 
    df_summary['Quality Note'] = '' 
    df_summary.Date = pd.to_datetime(df_summary.Date).dt.strftime("%b %d %Y")
    
    f.write(df_summary.to_html())
    end_html(f)


def file_output(list_of_bom, wo):

    with open('artisans_material_pull_sheet.html', 'w') as f:
        for w, df in list_of_bom.iteritems():
            write_file(f, w, wo, df)           
            with open(w + '.html', 'w') as f2:
                write_file(f2, w, wo, df)

    print "files saved"


def slugify(s):
    """ make string nice for filename"""
    return "".join(x for x in s if x.isalnum())


def generate_all_boms_html():
    bom = load_last_file(path_bom, root_bom)
    bom = bom[['Assembly', 'Component', 'Quantity']]
    bom = bom.fillna(method='ffill')
    for ass in set(list(bom.Assembly)):
        with open('boms_html/{}.html'.format(slugify(ass)), 'w') as f:
            start_html(f)
            f.write("<h1>Materials for: {} </h1>".format(ass))
            f.write(bom[bom.Assembly == ass].to_html())

def generate_raw_materials():
    wo = load_last_file(path_wo, root_wo)
    bom = load_last_file(path_bom, root_bom)
    wo = wo[['WorkOrderNumber', 'Date', 'Item', 'Quantity', 'Memo']]
    bom = bom[['Assembly', 'Component', 'Quantity']]
    bom = bom.fillna(method='ffill')
    list_of_bom = generate_wo_boms(wo, bom)
    file_output(list_of_bom, wo)

if __name__ == "__main__":
    generate_raw_materials()
