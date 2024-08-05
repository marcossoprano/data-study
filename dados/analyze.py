import pandas as pd

# Função para ler arquivos com delimitadores diferentes
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

# Verificar tipos de dados
print(app_usage_trace.dtypes)
print(app2category.dtypes)
print(categories.dtypes)

# Verificar valores nulos
print(app2category['Category ID'].isnull().sum())
print(categories['Category ID'].isnull().sum())

# Realizar a junção
app_usage_with_category = app_usage_trace.merge(app2category, on='App ID')
app_usage_with_category = app_usage_with_category.merge(categories, on='Category ID')

# Exibir resultados da junção
print(app_usage_with_category.head())

# Análise temporal
app_usage_with_category['Timestamp'] = pd.to_datetime(app_usage_with_category['Timestamp'], format='%Y%m%d%H%M%S')
app_usage_with_category.set_index('Timestamp', inplace=True)

# Gráficos de Análise Temporal
import matplotlib.pyplot as plt
import seaborn as sns

# Tráfego de dados ao longo do tempo
plt.figure(figsize=(12, 6))
app_usage_with_category['Traffic'].resample('D').sum().plot()
plt.title('Tráfego de Dados por Dia')
plt.xlabel('Data')
plt.ylabel('Tráfego Total')
plt.show()

# Média de tráfego por categoria ao longo do tempo
category_traffic = app_usage_with_category.groupby(['English Name']).resample('D')['Traffic'].mean().unstack(0)
category_traffic.plot(figsize=(12, 6))
plt.title('Média de Tráfego por Categoria ao Longo do Tempo')
plt.xlabel('Data')
plt.ylabel('Média de Tráfego')
plt.legend(title='Categoria')
plt.show()

# Correlação entre categorias e tráfego
plt.figure(figsize=(12, 6))
sns.boxplot(data=app_usage_with_category, x='English Name', y='Traffic')
plt.xticks(rotation=90)
plt.title('Distribuição do Tráfego de Dados por Categoria')
plt.xlabel('Categoria')
plt.ylabel('Tráfego')
plt.show()
