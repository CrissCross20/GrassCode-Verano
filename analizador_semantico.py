import ply.yacc as yacc
from analizador_lexico import palabras_reservadas

class TablaSimbolos:
     
    # Constructor
    def __init__(self):
        # Lista para almacenar <Variables>
        self.tabla_variables = []
        # Lista para almacenar <Funciones>
        self.tabla_funciones = []
        self.tabla_variables_funcion = []
        # Arreglo para ir alamacenando todos los <Errores>
        self.errores = [] 

    # Registro de <Variables Globales> en la tabla de símbolos
    def agregar_variable(self, nombre_variable, tipo_dato, valor_variable, ambito):
        
        if ambito == False:
            # Variable es la represenctación individual de todos los elementos que se encuentran en la tabla
            for variable in self.tabla_variables:
                # Si el nombre de la variable que se quiere agregar ya existe entonces no se va añadir 
                if variable['nombre'] == nombre_variable:
                    mensaje = (f"Error Semántico: La variable '{nombre_variable}' ya ha sido declarada.")
                    self.errores.append(mensaje)
                    return
            self.tabla_variables.append({'nombre': nombre_variable, 'tipo': tipo_dato, 'valor': valor_variable})
        
        if ambito == True:
            # Variable es la represenctación individual de todos los elementos que se encuentran en la tabla de variables dentro de una función
            for variable in self.tabla_variables_funcion:
                # Si el nombre de la variable que se quiere agregar ya existe entonces no se va añadir 
                if variable['nombre'] == nombre_variable:
                    mensaje = (f"Error Semántico: La variable '{nombre_variable}' se encuentra duplicada dentro de una función.")
                    self.errores.append(mensaje)
                    return
            self.tabla_variables_funcion.append({'nombre': nombre_variable, 'tipo': tipo_dato, 'valor': valor_variable})
        
    # Registro de <Funciones> en la tabla de símbolos
    def agregar_funcion(self, nombre_funcion, return_valor):
        # Reiniciar
        self.tabla_variables_funcion = []
        # Variable es la represenctación individual de todos los elementos que se encuentran en la tabla
        for funcion in self.tabla_funciones:
            # Si el nombre de la variable que se quiere agregar ya existe entonces no se va añadir 
            if funcion['nombre_funcion'] == nombre_funcion:
                mensaje = (f"Error Semántico: La función '{nombre_funcion}' ya ha sido declarada.")
                self.errores.append(mensaje)
                return
        self.tabla_funciones.append({'nombre_funcion': nombre_funcion, 'return': return_valor}) 
    
    
    
    #   def obtener_variable(self, nombre):
    #    for tabla in reversed(self.tablas):
    #        if nombre in tabla:
    #            return tabla[nombre]
    #   mensaje = (f"Error semántico: La variable '{nombre}' no está declarada.")
    #    self.errores.append(mensaje)

        

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
        self.tabla_variables = []
        self.tabla_funciones = []
        self.tabla_variables_funcion = []
        self.errores = [] 

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