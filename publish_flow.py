import os
from genesys.archy import Archy
import datetime

org = input('Digite o nome do cliente: ')
archy = Archy(org)
dir = 'flows/'
arquivos = os.listdir(dir)
inicio_t = datetime.datetime.today()
for arquivo in sorted(arquivos):
    flow_file = os.path.abspath(os.path.join(dir, arquivo))
    print(archy.publish_flow_subprocess(flow_file))
fim_t = datetime.datetime.today()
print(f'Qtds de arquivos: {len(arquivos)}\nDemorou: {fim_t-inicio_t}')

