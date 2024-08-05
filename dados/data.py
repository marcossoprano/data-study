import pandas as pd
import numpy as np

# Funções para ler arquivos com delimitadores diferentes
def read_space_delimited_file(file_path, column_names=None):
    return pd.read_csv(file_path, sep=r'\s+', header=None, names=column_names)

def read_tab_delimited_file(file_path, column_names=None):
    return pd.read_csv(file_path, delimiter='\t', header=None, names=column_names)

# Caminhos dos arquivos de dados
app_usage_trace_file = 'App_Usage_Trace.txt'
app2category_file = 'App2Category.txt'
categories_file = 'Categorys.txt'
base_poi_file = 'base_poi.txt'

# Carregar os dados dos arquivos
app_usage_trace = read_space_delimited_file(app_usage_trace_file, column_names=['User ID', 'Timestamp', 'Location', 'App ID', 'Traffic'])
app2category = read_tab_delimited_file(app2category_file, column_names=['App ID', 'Category ID'])
categories = read_tab_delimited_file(categories_file, column_names=['Category ID', 'English Name'])
base_poi = read_tab_delimited_file(base_poi_file)

# Definir cabeçalhos de acordo com o conteúdo do arquivo base_poi
base_poi.columns = ['Basestation ID', 'Medical care', 'Hotel', 'Business affairs', 'Life service', 'Transportation hub', 'Culture', 'Sports', 'Residence', 'Entertainment and leisure', 'Scenic spot', 'Government', 'Factory', 'Shopping', 'Restaurant', 'Education', 'Landmark', 'Other']

# Filtrar valores não numéricos e converter para int
def filter_and_convert_to_int(series):
    series = pd.to_numeric(series, errors='coerce')  # Converte valores válidos e força NaN para inválidos
    return series.dropna().astype(int)  # Remove NaN e converte para int

app2category['Category ID'] = filter_and_convert_to_int(app2category['Category ID'])
categories['Category ID'] = filter_and_convert_to_int(categories['Category ID'])

# Exibir os primeiros registros de cada dataframe
print("App Usage Trace:")
print(app_usage_trace.head(), "\n")
print("App to Category:")
print(app2category.head(), "\n")
print("Categories:")
print(categories.head(), "\n")
print("Base POI:")
print(base_poi.head(), "\n")

# Número total de registros
print(f"Total de registros de uso de apps: {len(app_usage_trace)}\n")

# Analisar a distribuição de categorias de apps
app_usage_with_category = app_usage_trace.merge(app2category, on='App ID')
app_usage_with_category = app_usage_with_category.merge(categories, on='Category ID')
category_counts = app_usage_with_category['English Name'].value_counts()
print("Distribuição de Categorias de Apps:")
print(category_counts, "\n")

# Analisar o tráfego de dados por usuário
user_traffic = app_usage_trace.groupby('User ID')['Traffic'].sum()
print("Tráfego de Dados por Usuário:")
print(user_traffic.describe(), "\n")

# Limpar e analisar a distribuição de PoIs por estação base
# Remove a primeira linha que contém cabeçalhos
base_poi_cleaned = base_poi[1:].reset_index(drop=True)
# Converte todas as colunas para numérico, forçando erros a NaN
base_poi_cleaned = base_poi_cleaned.apply(pd.to_numeric, errors='coerce')
# Calcula a média das colunas numéricas
mean_poi_per_category = base_poi_cleaned.mean()
print("Distribuição de PoIs por Categoria:")
print(mean_poi_per_category, "\n")
