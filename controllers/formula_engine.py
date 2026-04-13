import re
from controllers.functions import Functions
from controllers.helpers import Helpers


class FormulaEngine:
    def __init__(self, grid_model):
        if not hasattr(grid_model, "get_cell"):
            raise Exception("Grid inválido")

        self.grid = grid_model
        self.helpers = Helpers(grid_model)
        self.functions = Functions(self.helpers.resolve_value)

    # =========================
    # MAIN
    # =========================
    def evaluate(self, formula):
        parsed = self.parse(formula)
        if parsed["type"] == "operation":
            return self.eval_operation(parsed)

        elif parsed["type"] == "function":
            return self.eval_function(parsed)

    # =========================
    # PARSER
    # =========================
    def parse(self, formula):
        formula = formula.strip()

        if not formula.startswith("="):
            raise Exception("No es fórmula válida")

        formula = formula[1:].strip()

        # función
        func_match = re.match(r'^([A-Z]+)\((.*?)\)$', formula)
        if func_match:
            name, args = func_match.groups()
            args = [a.strip() for a in args.split(",") if a.strip()]

            return {
                "type": "function",
                "name": name,
                "args": args
            }

        # operación
        return self.parse_operation(formula)

    def parse_operation(self, formula):
        if formula.count("+") + formula.count("-") + formula.count("*") + formula.count("/") > 1:
            raise Exception("Solo se permiten 2 operandos")

        match = re.match(r'^(.+?)\s*([\+\-\*/])\s*(.+)$', formula)

        if not match:
            raise Exception("Fórmula inválida")

        left, operator, right = match.groups()

        return {
            "type": "operation",
            "operator": operator,
            "operands": [left.strip(), right.strip()]
        }

    # =========================
    # EVALUADORES
    # =========================
    def eval_operation(self, parsed):
        left, right = parsed["operands"]
        operator = parsed["operator"]

        val1, type1 = self.helpers.resolve_value(left)
        val2, type2 = self.helpers.resolve_value(right)

        # texto
        if type1 == "text" and type2 == "text":
            if operator != "+":
                raise Exception("Solo se permite concatenar texto con +")
            return str(val1) + str(val2)

        # numérico
        if type1 != "number" or type2 != "number":
            raise Exception("Operación inválida entre tipos")

        if operator == "+":
            return val1 + val2
        elif operator == "-":
            return val1 - val2
        elif operator == "*":
            return val1 * val2
        elif operator == "/":
            if val2 == 0:
                raise Exception("División por cero")
            return val1 / val2

    def eval_function(self, parsed):
        funcs = self.functions.get_functions()

        name = parsed["name"]

        if name not in funcs:
            raise Exception(f"Función no soportada: {name}")

        return funcs[name](parsed["args"])