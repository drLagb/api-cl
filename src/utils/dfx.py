from collections import deque
from ezdxf import recover
from ezdxf.addons.drawing import RenderContext, Frontend
from ezdxf.addons.drawing.matplotlib import MatplotlibBackend
import math
import os
import matplotlib.pyplot as plt
from src.utils import minBuyValue
from src.utils.bibliotecas import Velocidad_corte_segundoxmetro, Valor_lamina_m2, biblioteca
from src.utils.errors import NotClosedFiguredException, AuditorException, InterpoleFigureException

class DXFGraphic:
    def __init__(self, entity):
        self.entity = entity

    def isClose(self):
        return True

    def calculate_perimeter(self):
        return 0

class DXFLine(DXFGraphic):
    def calculate_perimeter(self):
        start = self.entity.dxf.start
        end = self.entity.dxf.end
        return math.sqrt((start[0] - end[0])**2 + (start[1] - end[1])**2)
    
    def isClose(self):
        return self.entity.closed

class DXFArc(DXFGraphic):
    def calculate_perimeter(self):
        radius = self.entity.dxf.radius
        start_angle = math.radians(self.entity.dxf.start_angle)
        end_angle = math.radians(self.entity.dxf.end_angle)
        return abs(radius * (end_angle - start_angle))

class DXFCircle(DXFGraphic):
    def calculate_perimeter(self):
        radius = self.entity.dxf.radius
        return 2 * math.pi * radius

class DXFLWPolyline(DXFGraphic):
    def calculate_perimeter(self):
        perimeter = 0
        points = self.entity.get_points('xyb')
        for i in range(len(points) - 1):
            point1 = points[i]
            point2 = points[i + 1]
            distance = math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)
            perimeter += distance
        if self.entity.is_closed:
            first_point = points[0]
            last_point = points[-1]
            distance = math.sqrt((first_point[0] - last_point[0])**2 + (first_point[1] - last_point[1])**2)
            perimeter += distance
        return perimeter
    
    def isClose(self):
        return self.entity.closed

class DFXSpline(DXFGraphic):
    def calculate_perimeter(self):
        DISTANCE = 0.0
        points = list(self.entity.flattening(DISTANCE))
        perimeter = 0.0
        for i in range(len(points) - 1):
            pointOne = points[i]
            pointTwo = points[i + 1]
            distance = math.sqrt((pointOne[0] - pointTwo[0])**2 + (pointOne[1] - pointTwo[1])**2)
            perimeter += distance
        return perimeter

class DXFElipse(DXFGraphic):
    def calculate_perimeter(self):
        a = self.entity.dxf.major_axis.magnitude
        b = self.entity.dxf.minor_axis.magnitude
        h = ((a - b)**2) / ((a + b)**2)
        perimeter = math.pi * (a + b) * (1 + (3 * h) / (10 + math.sqrt(4 - 3 * h)))
        return perimeter

