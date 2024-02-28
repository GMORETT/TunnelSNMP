import sys
from snmp import Engine,MessageProcessingModel
from snmp.smi import Integer32,OCTET_STRING,Counter32,Counter64

def returnValueByType(result):
    optionstipo = {
            'Integer32': retornaInteger,
            'Counter32': retornaInteger,
            'Counter64': retornaInteger,
            'OctetString': retornaOctetString
        }
    return optionstipo[result.variables[0].value.__class__.__name__](result)

def retornaInteger(result):
    return result.variables[0].value.value

def retornaOctetString(result):
    return result.variables[0].value.data.decode()

class SNMPfunctions:
    @staticmethod
    def walk(addr: str,community: str,oid: str):
        '''
        Essa função recebe um endereço, uma comunidade e uma OID númerica(arvore)
        retorna uma lista de resultado de um SNMP Walk
        '''
        resultlist = []
        onloop = True
        with Engine(
        defaultVersion=MessageProcessingModel.SNMPv2c,
        defaultCommunity=bytes(community,encoding="utf-8") 
        ) as engine:
            manager = engine.Manager(address=str(addr))
            actualOID = oid
            while onloop:
                result = manager.getNext(actualOID)
                actualOID = str(result.variables[0].name)
                compareOID = actualOID.split('.')[:-1]
                compareOID = ".".join(compareOID)
                if str(compareOID) != str(oid):
                    onloop = False
                else: 
                    resultlist.append((str(result.variables[0].name),returnValueByType(result)))
        return resultlist
    def get(addr,community,oid):
        '''
        Essa função recebe um endereço, uma comunidade e uma OID númerica(arvore+folha)
        retorna um valor
        '''
        with Engine(
        defaultVersion=MessageProcessingModel.SNMPv2c,
        defaultCommunity=bytes(community,encoding="utf-8") 
        ) as engine:
            manager = engine.Manager(address=str(addr))
            result = manager.get(oid)
            return returnValueByType(result)
        
        