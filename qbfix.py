#!/usr/bin/env python3
import argparse
import pandas as pd
from unidecode import unidecode
from pathlib import Path

def fix_date(date):
    date = date.replace('Ene.', '01')
    date = date.replace('Feb.', '02')
    date = date.replace('Mar.', '03')
    date = date.replace('Abr.', '04')
    date = date.replace('May.', '05')
    date = date.replace('Jun.', '06')
    date = date.replace('Jul.', '07')
    date = date.replace('Ago.', '08')
    date = date.replace('Sep.', '09')
    date = date.replace('Oct.', '10')
    date = date.replace('Nov.', '11')
    date = date.replace('Dic.', '12')
    return date

def trim_spaces(df):
    trim_strings = lambda x: x.strip() if isinstance(x, str) else x
    return df.applymap(trim_strings)

def dollar_to_float(df):
    dtof = lambda x: x.strip('$') if isinstance(x, str) else x
    return df.applyMap(dtof)

# Excel file with CSV extension
def convert_banregio(csv):
    data = pd.read_excel(csv)
    data.columns = [unidecode(str(header)) for header in data.iloc[3]]
    data.drop(range(5), inplace=True)
    data.drop(columns=['Referencia', 'Clasificacion', 'Saldo'], inplace=True)
    data.reset_index(drop=True, inplace=True)
    data = trim_spaces(data)
    data[data.columns[-2:]] = data[data.columns[-2:]].replace('[\$,]', '', regex=True).astype(float)
    store_csv(data, "Banregio")
    
# CSV file
def convert_banorte(csv):
    clean_file(csv)
    data = pd.read_csv('cleanfile.csv')
    data.columns = [x.replace('.', '').replace(' ', '_') for x in data.columns]
    data.drop(columns=['Movimiento', 'Cod_Trans', 'Saldos', 'Cheque'], inplace=True)
    data[data.columns[-2:]] = data[data.columns[-2:]].replace('[\$,]', '', regex=True).astype(float)
    data['Fecha'] = data['Fecha'].apply(lambda x: fix_date(x))
    store_csv(data, 'Banorte')


def store_csv(df, bank):
    dateRange = df.Fecha.iloc[1].replace('/','_') + '-' + df.Fecha.iloc[-1].replace('/','_')
    filepath = Path(f'converted/{bank}-{dateRange}.csv')  
    filepath.parent.mkdir(parents=True, exist_ok=True)  
    df.to_csv(filepath, index=False)

def clean_file(csv):
    with open(csv, "r") as file:
        with open("cleanfile.csv", 'w') as wf:
            for line in file.readlines():
                wf.write(unidecode(line))


parser = argparse.ArgumentParser(description='Generate Quickbooks compatible file')
parser.add_argument('file', help='Bank File')

args = parser.parse_args()
try:
    pd.read_excel(args.file)
    print("Banregio Detected.")
    convert_banregio(args.file)
except ValueError:
    print("Banorte Detected.")
    convert_banorte(args.file)