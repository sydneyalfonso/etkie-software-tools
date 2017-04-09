import pandas as pd
import os

path_wo = 'work_orders'
root_wo = 'work_orders/work_orders_'
path_bom = 'bom'
root_bom = 'bom/boms_'


def get_last_file_date(path):
    l = os.listdir(path)
    dates = sorted([name[-12:-4] for name in l if name[-4:] == '.csv'])
    return dates[-1]


def load_last_file(path, root):
    """load the last file (alphabetically) of a folder in a pandas table,
    @input path to the folder
    @input root : root name of the file"""  
    d = get_last_file_date(path)
    file_path =  root + str(d) + '.csv'
    print "loading file : ", file_path
    return pd.read_csv(file_path)


def generate_wo_boms(wo, bom):
    work_orders_boms = {}
    work_order_numbers = list(set(wo.WorkOrderNumber))
    for w in work_order_numbers:    
        wo_temp = wo[wo.WorkOrderNumber==w].copy()
        bom_items = []
        for id_r, row in wo_temp.iterrows():
            name = row['Item']
            qt = row['Quantity']
            bom_item = bom[bom.Assembly == name].copy()
            bom_item = bom_item[['Component', 'Quantity']]
            bom_item.Quantity *= qt
            bom_items.append(bom_item)
        work_orders_boms[w] = pd.concat(bom_items).groupby('Component').sum()
    return work_orders_boms


def file_output(list_of_bom, wo):

    with open('artisans_material_pull_sheet.html', 'w') as f:
        for w, df in list_of_bom.iteritems():
            f.write('<h1> Work Order {} </h1>'.format(w))
            f.write('<h2> Artisan : {}  </h2>'.format(w[:2]))
            f.write('<h2> Raw materials </h2>'.format(w))
            f.write(df.to_html())
            f.write('<h2> Summary </h2>')
            f.write(wo[wo.WorkOrderNumber==w][['Date', 'Item', 'Quantity', 'Memo']].fillna('__').groupby('Item').first().to_html())
    print "file saved"


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
