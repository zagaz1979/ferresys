import math

class Paginator:
    def __init__(self, items, page=1, per_page=10):
        self.items = items
        self.page = page
        self.per_page = per_page
        self.total = len(items)
        self.pages = math.ceil(self.total / per_page) if self.total > 0 else 1
        
        # Validar página
        if self.page < 1: self.page = 1
        if self.page > self.pages: self.page = self.pages

        self.start = (self.page - 1) * per_page
        self.end = self.start + per_page
        self.data = self.items[self.start:self.end]

    def get_page_numbers(self):
        # Retorna un rango de páginas para mostrar en la UI (ej: 1 2 3 4 5)
        return range(1, self.pages + 1)