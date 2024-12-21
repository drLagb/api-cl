ERRORS_DIC = {
    "NotClosedFiguredException":"La figura no esta cerrada correctamente",
    "AuditorException": "El archivos tiene errores irrecuperables",
    "InterpoleFigureError": "La figura esta solapada en otra"
}
class NotClosedFiguredException(Exception):
    def __init__(self, mensaje:str=ERRORS_DIC.get("NotClosedFiguredException")):
        super().__init__(mensaje)

class InterpoleFigureError(Exception):
    def __init__(self, mensaje:str=ERRORS_DIC.get("InterpoleFigureError")):
        super().__init__(mensaje)

class AuditorException(Exception):
    def __init__(self, mensaje:str=ERRORS_DIC.get("AuditorException")):
        super().__init__(mensaje)