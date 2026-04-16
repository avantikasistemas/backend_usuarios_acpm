from Utils.tools import Tools, CustomException
from sqlalchemy import text, func, case, extract, and_, or_, Date, cast
from datetime import datetime, date
import traceback
import pytz

class Querys:

    def __init__(self, db):
        self.db = db
        self.tools = Tools()
        self.query_params = dict()
        self.colombia_tz = pytz.timezone('America/Bogota')

    def get_personal_activo(self, page=1, limit=10, filtro=""):
        """Retorna el personal activo con paginación y filtro opcional."""
        try:
            offset     = (page - 1) * limit
            like_param = f"%{filtro}%" if filtro else "%"

            total = self.db.execute(text("""
                SELECT COUNT(*) FROM v_personal_activo
                WHERE CAST(nit AS NVARCHAR) LIKE :f
                   OR nombres              LIKE :f
            """), {"f": like_param}).scalar()

            rows = self.db.execute(text("""
                SELECT * FROM v_personal_activo
                WHERE CAST(nit AS NVARCHAR) LIKE :f
                   OR nombres              LIKE :f
                ORDER BY nombres ASC
                OFFSET :offset ROWS FETCH NEXT :limit ROWS ONLY
            """), {"f": like_param, "offset": offset, "limit": limit}).fetchall()

            return {
                "items": [{"nit": r.nit, "nombres": r.nombres} for r in rows],
                "total": total,
                "page": page,
                "limit": limit,
                "pages": max(1, -(-total // limit)),
            }
        except Exception as e:
            traceback.print_exc()
            raise CustomException(f"Error consultando personal activo: {e}")

    def insertar_usuario(self, nit: int):
        """
        Flujo:
        1. Si el NIT NO está en terceros → error (debe crearse primero como tercero).
        2. Si el NIT ya está en y_personal_contratos → error (ya registrado).
        3. Si el NIT NO está en y_personal → crearlo.
        4. Insertar en y_personal_contratos.
        """
        try:
            # 1. Validar existencia en terceros
            en_terceros = self.db.execute(text("""
                SELECT COUNT(*) FROM terceros WHERE nit = :nit
            """), {"nit": nit}).scalar()

            if not en_terceros:
                raise CustomException(
                    f"El NIT {nit} no existe como tercero. Debe crearlo primero en el módulo de terceros antes de continuar."
                )

            # 2. Validar duplicado en contratos
            en_contratos = self.db.execute(text("""
                SELECT COUNT(*) FROM y_personal_contratos WHERE nit = :nit
            """), {"nit": nit}).scalar()

            if en_contratos:
                raise CustomException(f"El NIT {nit} ya se encuentra registrado.")

            # 3. Verificar existencia en y_personal
            en_personal = self.db.execute(text("""
                SELECT COUNT(*) FROM y_personal WHERE nit = :nit
            """), {"nit": nit}).scalar()

            if not en_personal:
                hoy = datetime.now(self.colombia_tz).strftime("%Y%m%d")
                self.db.execute(text("""
                    INSERT INTO y_personal
                        (nit, estado_civil, sexo, fecha_nacimiento, fecha_grabacion, rh, ciudad, departamento)
                    VALUES
                        (:nit, 'S', 'F', '19950615', :fecha, '+', '001', '08')
                """), {"nit": nit, "fecha": hoy})

            # 4. Insertar en contratos
            self.db.execute(text("""
                INSERT INTO y_personal_contratos
                    (nit, codigo, nomina, estado, tipo_contrato, regimen, tipo_salario, fondo_pension, fondo_salud)
                VALUES
                    (:nit, :codigo, 1, 'A', 'I', 'P', 'V', 8, 9)
            """), {"nit": nit, "codigo": nit})

            self.db.commit()
        except CustomException:
            raise
        except Exception as e:
            self.db.rollback()
            traceback.print_exc()
            raise CustomException(f"Error insertando usuario: {e}")

    def inactivar_usuario(self, nit: int):
        """Marca el estado del usuario como 'R' (Retirado) en y_personal_contratos."""
        try:
            en_contratos = self.db.execute(text("""
                SELECT COUNT(*) FROM y_personal_contratos WHERE nit = :nit
            """), {"nit": nit}).scalar()

            if not en_contratos:
                raise CustomException(f"El NIT {nit} no se encuentra registrado en contratos.")

            self.db.execute(text("""
                UPDATE y_personal_contratos SET estado = 'R' WHERE nit = :nit
            """), {"nit": nit})

            self.db.commit()
        except CustomException:
            raise
        except Exception as e:
            self.db.rollback()
            traceback.print_exc()
            raise CustomException(f"Error inactivando usuario: {e}")
