import json


def cargar_catalogo(ruta="productos.json"):
    with open(ruta, "r", encoding="utf-8") as archivo:
        return json.load(archivo)


def calcular_total(carrito):
    total = 0
    for item in carrito:
        total += item["precio"]
    return total


def armar_carrito_imperativo(catalogo, tipo_piel, presupuesto):
    tipo_piel = tipo_piel.lower().strip()
    prioridad = ["Limpieza", "Hidratacion", "Proteccion_solar", "Serum", "Complementario", "Accesorio"]
    carrito = []
    total = 0

    for categoria in prioridad:
        candidatos = []
        for prod in catalogo:
            if prod["categoria"] == categoria and tipo_piel in prod["pieles"]:
                candidatos.append(prod)

        for i in range(len(candidatos)):
            for j in range(i + 1, len(candidatos)):
                if candidatos[j]["precio"] < candidatos[i]["precio"]:
                    aux = candidatos[i]
                    candidatos[i] = candidatos[j]
                    candidatos[j] = aux

        for prod in candidatos:
            if total + prod["precio"] <= presupuesto:
                carrito.append(prod)
                total += prod["precio"]
                break

    ids_usados = [p["id"] for p in carrito]
    restantes = []
    for prod in catalogo:
        if tipo_piel in prod["pieles"] and prod["id"] not in ids_usados:
            restantes.append(prod)

    for i in range(len(restantes)):
        for j in range(i + 1, len(restantes)):
            if restantes[j]["precio"] < restantes[i]["precio"]:
                aux = restantes[i]
                restantes[i] = restantes[j]
                restantes[j] = aux

    for prod in restantes:
        if total + prod["precio"] <= presupuesto:
            carrito.append(prod)
            total += prod["precio"]

    return carrito, total