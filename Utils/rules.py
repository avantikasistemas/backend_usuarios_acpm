from .validator import Validator


class Rules:
    """ Esta clase se encarga de validar los datos de entrada de la API
        y si hay un error, lanza una excepcion """

    val = Validator()

    def __init__(self, path: str, params: dict):
        path_dict = {
            "/consultar_activo": self.__val_consultar_activo,
            "/retirar_activo": self.__val_retirar_activo,
            "/guardar_activo": self.__val_guardar_activo,
            "/actualizar_activo": self.__val_actualizar_activo,
            "/responder_acta": self.__val_responder_acta,
            "/guardar_orden_trabajo": self.__val_guardar_orden_trabajo,
        }
        # Se obtiene la funcion a ejecutar
        func = path_dict.get(path, None)
        if func:
            # Se ejecuta la funcion para obtener las reglas de validacion
            validacion_dict = func(params)

            # Se valida la datas
            self.val.validacion_datos_entrada(validacion_dict)

    def __val_consultar_activo(self, params):
        validacion_dict = [
            {
                "tipo": "string",
                "campo": "codigo",
                "valor": params["codigo"],
                "obligatorio": True,
            }
        ]
        return validacion_dict

    def __val_retirar_activo(self, params):
        validacion_dict = [
            {
                "tipo": "string",
                "campo": "codigo",
                "valor": params["codigo"],
                "obligatorio": True,
            },
            # {
            #     "tipo": "string",
            #     "campo": "motivo",
            #     "valor": params["motivo"],
            #     "obligatorio": True,
            # }
        ]
        return validacion_dict

    def __val_guardar_activo(self, params):
        validacion_dict = [
            {
                "tipo": "string",
                "campo": "codigo",
                "valor": params["codigo"],
                "obligatorio": True,
            },
            {
                "tipo": "string",
                "campo": "descripcion",
                "valor": params["descripcion"],
                "obligatorio": True,
            },
            {
                "tipo": "string",
                "campo": "modelo",
                "valor": params["modelo"],
                "obligatorio": False,
            },
            {
                "tipo": "string",
                "campo": "serie",
                "valor": params["serie"],
                "obligatorio": False,
            },
            {
                "tipo": "string",
                "campo": "marca",
                "valor": params["marca"],
                "obligatorio": False,
            },
            {
                "tipo": "int",
                "campo": "estado",
                "valor": params["estado"],
                "obligatorio": True,
            },
            {
                "tipo": "int",
                "campo": "vida_util",
                "valor": params["vida_util"],
                "obligatorio": False,
            },
            {
                "tipo": "int",
                "campo": "proveedor",
                "valor": params["proveedor"],
                "obligatorio": True,
            },
            {
                "tipo": "int",
                "campo": "tercero",
                "valor": params["tercero"],
                "obligatorio": True,
            },
            {
                "tipo": "string",
                "campo": "docto_compra",
                "valor": params["docto_compra"],
                "obligatorio": True,
            },
            {
                "tipo": "string",
                "campo": "fecha_compra",
                "valor": params["fecha_compra"],
                "obligatorio": True,
            },
            {
                "tipo": "string",
                "campo": "caracteristicas",
                "valor": params["caracteristicas"],
                "obligatorio": False,
            },
            {
                "tipo": "int",
                "campo": "sede",
                "valor": params["sede"],
                "obligatorio": True,
            },
            {
                "tipo": "int",
                "campo": "centro",
                "valor": params["centro"],
                "obligatorio": True,
            },
            {
                "tipo": "string",
                "campo": "grupo",
                "valor": params["grupo"],
                "obligatorio": True,
            },
            {
                "tipo": "int",
                "campo": "macroproceso_encargado",
                "valor": params["macroproceso_encargado"],
                "obligatorio": True,
            },
            {
                "tipo": "int",
                "campo": "macroproceso",
                "valor": params["macroproceso"],
                "obligatorio": True,
            },
            {
                "tipo": "float",
                "campo": "costo_compra",
                "valor": params["costo_compra"],
                "obligatorio": True,
            }
        ]
        return validacion_dict

    def __val_actualizar_activo(self, params):
        validacion_dict = [
            {
                "tipo": "string",
                "campo": "codigo",
                "valor": params["codigo"],
                "obligatorio": True,
            },
            {
                "tipo": "string",
                "campo": "descripcion",
                "valor": params["descripcion"],
                "obligatorio": True,
            },
            {
                "tipo": "string",
                "campo": "modelo",
                "valor": params["modelo"],
                "obligatorio": False,
            },
            {
                "tipo": "string",
                "campo": "serie",
                "valor": params["serie"],
                "obligatorio": False,
            },
            {
                "tipo": "string",
                "campo": "marca",
                "valor": params["marca"],
                "obligatorio": False,
            },
            {
                "tipo": "int",
                "campo": "estado",
                "valor": params["estado"],
                "obligatorio": True,
            },
            {
                "tipo": "int",
                "campo": "vida_util",
                "valor": params["vida_util"],
                "obligatorio": False,
            },
            {
                "tipo": "int",
                "campo": "proveedor",
                "valor": params["proveedor"],
                "obligatorio": True,
            },
            {
                "tipo": "int",
                "campo": "tercero",
                "valor": params["tercero"],
                "obligatorio": True,
            },
            {
                "tipo": "string",
                "campo": "docto_compra",
                "valor": params["docto_compra"],
                "obligatorio": True,
            },
            {
                "tipo": "string",
                "campo": "fecha_compra",
                "valor": params["fecha_compra"],
                "obligatorio": True,
            },
            {
                "tipo": "string",
                "campo": "caracteristicas",
                "valor": params["caracteristicas"],
                "obligatorio": False,
            },
            {
                "tipo": "int",
                "campo": "sede",
                "valor": params["sede"],
                "obligatorio": True,
            },
            {
                "tipo": "int",
                "campo": "centro",
                "valor": params["centro"],
                "obligatorio": True,
            },
            {
                "tipo": "string",
                "campo": "grupo",
                "valor": params["grupo"],
                "obligatorio": True,
            },
            {
                "tipo": "int",
                "campo": "macroproceso_encargado",
                "valor": params["macroproceso_encargado"],
                "obligatorio": True,
            },
            {
                "tipo": "int",
                "campo": "macroproceso",
                "valor": params["macroproceso"],
                "obligatorio": True,
            },
            {
                "tipo": "float",
                "campo": "costo_compra",
                "valor": params["costo_compra"],
                "obligatorio": True,
            }
        ]
        return validacion_dict

    def __val_responder_acta(self, params):
            validacion_dict = [
                {
                    "tipo": "string",
                    "campo": "observaciones",
                    "valor": params["observaciones"],
                    "obligatorio": True,
                },
                {
                    "tipo": "string",
                    "campo": "firma_tercero",
                    "valor": params["firma_tercero"],
                    "obligatorio": True,
                },
            ]
            return validacion_dict

    def __val_guardar_orden_trabajo(self, params):
        validacion_dict = [
            {
                "tipo": "int",
                "campo": "activo id",
                "valor": params["activo_id"],
                "obligatorio": True,
            },
            {
                "tipo": "int",
                "campo": "tipo mantenimiento",
                "valor": params["tipo_mantenimiento"],
                "obligatorio": True,
            },
            {
                "tipo": "string",
                "campo": "fecha programacion desde",
                "valor": params["fecha_programacion_desde"],
                "obligatorio": True,
            },
            {
                "tipo": "string",
                "campo": "fecha programacion hasta",
                "valor": params["fecha_programacion_hasta"],
                "obligatorio": False,
            },
            {
                "tipo": "int",
                "campo": "tecnico asignado",
                "valor": params["tecnico_asignado"],
                "obligatorio": True,
            },
            {
                "tipo": "string",
                "campo": "descripcion",
                "valor": params["descripcion"],
                "obligatorio": True,
            }
        ]
        return validacion_dict
