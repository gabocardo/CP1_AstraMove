from mobilidadekit_dados import veiculos, rotas, cargas, pontos_interesse, mapa_terreno
from residenciakit_dados import modulos, leituras_ambientais, mapa_base

condicoes_missao = ("Capacidade", "Autonomia", "Risco")
condicao1, condicao2, condicao3 = condicoes_missao

def mostrar_veiculos():
    print("\n===== ROVERS =====")

    for i, veiculo in enumerate(veiculos):
        print(
            i + 1,
            "-",
            veiculo["id"],
            "|",
            veiculo["modelo"],
            "| Capacidade:",
            veiculo["capacidade_kg"],
            "kg | Autonomia:",
            veiculo["autonomia_km"],
            "km"
        )




def mostrar_cargas():
    print("\n===== CARGAS =====")

    for i, carga in enumerate(cargas):
        print(
            i + 1,
            "-",
            carga["id"],
            "|",
            carga["tipo"],
            "|",
            carga["massa_kg"],
            "kg"
        )




def mostrar_rotas():
    print("\n===== ROTAS =====")

    for i, rota in enumerate(rotas):
        print(
            i + 1,
            "-",
            rota["id"],
            "|",
            rota["origem"],
            "->",
            rota["destino"],
            "|",
            rota["distancia_km"],
            "km | Risco:",
            rota["risco"]
        )




print("=" * 50)
print("     SIMULADOR DE OPERAÇÃO LUNAR")
print("=" * 50)




mostrar_veiculos()

opcao_rover = int(input("\nEscolha o rover: "))

rover = veiculos[opcao_rover - 1]




mostrar_cargas()

opcao_carga = int(input("\nEscolha a carga: "))

carga = cargas[opcao_carga - 1]




mostrar_rotas()

opcao_rota = int(input("\nEscolha a rota: "))

rota = rotas[opcao_rota - 1]




distancia_total = rota["distancia_km"] * 2

tempo = distancia_total / rover["velocidade_kmh"]




capacidade_ok = carga["massa_kg"] <= rover["capacidade_kg"]

autonomia_ok = distancia_total <= rover["autonomia_km"]




if capacidade_ok and autonomia_ok:

    if rota["risco"] == "alto":
        resultado = "MISSÃO AUTORIZADA COM RESTRIÇÕES"
        recomendacao = "A missão é possível, mas a rota possui risco alto."
        condicoes_missao = condicao3

    elif rota["risco"] == "medio":
        resultado = "MISSÃO AUTORIZADA COM RESTRIÇÕES"
        recomendacao = "A missão é possível, mas exige atenção à rota."
        condicoes_missao = condicao1

    else:
        resultado = "MISSÃO AUTORIZADA"
        recomendacao = "O rover possui capacidade e autonomia suficientes."
        condicoes_missao = condicao2
else:

    resultado = "MISSÃO NEGADA"

    if not capacidade_ok:
        recomendacao = "A carga ultrapassa a capacidade do rover."
        condicoes_missao = condicao3

    else:
        recomendacao = "A autonomia do rover não é suficiente."
        condicoes_missao = condicao3




print("\n")
print("=" * 50)
print("          RESULTADO DA SIMULAÇÃO")
print("=" * 50)

print("Rover:", rover["id"], "-", rover["modelo"])
print("Carga:", carga["tipo"])
print("Massa da carga:", carga["massa_kg"], "kg")
print("Capacidade do rover:", rover["capacidade_kg"], "kg")

print("\nRota:", rota["id"])
print("Destino:", rota["destino"])
print("Distância de ida:", rota["distancia_km"], "km")
print("Distância total:", distancia_total, "km")

print("Autonomia:", rover["autonomia_km"], "km")
print("Bateria:", rover["bateria_pct"], "%")
print("Risco:", rota["risco"])

print("Tempo estimado:", round(tempo, 2), "horas")




print("\nCoordenada da Base Alpha:",
      pontos_interesse[0]["coordenada"])

print("Posição inicial do mapa:",
      mapa_terreno[0][0])


print("\nRESULTADO:", resultado)
print("RECOMENDAÇÃO:", recomendacao)
print("CONDIÇÕES AVALIADAS:", condicoes_missao)
print("=" * 50)
