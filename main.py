import math
import random

import matplotlib.pyplot as plt
import numpy as np


def gerar_ordenadas(dimensao, quantidade):
    coordenadas = set()
    while len(coordenadas) < quantidade:
        x = random.randint(0, dimensao - 1)
        y = random.randint(0, dimensao - 1)
        coordenadas.add((x, y))
    return list(coordenadas)


def calcular_distancia(ponto1, ponto2):
    return np.linalg.norm(np.array(ponto1) - np.array(ponto2))


def calcular_distancia_total(rota, pontos_entrega):
    distancia_total = 0
    for i in range(len(rota) - 1):
        distancia_total += calcular_distancia(
            pontos_entrega[rota[i]], pontos_entrega[rota[i + 1]]
        )
    distancia_total += calcular_distancia(
        pontos_entrega[rota[-1]], pontos_entrega[rota[0]]
    )
    return distancia_total


def simulated_annealing(pontos_entrega, temperatura_inicial, resfriamento, iteracoes):
    rota_atual = list(range(len(pontos_entrega)))
    random.shuffle(rota_atual)
    melhor_rota = rota_atual[:]
    menor_distancia = calcular_distancia_total(melhor_rota, pontos_entrega)

    temperatura = temperatura_inicial

    for i in range(iteracoes):
        nova_rota = rota_atual[:]
        a, b = random.sample(range(len(nova_rota)), 2)
        nova_rota[a], nova_rota[b] = nova_rota[b], nova_rota[a]

        nova_distancia = calcular_distancia_total(nova_rota, pontos_entrega)

        delta_e = nova_distancia - calcular_distancia_total(rota_atual, pontos_entrega)

        if delta_e < 0 or random.uniform(0, 1) < math.exp(-delta_e / temperatura):
            rota_atual = nova_rota[:]
            if nova_distancia < menor_distancia:
                melhor_rota = nova_rota[:]
                menor_distancia = nova_distancia

        temperatura *= resfriamento

    return melhor_rota, menor_distancia


def plotar_rota(pontos_entrega, rota):
    plt.figure(figsize=(8, 6))
    for ponto in pontos_entrega:
        plt.scatter(ponto[0], ponto[1], c="blue")

    for i in range(len(rota) - 1):
        ponto_atual = pontos_entrega[rota[i]]
        proximo_ponto = pontos_entrega[rota[i + 1]]
        plt.plot(
            [ponto_atual[0], proximo_ponto[0]], [ponto_atual[1], proximo_ponto[1]], "k-"
        )

    ponto_atual = pontos_entrega[rota[-1]]
    proximo_ponto = pontos_entrega[rota[0]]
    plt.plot(
        [ponto_atual[0], proximo_ponto[0]], [ponto_atual[1], proximo_ponto[1]], "k-"
    )

    plt.title("Rota de Entrega dos Drones")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.show()


pontos_entrega = gerar_ordenadas(150, 200)

melhor_rota, menor_distancia = simulated_annealing(
    pontos_entrega, temperatura_inicial=1000, resfriamento=0.99, iteracoes=10000
)

print("Melhor rota:", melhor_rota)
print("Menor distância:", menor_distancia)

plotar_rota(pontos_entrega, melhor_rota)