class DXFAnalyzer:

    unitsToMeters = {
        0: None,  # Unidades sin definir
        1: 0.0254,  # Pulgadas a metros
        2: 0.3048,  # Pies a metros
        3: 1609.34,  # Millas a metros
        4: 0.001,  # Milímetros a metros
        5: 0.01,  # Centímetros a metros
        6: 1.0,  # Metros
        7: 1000.0,  # Kilómetros a metros
        8: 2.54e-08,  # Micro-pulgadas a metros
        9: 2.54e-05,  # Mils a metros
        10: 0.9144,  # Yardas a metros
        11: 1e-10,  # Ángstroms a metros
        12: 1e-09,  # Nanómetros a metros
        13: 1e-06,  # Micrones a metros
        14: 0.1,  # Decímetros a metros
        15: 10.0,  # Decámetros a metros
        16: 100.0,  # Hectómetros a metros
        17: 1e+09,  # Gigámetros a metros
        18: 1.495978707e+11,  # Unidades astronómicas a metros
        19: 9.461e+15,  # Años luz a metros
        20: 3.086e+16,  # Parsecs a metros
}


    @staticmethod
    def create():
        MATERIALES:MaterialLibrary = MaterialLibrary()
        for i in list(Velocidad_corte_segundoxmetro.keys()):
            MATERIALES.add_material(Material())
        return MATERIALES

    def __init__(self, file_path):
        self.file_path = file_path
        self.doc, self.auditor = recover.readfile(self.file_path)
        self.msp = self.doc.modelspace()
        self.convertion = DXFAnalyzer.unitsToMeters.get(self.doc.header.get('$INSUNITS'))

    def getArea(self):
        external_polyline, _ = self.get_external_polyline()
        external_polyline = external_polyline.get_points()
        width = (max(external_polyline, key=lambda p: p[0])[0] - min(external_polyline, key=lambda p: p[0])[0])*self.convertion
        height = (max(external_polyline, key=lambda p: p[1])[1] - min(external_polyline, key=lambda p: p[1])[1])*self.convertion
        return width * height

    def get_external_polyline(self):
        area_max = 0
        external_polyline = None
        for entity in self.msp:
            if entity.dxftype() == 'LWPOLYLINE' and entity.is_closed:
                area = self._calculate_polyline_area(entity.get_points())
                if area > area_max:
                    area_max = area
                    external_polyline = entity
        return external_polyline, area_max

    def _calculate_polyline_area(self, points):
        sum = 0
        for i in range(len(points)):
            p1 = points[i]
            p2 = points[(i + 1) % len(points)]
            sum += p1[0] * p2[1] - p1[1] * p2[0]
        return abs(sum) / 2

    def calculate_perimeter(self):
        perimeter = 0
        for entity in self.msp:
            graphic = self.create_dxf_graphic(entity)
            perimeter += graphic.calculate_perimeter()
        return perimeter*self.convertion

    def create_dxf_graphic(self, entity):
        shape = None
        match entity.dxftype():
            case 'LINE':
                shape = DXFLine(entity)
            case 'Arc':
                shape = DXFArc(entity)
            case 'CIRCLE':
                shape = DXFCircle(entity)
            case 'LWPOLYLINE':
                shape = DXFLWPolyline(entity)
            case 'SPLINE':
                shape = DFXSpline(entity)
            case _:
                shape = DXFGraphic(entity)
        return shape
    
    def angle_between(self, a, b, p):
        ax, ay = a[:2]
        bx, by = b[:2]
        px, py = p
        angle1 = math.atan2(ay - py, ax - px)
        angle2 = math.atan2(by - py, bx - px)
        angle = angle2 - angle1
        if angle > math.pi:
            angle -= 2 * math.pi
        if angle < -math.pi:
            angle += 2 * math.pi
        
        return angle
    
    def pointIntoFigure(self, punto, polilinea_externa):
        puntos_externa = polilinea_externa.get_points()
        angulo = 0.0
        n = len(puntos_externa)
        for i in range(n):
            angulo += self.angle_between(puntos_externa[i], puntos_externa[(i+1)%n], punto)
        return abs(angulo) > math.pi
    
    def traslateFigure(self, polilinea1, polilinea2):
        puntos1 = polilinea1.get_points()
        puntos2 = polilinea2.get_points()
        for punto in puntos1:
            if self.pointIntoFigure(punto[:2], polilinea2):
                return True
        for punto in puntos2:
            if self.pointIntoFigure(punto[:2], polilinea1):
                return True
        return False

    def verifyFile(self):
        if self.auditor.has_errors:
            raise AuditorException()
        externalLine, _ = self.get_external_polyline()
        cola = deque(self.msp)
        while len(cola) > 0:
            figure = cola.pop()
            graphic = self.create_dxf_graphic(figure)
            if not graphic.isClose():
                raise NotClosedFiguredException()
            if id(externalLine) == id(figure):
                continue
            for point in figure.get_points():
                if not self.pointIntoFigure(point[:2], externalLine):
                    raise InterpoleFigureException()
            for _figure in cola:
                if id(_figure) != id(figure) and id(externalLine) != id(_figure) and self.traslateFigure(figure, _figure):
                    raise InterpoleFigureException()
                

    def draw_dxf(self, filePath: str, show: bool = False, dpi: int = 300, line_color: str = "black", background_color: str = "white"):
        # Crear la figura y el eje
        fig, ax = plt.subplots()
        fig.patch.set_facecolor(background_color)
        ax.set_facecolor(background_color)
        ctx = RenderContext(self.doc)
        ctx.set_current_layout(self.msp)
        ctx.set_background(background_color)  # Ajustar el fondo del render
        out = MatplotlibBackend(ax)
        frontend = Frontend(ctx, out)
        frontend.draw_layout(self.msp, finalize=True)
        # Mejorar la presentación
        ax.set_aspect('equal', adjustable='datalim')
        ax.axis('off')  # Ocultar los ejes
        plt.title("Vista previa del archivo DXF", color=line_color)
        # Guardar la imagen
        fig.savefig(filePath, dpi=dpi, bbox_inches='tight', pad_inches=0)

class Material:
    def __init__(self, name, thickness, cutting_speed, sheet_value):
        self.name = name
        self.thickness = thickness
        self.cutting_speed = cutting_speed
        self.sheet_value = sheet_value

class MaterialLibrary:
    @staticmethod
    def get_material_from_dicts(material, thickness):
        phrase = f"{material}{thickness}".upper()
        speed = Velocidad_corte_segundoxmetro.get(phrase)
        value = Valor_lamina_m2.get(phrase)
        if value == None or speed == None:
            return None
        return Material(material, thickness, speed, value)

    def __init__(self):
        self.materials = {}

    def add_material(self, material):
        key = material.name + material.thickness
        self.materials[key] = material

    def get_material(self, name, thickness):
        key = name + thickness
        return self.materials.get(key)


class Calculator:
    def __init__(self, dxf_analyzer):
        self.dxf_analyzer = dxf_analyzer

    def getDiscount(self, amount: int):
        return biblioteca.get(amount) if biblioteca.get(amount) != None else 0.6

    def magancyMargin(self, price):
        return max(-0.0000012*price + 0.6, 0.3)

    def calculate_price(self, material:Material, amount:int):
        perimeter = self.dxf_analyzer.calculate_perimeter()
        material_area = self.dxf_analyzer.getArea()
        if material:
            cutting_time = perimeter * material.cutting_speed 
            material_cost = material_area * material.sheet_value
            final_price = (material_cost + cutting_time)*amount
            final_price += final_price*self.magancyMargin(final_price)*(1-self.getDiscount(amount))
            print(final_price, minBuyValue)
            return max(final_price, minBuyValue)
        return -1


# Example usage
if __name__ == "__main__":
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Files", "perchero_polyline_9_2432.7.dxf")
    print(1)
    dxf_analyzer = DXFAnalyzer(file_path)
    dxf_analyzer.draw_dxf()
