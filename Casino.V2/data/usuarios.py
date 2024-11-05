class Usuario:
    def __init__(self, nombre, saldo_local=1000, saldo_multi=1000):
        self.nombre = nombre
        self.saldo_local = saldo_local
        self.saldo_multi = saldo_multi
        self.inventario_local = []
        self.inventario_multi = []

    def agregar_item_local(self, item):
        self.inventario_local.append(item)

    def agregar_item_multi(self, item):
        self.inventario_multi.append(item)

    def remover_item_local(self, item):
        if item in self.inventario_local:
            self.inventario_local.remove(item)
            return True
        return False

    def remover_item_multi(self, item):
        if item in self.inventario_multi:
            self.inventario_multi.remove(item)
            return True
        return False

    def actualizar_saldo_local(self, cantidad):
        self.saldo_local += cantidad

    def actualizar_saldo_multi(self, cantidad):
        self.saldo_multi += cantidad

    def obtener_saldo_local(self):
        return self.saldo_local

    def obtener_saldo_multi(self):
        return self.saldo_multi

    def obtener_inventario_local(self):
        return self.inventario_local

    def obtener_inventario_multi(self):
        return self.inventario_multi

    def to_dict(self):
        return {
            'nombre': self.nombre,
            'saldo_local': self.saldo_local,
            'saldo_multi': self.saldo_multi,
            'inventario_local': self.inventario_local,
            'inventario_multi': self.inventario_multi
        }

    @classmethod
    def from_dict(cls, data):
        usuario = cls(data['nombre'])
        usuario.saldo_local = data['saldo_local']
        usuario.saldo_multi = data['saldo_multi']
        usuario.inventario_local = data['inventario_local']
        usuario.inventario_multi = data['inventario_multi']
        return usuario