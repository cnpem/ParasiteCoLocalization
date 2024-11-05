# %%
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#%%
raw_spots = pd.read_csv("./results/Spots.csv")
raw_nuclei = pd.read_csv("./results/Nuclei.csv")
raw_image = pd.read_csv("./results/Image.csv")
raw_cytoplasm = pd.read_csv("./results/Cytoplasm.csv")
raw_cell = pd.read_csv("./results/Cell.csv")

print(raw_cytoplasm.columns)
print(raw_image.columns)
print(raw_cell.columns)
# %%
def run(
    datadir: str = "./results",
    save_raw_data: bool = False,
    save_as: str = "xlsx",
    verbose: bool = False,
):
    
# %%


# %%


#TODO: scatterplots com diagonal de refeência para cada imágem de:
#TODO: criar metadado compatível do dado 
# TODO: contagem de spots por área
# TODO: selecionar casos discrepantes e analisar qualitativamente






# %%

def infection_rate(filename: str, min_spots: int = 3, plot: bool = False):
    """
    Função para calcular a taxa de infectação a partir de um valor mínimo de spots.

    Parameters
    ----------
    min_spots : int
        Valor mínimo de spots para considerar o estado de infeccão.

    Returns
    -------
    float
        Taxa de infeccão calculada a partir do valor mínimo de spots.
    """
    print("[==> Calculating the infection rate ...")
        
    pass
    if plot:
        _plot_infection_rate()

def _plot_infection_rate(): 
    pass

def spots_per_cell(filename: str):
    pass

def spots_density(filename: str):
    pass

def nuclei_density(filename: str):
    pass

def 


# %%
metadata = ['ImageNumber', 'Metadata_Field', 'Metadata_PlateID']
metadata_df = raw_image[metadata]
print(metadata_df)

# %%

data = raw_image.groupby(['Metadata_PlateID']).agg(
    total_cells=('Count_Nuclei', 'sum'),
    total_spots=('Count_Spots', 'sum')
).reset_index()
left_join = pd.merge(metadata_df, data, on='Metadata_PlateID')


# %% 

# Aqui tem número de células, numero de celulas contaminadas e não contaminadas, numero de spots por celula, média de spots por célula

spots_per_cell = raw_cell.groupby(['ImageNumber', 'ObjectNumber']).agg(
    total_spots=('Children_Spots_Count', 'sum')
).reset_index()


spots_per_cell['is_contaminated'] = spots_per_cell['total_spots'] > 3 # Adicionar uma coluna para classificar as células contaminadas (total_spots > 5)
# %%
results = spots_per_cell.groupby('ImageNumber').agg(
    total_spots=('total_spots', 'sum'),
    median_contaminated=('total_spots', lambda x: x[spots_per_cell.loc[x.index, 'is_contaminated']].median()),
    mean_spots_per_cell=('total_spots', 'mean'),            # Média de spots por celula
    infection_rate=('is_contaminated', 'mean'),            # Taxa de infeccão
    num_cells=('ObjectNumber', 'nunique'),                  # Total de células únicas por imagem
    contaminated_cells=('is_contaminated', 'sum'),          # Células com mais de 5 spots
    #median_spots_per_cell=(('total_spots'), 'median'),       # Mediana de spots por celula
    non_contaminated_cells=('is_contaminated', lambda x: (~x).sum())  # Células com 5 spots ou menos
).reset_index()
results = pd.merge(metadata_df, results, on='ImageNumber')

results_final = results.groupby('Metadata_PlateID').agg(
    total_spots=('total_spots', 'sum'),
    median_contaminated=('median_contaminated', 'median'),
    infection_rate_cellprofiler=('infection_rate', 'mean'),
    total_cells_cellprofiler=('num_cells', 'sum'),
    infected_cells_cellprofiler=('contaminated_cells', 'sum'),
    mean_mean_spots_per_cell=('mean_spots_per_cell', 'mean')
)
print(results_final)

# %%
sns.scatterplot(data=results, x='contaminated_cells', y='non_contaminated_cells', hue='infection_rate')
plt.xlabel("Contaminated Cells")
plt.ylabel("Non Contamined Cells")
plt.title("Number of Cells vs. Contaminated Cells")
plt.show()

sns.scatterplot(data=results_final, x='total_spots', y='infected_cells_cellprofiler', hue='infection_rate_cellprofiler')
plt.xlabel("Total Spots")
plt.ylabel("Number of Cells")
plt.title("Number of Cells vs. Total Spots")
plt.show()
# %%
linhas = 'ABCDEFGHIJKLMNOP'  # 16 letras para as linhas
colunas = 24  # Total de colunas

dicionario_plateID = {}

for i, linha in enumerate(linhas):
    for coluna in range(1, colunas + 1):
        plate_id = 1000 * (i + 1) + coluna  # Calcular o número (1001, 1002, ...)
        poço = f"{linha}{coluna}"  # Definir o código do poço (A1, A2, ...)
        dicionario_plateID[plate_id] = poço  # Adicionar ao dicionário

print(dicionario_plateID)
# %%
columbus = pd.read_csv("columbus.txt", sep = "\t")
columbus_df = columbus[['WellName', 'spots in infected cells (median)', 'infected_cells (N)','Total Cells (N)', 'Infection Rate']]
#print(columbus_df)
# %%
results_final['WellName'] = results_final.index.map(dicionario_plateID)
res = results_final.merge(columbus_df, on='WellName')
print(columbus_df)
print(res)  

# %%
sns.scatterplot(data=res, x='Infection Rate', y='infection_rate_cellprofiler', hue='infected_cells_cellprofiler', )
plt.xlabel("Infection Rate")    
plt.ylabel("CellProfiler Infection Rate")
plt.show() 

sns.scatterplot(data=res, x='Total Cells (N)', y='total_cells_cellprofiler', hue='infection_rate_cellprofiler')
plt.xlabel("Total Cells")
plt.ylabel("CellProfiler Total Cells")
plt.show()

sns.scatterplot(data=res, x='spots in infected cells (median)', y='median_contaminated', hue='infection_rate_cellprofiler')
plt.xlabel("Spots in Infected Cells")
plt.ylabel("Median Contaminated")
plt.show()


