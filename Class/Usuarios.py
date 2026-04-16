from Utils.tools import Tools
from Utils.querys import Querys

class Usuarios:
    def __init__(self, db):
        self.tools  = Tools()
        self.querys = Querys(db)

    def listar(self, data={}):
        page   = int(data.get("page", 1))
        filtro = str(data.get("filtro", "")).strip()
        result = self.querys.get_personal_activo(page=page, limit=10, filtro=filtro)
        return self.tools.output(200, "Personal obtenido", result)

    def guardar_usuario(self, data={}):
        nit = data.get("nit")
        if not nit:
            return self.tools.output(400, "El campo NIT es requerido")
        try:
            nit = int(nit)
        except (ValueError, TypeError):
            return self.tools.output(400, "El NIT debe ser un valor numérico")
        self.querys.insertar_usuario(nit)
        return self.tools.output(200, f"NIT {nit} registrado correctamente")
