import os
from genesys.archy import Archy

caminho = r'flows/'

if True:
    for fluxo in os.listdir(caminho):
        os.remove(caminho + fluxo)

org = input('Digite o nome do cliente: ')
archy = Archy(org)


def export_flows(flows_names: list, dict_flows:dict={}) -> dict:
    for flow_name, flow_type in flows_names:
        if flow_name in dict_flows.keys():
            continue         
        dados_flow_entities = archy.api.get_flows(flow_name_or_description=flow_name, type_flow=flow_type)
        dados_flow = dados_flow_entities.entities[0]
        flow_name = dados_flow.name
        flow_type = dados_flow.type.lower()
        flow_version = dados_flow.publishedVersion.id
        result = archy.export_flow_subprocess(flow_name=flow_name, flow_type=flow_type, flow_version=flow_version, output_dir=caminho)
        if result[0]['exit code'] != '0' or result[2] is None:
            print(result)
            continue
        dict_flows[flow_name] = result[2]
        if dict_flows[flow_name].flow is not None:
            dependencies = dict_flows[flow_name].flow.get_dependencies('flows')
            flows_dependencies = [(flow_name, flow_type) for flow_name, flow_type in dependencies if flow_name not in dict_flows.keys() and flow_name not in flows_names]
            if flows_dependencies:
                dict_flows = export_flows(flows_dependencies, dict_flows)  

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

name_flow = 'PRD_IVR_Reservas_V8_Modulo' 
type_flow = 'inboundCall'
recipient_objects = archy.api.get_recipients_routing(page_size=50)
list_flows_names = []
for recipient in recipient_objects.entities:
    flow_id = recipient.flow.id
    dados_flow = archy.api.get_flow_by_id(flow_id)
    flow_name = dados_flow.name
    flow_type = dados_flow.type.lower()
    list_flows_names.append((flow_name, flow_type))

flows_names = export_flows(list_flows_names)
exit()

list_flows_names = [(flow_name.name, flow_name.type) for flow_name in archy.api.get_flows(flow_name_or_description=name_flow, type_flow=type_flow).entities]
flows_names = export_flows(list_flows_names)