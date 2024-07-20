import os
from genesys.archy import Archy, FileYaml
from genesys.thread import Thread
import datetime

org = input('Digite o nome do cliente: ')
archy = Archy(org)
dir = 'flows/'
arquivos = os.listdir(dir)
resultados, threads = [], []
inicio_t = datetime.datetime.today()

for arquivo in sorted(arquivos):
    flow_file = os.path.abspath(os.path.join(dir, arquivo))
    file = FileYaml(flow_file)
    print(file)
    #if archy.api.get_flows(flow_name_or_description=file.flow.name, type_flow=file.flow_type):
    #    continue
    t = Thread(name=arquivo, funcao=archy.publish_flow_empty_subprocess, args=(file.flow.name,), daemon=True)
    threads.append(t)
    t.start()

for t in threads:
    t.join()
    tupla = t.get_resultado()
    if tupla[0].get('exit code','-1') != '0':
        raise Exception(f'Ocorreu um erro na função(publish_flow_subprocess): {tupla=}')
    resultados.append(tupla)
fim_t = datetime.datetime.today()
print("Resultados:", resultados)

print(f'Qtds de arquivos: {len(arquivos)}\nDemorou: {fim_t-inicio_t}')

for arquivo in sorted(arquivos):
    flow_file = os.path.abspath(os.path.join(dir, arquivo))
    t = Thread(name=arquivo, funcao=archy.publish_flow_subprocess, args=(flow_file,), daemon=True)
    threads.append(t)
    t.start()

for t in threads:
    t.join()
    tupla = t.get_resultado()
    if tupla[0].get('exit code','-1') != '0':
        raise Exception(f'Ocorreu um erro na função(publish_flow_subprocess): {tupla=}')
    resultados.append(tupla)
fim_t = datetime.datetime.today()
print("Resultados:", resultados)

print(f'Qtds de arquivos: {len(arquivos)}\nDemorou: {fim_t-inicio_t}')

"""
org = input('Digite o nome do cliente: ')
archy = Archy(org)
dir = 'flows/'
arquivos = os.listdir(dir)
threads = []
for arquivo in sorted(arquivos):
    flow_file = os.path.abspath(os.path.join(dir, arquivo))
    t = thread.Thread(name=arquivo, funcao=archy.publish_flow, args=(flow_file,), daemon=True)
    threads.append(t)
    t.start()

resultados = []
for t in threads:
    t.join()
    resultados.append(t.get_resultado())

print("Resultados:", resultados)

"""