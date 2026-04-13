from models.grid_model import GridModel

grid = GridModel()

grid.set_cell("A10", "10")
grid.set_cell("B1", "5")

grid.set_cell("C1", "=A10+B1")
print("C1:", grid.get_value("C1"))  # 15

grid.set_cell("D1", "=A10*B1")
print("D1:", grid.get_value("D1"))  # 50

grid.set_cell("E1", "=SQRT(A10)")
print("E1:", grid.get_value("E1"))  # raíz de 10

grid.set_cell("F1", "=MAX(A10,B1)")
print("F1:", grid.get_value("F1"))  # 10

# TEXTO
grid.set_cell("A2", "Hola")
grid.set_cell("B2", "Mundo")

grid.set_cell("C2", "=Hola+Mundo")
print("C2:", grid.get_value("C2"))  # Hola Mundo

# ERROR
grid.set_cell("D2", "=A2*B2")
print("D2:", grid.get_value("D2"))  # Error

# ERROR 2
grid.set_cell("C3", "=ADD(10,200)")
print("🚀", grid.get_value("C3"))  



