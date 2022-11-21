import scrapy
import csv
from deputados.spiders.collector import *

class DeputadosSpider(scrapy.Spider):
  name = "deputados"

  def start_requests(self):
    
    colunas = [
      'nome', 'genero', 'presenca_plenario', 'ausencia_justificada_plenario',
      'ausencia_nao_justificada_plenario', 'presenca_comissao',
      'ausencia_justificada_comissao', 'ausencia_nao_justificada_comissao', 
      'data_nascimento', 'quant_viagem', 'salario_bruto',
      'gasto_total_par', 'gasto_total_gab', 'gasto_jan_par', 'gasto_fev_par',
      'gasto_mar_par', 'gasto_abr_par', 'gasto_maio_par', 'gasto_junho_par',
      'gasto_jul_par', 'gasto_agosto_par', 'gasto_set_par', 'gasto_out_par',
      'gasto_nov_par', 'gasto_jan_gab', 'gasto_fev_gab', 'gasto_mar_gab', 'gasto_abr_gab', 
      'gasto_maio_gab', 'gasto_junho_gab', 'gasto_jul_gab', 'gasto_agosto_gab', 'gasto_set_gab', 
      'gasto_out_gab', 'gasto_nov_gab'
    ]
    
    with open('data_H.csv', 'w') as file:
      writer = csv.writer(file)
      writer.writerow(colunas)
      
    with open('data_M.csv', 'w') as file:
      writer = csv.writer(file)
      writer.writerow(colunas)
      
    with open('lista_deputados_string_list.txt') as f:
      urls = f.readlines()
      urls = list(map(lambda x: x.replace("\n", "").replace(",", "").replace('"', ""), urls))
      for url in urls:
        yield scrapy.Request(url=url, callback=lambda res: self.parse(res, "H"))

    with open('lista_deputadas_string_list.txt') as f:
      urls = f.readlines()
      urls = list(map(lambda x: x.replace("\n", "").replace(",", "").replace('"', ""), urls))
      for url in urls:
        yield scrapy.Request(url=url, callback=lambda res: self.parse(res, "M"))

  def parse(self, response, genero):
    info_dep = []

    # nome
    dep_nome = get_nome(response)

    # presenca
    presenca = get_presenca(response)

    # data de nascimento
    nascimento = get_nascimento(response)

    # gasto total parlamento e gabinete

    gasto_total_parlamentar = get_gasto_total_parlamento(response)
    gasto_total_gabinete = get_gasto_total_gabinete(response)

    # quantidade de viagens
    quant_viagem = get_quant_viagens(response)

    # salario bruto
    salario_bruto = get_salario_bruto(response)

    # gastos mensais
    gastos_mensais = get_salario_mensal(response)

    info_dep += [dep_nome]
    info_dep += [genero]
    info_dep += presenca
    info_dep += [nascimento]
    info_dep += [quant_viagem]
    info_dep += [salario_bruto]
    info_dep += [gasto_total_parlamentar]
    info_dep += [gasto_total_gabinete]
    info_dep += gastos_mensais

    colunas = [
      'nome', 'genero', 'presenca_plenario', 'ausencia_justificada_plenario',
      'ausencia_nao_justificada_plenario', 'presenca_comissao',
      'ausencia_justificada_comissao', 'ausencia_nao_justificada_comissao', 
      'data_nascimento', 'quant_viagem', 'salario_bruto',
      'gasto_total_par', 'gasto_total_gab', 'gasto_jan_par', 'gasto_fev_par',
      'gasto_mar_par', 'gasto_abr_par', 'gasto_maio_par', 'gasto_junho_par',
      'gasto_jul_par', 'gasto_agosto_par', 'gasto_set_par', 'gasto_out_par',
      'gasto_nov_par', 'gasto_jan_gab', 'gasto_fev_gab', 'gasto_mar_gab', 'gasto_abr_gab', 
      'gasto_maio_gab', 'gasto_junho_gab', 'gasto_jul_gab', 'gasto_agosto_gab', 'gasto_set_gab', 
      'gasto_out_gab', 'gasto_nov_gab'
    ]
    
    if (len(info_dep) != len(colunas)):
      print(len(info_dep), len(colunas))
      print(len(gastos_mensais))

    
    with open(f'data_{genero}.csv', 'a') as file:
        writer = csv.writer(file)
        writer.writerow(info_dep)