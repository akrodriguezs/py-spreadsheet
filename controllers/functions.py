import math


class Functions:
    def __init__(self, resolver):
        self.resolve = resolver

    # =========================
    # FUNCIONES
    # =========================
    def sqrt(self, args):
        if len(args) != 1:
            raise Exception("SQRT requiere 1 argumento")

        value, type_ = self.resolve(args[0])

        if type_ != "number":
            raise Exception("SQRT solo acepta números")

        return math.sqrt(value)

    def max(self, args):
        if len(args) != 2:
            raise Exception("MAX requiere 2 argumentos")

        v1, t1 = self.resolve(args[0])
        v2, t2 = self.resolve(args[1])

        if t1 != "number" or t2 != "number":
            raise Exception("MAX solo acepta números")

        return max(v1, v2)

    def sum(self, args):
        if len(args) < 1:
            raise Exception("SUM requiere al menos 1 argumento")
        if len(args) != 2:
            raise Exception("SUM requiere 2 argumentos")
        
        total = 0

        for arg in args:
            value, type_ = self.resolve(arg)

            if type_ != "number":
                raise Exception("SUM solo acepta números")

            total += value

        return total

    # =========================
    # OPERACIONES COMO FUNCIONES
    # =========================
    def add(self, args):
        if len(args) != 2:
            raise Exception("ADD requiere 2 argumentos")

        v1, t1 = self.resolve(args[0])
        v2, t2 = self.resolve(args[1])

        if t1 == "text" and t2 == "text":
            return str(v1) + str(v2)

        if t1 != "number" or t2 != "number":
            raise Exception("ADD inválido entre tipos")

        return v1 + v2

    def sub(self, args):
        if len(args) != 2:
            raise Exception("SUB requiere 2 argumentos")

        v1, t1 = self.resolve(args[0])
        v2, t2 = self.resolve(args[1])

        if t1 != "number" or t2 != "number":
            raise Exception("SUB solo acepta números")

        return v1 - v2

    def mul(self, args):
        if len(args) != 2:
            raise Exception("MUL requiere 2 argumentos")

        v1, t1 = self.resolve(args[0])
        v2, t2 = self.resolve(args[1])

        if t1 != "number" or t2 != "number":
            raise Exception("MUL solo acepta números")

        return v1 * v2

    def div(self, args):
        if len(args) != 2:
            raise Exception("DIV requiere 2 argumentos")

        v1, t1 = self.resolve(args[0])
        v2, t2 = self.resolve(args[1])

        if t1 != "number" or t2 != "number":
            raise Exception("DIV solo acepta números")

        if v2 == 0:
            raise Exception("División por cero")

        return v1 / v2

    # =========================
    # REGISTRO DE FUNCIONES
    # =========================
    def get_functions(self):
        return {
            "SQRT": self.sqrt,
            "MAX": self.max,
            "SUM": self.sum,
            "ADD": self.add,
            "SUB": self.sub,
            "MUL": self.mul,
            "DIV": self.div
        }