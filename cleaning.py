import pandas as pd
import numpy as np

def carregar_e_limpar():
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