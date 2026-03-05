import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

emendas = pd.read_csv('EmendasParlamentares.csv', encoding='latin1', sep=';')

# excluindo colunas que não serão úteis:
emendas = emendas.drop(["Código da Emenda", "Tipo de Emenda", "Código Município IBGE", "Município", "Nome do Autor da Emenda", "Código do Autor da Emenda", "Número da emenda", "Código Ação", "Código Plano Orçamentário", "Valor Liquidado", "Valor Restos A Pagar Inscritos"], axis=1)
# colunas "Código da Emenda", "Código Município IBGE" e "Município" possuiam muitos campos "Sem informação", foram excluídos porque não serão utilizados

#limpando campos Sem informação
emendas = emendas.replace("Sem informação", np.nan) # substitui os celulas com valor "Sem informação" por vazio
emendas = emendas.dropna() # Exclui toda a linha caso tenha pelo menos um valor vazio

# Substituindo valores "Múltiplos" por "Interestadual" da coluna UF
emendas['UF'] = emendas['UF'].replace("Múltiplo", "Interestadual")

# transformando colunas de texto em numero:
colunas_a_transformar = ["Valor Empenhado", "Valor Pago", "Valor Restos A Pagar Cancelados", "Valor Restos A Pagar Pagos"]

def tranformar_em_int(colunas):
    for coluna in colunas:
        emendas[coluna] = emendas[coluna].astype(str).str.replace(',', '.', regex=False).astype(float)    

tranformar_em_int(colunas_a_transformar)

# definindo o campo Ano da Emenda como string para evitar que o codigo realize operaçoes com ele, prejudicando os graficos
emendas["Ano da Emenda"] = emendas["Ano da Emenda"].astype(str)

# criando medidas:
def calcular_medidas():
    global total_por_uf_bi, total_por_funcao_bi, total_pago_por_ano_bi, gap_empenhado_e_pago

    total_por_uf = emendas.groupby(emendas["UF"]).sum(numeric_only=True).round(2)
    total_por_uf_bi = total_por_uf / 1000000000 # total gasto por bilhao

    total_por_funcao = emendas.groupby(emendas["Nome Função"]).sum(numeric_only=True).round(2)
    total_por_funcao_bi = total_por_funcao / 1000000000 # total gasto por bilhao

    total_por_ano = emendas.groupby(emendas["Ano da Emenda"]).sum(numeric_only=True).round(2)
    total_por_ano_bi = total_por_ano / 1000000000 # total gasto por bilhao
    total_por_ano_bi = total_por_ano_bi.reset_index() # transformando o index em uma coluna

    gap_empenhado_e_pago = total_por_uf_bi[["Valor Empenhado", "Valor Pago"]]

calcular_medidas()

# ordenando e limitando a 10 primeiras linhas
top_10_uf = total_por_uf_bi.sort_values(by='Valor Pago', ascending=False).head(10)

# visual
sns.set_theme(style="whitegrid")
plt.figure(figsize=(12, 6))

grafico = sns.barplot(
    data=top_10_uf, 
    x='Valor Pago', 
    y='UF', 
    hue='UF',  
    palette='viridis',
    legend=False
)

plt.title('Top 10 Estados com Maior Volume de Emendas Pagas', fontsize=16, pad=20) #titulo
plt.xlabel('Valor Total Pago (BI)', fontsize=12) 
plt.ylabel('')

plt.show()
plt.close()

# excluindo o ano 2026 p/ não prejudicar o gráfico (ano vigente)
total_pago_por_ano_bi = total_pago_por_ano_bi.loc[total_pago_por_ano_bi["Ano da Emenda"] != "2026"]

# definindo visual
sns.set_theme(style="whitegrid") 
plt.figure(figsize=(12, 6))

grafico = sns.lineplot(
    data=total_pago_por_ano_bi, 
    x='Ano da Emenda', 
    y='Valor Pago', 
    marker='o', 
    linewidth=2
)

plt.title('Emendas ao longo dos anos', fontsize=16, pad=20)
plt.xlabel('Ano da Emenda', fontsize=12)
plt.ylabel('Valor Pago (BI)', fontsize=12)

plt.show()
plt.close()

# ordenando e coletando somente os top 10
top_10_funcao = total_por_funcao_bi.sort_values(by='Valor Pago', ascending=False).head(10)

# definindo visual
sns.set_theme(style="whitegrid") 
plt.figure(figsize=(12, 6))

grafico = sns.barplot(
    data=top_10_funcao, 
    x='Valor Pago', 
    y='Nome Função', 
    hue="Nome Função",
    palette='viridis',
    legend=False
)

plt.title('Áreas que mais gastaram Emendas', fontsize=16, pad=20)
plt.xlabel('Valor Pago (BI)', fontsize=12)
plt.ylabel('')

plt.show()
plt.close()

# ordenando e filtrando somente os 10 maiores
gap_empenhado_e_pago = gap_empenhado_e_pago.sort_values(by="Valor Empenhado", ascending=False).head(10)

gap_empenhado_e_pago.plot(kind='barh', figsize=(15, 5), color=['#1f77b4', '#ff7f0e'])
plt.title('Diferença entre Valor Empenhado x Valor Pago por UF')
plt.xlabel('Bilhões')
plt.ylabel('')
plt.show()
plt.close()

# criando a coluna eficiencia, que mostra a porcentagem de valor empenhado que foi pago
emendas.loc[:, "Eficiência"] = emendas["Valor Pago"] / emendas["Valor Empenhado"] * 100

estados_eficientes = emendas.loc[emendas["UF"] != "Interestadual", "Eficiência"] # excluindo os estados "Interestadual"
estados_eficientes = estados_eficientes.groupby(emendas["UF"]).mean(numeric_only=True).sort_values(ascending=False) 

estados_eficientes = estados_eficientes.head(10) # coletando somente os 10 estados mais eficientes

estados_eficientes.plot(kind='barh', figsize=(18, 6), color=["#061c9c","#374cc5"])
plt.title('Estados mais Eficientes')
plt.xlabel("Eficiência (%)")
plt.ylabel('')
plt.show()