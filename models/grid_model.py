from models.cell import Cell
from controllers.formula_engine import FormulaEngine

class GridModel:
    def __init__(self, rows=10, cols=10):
        self.rows = rows
        self.cols = cols
        self.engine = FormulaEngine(self)

        # Crear matriz de celdas
        self.grid = [[Cell() for _ in range(cols)] for _ in range(rows)]

    # Convertir A1 → (0,0)
    def ref_to_index(self, ref):
        col = ord(ref[0].upper()) - ord('A')
        row = int(ref[1:]) - 1
        return row, col

    def get_cell(self, ref):
        try:
            row, col = self.ref_to_index(ref)
            return self.grid[row][col]
        except:
            raise Exception(f"Referenci invalidad: {ref}")

    def set_cell(self, ref, value):
        cell = self.get_cell(ref)
        cell.set_value(value)
        
        if cell.type == "formula":
            try:
                result = self.engine.evaluate(cell.raw_value)
                cell.value = result
            except Exception as e:
                cell.value= f"Error: {str(e)}"    

    def get_value(self, ref):
        cell = self.get_cell(ref)
        return cell.value