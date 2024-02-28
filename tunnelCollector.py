#!/usr/bin/python3.6
from snmp import Engine,MessageProcessingModel
from lib.snmpFunctions import SNMPfunctions
import sys
import os

ifDescrOID = '1.3.6.1.2.1.2.2.1.2'
ifTypeOID = '1.3.6.1.2.1.2.2.1.3'
ifAliasOID = '1.3.6.1.2.1.31.1.1.1.18'
ifNameOID = '1.3.6.1.2.1.31.1.1.1.1'
tunnelnumero = [131, 150]
tunnelstring = {
    131: 'Common Tunnel',
    150: 'MPLS Tunnel'
}

def main(args):
    resultfinal = []
    address = args[1]
    community = args[2]
    resultlist = SNMPfunctions.walk(address,community,ifTypeOID)
    filtrados = [tupla for tupla in resultlist if tupla[-1] in tunnelnumero]
    for tupla_atual in filtrados:
        numero_folha = int(tupla_atual[0].split('.')[-1])
        description = SNMPfunctions.get(address, community, ifDescrOID +'.'+ str(numero_folha))
        alias = SNMPfunctions.get(address, community, ifAliasOID +'.'+ str(numero_folha))
        type = SNMPfunctions.get(address, community, ifTypeOID +'.'+ str(numero_folha))
        resultfinal.append(':'.join([description, alias, tunnelstring[type]]))
    print('\n'.join(resultfinal))

if __name__ == '__main__':
    if len(sys.argv[-2:]) == 2:
        main(sys.argv)
        os._exit(os.EX_OK)




