import os
from time import sleep
from genesys.archy import Archy

caminho = r'flows/'

if True:
    for fluxo in os.listdir(caminho):
        os.remove(caminho + fluxo)

org = input('Digite o nome do cliente: ')
archy = Archy(org)

def export_flow(flow_name: str, flow_type: str, dict_flows: dict) -> dict:
    dados_flow_entities = archy.api.get_flows(flow_name_or_description=flow_name, type_flow=flow_type)
    dados_flow = dados_flow_entities.entities[0]
    flow_name = dados_flow.name
    flow_type = dados_flow.type.lower()
    flow_version = dados_flow.publishedVersion.id
    result = archy.export_flow_subprocess(flow_name=flow_name, flow_type=flow_type, flow_version=flow_version, output_dir=caminho)
    if result[0]['exit code'] != '0' or result[2] is None:
        print(result)
        exit()
    dict_flows[flow_name] = result[2]
    return dict_flows


def export_flows(flows_dependencies: list, dict_flows:dict={}) -> dict:
    if flows_dependencies:
        while True:
            os.system('cls')
            tipos = [f'{index} - {flow_name}: {flow_type}' for index, (flow_name, flow_type) in enumerate(flows_dependencies)]
            entrada_index_flow = input(f'Digite o indice do fluxo que você quer exportar: \n{'\n'.join(tipos)}\n{len(flows_dependencies)} - Sair\nOpção: ')          
            index_flow = int(entrada_index_flow) if entrada_index_flow.isdigit() else -2
            if index_flow == len(flows_dependencies):
                break
            if index_flow < 0 or index_flow >= len(flows_dependencies):
                print('Opção inválida, tente denovo')
                sleep(3)
                continue 
            dict_flows = export_flow(flows_dependencies[index_flow][0], flows_dependencies[index_flow][1], dict_flows)
            if dict_flows[flows_dependencies[index_flow][0]].flow is not None:
                dependencies = dict_flows[flows_dependencies[index_flow][0]].flow.get_dependencies('flows')
                flows_dependencies.extend([(flow_name, flow_type) for flow_name, flow_type in dependencies if flow_name not in dict_flows.keys() and (flow_name, flow_type) not in flows_dependencies])
            flows_dependencies.pop(index_flow)
            if not flows_dependencies:
                break  

    return dict_flows


"""
Pesquisar FLOW

ID:
flow_id = 'a85ea029-89cb-4b44-8e78-6a6fbaa264ed'
dados_flow = archy.api.architect_api.get_flow(flow_id)

NAME:
name = 'PRD_IVR_ClubeSaude_v29_Modulo1_Fluxo_Inicial'
dados_flow = archy.api.architect_api.get_flows(name=name)

IVR_JIRA:
description = 'IVR-206469'
dados_flow = archy.api.architect_api.get_flows(description=description)

IVRS:
recipient_objects = api.routing_api.get_routing_message_recipients(page_size=50)
ivr_objects = archy.api.architect_api.get_architect_ivrs()

"""
if False:
    recipient_objects = archy.api.get_recipients_routing(page_size=50)
    list_flows = []
    for recipient in recipient_objects.entities:
        flow_id = recipient.flow.id
        dados_flow = archy.api.get_flow_by_id(flow_id)
        flow_name = dados_flow.name
        flow_type = dados_flow.type.lower()
        list_flows.append((flow_name, flow_type))

    flows_names = export_flows(list_flows)
    exit()

name_flow = 'PRD_IVR_Reservas_V8_Modulo1' 
type_flow = 'inboundCall'
flows = archy.api.get_flows(flow_name_or_description=name_flow, type_flow=type_flow).entities
list_flows = [(flow_name.name, flow_name.type.lower()) for flow_name in flows]
print(f'EXPORTANDO {len(list_flows)} FLUXOS')
print('\n'.join([f'{flow_name} - {flow_type}' for flow_name, flow_type in list_flows]))
flows_names = export_flows(list_flows)