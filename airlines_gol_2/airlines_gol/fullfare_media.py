import pandas as pd
import openpyxl
from datetime import datetime
from dateutil.tz import tzlocal
import glob
import os
import shutil

data_hoje = str(datetime.now(tzlocal()).date().strftime("%d-%m-%Y"))
#pega o arquivo GOL_Geral_{hoje}.csv
df = pd.read_csv(f"L:/Estrategia/Macro_novo/Inflation/Coleta_passagem_aerea_nova/airlines_gol/GOL_Geral_{data_hoje.replace("-","_")}.csv")

df_media = df.copy()
#calcula a média do arquivo de hoje
medias_estacoes = df_media.groupby('departurestation')['fullfare'].mean().reset_index()
medias_estacoes = medias_estacoes.pivot(columns='departurestation', values='fullfare')
valores_diagonal = medias_estacoes.values.diagonal()
medias = pd.DataFrame([valores_diagonal], columns=medias_estacoes.columns)
#exporta o arquivo de hoje
nome_excel = f"media_{data_hoje}.xlsx"

medias.to_excel(nome_excel, index=False)

print("DataFrame exported to output.xlsx")

# mover os arquivos GOL_Geral_*
source = "L:/Estrategia/Macro_novo/Inflation/Coleta_passagem_aerea_nova/airlines_gol"
destination = "L:/Estrategia/Macro_novo/Inflation/Coleta_passagem_aerea_nova/airlines_gol/coleta_e_media"
Padrao_dos_arquivos = "GOL_Geral_*"
file_list = glob.glob(os.path.join(source,Padrao_dos_arquivos), recursive=True)
for file_path in file_list:
    dst_path = os.path.join(destination, os.path.basename(file_path))
    shutil.move(file_path, dst_path)
    print(f"Moved {file_path} -> {dst_path}")


# mover os arquivos media_*
source = "L:/Estrategia/Macro_novo/Inflation/Coleta_passagem_aerea_nova/airlines_gol"
destination = "L:/Estrategia/Macro_novo/Inflation/Coleta_passagem_aerea_nova/airlines_gol/coleta_e_media"
Padrao_dos_arquivos = "media_*"
file_list = glob.glob(os.path.join(source,Padrao_dos_arquivos), recursive=True)
for file_path in file_list:
    dst_path = os.path.join(destination, os.path.basename(file_path))
    shutil.move(file_path, dst_path)
    print(f"Moved {file_path} -> {dst_path}")