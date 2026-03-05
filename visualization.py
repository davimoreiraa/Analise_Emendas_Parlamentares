import seaborn as sns
import matplotlib.pyplot as plt

def top_10_uf(emendas):
    total_por_uf = emendas.groupby(emendas["UF"]).sum(numeric_only=True).round(2)
    # ordenando e limitando a 10 primeiras linhas
    top_10_uf = total_por_uf.sort_values(by='Valor Pago', ascending=False).head(10)

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

def total_por_ano(emendas):
    total_por_ano = emendas.groupby(emendas["Ano da Emenda"]).sum(numeric_only=True).round(2)
    total_por_ano = total_por_ano.reset_index() # transformando o index em uma coluna
    total_por_ano = total_por_ano.loc[total_por_ano["Ano da Emenda"] != "2026"] # excluindo o ano 2026 p/ não prejudicar o gráfico (ano vigente)

    # definindo visual
    sns.set_theme(style="whitegrid") 
    plt.figure(figsize=(12, 6))

    grafico = sns.lineplot(
        data=total_por_ano, 
        x='Ano da Emenda', 
        y='Valor Pago', 
        marker='o', 
        linewidth=2
    )

    plt.title('Emendas ao longo dos anos', fontsize=16, pad=20)
    plt.xlabel('', fontsize=12)
    plt.ylabel('Valor Pago (BI)', fontsize=12)

    plt.show()
    plt.close()

def top_10_funcao(emendas):
    total_por_funcao = emendas.groupby(emendas["Nome Função"]).sum(numeric_only=True).round(2)
    top_10_funcao = total_por_funcao.sort_values(by='Valor Pago', ascending=False).head(10)# ordenando e coletando somente os top 10

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

def empenhado_e_pago(emendas):
    total_por_uf = emendas.groupby(emendas["UF"]).sum(numeric_only=True).round(2)
    gap_empenhado_e_pago = total_por_uf[["Valor Empenhado", "Valor Pago"]]
    # ordenando e filtrando somente os 10 maiores
    gap_empenhado_e_pago = gap_empenhado_e_pago.sort_values(by="Valor Empenhado", ascending=False).head(10)

    gap_empenhado_e_pago.plot(kind='barh', figsize=(15, 5), color=['#1f77b4', '#ff7f0e'])
    plt.title('Diferença entre Valor Empenhado x Valor Pago por UF')
    plt.xlabel('Bilhões')
    plt.ylabel('')
    plt.show()
    plt.close()
    
def top_10_eficientes(emendas):
    # criando a coluna eficiencia, que mostra a porcentagem de valor empenhado que foi pago
    emendas.loc[:, "Eficiência"] = emendas["Valor Pago"] / emendas["Valor Empenhado"] * 100

    estados_eficientes = emendas.loc[emendas["UF"] != "Interestadual", "Eficiência"] # excluindo os estados "Interestadual"
    estados_eficientes = estados_eficientes.groupby(emendas["UF"]).mean(numeric_only=True).sort_values(ascending=False) 

    estados_eficientes = estados_eficientes.head(10) # coletando somente os 10 estados mais eficientes

    estados_eficientes.plot(kind='barh', figsize=(18, 7), color=["#3b55e4","#2c7fb8"])
    plt.title('Estados mais Eficientes')
    plt.xlabel("Eficiência (%)")
    plt.ylabel('')
    plt.show()
    plt.close()
