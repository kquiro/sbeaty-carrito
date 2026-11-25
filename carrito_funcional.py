import json
from functools import reduce

PRIORIDAD = ("Limpieza", "Hidratacion", "Proteccion_solar", "Serum", "Complementario", "Accesorio")


def cargar_catalogo_inmutable(ruta="productos.json"):
    with open(ruta, "r", encoding="utf-8") as f:
        datos = json.load(f)
    return tuple(
        {
            "id": d["id"],
            "nombre": d["nombre"],
            "categoria": d["categoria"],
            "pieles": tuple(d["pieles"]),
            "precio": d["precio"],
        }
        for d in datos
    )


def total_funcional(carrito):
    return reduce(lambda acc, item: acc + item["precio"], carrito, 0)


def seleccionar_por_categoria(catalogo, tipo_piel, presupuesto):
    piel = tipo_piel.lower().strip()

    def paso_categoria(estado, categoria):
        seleccionados, acumulado = estado
        compatibles = sorted(
            filter(lambda p: p["categoria"] == categoria and piel in p["pieles"], catalogo),
            key=lambda p: p["precio"],
        )
        elegido = next(filter(lambda p: acumulado + p["precio"] <= presupuesto, compatibles), None)
        if elegido:
            return (seleccionados + (elegido,), acumulado + elegido["precio"])
        return (seleccionados, acumulado)

    return reduce(paso_categoria, PRIORIDAD, ((), 0))


def completar_restantes(catalogo, seleccion_inicial, acumulado_inicial, tipo_piel, presupuesto):
    piel = tipo_piel.lower().strip()
    ids_usados = frozenset(map(lambda p: p["id"], seleccion_inicial))
    restantes = sorted(
        filter(lambda p: piel in p["pieles"] and p["id"] not in ids_usados, catalogo),
        key=lambda p: p["precio"],
    )

    def agregar_si_cabe(estado, prod):
        items, total = estado
        if total + prod["precio"] <= presupuesto:
            return (items + (prod,), total + prod["precio"])
        return (items, total)

    return reduce(agregar_si_cabe, restantes, (seleccion_inicial, acumulado_inicial))


def ejecutar_funcional(ruta_json, tipo_piel, presupuesto):
    catalogo = cargar_catalogo_inmutable(ruta_json)
    base, total_base = seleccionar_por_categoria(catalogo, tipo_piel, presupuesto)
    final, total_final = completar_restantes(catalogo, base, total_base, tipo_piel, presupuesto)
    return list(final), total_final