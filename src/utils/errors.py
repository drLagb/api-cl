ERRORS_DIC = {
    "NotClosedFiguredException":"La figura no esta cerrada correctamente",
    "AuditorException": "El archivos tiene errores irrecuperables",
    "InterpoleFigureException": "La figura esta solapada en otra",
    "MaterialNotExistException": "El material a consultar no existe en la base de datos"
}
class NotClosedFiguredException(Exception):
    def __init__(self, mensaje:str=ERRORS_DIC.get("NotClosedFiguredException")):
        super().__init__(mensaje)

class InterpoleFigureException(Exception):
    def __init__(self, mensaje:str=ERRORS_DIC.get("InterpoleFigureException")):
        super().__init__(mensaje)

class AuditorException(Exception):
    def __init__(self, mensaje:str=ERRORS_DIC.get("AuditorException")):
        super().__init__(mensaje)

class MaterialNotExistException(Exception):
    def __init__(self, mensaje:str=ERRORS_DIC.get("MaterialNotExistException")):
        super().__init__(mensaje)