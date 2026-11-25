import json


class Producto:
    def __init__(self, id_prod, nombre, categoria, pieles, precio):
        self.id = id_prod
        self.nombre = nombre
        self.categoria = categoria
        self.pieles = pieles
        self.precio = precio

    def es_compatible(self, tipo_piel):
        return tipo_piel.lower().strip() in self.pieles

    def a_diccionario(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "categoria": self.categoria,
            "pieles": self.pieles,
            "precio": self.precio,
        }


class CarritoEventoEspecial:
    PRIORIDAD = ["Limpieza", "Hidratacion", "Proteccion_solar", "Serum", "Complementario", "Accesorio"]

    def __init__(self, tipo_piel, presupuesto):
        self.tipo_piel = tipo_piel.lower().strip()
        self.presupuesto = presupuesto
        self.items = []

    def total(self):
        return sum(item.precio for item in self.items)

    def puede_agregar(self, producto):
        ids_actuales = {item.id for item in self.items}
        return (
            producto.es_compatible(self.tipo_piel)
            and producto.id not in ids_actuales
            and self.total() + producto.precio <= self.presupuesto
        )

    def armar_automatico(self, productos):
        self.items = []
        for categoria in self.PRIORIDAD:
            candidatos = sorted(
                [p for p in productos if p.categoria == categoria and p.es_compatible(self.tipo_piel)],
                key=lambda x: x.precio,
            )
            for prod in candidatos:
                if self.puede_agregar(prod):
                    self.items.append(prod)
                    break

        restantes = sorted(
            [p for p in productos if p.es_compatible(self.tipo_piel)],
            key=lambda x: x.precio,
        )
        for prod in restantes:
            if self.puede_agregar(prod):
                self.items.append(prod)

        return [item.a_diccionario() for item in self.items], self.total()


def ejecutar_poo(ruta_json, tipo_piel, presupuesto):
    with open(ruta_json, "r", encoding="utf-8") as f:
        datos = json.load(f)
    productos = [Producto(d["id"], d["nombre"], d["categoria"], d["pieles"], d["precio"]) for d in datos]
    carrito = CarritoEventoEspecial(tipo_piel, presupuesto)
    return carrito.armar_automatico(productos)