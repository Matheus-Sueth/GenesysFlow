import os
from genesys.archy import FileYaml, Genesys
from collections import defaultdict
import json

org = input('Digite o nome do cliente: ')
api = Genesys(org)
dir = 'flows/'
arquivos = os.listdir(dir)
flows = defaultdict(FileYaml)
for arquivo in arquivos:
    file = FileYaml(os.path.abspath(os.path.join(dir, arquivo)))
    flow_name = file.flow.name
    if flow_name in flows.keys():
        continue
    flows[flow_name] = file

flow_name_final = list(flows.keys())[0]
index_letter_v = flow_name_final.find('_V') + 1
assert index_letter_v != -1 and index_letter_v != 0
#flow_name_search = 'PRD' + flow_name_final[3:index_letter_v+1]

flow_name_search = 'HML' + flow_name_final[3:index_letter_v+1] if 'PRD' == flow_name_final[:3] else 'PRD' + flow_name_final[3:index_letter_v+1]
#flow_name_search = 'PRD' + flow_name_final[3:index_letter_v+1]
version_final = api.get_version_last_flow_by_name(flow_name_search)
new_flow_name = f'{flow_name_search}{version_final+1}'
old_flow_name = flow_name_final[:flow_name_final.find('_', index_letter_v)]
new_description = input('Cole a nova descrição: ') #f"testes_{version_final}"#
old_description = flows[flow_name].flow.description

with open('apis.json') as file:
    data = json.loads(file.read())

for flow_name, file_flow in flows.items():
    if False:
        actions_dependencies = file_flow.flow.get_dependencies('data_actions')
        for category, variable_old in actions_dependencies:
            actions_search = [dado for dado in data if variable_old in dado and dado[0] != dado[1]]
            if actions_search:
                action = actions_search[0]
                variable_new = action[0] if action.index(variable_old) == 1 else action[1]
                file_flow.trocar_dados(variable_old, variable_new)
            if 'Qualicorp' in flow_name:
                if 'QLCP_e_CS_Bearer_Token_prd_20220810' == category:
                    file_flow.trocar_dados('QLCP_e_CS_Bearer_Token_prd_20220810', 'QLCP_e_CS_Bearer_Token_hml_20220810')
                if 'QLCP_e_CS_Bearer_Token_hml_20220810' == category:
                    file_flow.trocar_dados('QLCP_e_CS_Bearer_Token_hml_20220810', 'QLCP_e_CS_Bearer_Token_prd_20220810')
    
    file_flow.trocar_dados(old_flow_name, new_flow_name)
    file_flow.trocar_dados(old_description, new_description)
    file_flow = file_flow.save_yaml_to_file()
    