import re


class Helpers:
    def __init__(self, grid):
        self.grid = grid

    def resolve_value(self, token):
        # número
        if re.match(r'^\d+(\.\d+)?$', token):
            return float(token), "number"

        # celda (A1, AA10)
        if re.match(r'^[A-Z]+\d+$', token):
            cell = self.grid.get_cell(token)

            if cell.value is None:
                raise Exception(f"{token} está vacío")

            return cell.value, cell.type

        raise Exception(f"Valor inválido: {token}")