import cleaning as clean
import visualization as visu

emendas = clean.carregar_e_limpar()

visu.top_10_uf(emendas)
visu.total_por_ano(emendas)
visu.top_10_funcao(emendas)
visu.empenhado_e_pago(emendas)
visu.top_10_eficientes(emendas)
