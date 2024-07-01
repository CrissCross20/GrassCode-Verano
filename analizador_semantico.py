import ply.yacc as yacc
from analizador_lexico import palabras_reservadas

class TablaSimbolos:
     
     # Constructor
     def __init__(self):
         # Lista para almacenar <Variables>
         self.tabla = []
         # Arreglo para ir alamacenando todos los <Errores>
         self.errores = [] 

     # Registro de variables en la tabla de símbolos
     def agregar(self, nombre, tipo, valor):
        # Verficar que la variable no sea una palabra reservada
        for clave in palabras_reservadas.keys():
            if clave == nombre:
                mensaje = (f"Error Semántico: 'ID' no válido, el nombre para la variable '{nombre}' esta haciendo uso de una palabra reservada.")
                self.errores.append(mensaje)
                print(f"TABLA SIMBOLOS WAAAAAAAZAAAAAAError Semántico: 'ID' no válido, el nombre para la variable '{nombre}' esta haciendo uso de una palabra reservada. ")
                return
              
        # variable es la represenctación individual de todos los elementos que se encuentran en la tabla
        for variable in self.tabla:
            # Si el nombre de la varaible que se quiere agrear ya existe entonces no se va añadir 
            if variable['nombre'] == nombre:
                mensaje = (f"Error Semántico: La variable '{nombre}' ya está declarada en este ámbito.")
                self.errores.append(mensaje)
                return
        
        self.tabla.append({'nombre': nombre, 'tipo': tipo, 'valor': valor})
    # Agregar -------------------------------------------------------------------------------------------------------------------------------------
    
    
    
     def obtener(self, nombre):
        for tabla in reversed(self.tablas):
            if nombre in tabla:
                return tabla[nombre]
        mensaje = (f"Error semántico: La variable '{nombre}' no está declarada.")
        self.errores.append(mensaje)

    #  def agregar_funcion(self, nombre, tipo_retorno, parametros):
    #      if nombre in self.funciones:
    #          mensaje = (f"Error semántico: La función '{nombre}' ya está declarada.")
    #          self.errores.append(mensaje)
    #      self.funciones[nombre] = {'tipo_retorno': tipo_retorno, 'parametros': parametros}

    #  def obtener_funcion(self, nombre):
    #      if nombre not in self.funciones:
    #          mensaje = (f"Error semántico: La función '{nombre}' no está declarada.")
    #          self.errores.append(mensaje)
    #      return self.funciones[nombre]

     def entrar_ambito(self):
         self.tablas.append({})

     def salir_ambito(self):
         self.tablas.pop()
    
     def obtener_errores(self):
         return self.errores
     
     def reinicio_clase(self):
         self.errores = []
         self.tablas = [{}]
         self.funciones = {}

tabla_simbolos = TablaSimbolos()


# Tipos de Ámbitos

# Ámbito Global:
# Es el ámbito más externo y generalmente se refiere al ámbito que cubre todo el programa.
# Las variables y funciones declaradas en el ámbito global son accesibles desde cualquier parte del programa.

# Ámbito Local:
# Es el ámbito que existe dentro de una función, un bloque de código, una clase, etc.
# Las variables declaradas en un ámbito local solo son accesibles dentro de ese bloque específico y no desde fuera de él.

# Ámbito de Bloque:
# Algunos lenguajes de programación permiten definir variables dentro de bloques específicos (por ejemplo, dentro de un if, for, while, etc.).
# Las variables tienen un alcance limitado al bloque donde fueron declaradas.