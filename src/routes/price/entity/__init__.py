class PriceEntity:
    
    def __init__(self, id, area, price, perimetro, message):
        self.message: str = message
        self.id = id
        self.area = area
        self.price = price
        self.perimetro = perimetro