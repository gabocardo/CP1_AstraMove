from mobilidadekit_dados import veiculos, leituras_operacionais, mapa_terreno
from residenciakit_dados import modulos, leituras_ambientais, mapa_base

limites_seguranca = (1000.0, 20.5, 80.0)

# o comando da raw string não quebra o desenho

ARTE_FINAL = r"""
                                 \       |       /          *
             *                     \     |     /
*                                    \   _   /      *
                                      -     -
                   .-_'''-.   ______ /       \ ______
   *             ,'/  (/.' '.        \       /
                /  :  _ /    \        -  _  -
               |    \(_'    ( |      /       \           *
          .-.  |      y __   `|    /     |     \
         {(")}  \     /  _)  /   /       |       \
        o[/_\]o  '.    \/  .'
          |_|      '-....-'                   *
  ...,,...d b...,,,......,,... Astra Move  
"""


def classificar_rover(bateria_pct):
    bateria_minima = limites_seguranca[2]
    if bateria_pct >= bateria_minima:
        return "Rover seguro para operação"
    elif bateria_pct >= 50.0:
        return "ATENÇÃO. Rover em condição de ALERTA"
    else:
        return "ALERTA!!! Rover em condição CRÍTICA!"


def classificar_modulo(modulo_id):
    co2_limite = limites_seguranca[0]
    o2_limite = limites_seguranca[1]

    leituras_modulo = [leitura for leitura in leituras_ambientais if leitura["modulo"] == modulo_id]
    if not leituras_modulo:
        return "Nenhuma leitura disponível para o módulo especificado."

    ultima_leitura = leituras_modulo[-1]

    if ultima_leitura["co2_ppm"] > co2_limite or ultima_leitura["o2_pct"] < o2_limite:
        return f"ALERTA!!! (CO2: {ultima_leitura['co2_ppm']} ppm, O2: {ultima_leitura['o2_pct']}%) - Condição CRÍTICA!"
    else:
        return f"Módulo seguro para operação (CO2: {ultima_leitura['co2_ppm']} ppm, O2: {ultima_leitura['o2_pct']}%)"

# sum() soma os valores e len() conta a quantidade de elementos, usei porque permitem calcular os totais e a média de forma mais simples

def calcular_indicadores_globais():
    total_capacidade = sum(modulo["capacidade"] for modulo in modulos)
    total_ocupacao = sum(modulo["ocupacao"] for modulo in modulos)
    taxa_ocupacao = (total_ocupacao / total_capacidade) * 100 if total_capacidade > 0 else 0

    total_autonomia = sum(veiculo["autonomia_km"] for veiculo in veiculos)
    media_autonomia = total_autonomia / len(veiculos) if veiculos else 0

    vagas_totais = sum(modulo["capacidade"] - modulo["ocupacao"] for modulo in modulos)

    return taxa_ocupacao, media_autonomia, vagas_totais


def analisar_matriz_terreno(matriz):
    seguro = 0
    atencao = 0
    perigoso = 0

    for linha in matriz:
        for celula in linha:
            if celula == 1:
                seguro += 1
            elif celula == 2:
                atencao += 1
            elif celula == 0:
                perigoso += 1
    return seguro, atencao, perigoso


def executar_diagnostico():
    print("================================================================")
    print("       CENTRO DE CONTROLE LUNAR | DIAGNÓSTICO OPERACIONAL       ")
    print("================================================================")

    print("Status dos módulos de residência e habitat")
    modulos_alerta = 0
    for modulo in modulos:
        vagas = modulo["capacidade"] - modulo["ocupacao"]
        status_ambiental = classificar_modulo(modulo["id"])

        if "CRÍTICA" in status_ambiental:
            modulos_alerta += 1
            print(f"ALERTA!!! Módulo {modulo['nome']} em condição CRÍTICA! (Vagas: {vagas})")
    print("\n" + "-" * 66 + "\n")

    print("Status dos rovers e veículos de transporte")
    rovers_aptos = 0
    for veiculo in veiculos:
        status_rover = classificar_rover(veiculo["bateria_pct"])
        if "seguro" in status_rover:
            rovers_aptos += 1
        print(f"Rover {veiculo['modelo']} (Bateria: {veiculo['bateria_pct']}%) - {status_rover}")
    print("\n" + "-" * 66 + "\n")

    seg, atenc, per = analisar_matriz_terreno(mapa_terreno)
    print("Mapeamento do terreno ao redor da base")
    print(f"Seguros: {seg}, Atenção: {atenc}, Perigosos: {per}")
    print("\n" + "-" * 66 + "\n")

    taxa_ocupacao, media_autonomia, vagas_totais = calcular_indicadores_globais()
    print("Indicadores globais da base lunar")
    print(f"Taxa de ocupação da base: {taxa_ocupacao:.1f}%")
    print(f"Média de autonomia dos rovers: {media_autonomia:.2f} km")
    print(f"Vagas totais disponíveis nos módulos: {vagas_totais}")
    print("\n" + "-" * 66 + "\n")

    print("Diagnóstico completo. Encerrando o relatório do Centro de Controle Lunar.")
    if modulos_alerta > 0:
        print(f"ALERTA!!! Existem {modulos_alerta} módulos em condição CRÍTICA. Ação imediata recomendada.")
        print(f"Existem {vagas_totais} vagas disponíveis e {rovers_aptos} rovers APTOS para realocação/resgate.")
        print("Recomendação: Execute o 'Programa 02' para planejar a evacuação dos módulos afetados.")
    else:
        print("Todos os módulos estão operando dentro dos parâmetros de segurança. Nenhuma ação corretiva necessária.")

    print(ARTE_FINAL)

# o programa não estava executando nada no terminal, então coloquei esse comando para chamar a função quando o arquivo é executado (não entendi muito bem mas foi o que funcionou kk)

if __name__ == "__main__":
    executar_diagnostico()
