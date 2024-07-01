import ply.yacc as yacc
from analizador_semantico import tabla_simbolos
# Tokens contiene toda la información necesaria y palabras_reservadas podría servir para el analisis sintáctico
from analizador_lexico import tokens, palabras_reservadas
# from graphviz import Digraph

print(tokens)
# Listas para almacenar errores de sintaxis y debuggeos sobre se declaró y detectó correctametne
declaracionesRegistro = []
errores = []
errores_semanticos = []


# Precedencia de operadores (si es necesario)
precedence = (
    ('left', 'SUMA', 'RESTA'),
    ('left', 'MULTIPLICACION', 'DIVISION'),
)
#########################################################################################################################################################
# Agrupaciones (Esqueleto del programa) -----------------------------------------------------------------------------------------------------------------
def p_programa(p):
    '''programa : sentencias'''
    p[0] = ('programa', p[1])
def p_sentencias(p):
    '''sentencias : sentencia
                  | sentencias sentencia'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]
def p_sentencia(p):
    '''sentencia : imports
                 | clase'''
    p[0] = p[1]
def p_imports(p):
    '''imports : import
               | imports import'''             
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]
def p_declaraciones(p):
    '''declaraciones : declaracion
                     | declaraciones declaracion'''
def p_declaracion(p):
    '''declaracion : declaracion_variable
                   | declaracion_if
                   | declaracion_if_else
                   | declaracion_while
                   | declaracion_funcion
                   | declaracion_funcion_return
                   | asignacion_variable_variable
                   | asignacion_variable_funcion_return
                   | llamar_funcion
                   | llamar_funcion_return
                   | incremento_individual
                   | decremento_individual
                   | vacio'''
    p[0] = p[1]
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]
# Regla vacía, tipos de datos y la representacón de sus valores
def p_tipo_dato(p):
    '''
    tipo_dato : INT
              | FLOAT
              | BOOL
              | STRING
    '''
    p[0] = p[1]
def p_valor_dato(p):
    '''
    valor_dato : NUMERO_ENTERO
               | NUMERO_FLOTANTE
               | TRUE
               | FALSE
               | CADENA
    '''
    p[0] = p[1]

def p_palabras_reservadas(p):
    '''
    palabras_reservadas : INT
                           | FLOAT
                           | BOOL
                           | STRING
                           | NEW
                           | FROM
                           | BRING
                           | AS
                           | CLASS
                           | FUNCT
                           | RETURN
                           | IF
                           | ELSE
                           | WHILE
                           | OR
                           | AND
                           | NOT
                           | TRUE
                           | FALSE
'''
    p[0] = p[1]

def p_vacio(p):
    '''vacio : '''
    p[0] = None
#Fin Esqueleto del programa -----------------------------------------------------------------------------------------------------------------------------
#########################################################################################################################################################


##########################################################################################################################################################
# Cuerpos para clase, if y blucles -----------------------------------------------------------------------------------------------------------------------
def p_cuerpo(p):
    '''cuerpo : declaracion
              | cuerpo declaracion
              | vacio'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]
# Cuerpo para funciones
def p_cuerpo_funcion(p):
    '''cuerpo_funcion : declaracion_en_funcion
                      | cuerpo declaracion_en_funcion
                      | vacio'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]   
def p_declaracion_en_funcion(p):
    '''declaracion_en_funcion : declaracion_variable
                              | declaracion_if
                              | declaracion_if_else
                              | declaracion_while
                              | llamar_funcion
                              | llamar_funcion_return
                              | asignacion_variable_variable
                              | asignacion_variable_funcion_return
                              | incremento_individual
                              | decremento_individual
                              | vacio'''
    p[0] = p[1]
# Cuerpo para condiciones en for, while e if's
def p_condiciones(p):
    '''condiciones : condicion
                   | condiciones AND condicion
                   | condiciones OR condicion'''
    if len(p) == 4:
        p[0] = ('condiciones', p[1], p[2], p[3])
    else:
        p[0] = ('condiciones', p[1])
def p_condicion(p):
    '''condicion : variable comparadores variable 
                 | NOT variable '''  
    if len(p) == 4:
        p[0] = ('condicion', p[1], p[2], p[3])
    else:
        p[0] = ('condicion', p[1], p[2])

def p_condicion_while(p):
    '''condicion_while : variable_while comparadores_while variable_while 
                       | TRUE
                       | NOT ID'''
    if len(p) == 4:
        p[0] = ('condicion_while', p[1], p[2], p[3])
    elif p[1] == 'true':
        p[0] = ('condicion_while', p[1])
    else:
        p[0] = ('condicion_while', p[1], p[2])
# Definicion general de qué puede ser una "variable" 
def p_variable(p):
    ''' variable : ID
                 | NUMERO_ENTERO
                 | NUMERO_FLOTANTE
                 | CADENA
                 | TRUE
                 | FALSE'''
    if isinstance(p[1], tuple):
        p[0] = p[1]
    else:
        p[0] = ('variable', p[1])
def p_comparadores(p):
    ''' comparadores : IGUAL
                     | MAYOR_QUE
                     | MAYOR_IGUAL
                     | MENOR_QUE
                     | MENOR_IGUAL'''
    p[0] = ('comparadores', p[1])
# Cuerpos para clase, if y blucles -----------------------------------------------------------------------------------------------------------------------
##########################################################################################################################################################

                        
##########################################################################################################################################################
# Declaraciones finales ----------------------------------------------------------------------------------------------------------------------------------
def p_import(p):
    '''import : BRING RUTA_IMPORT AS ID PUNTO_COMA'''
    mensaje = ("Se ha declarado un import")
    declaracionesRegistro.append(mensaje)
    p[0] = ('import', p[2], p[4])
def p_clase(p):
    '''clase : CLASS ID LLAVE_APERTURA cuerpo LLAVE_CIERRE'''
    p[0] = ('clase', p[2], p[4])
    mensaje = ("Se ha declarado una clase")
    declaracionesRegistro.append(mensaje)
def p_declaracion_variable(p):
    'declaracion_variable : ID PARENTESIS_APERTURA tipo_dato PARENTESIS_CIERRE ASIGNAR valor_dato PUNTO_COMA'

                            # nombreVariablePrueba_0291A(int) = 58.1 / true / false / "cad";
                            
    nombre_variable = p[1] # Guardar el nombre propuesto en ID
    tipo_dato = p[3] # Guardar el dato encerrado entre parentesis () -> int / float / bool /  string
    valor_variable = p[6] # Guardar el valor asignado 0, 0.0, true / false, "cadena"
    
    # Verificación semántica
    if tipo_dato == 'int': # Si lo recuperado del tipo dato resulta en la palabra reservada int
        # ¿Es insitacia de int? o El valor rescatado de valor_dato ¿es entero?
        if not isinstance(valor_variable, int):
            mensaje = (f"Error Semántico: El valor asignado a la variable '{nombre_variable}' debe ser un entero.")
            errores.append(mensaje)
    elif tipo_dato == 'float':
        if not isinstance(valor_variable, float) and not isinstance(valor_variable, int):
            mensaje = (f"Error Semántico: El valor asignado a la variable '{nombre_variable}' debe ser un número flotante o entero.")
            errores.append(mensaje)
    elif tipo_dato == 'string':
        if not isinstance(valor_variable, str):
            mensaje = (f"Error Semántico: El valor asignado a la variable '{nombre_variable}' debe ser una cadena.")
            errores.append(mensaje)
    elif tipo_dato == 'bool':
        if valor_variable not in ['true', 'false']:
            mensaje = (f"Error Semántico: El valor asignado a la variable '{nombre_variable}' debe ser 'true' o 'false'.")
            errores.append(mensaje)
    else:
        mensaje = (f"Tipo de dato '{tipo_dato}' no reconocido.")
        errores.append(mensaje)
    tabla_simbolos.agregar(nombre_variable, tipo_dato, valor_variable)
   
   
    p[0] = ('declaracion_variable', nombre_variable, tipo_dato, valor_variable)
    mensaje = (f"Se ha declarado una variable en la línea {p.lineno(1)}")
    declaracionesRegistro.append(mensaje)


   #-.-----------------------------------------------------

    # Agregar mensaje a las declaraciones registradas
    declaracionesRegistro.append(mensaje)
    
    # try:
    #     # Intentar agregar el objeto a la tabla de símbolos
    #     #tabla_simbolos.agregar(nombre, tipo)
    #     p[0] = ('declaracion_objeto', nombre, tipo)
    # except ValueError as e:
    #     # Capturar el error semántico y agregarlo a la lista de errores
    #     errores_semanticos.append(f"Error semántico: {str(e)}")
    #     p[0] = ('error', str(e))

    # new patron(object) from Patron_Class;
# Sentencias de control if
def p_declaracion_if(p):
    '''declaracion_if : IF PARENTESIS_APERTURA condiciones PARENTESIS_CIERRE LLAVE_APERTURA cuerpo LLAVE_CIERRE'''
    mensaje = ("Se ha declarado un if")
    declaracionesRegistro.append(mensaje)
    p[0] = ('declaracion_if', p[3], p[6])
def p_declaracion_if_else(p):
    '''declaracion_if_else : IF PARENTESIS_APERTURA condiciones PARENTESIS_CIERRE LLAVE_APERTURA cuerpo LLAVE_CIERRE ELSE LLAVE_APERTURA cuerpo LLAVE_CIERRE'''
    mensaje = ("Se ha declarado una estructura if - else")
    declaracionesRegistro.append(mensaje)
    p[0] = ('declaracion_if_else', p[3], p[6], p[10])

# Ciclo While
def p_declaracion_while(p):
    '''declaracion_while : WHILE PARENTESIS_APERTURA condicion_while PARENTESIS_CIERRE LLAVE_APERTURA cuerpo LLAVE_CIERRE'''
    mensaje = ("Se ha declarado un ciclo while")
    declaracionesRegistro.append(mensaje)
    p[0] = ('declaracion_while', p[3], p[6])
# Elementos de la estrucutra del ciclo while
def p_variable_while(p):
    '''variable_while : NUMERO_ENTERO
                      | ID
                      | TRUE
                      | FALSE'''
    if isinstance(p[1], tuple):
        p[0] = p[1]
    else:
        p[0] = ('variable_while', p[1])
def p_comparadores_while(p):
    '''comparadores_while : IGUAL
                          | MAYOR_QUE
                          | MAYOR_IGUAL
                          | MENOR_QUE
                          | MENOR_IGUAL'''
    p[0] = ('comparadores_while', p[1])
# Funcion con retorno de valor
def p_declaracion_funcion_return(p):
    ''' declaracion_funcion_return : FUNCT CORCHETE_APERTURA tipo_dato CORCHETE_CIERRE ID PARENTESIS_APERTURA parametros PARENTESIS_CIERRE LLAVE_APERTURA cuerpo_funcion return LLAVE_CIERRE'''
    mensaje = ("Se ha declarado una función que devuelve un valor")
    declaracionesRegistro.append(mensaje)
def p_return(p):
    '''return : RETURN ID PUNTO_COMA'''    
# Funcion sin retorno de valor
def p_declaracion_funcion(p):
    ''' declaracion_funcion : FUNCT ID PARENTESIS_APERTURA parametros PARENTESIS_CIERRE LLAVE_APERTURA cuerpo_funcion LLAVE_CIERRE'''
    tabla_simbolos.entrar_ambito()
    mensaje = ("Se ha declarado una función")
    declaracionesRegistro.append(mensaje)
    tabla_simbolos.salir_ambito()
# Elementos de la estrucura de funcion sin y con retorno de valor
def p_parametros(p):
    '''parametros : parametro
                  | parametros COMA parametro
                  | vacio'''
    if len(p) == 4:
        p[0] = ('parametros', p[1], p[3])
    elif p[1] is not None:
        p[0] = ('parametros', p[1])
    else:
        p[0] = ('parametros', )

def p_parametro(p):
    '''parametro : ID PARENTESIS_APERTURA tipo_dato PARENTESIS_CIERRE'''
    nombre=p[1]
    tipo=p[3]
     # Verificar si el parámetro ya ha sido declarado
    if tabla_simbolos.obtener(nombre) is None:
        mensaje = (f"Error Semántico: La variable '{nombre}' no está declarada.")
        errores.append(mensaje)

    p[0] = ('parametro', nombre, tipo)
# Llamadas para objetos y funciones con y sin retorno de valor
def p_llamar_funcion(p):
    '''llamar_funcion : ID PARENTESIS_APERTURA envio_parametros PARENTESIS_CIERRE PUNTO_COMA'''
    mensaje = ("Se ha hecho una llamada a una función")
    declaracionesRegistro.append(mensaje)
    p[0] = ('llamar_funcion', p[1], p[3])
def p_llamar_funcion_return(p):
    '''llamar_funcion_return : CORCHETE_APERTURA tipo_dato CORCHETE_CIERRE ID PARENTESIS_APERTURA envio_parametros PARENTESIS_CIERRE PUNTO_COMA'''
    mensaje = ("Se ha hecho una llamada a una función que retorna un valor")
    declaracionesRegistro.append(mensaje)
    p[0] = ('llamar_funcion_return', p[2], p[4], p[6])

# Envio de parámetros
def p_envio_parametros(p):
    '''envio_parametros : envio_parametro
                        | envio_parametros COMA envio_parametro
                        | vacio'''
    if len(p) == 4:
        p[0] = ('envio_parametros', p[1], p[3])
    elif p[1] is not None:
        p[0] = ('envio_parametros', p[1])
    else:
        p[0] = ('envio_parametros', )
def p_envio_parametro(p):
    '''envio_parametro : tipo_envio_parametro'''
    p[0] = ('envio_parametro', p[1])
def p_tipo_envio_parametro(p):
    ''' tipo_envio_parametro : ID
                             | NUMERO_ENTERO 
                             | NUMERO_FLOTANTE
                             | CADENA
                             | TRUE
                             | FALSE'''
    p[0] = ('tipo_envio_parametro', p[1])
# Asignaciones
def p_asignacion_variable_variable(p):
    '''asignacion_variable_variable : ID PARENTESIS_APERTURA tipo_dato PARENTESIS_CIERRE ASIGNAR ID PARENTESIS_APERTURA tipo_dato PARENTESIS_CIERRE PUNTO_COMA'''
    mensaje = ("Se le ha asignado a una variable el valor de otra")
    declaracionesRegistro.append(mensaje)
    p[0] = ('asignacion_variable_variable', p[1], p[3], p[6], p[8])
def p_asignacion_variable_funcion_return(p):
    ''' asignacion_variable_funcion_return : ID PARENTESIS_APERTURA tipo_dato PARENTESIS_CIERRE ASIGNAR CORCHETE_APERTURA tipo_dato CORCHETE_CIERRE ID PARENTESIS_APERTURA parametros PARENTESIS_CIERRE PUNTO_COMA'''
    mensaje = ("Se le ha asignado a una variable el valor resultado de la una funcion return")
    declaracionesRegistro.append(mensaje)
    p[0] = ('asignacion_variable_funcion_return', p[1], p[3], p[7], p[9], p[11])

# Decremento/incremento individuales
def p_incremento_individual(p):
    ''' incremento_individual : ID INCREMENTO PUNTO_COMA'''
    mensaje = ("Se le ha hecho un incremento en una variable")
    declaracionesRegistro.append(mensaje)
    p[0] = ('incremento_individual', p[1])
def p_decremento_individual(p):
    ''' decremento_individual : ID DECREMENTO PUNTO_COMA'''
    mensaje = ("Se le ha hecho un decremento en una variable")
    declaracionesRegistro.append(mensaje)
    p[0] = ('decremento_individual', p[1])
# Declaraciones finales ----------------------------------------------------------------------------------------------------------------------------------
##########################################################################################################################################################


##########################################################################################################################################################
# Errores para clase -------------------------------------------------------------------------------------------------------------------------------------
def p_clase_e1(p):
    '''clase : ID LLAVE_APERTURA cuerpo LLAVE_CIERRE'''
    mensaje = ("Error de sintaxis: se esperaba 'class' al inicio de la declaración en la línea {}".format(p.lineno(1)))
    errores.append(mensaje)
def p_clase_e2(p):
    '''clase : CLASS LLAVE_APERTURA cuerpo LLAVE_CIERRE'''
    mensaje = ("Error de sintaxis: se esperaba el identificador de la clase antes de '{' y después de 'class' en la línea {}".format(p.lineno(1)))
    errores.append(mensaje)
def p_clase_e3(p):
    '''clase : CLASS ID cuerpo LLAVE_CIERRE'''
    mensaje = ("Error de sintaxis: se esperaba una llave de apertura '{' después del identificador de la clase en la línea {}".format(p.lineno(1)))
    errores.append(mensaje)
def p_clase_e4(p):
    '''clase : CLASS ID LLAVE_APERTURA cuerpo'''
    mensaje = ("Error de sintaxis: se esperaba un parentesis de cierre para el bloque de código en la línea {}".format(p.lineno(1)))
    errores.append(mensaje)
# Errores para importe:
def p_import_e1(p):
    '''import : RUTA_IMPORT AS ID PUNTO_COMA'''
    mensaje = "Error de sintaxis: se esperaba 'bring' al inicio de la declración en la línea {}".format(p.lineno(1))
    errores.append(mensaje)
def p_import_e2(p):
    '''import : BRING AS ID PUNTO_COMA'''
    mensaje = "Error de sintaxis: se esperaba una ruta válida después de 'bring' para traer código al archivo actual en la línea {}".format(p.lineno(1))
    errores.append(mensaje)
def p_import_e4(p):
    '''import : BRING RUTA_IMPORT ID PUNTO_COMA'''
    mensaje = "Error de sintaxis: se esperaba un 'as' después de la ruta y antes del id para renombrar la implementación de código en 'bring' en la línea {}".format(p.lineno(1))
    errores.append(mensaje)
def p_import_e5(p):
    '''import : BRING RUTA_IMPORT AS PUNTO_COMA'''
    mensaje = "Error de sintaxis: se esperaba un identificador 'ID' después de 'as' y antas del punto y coma ';' en la implementación de código 'bring' en la línea {}".format(p.lineno(1))
    errores.append(mensaje)
def p_import_e6(p):
    '''import : BRING RUTA_IMPORT AS ID'''
    mensaje = "Error de sintaxis: se esperaba un ';' al final del import en la línea {}".format(p.lineno(1))
    errores.append(mensaje)
def p_import_e7(p):
    '''import : BRING RUTA_IMPORT AS'''
    mensaje = '''Error de sintaxis: se ha detectado una sentencia de importación incompleta. 
                   Estructura para traer código: bring ruta de clase as idReferencia. 
                   Ejemplo: bring default.operations as operaciones.'''
    errores.append(mensaje)
def p_import_e8(p):
    '''import : BRING RUTA_IMPORT PUNTO_COMA'''
    mensaje = '''Error de sintaxis: se ha detectado una sentencia de importación incompleta. 
                   Estructura para traer código: bring ruta de clase as idReferencia. 
                   Ejemplo: bring default.operations as operaciones.'''
    errores.append(mensaje)
def p_import_e9(p):
    '''import : BRING ID PUNTO_COMA'''
    mensaje = '''Error de sintaxis: se ha detectado una sentencia de importación incompleta. 
                   Estructura para traer código: bring ruta de clase as idReferencia. 
                   Ejemplo: bring default.operations as operaciones.'''
    errores.append(mensaje)
def p_import_e10(p):
    '''import :  AS ID PUNTO_COMA'''
    mensaje = '''Error de sintaxis: se ha detectado una sentencia de importación incompleta. 
                   Estructura para traer código: bring ruta de clase as idReferencia. 
                   Ejemplo: bring default.operations as operaciones.'''
    errores.append(mensaje)
def p_import_e11(p):
    '''import : BRING PUNTO_COMA'''
    mensaje = '''Error de sintaxis: se ha detectado una sentencia de importación incompleta. 
                   Estructura para traer código: bring ruta de clase as idReferencia. 
                   Ejemplo: bring default.operations as operaciones.'''
    errores.append(mensaje)

# Errores tipo de dato/valor dato
def p_tipo_dato_e1(p):
    '''tipo_dato : '''
    mensaje = ("Error de sintaxis: se esperaba un el identificador del tipo de dato 'int / float / string / bool ' en la línea {}".format(p.lineno(1)))
    errores.append(mensaje)
def p_valor_dato_e1(p):
    '''valor_dato : '''
    mensaje = ("Error de sintaxis: se esperaba un el valor del dato 'numero_entero / numero_flotante / cadena / true / false  en la línea {}".format(p.lineno(1)))
    errores.append(mensaje)
# Errores para la declaración de variables
def p_declaracion_variable_e1(p):
    'declaracion_variable : PARENTESIS_APERTURA tipo_dato PARENTESIS_CIERRE ASIGNAR valor_dato PUNTO_COMA'
    mensaje = ("Error de sintaxis: se esperaba un identificador antes del parentesis de apertura '(' en la línea {}".format(p.lineno(1)))
    errores.append(mensaje)
def p_declaracion_variable_e2(p):
    'declaracion_variable : ID tipo_dato PARENTESIS_CIERRE ASIGNAR valor_dato PUNTO_COMA'
    mensaje = ("Error de sintaxis: se esperaba un parentesis de apertura '(' después del identificador en la línea {}".format(p.lineno(1)))
    errores.append(mensaje)
def p_declaracion_variable_e3(p):
    'declaracion_variable : ID PARENTESIS_APERTURA PARENTESIS_CIERRE ASIGNAR valor_dato PUNTO_COMA'
    mensaje = ("Error de sintaxis: se esperaba int, float, string o bool dentro de '( )' en la línea {}".format(p.lineno(1)))
    errores.append(mensaje)
def p_declaracion_variable_e4(p):
    'declaracion_variable : ID PARENTESIS_APERTURA tipo_dato ASIGNAR valor_dato PUNTO_COMA'
    mensaje = ("Error de sintaxis: se esperaba un parentesis de cierre ')' después del tipo de dato en la línea {}".format(p.lineno(1)))
    errores.append(mensaje)
def p_declaracion_variable_e5(p):
    'declaracion_variable : ID PARENTESIS_APERTURA tipo_dato PARENTESIS_CIERRE valor_dato PUNTO_COMA'
    mensaje = ("Error de sintaxis: se esperaba un '=' antes de valo de la variable y después del parentesis de cierre ')' en la línea {}".format(p.lineno(1)))
    errores.append(mensaje)
def p_declaracion_variable_e6(p):
    'declaracion_variable : ID PARENTESIS_APERTURA tipo_dato PARENTESIS_CIERRE ASIGNAR PUNTO_COMA'
    mensaje = ("Error de sintaxis: se esperaba una cadena, true/false o un numero entero/flotante después del igual '=' y antes del punto y coma ';' en la línea {}".format(p.lineno(1)))
    errores.append(mensaje)
def p_declaracion_variable_e7(p):
    'declaracion_variable : ID PARENTESIS_APERTURA tipo_dato PARENTESIS_CIERRE ASIGNAR valor_dato'
    mensaje = ("Error de sintaxis: se esperaba un ';' para finalizar la declaración de variable en la línea {}".format(p.lineno(1)))
    errores.append(mensaje)
def p_declaracion_variable_e8(p):
    'declaracion_variable : ID PARENTESIS_APERTURA tipo_dato PARENTESIS_CIERRE ASIGNAR'
    mensaje = ('''Error de sintaxis: se ha detectado una declaración de variable incompleta. 
                    Estructura para declarar unaa variable: nombreVariable(int, float, bool o string) = numero entero, numero con punto decimal, cadena, true o falase. \n
                    Ejemplo: nombreEstudiante(string) = "Leon. S. Kennedy" ''')
    errores.append(mensaje)
def p_declaracion_variable_e9(p):
    'declaracion_variable : ID PARENTESIS_APERTURA tipo_dato PARENTESIS_CIERRE PUNTO_COMA'
    mensaje = ('''Error de sintaxis: se ha detectado una declaración de variable incompleta. 
                    Estructura para declarar unaa variable: nombreVariable(int, float, bool o string) = numero entero, numero con punto decimal, cadena, true o falase. \n
                    Ejemplo: nombreEstudiante(string) = "Leon. S. Kennedy" ''')
    errores.append(mensaje)
def p_declaracion_variable_e10(p):
    'declaracion_variable : ID PARENTESIS_APERTURA tipo_dato PARENTESIS_CIERRE valor_dato '
    mensaje = ('''Error de sintaxis: se ha detectado una declaración de variable incompleta. 
                    Estructura para declarar unaa variable: nombreVariable(int, float, bool o string) = numero entero, numero con punto decimal, cadena, true o falase. \n
                    Ejemplo: nombreEstudiante(string) = "Leon. S. Kennedy" ''')
    errores.append(mensaje)
def p_declaracion_variable_e11(p):
    'declaracion_variable : ID PARENTESIS_APERTURA tipo_dato'
    mensaje = ('''Error de sintaxis: se ha detectado una declaración de variable incompleta. 
                    Estructura para declarar unaa variable: nombreVariable(int, float, bool o string) = numero entero, numero con punto decimal, cadena, true o falase. \n
                    Ejemplo: nombreEstudiante(string) = "Leon. S. Kennedy" ''')
    errores.append(mensaje)
def p_declaracion_variable_e12(p):
    'declaracion_variable : ID PARENTESIS_APERTURA tipo_dato ASIGNAR valor_dato'
    mensaje = ('''Error de sintaxis: se ha detectado una declaración de variable incompleta. 
                    Estructura para declarar unaa variable: nombreVariable(int, float, bool o string) = numero entero, numero con punto decimal, cadena, true o falase. \n
                    Ejemplo: nombreEstudiante(string) = "Leon. S. Kennedy" ''')
    errores.append(mensaje)
def p_declaracion_variable_e13(p):
    'declaracion_variable : PARENTESIS_CIERRE ASIGNAR valor_dato PUNTO_COMA'
    mensaje = ('''Error de sintaxis: se ha detectado una declaración de variable incompleta. 
                    Estructura para declarar unaa variable: nombreVariable(int, float, bool o string) = numero entero, numero con punto decimal, cadena, true o falase. \n
                    Ejemplo: nombreEstudiante(string) = "Leon. S. Kennedy" ''')
    errores.append(mensaje)

# Sentencia IF-ELSE
def p_declaracion_if_else_e1(p):
    '''declaracion_if_else : PARENTESIS_APERTURA condiciones PARENTESIS_CIERRE LLAVE_APERTURA cuerpo LLAVE_CIERRE ELSE LLAVE_APERTURA cuerpo LLAVE_CIERRE'''
    mensaje = ("Error de sintaxis: se esperaba un 'if' al inicio de la sentencia en la línea {}".format(p.lineno(1)))
    errores.append(mensaje)
def p_declaracion_if_else_e2(p):
    '''declaracion_if_else : IF condiciones PARENTESIS_CIERRE LLAVE_APERTURA cuerpo LLAVE_CIERRE ELSE LLAVE_APERTURA cuerpo LLAVE_CIERRE'''
    mensaje = ("Error de sintaxis: se esperaba un parentesis de apertura '(' después de 'if' en la línea {}".format(p.lineno(1)))
    errores.append(mensaje)
def p_declaracion_if_else_e3(p):
    '''declaracion_if_else : IF PARENTESIS_APERTURA PARENTESIS_CIERRE LLAVE_APERTURA cuerpo LLAVE_CIERRE ELSE LLAVE_APERTURA cuerpo LLAVE_CIERRE'''
    mensaje = ("Error de sintaxis: se esperaba alguna condicón entre parentesis, ejemplo: '(x > 2)' después de 'if' en la línea {}".format(p.lineno(1)))
    errores.append(mensaje)
def p_declaracion_if_else_e4(p):
    '''declaracion_if_else : IF PARENTESIS_APERTURA condiciones LLAVE_APERTURA cuerpo LLAVE_CIERRE ELSE LLAVE_APERTURA cuerpo LLAVE_CIERRE'''
    mensaje = ("Error de sintaxis: se esperaba un parentesis de cierre después del if ( condicion / condiciones ')'  en la línea {}".format(p.lineno(1)))
    errores.append(mensaje)
def p_declaracion_if_else_e5(p):
    '''declaracion_if_else : IF PARENTESIS_APERTURA condiciones PARENTESIS_CIERRE cuerpo LLAVE_CIERRE ELSE LLAVE_APERTURA cuerpo LLAVE_CIERRE'''
    mensaje = ("Error de sintaxis: se esperaba una llave de apertura '{' en la sentencia if-else en la línea {}".format(p.lineno(1)))
    errores.append(mensaje)
def p_declaracion_if_else_e6(p):
    '''declaracion_if_else : IF PARENTESIS_APERTURA condiciones PARENTESIS_CIERRE LLAVE_APERTURA cuerpo ELSE LLAVE_APERTURA cuerpo LLAVE_CIERRE'''
    mensaje = ("Error de sintaxis: se esperaba una llave de cierre '}' para cerrar el if en la sentencia if-else en la línea {}".format(p.lineno(1)))
    errores.append(mensaje)
def p_declaracion_if_else_e7(p):
    '''declaracion_if_else : IF PARENTESIS_APERTURA condiciones PARENTESIS_CIERRE LLAVE_APERTURA cuerpo LLAVE_CIERRE LLAVE_APERTURA cuerpo LLAVE_CIERRE'''
    mensaje = ("Error de sintaxis: se esperaba un 'else' después de la llave de cierre '}' en la sentencia IF-ELSE en la línea {}".format(p.lineno(1)))
    errores.append(mensaje)
def p_declaracion_if_else_e8(p):
    '''declaracion_if_else : IF PARENTESIS_APERTURA condiciones PARENTESIS_CIERRE LLAVE_APERTURA cuerpo LLAVE_CIERRE ELSE cuerpo LLAVE_CIERRE'''
    mensaje = ("Error de sintaxis: se esperaba una llave de apertura '{' para iniciar el bloque 'else' en la sentencia IF-ELSE en la línea {}".format(p.lineno(1)))
    errores.append(mensaje)
def p_declaracion_if_else_e9(p):
    '''declaracion_if_else : IF PARENTESIS_APERTURA condiciones PARENTESIS_CIERRE LLAVE_APERTURA cuerpo LLAVE_CIERRE ELSE LLAVE_APERTURA cuerpo'''
    mensaje = ("Error de sintaxis: se esperaba una llave de cierre '}' para cerrar el bloque 'else' la sentencia if-else en la línea {}".format(p.lineno(1)))
    errores.append(mensaje)
# Sentencia IF
def p_declaracion_if_e1(p):
    '''declaracion_if : PARENTESIS_APERTURA condiciones PARENTESIS_CIERRE LLAVE_APERTURA cuerpo LLAVE_CIERRE'''
    mensaje = ("Error de sintaxis: se esperaba 'if' al inicio de la declaración de sentencia IF en la línea {}".format(p.lineno(1)))
    errores.append(mensaje)
def p_declaracion_if_e2(p):
    '''declaracion_if : IF condiciones PARENTESIS_CIERRE LLAVE_APERTURA cuerpo LLAVE_CIERRE'''
    mensaje = ("Error de sintaxis: se esperaba un parentesis de apertura '(' entre la palabra if y las condiciones de la sentencia IF en la línea {}".format(p.lineno(1)))
    errores.append(mensaje)
def p_declaracion_if_e3(p):
    '''declaracion_if : IF PARENTESIS_APERTURA PARENTESIS_CIERRE LLAVE_APERTURA cuerpo LLAVE_CIERRE'''
    mensaje = ("Error de sintaxis: se esperaba alguna condicion en if('condicion') en la sentencia IF en la línea {}".format(p.lineno(1)))
    errores.append(mensaje)
def p_declaracion_if_e4(p):
    '''declaracion_if : IF PARENTESIS_APERTURA condiciones LLAVE_APERTURA cuerpo LLAVE_CIERRE'''
    mensaje = ("Error de sintaxis: se esperaba un parentesis de cierre ')' antes de la llave de apertura '{' en la sentencia IF en la línea {}".format(p.lineno(1)))
    errores.append(mensaje)
def p_declaracion_if_e5(p):
    '''declaracion_if : IF PARENTESIS_APERTURA condiciones PARENTESIS_CIERRE cuerpo LLAVE_CIERRE'''
    mensaje = ("Error de sintaxis: se esperaba una llave de apertura '{' después del parentesis de cierre en la sentencia IF en la línea {}".format(p.lineno(1)))
    errores.append(mensaje)
def p_declaracion_if_e6(p):
    '''declaracion_if : IF PARENTESIS_APERTURA condiciones PARENTESIS_CIERRE LLAVE_APERTURA cuerpo'''
    mensaje = ("Error de sintaxis: se esperaba una llave de cierre '}' para cerrar la sentencia IF en la línea {}".format(p.lineno(1)))
    errores.append(mensaje)

# Ciclo While
def p_declaracion_while_e1(p):
    '''declaracion_while : PARENTESIS_APERTURA condicion_while PARENTESIS_CIERRE LLAVE_APERTURA cuerpo LLAVE_CIERRE'''
    mensaje = ("Error de sintaxis: se esperaba un 'while' para iniciar la declaración del ciclo WHILE en la línea {}".format(p.lineno(1)))
    errores.append(mensaje)
def p_declaracion_while_e2(p):
    '''declaracion_while : WHILE condicion_while PARENTESIS_CIERRE LLAVE_APERTURA cuerpo LLAVE_CIERRE'''
    mensaje = ("Error de sintaxis: se esperaba un parentesis de apertura '(' para iniciar el bloque de condiciones del ciclo WHILE en la línea {}".format(p.lineno(1)))
    errores.append(mensaje)
def p_declaracion_while_e3(p):
    '''declaracion_while : WHILE PARENTESIS_APERTURA  PARENTESIS_CIERRE LLAVE_APERTURA cuerpo LLAVE_CIERRE'''
    mensaje = ("Error de sintaxis: se esperaba el bloque de condiciones para la declaración del ciclo WHILE en la línea {}".format(p.lineno(1)))
    errores.append(mensaje)
def p_declaracion_while_e4(p):
    '''declaracion_while : WHILE PARENTESIS_APERTURA condicion_while LLAVE_APERTURA cuerpo LLAVE_CIERRE'''
    mensaje = ("Error de sintaxis: se esperaba un parentesis de cierre ')' para finalizar la declaración del bloque de condiciones del ciclo WHILE en la línea {}".format(p.lineno(1)))
    errores.append(mensaje)
def p_declaracion_while_e5(p):
    '''declaracion_while : WHILE PARENTESIS_APERTURA condicion_while PARENTESIS_CIERRE cuerpo LLAVE_CIERRE'''
    mensaje = ("Error de sintaxis: se esperaba una llave de apertura '{' para iniciar el bloque de código del ciclo WHILE en la línea {}".format(p.lineno(1)))
    errores.append(mensaje)
def p_declaracion_while_e6(p):
    '''declaracion_while : WHILE PARENTESIS_APERTURA condicion_while PARENTESIS_CIERRE LLAVE_APERTURA cuerpo'''
    mensaje = ("Error de sintaxis: se esperaba una llave de cierre '}' para finalizar el bloque de código del ciclo WHILE en la línea {}".format(p.lineno(1)))
    errores.append(mensaje)
# Compradores while
def p_comparadores_while_e1(p):
    '''comparadores_while : '''
    mensaje = ("Error de sintaxis: se esperaba un comparador '< / > / <= / >= / ==' en la condición del ciclo WHILE en la línea {}".format(p.lineno(1)))
    errores.append(mensaje)
# Variable while
def p_variable_while_e1(p):
    '''variable_while : '''
    mensaje = ("Error de sintaxis: se esperaba un valor 'int / ID / true / false' en la condición del ciclo WHILE en la línea {}".format(p.lineno(1)))
    errores.append(mensaje)
# Errores: Declaración de funciones con return
def p_declaracion_funcion_return_e1(p):
    ''' declaracion_funcion_return : CORCHETE_APERTURA tipo_dato CORCHETE_CIERRE ID PARENTESIS_APERTURA parametros PARENTESIS_CIERRE LLAVE_APERTURA cuerpo_funcion return LLAVE_CIERRE'''
    
    mensaje = ("Error de sintaxis: se esperaba 'funct' para iniciar la declaración de una función que devuelve un valor en la línea {}".format(p.lineno(1)))
    errores.append(mensaje)
    
def p_declaracion_funcion_return_e2(p):
    ''' declaracion_funcion_return : FUNCT tipo_dato CORCHETE_CIERRE ID PARENTESIS_APERTURA parametros PARENTESIS_CIERRE LLAVE_APERTURA cuerpo_funcion return LLAVE_CIERRE'''
    mensaje = ("Error de sintaxis: se esperaba un corchete de apertura '[' para iniciar la indicación del tipo de dato que devolverá la función en la línea {}".format(p.lineno(1)))
    errores.append(mensaje)
def p_declaracion_funcion_return_e3(p):
    ''' declaracion_funcion_return : FUNCT CORCHETE_APERTURA CORCHETE_CIERRE ID PARENTESIS_APERTURA parametros PARENTESIS_CIERRE LLAVE_APERTURA cuerpo_funcion return LLAVE_CIERRE'''
    mensaje = ("Error de sintaxis: se esperaba 'int/float/bool/string' indicar el tipo de dato que la función devolverá en la línea {}".format(p.lineno(1)))
    errores.append(mensaje)
def p_declaracion_funcion_return_e4(p):
    ''' declaracion_funcion_return : FUNCT CORCHETE_APERTURA tipo_dato ID PARENTESIS_APERTURA parametros PARENTESIS_CIERRE LLAVE_APERTURA cuerpo_funcion return LLAVE_CIERRE'''
    mensaje = ("Error de sintaxis: se esperaba un corchete de cierre ']' para iniciar la indicación del tipo de dato que devolverá la función en la línea {}".format(p.lineno(1)))
    errores.append(mensaje)
def p_declaracion_funcion_return_e5(p):
    ''' declaracion_funcion_return : FUNCT CORCHETE_APERTURA tipo_dato CORCHETE_CIERRE PARENTESIS_APERTURA parametros PARENTESIS_CIERRE LLAVE_APERTURA cuerpo_funcion return LLAVE_CIERRE'''
    mensaje = ("Error de sintaxis: se esperaba el 'ID' de identificación de la función en la línea {}".format(p.lineno(1)))
    errores.append(mensaje)
def p_declaracion_funcion_return_e6(p):
    ''' declaracion_funcion_return : FUNCT CORCHETE_APERTURA tipo_dato CORCHETE_CIERRE ID parametros PARENTESIS_CIERRE LLAVE_APERTURA cuerpo_funcion return LLAVE_CIERRE'''
    mensaje = ("Error de sintaxis: se esperaba el parentesis de apertura '(' para iniciar la declaración de parámetros de función return en la línea {}".format(p.lineno(1)))
    errores.append(mensaje)
def p_declaracion_funcion_return_e7(p):
    ''' declaracion_funcion_return : FUNCT CORCHETE_APERTURA tipo_dato CORCHETE_CIERRE ID PARENTESIS_APERTURA parametros LLAVE_APERTURA cuerpo_funcion return LLAVE_CIERRE'''
    mensaje = ("Error de sintaxis: se esperaba el parentesis de apertura '(' para finalizar la declaración de parámetros de función return en la línea {}".format(p.lineno(1)))
    errores.append(mensaje)
def p_declaracion_funcion_return_e8(p):
    ''' declaracion_funcion_return : FUNCT CORCHETE_APERTURA tipo_dato CORCHETE_CIERRE ID PARENTESIS_APERTURA parametros PARENTESIS_CIERRE cuerpo_funcion return LLAVE_CIERRE'''
    mensaje = ("Error de sintaxis: se esperaba una llave de apertura '{' para iniciar el bloque de código de la función return en la línea {}".format(p.lineno(1)))
    errores.append(mensaje)
def p_declaracion_funcion_return_e9(p):
    ''' declaracion_funcion_return : FUNCT CORCHETE_APERTURA tipo_dato CORCHETE_CIERRE ID PARENTESIS_APERTURA parametros PARENTESIS_CIERRE LLAVE_APERTURA cuerpo_funcion return'''
    mensaje = ("Error de sintaxis: se esperaba una llave de cierre '{' para finalizar el bloque de código de la función return en la línea {}".format(p.lineno(1)))
    errores.append(mensaje)
# Errores: Return
def p_return_e1(p):
    '''return : ID PUNTO_COMA'''    
    mensaje = ("Error de sintaxis: se esperaba 'return' para iniciar el retorno del valor en función return en la línea {}".format(p.lineno(1)))
    errores.append(mensaje)
def p_return_e2(p):
    '''return : RETURN PUNTO_COMA'''    
    mensaje = ("Error de sintaxis: se esperaba el 'ID' de la variable para del valor en función return en la línea {}".format(p.lineno(1)))
    errores.append(mensaje)
def p_return_e3(p):
    '''return : RETURN ID'''    
    mensaje = ("Error de sintaxis: se esperaba un ';' para finalizar el retorno del valor en función return en la línea {}".format(p.lineno(1)))
    errores.append(mensaje)
# Errores: Declaración de funciones
def p_declaracion_funcion_e1(p):
    ''' declaracion_funcion : ID PARENTESIS_APERTURA parametros PARENTESIS_CIERRE LLAVE_APERTURA cuerpo_funcion LLAVE_CIERRE'''
    mensaje = ("Error de sintaxis: se esperaba 'funct' para iniciar la declaración de una función en la línea {}".format(p.lineno(1)))
    errores.append(mensaje)
def p_declaracion_funcion_e2(p):
    ''' declaracion_funcion : FUNCT PARENTESIS_APERTURA parametros PARENTESIS_CIERRE LLAVE_APERTURA cuerpo_funcion LLAVE_CIERRE'''
    mensaje = ("Error de sintaxis: se esperaba un 'ID' para la identificación de la función en la línea {}".format(p.lineno(1)))
    errores.append(mensaje)
def p_declaracion_funcion_e3(p):
    ''' declaracion_funcion : FUNCT ID parametros PARENTESIS_CIERRE LLAVE_APERTURA cuerpo_funcion LLAVE_CIERRE'''
    mensaje = ("Error de sintaxis: se esperaba un parentesis de apertura '(' para iniciar la declaración de los parámetros de la función en la línea {}".format(p.lineno(1)))
    errores.append(mensaje)
def p_declaracion_funcion_e4(p):
    ''' declaracion_funcion : FUNCT ID PARENTESIS_APERTURA parametros LLAVE_APERTURA cuerpo_funcion LLAVE_CIERRE'''
    mensaje = ("Error de sintaxis: se esperaba un parentesis de cierre '(' para finalizar la declaración de los parámetros de la función en la línea {}".format(p.lineno(1)))
    errores.append(mensaje)
def p_declaracion_funcion_e5(p):
    ''' declaracion_funcion : FUNCT ID PARENTESIS_APERTURA parametros PARENTESIS_CIERRE cuerpo_funcion LLAVE_CIERRE'''
    mensaje = ("Error de sintaxis: se esperaba una llave de apertura '{' para iniciar el bloque de código de la función en la línea {}".format(p.lineno(1)))
    errores.append(mensaje)
def p_declaracion_funcion_e6(p):
    ''' declaracion_funcion : FUNCT ID PARENTESIS_APERTURA parametros PARENTESIS_CIERRE LLAVE_APERTURA cuerpo_funcion'''
    mensaje = ("Error de sintaxis: se esperaba una llave de cierre '}' para finalizar el bloque de código de la función en la línea {}".format(p.lineno(1)))
    errores.append(mensaje)
# Errores: Parámetro
def p_parametro_e1(p):
    '''parametro : PARENTESIS_APERTURA tipo_dato PARENTESIS_CIERRE '''
    mensaje = ("Error de sintaxis: se esperaba el nombre del parámetro 'ID' en la declaración de los parámetros en la línea {}".format(p.lineno(1)))
    errores.append(mensaje)
def p_parametro_e2(p):
    '''parametro : ID tipo_dato PARENTESIS_CIERRE '''
    mensaje = ("Error de sintaxis: se esperaba un parentesis de apertura '(' para inicio a la indicación del tipo de dato del parámetro en declaración de los parámetros en la línea {}".format(p.lineno(1)))
    errores.append(mensaje)
def p_parametro_e3(p):
    '''parametro : ID PARENTESIS_APERTURA PARENTESIS_CIERRE '''
    mensaje = ("Error de sintaxis: se esperaba 'int/float/bool/string' dentro de los parentesis '( )' de la declaración de los parámetros en la línea {}".format(p.lineno(1)))
    errores.append(mensaje)
def p_parametro_e4(p):
    '''parametro : ID PARENTESIS_APERTURA tipo_dato '''
    mensaje = ("Error de sintaxis: se esperaba un parentesis de de cierre ')' para finalizar a la indicación del tipo de dato del parámetro en declaración de los parámetros en la línea {}".format(p.lineno(1)))
    errores.append(mensaje)
# Erorres: Asignación: Var-Var, Var-FunReturn y Var-ObjeFunReturn
# Var-var
def p_asignacion_variable_variable_e1(p):
    ''' asignacion_variable_variable : PARENTESIS_APERTURA tipo_dato PARENTESIS_CIERRE ASIGNAR ID PARENTESIS_APERTURA tipo_dato PARENTESIS_CIERRE PUNTO_COMA'''
    mensaje = ("Error de sintaxis: se esperaba un identificador 'ID' para el inicio de asignación variable-variable en la línea {}".format(p.lineno(1)))
    errores.append(mensaje)
def p_asignacion_variable_variable_e2(p):
    ''' asignacion_variable_variable : ID tipo_dato PARENTESIS_CIERRE ASIGNAR ID PARENTESIS_APERTURA tipo_dato PARENTESIS_CIERRE PUNTO_COMA'''
    mensaje = ("Error de sintaxis: se esperaba un parentesis de apertura '(' después del indentificiador 'ID' en la asiganción variable-variable en la línea {}".format(p.lineno(1)))
    errores.append(mensaje)
def p_asignacion_variable_variable_e3(p):
    ''' asignacion_variable_variable : ID PARENTESIS_APERTURA PARENTESIS_CIERRE ASIGNAR ID PARENTESIS_APERTURA tipo_dato PARENTESIS_CIERRE PUNTO_COMA'''
    mensaje = ("Error de sintaxis: se esperaba el tipo de dato 'int/float/bool/string' entre parentesis '( )' en la asignación variable-variable en la línea {}".format(p.lineno(1)))
    errores.append(mensaje)
def p_asignacion_variable_variable_e4(p):
    ''' asignacion_variable_variable : ID PARENTESIS_APERTURA tipo_dato ASIGNAR ID PARENTESIS_APERTURA tipo_dato PARENTESIS_CIERRE PUNTO_COMA'''
    mensaje = ("Error de sintaxis: se esperaba un parentesis de cierre ')' después del tipo de dato 'int/float/bool/string' en la asiganción variable-variable en la línea {}".format(p.lineno(1)))
    errores.append(mensaje)
def p_asignacion_variable_variable_e5(p):
    ''' asignacion_variable_variable : ID PARENTESIS_APERTURA tipo_dato PARENTESIS_CIERRE ID PARENTESIS_APERTURA tipo_dato PARENTESIS_CIERRE PUNTO_COMA'''
    mensaje = ("Error de sintaxis: se esperaba una asignación '=' después de la primera variable y antes de iniciar la segunda en asignación varaible-variable en la línea {}".format(p.lineno(1)))
    errores.append(mensaje)
def p_asignacion_variable_variable_e6(p):
    ''' asignacion_variable_variable : ID PARENTESIS_APERTURA tipo_dato PARENTESIS_CIERRE ASIGNAR PARENTESIS_APERTURA tipo_dato PARENTESIS_CIERRE PUNTO_COMA'''
    mensaje = ("Error de sintaxis: se esperaba un identificador 'ID' para el inicio de la 2da variable en asignación variable-variable en la línea {}".format(p.lineno(1)))
    errores.append(mensaje)
def p_asignacion_variable_variable_e7(p):
    ''' asignacion_variable_variable : ID PARENTESIS_APERTURA tipo_dato PARENTESIS_CIERRE ASIGNAR ID tipo_dato PARENTESIS_CIERRE PUNTO_COMA'''
    mensaje = ("Error de sintaxis: se esperaba un parentesis de apertura '(' después del indentificiador 'ID' de la 2da variable en la asiganción variable-variable en la línea {}".format(p.lineno(1)))
    errores.append(mensaje)
def p_asignacion_variable_variable_e8(p):
    ''' asignacion_variable_variable : ID PARENTESIS_APERTURA tipo_dato PARENTESIS_CIERRE ASIGNAR ID PARENTESIS_APERTURA PARENTESIS_CIERRE PUNTO_COMA'''
    mensaje = ("Error de sintaxis: se esperaba el tipo de dato 'int/float/bool/string' entre parentesis '( )' de la 2da variable en la asignación variable-variable en la línea {}".format(p.lineno(1)))
    errores.append(mensaje)
def p_asignacion_variable_variable_e9(p):
    ''' asignacion_variable_variable : ID PARENTESIS_APERTURA tipo_dato PARENTESIS_CIERRE ASIGNAR ID PARENTESIS_APERTURA tipo_dato PUNTO_COMA'''
    mensaje = ("Error de sintaxis: se esperaba un parentesis de cierre ')' después del tipo de dato 'int/float/bool/string' de la 2da variable en la asiganción variable-variable en la línea {}".format(p.lineno(1)))
    errores.append(mensaje)
def p_asignacion_variable_variable_e10(p):
    ''' asignacion_variable_variable : ID PARENTESIS_APERTURA tipo_dato PARENTESIS_CIERRE ASIGNAR ID PARENTESIS_APERTURA tipo_dato PARENTESIS_CIERRE'''
    mensaje = ("Error de sintaxis: se esperaba un punto y coma ';' después del parentesis de cierre ')' de la 2da variable en la asiganción variable-variable en la línea {}".format(p.lineno(1)))
    errores.append(mensaje)
# Var-FunReturn
def p_asignacion_variable_funcion_return_e1(p):
    ''' asignacion_variable_funcion_return : PARENTESIS_APERTURA tipo_dato PARENTESIS_CIERRE ASIGNAR CORCHETE_APERTURA tipo_dato CORCHETE_CIERRE ID PARENTESIS_APERTURA parametros PARENTESIS_CIERRE PUNTO_COMA'''
    mensaje = ("Error de sintaxis: se esperaba un identificador 'ID' para el inicio de asignación variable-FuncionReturn en la línea {}".format(p.lineno(1)))
    errores.append(mensaje)
def p_asignacion_variable_funcion_return_e2(p):
    ''' asignacion_variable_funcion_return : ID tipo_dato PARENTESIS_CIERRE ASIGNAR CORCHETE_APERTURA tipo_dato CORCHETE_CIERRE ID PARENTESIS_APERTURA parametros PARENTESIS_CIERRE PUNTO_COMA'''
    mensaje = ("Error de sintaxis: se esperaba un parentesis de apertura '(' después del indentificiador 'ID' en la asiganción variable-FuncionReturn en la línea {}".format(p.lineno(1)))
    errores.append(mensaje)
def p_asignacion_variable_funcion_return_e3(p):
    ''' asignacion_variable_funcion_return : ID PARENTESIS_APERTURA PARENTESIS_CIERRE ASIGNAR CORCHETE_APERTURA tipo_dato CORCHETE_CIERRE ID PARENTESIS_APERTURA parametros PARENTESIS_CIERRE PUNTO_COMA'''
    mensaje = ("Error de sintaxis: se esperaba el tipo de dato 'int/float/bool/string' entre parentesis '( )' en la asignación variable-FuncionReturn en la línea {}".format(p.lineno(1)))
    errores.append(mensaje)
def p_asignacion_variable_funcion_return_e4(p):
    ''' asignacion_variable_funcion_return : ID PARENTESIS_APERTURA tipo_dato ASIGNAR CORCHETE_APERTURA tipo_dato CORCHETE_CIERRE ID PARENTESIS_APERTURA parametros PARENTESIS_CIERRE PUNTO_COMA'''
    mensaje = ("Error de sintaxis: se esperaba un parentesis de cierre ')' después del tipo de dato 'int/float/bool/string' en la asiganción variable-FuncionReturn en la línea {}".format(p.lineno(1)))
    errores.append(mensaje)
def p_asignacion_variable_funcion_return_e5(p):
    ''' asignacion_variable_funcion_return : ID PARENTESIS_APERTURA tipo_dato PARENTESIS_CIERRE CORCHETE_APERTURA tipo_dato CORCHETE_CIERRE ID PARENTESIS_APERTURA parametros PARENTESIS_CIERRE PUNTO_COMA'''
    mensaje = ("Error de sintaxis: se esperaba una asignación '=' después de la primera variable y antes de iniciar la segunda en asignación variable-FuncionReturn en la línea {}".format(p.lineno(1)))
    errores.append(mensaje)
def p_asignacion_variable_funcion_return_e6(p):
    ''' asignacion_variable_funcion_return : ID PARENTESIS_APERTURA tipo_dato PARENTESIS_CIERRE ASIGNAR tipo_dato CORCHETE_CIERRE ID PARENTESIS_APERTURA parametros PARENTESIS_CIERRE PUNTO_COMA'''
    mensaje = ("Error de sintaxis: se esperaba un corchete de apertura '[' después del asignar '=' en asignación variable-FuncionReturn en la línea {}".format(p.lineno(1)))
    errores.append(mensaje)
def p_asignacion_variable_funcion_return_e7(p):
    ''' asignacion_variable_funcion_return : ID PARENTESIS_APERTURA tipo_dato PARENTESIS_CIERRE ASIGNAR CORCHETE_APERTURA CORCHETE_CIERRE ID PARENTESIS_APERTURA parametros PARENTESIS_CIERRE PUNTO_COMA'''
    mensaje = ("Error de sintaxis: se esperaba el tipo de dato de retorno 'int/float/bool/' dentro de los corchetes '[ ]' antes del nombre de la función en asignación variable-FuncionReturn en la línea {}".format(p.lineno(1)))
    errores.append(mensaje)
def p_asignacion_variable_funcion_return_e8(p):
    ''' asignacion_variable_funcion_return : ID PARENTESIS_APERTURA tipo_dato PARENTESIS_CIERRE ASIGNAR CORCHETE_APERTURA tipo_dato ID PARENTESIS_APERTURA parametros PARENTESIS_CIERRE PUNTO_COMA'''
    mensaje = ("Error de sintaxis: se esperaba un corchete de cierre ']' después del tipo de dato 'int/float/bool/string' en asignación variable-FuncionReturn en la línea {}".format(p.lineno(1)))
    errores.append(mensaje)
def p_asignacion_variable_funcion_return_e10(p):
    ''' asignacion_variable_funcion_return : ID PARENTESIS_APERTURA tipo_dato PARENTESIS_CIERRE ASIGNAR CORCHETE_APERTURA tipo_dato CORCHETE_CIERRE PARENTESIS_APERTURA parametros PARENTESIS_CIERRE PUNTO_COMA'''
    mensaje = ("Error de sintaxis: se esperaba un identificador 'ID' para la función después de los corchetes '[ ]' en asignación variable-FuncionReturn en la línea {}".format(p.lineno(1)))
    errores.append(mensaje)
def p_asignacion_variable_funcion_return_e11(p):
    ''' asignacion_variable_funcion_return : ID PARENTESIS_APERTURA tipo_dato PARENTESIS_CIERRE ASIGNAR CORCHETE_APERTURA tipo_dato CORCHETE_CIERRE ID parametros PARENTESIS_CIERRE PUNTO_COMA'''
    mensaje = ("Error de sintaxis: se esperaba un parentesis de apertura '(' después del indentificiador 'ID' de la función en la asiganción variable-FuncionReturn en la línea {}".format(p.lineno(1)))
    errores.append(mensaje)
def p_asignacion_variable_funcion_return_e12(p):
    ''' asignacion_variable_funcion_return : ID PARENTESIS_APERTURA tipo_dato PARENTESIS_CIERRE ASIGNAR CORCHETE_APERTURA tipo_dato CORCHETE_CIERRE ID PARENTESIS_APERTURA parametros PUNTO_COMA'''
    mensaje = ("Error de sintaxis: se esperaba un parentesis de apertura ')' después de la declaración de parámetros de la función en la asiganción variable-FuncionReturn en la línea {}".format(p.lineno(1)))
    errores.append(mensaje)
def p_asignacion_variable_funcion_return_e13(p):
    ''' asignacion_variable_funcion_return : ID PARENTESIS_APERTURA tipo_dato PARENTESIS_CIERRE ASIGNAR CORCHETE_APERTURA tipo_dato CORCHETE_CIERRE ID PARENTESIS_APERTURA parametros PARENTESIS_CIERRE'''
    mensaje = ("Error de sintaxis: se esperaba un punto y coma ';' para finalizar la asiganción variable-FuncionReturn en la línea {}".format(p.lineno(1)))
    errores.append(mensaje)

# Llamadas: funciones y funciones return

# Funcion return
def p_llamar_funcion_return_e1(p):
    '''llamar_funcion_return : tipo_dato CORCHETE_CIERRE ID PARENTESIS_APERTURA parametros PARENTESIS_CIERRE PUNTO_COMA'''
    mensaje = ("Error de sintaxis: se esperaba un corchete de apertura '[' para iniciar la llamada de una función return en la línea {}".format(p.lineno(1)))
    errores.append(mensaje)
def p_llamar_funcion_return_e2(p):
    '''llamar_funcion_return : CORCHETE_APERTURA CORCHETE_CIERRE ID PARENTESIS_APERTURA parametros PARENTESIS_CIERRE PUNTO_COMA'''
    mensaje = ("Error de sintaxis: se esperaba un tipo de dato 'int/float/bool/string' entre corchetes '[ ]' en llamada de una función return en la línea {}".format(p.lineno(1)))
    errores.append(mensaje)
def p_llamar_funcion_return_e3(p):
    '''llamar_funcion_return : CORCHETE_APERTURA tipo_dato ID PARENTESIS_APERTURA parametros PARENTESIS_CIERRE PUNTO_COMA'''
    mensaje = ("Error de sintaxis: se esperaba un corchete de cierre ']' en el llamado de función return en la línea {}".format(p.lineno(1)))
    errores.append(mensaje)
def p_llamar_funcion_return_e4(p):
    '''llamar_funcion_return : CORCHETE_APERTURA tipo_dato CORCHETE_CIERRE PARENTESIS_APERTURA parametros PARENTESIS_CIERRE PUNTO_COMA'''
    mensaje = ("Error de sintaxis: se esperaba el identificador de la función return 'ID' después del corchete de cierre ']' en la línea {}".format(p.lineno(1)))
    errores.append(mensaje)
def p_llamar_funcion_return_e5(p):
    '''llamar_funcion_return : CORCHETE_APERTURA tipo_dato CORCHETE_CIERRE ID parametros PARENTESIS_CIERRE PUNTO_COMA'''
    mensaje = ("Error de sintaxis: se esperaba un parentesis de apertura '(' después del identificador de la función en la línea {}".format(p.lineno(1)))
    errores.append(mensaje)
def p_llamar_funcion_return_e6(p):
    '''llamar_funcion_return : CORCHETE_APERTURA tipo_dato CORCHETE_CIERRE ID PARENTESIS_APERTURA parametros PUNTO_COMA'''
    mensaje = ("Error de sintaxis: se esperaba un parentesis de cierre ')' después de la declaración de los parámetros del llamado de la función return en la línea {}".format(p.lineno(1)))
    errores.append(mensaje)
def p_llamar_funcion_return_e7(p):
    '''llamar_funcion_return : CORCHETE_APERTURA tipo_dato CORCHETE_CIERRE ID PARENTESIS_APERTURA parametros PARENTESIS_CIERRE'''
    mensaje = ("Error de sintaxis: se esperaba un punto y coma ';' para finalizar llamada de la función return en la línea {}".format(p.lineno(1)))
    errores.append(mensaje)

# Funcion
def p_llamar_funcion_e1(p):
    '''llamar_funcion : PARENTESIS_APERTURA parametros PARENTESIS_CIERRE PUNTO_COMA'''
    mensaje = ("Error de sintaxis: se esperaba un identificador 'ID' para iniciar el llamado a una función en la línea {}".format(p.lineno(1)))
    errores.append(mensaje)
def p_llamar_funcion_e2(p):
    '''llamar_funcion : ID parametros PARENTESIS_CIERRE PUNTO_COMA'''
    mensaje = ("Error de sintaxis: se esperaba un parentesis de apertura '(' para iniciar la declaración de los parámetros en el llamado de una función en la línea {}".format(p.lineno(1)))
    errores.append(mensaje)
def p_llamar_funcion_e3(p):
    '''llamar_funcion : ID PARENTESIS_APERTURA parametros PUNTO_COMA'''
    mensaje = ("Error de sintaxis: se esperaba un parentesis de cierre ')' para finalizar la declaración de los parámetros en el llamado de una función en la línea {}".format(p.lineno(1)))
    errores.append(mensaje)
def p_llamar_funcion_e4(p):
    '''llamar_funcion : ID PARENTESIS_APERTURA parametros PARENTESIS_CIERRE'''
    mensaje = ("Error de sintaxis: se esperaba un punto y coma ';' para finalizar el llamado de una función  en la línea {}".format(p.lineno(1)))
    errores.append(mensaje)

# Variables y comparadores
def p_variable_e1(p):
    ''' variable : '''
    mensaje = ("Error de sintaxis: se esperaba un 'ID / numero_entero o flotante / cadena / true / false' para la variable  en la línea {}".format(p.lineno(1)))
    errores.append(mensaje)
def p_comparadores_e1(p):
    ''' comparadores : '''
    mensaje = ("Error de sintaxis: se esperaba un '== / > / >= / < / <=' para los comparadores de variables en la línea {}".format(p.lineno(1)))
    errores.append(mensaje)

# Decrementro e incremento
def p_incremento_individual_e1(p):
    ''' incremento_individual : INCREMENTO PUNTO_COMA'''
    mensaje = ("Error de sintaxis: se esperaba un identificador 'ID' al inicio del incremento para una variable en la línea {}".format(p.lineno(1)))
    errores.append(mensaje)
def p_incremento_individual_e2(p):
    ''' incremento_individual : ID PUNTO_COMA'''
    mensaje = ("Error de sintaxis: se esperaba un incremento '++' después del identificador 'ID' de una variable y antes del punto y coma ';' en la línea {}".format(p.lineno(1)))
    errores.append(mensaje)
def p_incremento_individual_e3(p):
    ''' incremento_individual : ID INCREMENTO '''
    mensaje = ("Error de sintaxis: se esperaba un punto y coma ';' para finalizar el incremento  para una variable en la línea {}".format(p.lineno(1)))
    errores.append(mensaje)

def p_decremento_individual_e1(p):
    ''' decremento_individual : DECREMENTO PUNTO_COMA'''
    mensaje = ("Error de sintaxis: se esperaba un identificador 'ID' al inicio del decremento para una variable en la línea {}".format(p.lineno(1)))
    declaracionesRegistro.append(mensaje)
def p_decremento_individual_e2(p):
    ''' decremento_individual : ID PUNTO_COMA'''
    mensaje = ("Error de sintaxis: se esperaba un decremento '++' después del identificador 'ID' de una variable y antes del punto y coma ';' en la línea {}".format(p.lineno(1)))
    declaracionesRegistro.append(mensaje)
def p_decremento_individual_e3(p):
    ''' decremento_individual : ID DECREMENTO'''
    mensaje = ("Error de sintaxis: se esperaba un punto y coma ';' para finalizar el decremento  para una variable en la línea {}".format(p.lineno(1)))
    declaracionesRegistro.append(mensaje)


# Errores ------------------------------------------------------------------------------------------------------------------------------------------------
##########################################################################################################################################################

# ########################################################################################################################################################
# ERRORES GRAMATICALES - SEMANTICOS
def p_declaracion_variable_es1(p):
    'declaracion_variable : palabras_reservadas PARENTESIS_APERTURA tipo_dato PARENTESIS_CIERRE ASIGNAR valor_dato PUNTO_COMA'
    identificador = p[1]
    mensaje = (f"Error Semántico: 'ID' <{identificador}> inválido, los tipos de datos <int, float, bool, string> no se pueden usar como identificador de la variable")
    errores.append(mensaje)
# ########################################################################################################################################################

# Manejo de errores de sintaxis
def find_column(input, token):
    last_cr = input.rfind('\n', 0, token.lexpos)
    if last_cr < 0:
        last_cr = -1
    return token.lexpos - last_cr

def p_error(p):
    if p:
        col = find_column(p.lexer.lexdata, p)
        error_message = f"Error de sintaxis en línea {p.lineno}, columna {col}: '{p.value}'"
        print(error_message)
        errores.append(error_message)
        parser.errok()
    else:
        error_message = "Error de sintaxis en EOF o faltó ';'"
        print(error_message)
        errores.append(error_message)
        
def parse(codigo):
    global errores
    parser = yacc.yacc()
    errores = []
    tabla_simbolos.reinicio_clase()
    parser.parse(codigo)
    errores.extend(tabla_simbolos.obtener_errores())
    return errores


def obtener_errores():
    return errores

# Construir el analizador sintáctico
parser = yacc.yacc()

# Función para realizar el análisis sintáctico
def analisis_sintactico(cadena):
    global errores
    errores=[]
    return parser.parse(cadena)
def crearASA(tree, dot, parent_id=None):
        if isinstance(tree, list):
            for item in tree:
                crearASA(item, dot, parent_id)
        elif isinstance(tree, tuple):
        #Se agrego la excepcion  para construirlo y parar justo cuando hay un error
            try:
                node_id = str(id(tree))
                label = str(tree[0])
                dot.node(node_id, label=label)
                
                if parent_id:
                    dot.edge(parent_id, node_id)
                
                for child in tree[1:]:
                    crearASA(child, dot, node_id)
            except Exception as e:
                print(f'Error al procesar nodo {tree}: {e}')
        else:
            try:
                node_id = str(id(tree))
                label = str(tree)
                dot.node(node_id, label=label)
                
                if parent_id:
                    dot.edge(parent_id, node_id)
            except Exception as e:
                print(f'Error al procesar nodo {tree}: {e}')

def recolectar_declaraciones(tree):
    if not tree:
        return []
    if tree[0] == 'declaracion':
        return [tree[1:]]
    else:
        return sum((recolectar_declaraciones(child) for child in tree[1:]), [])

if __name__ == '__main__':
    # codigo = '''
    # bring default.operations as operaciones;
    # class Podar{
        
    #     // Variables
    #     variableInt(string) = 2.0;
        
    #     // Crear un objeto
    #     new operaciones(object) from operations;
        
    #     // Encender dispositivo y ponerlo en marcha
    #     operaciones operations.turnOn();
    #     operaciones operations.go();
        
    #     // Declarar distancia para poder podar un cuadrado
    #     distancia(int) = 8;
        
    #     while(distancias > 0){
            
    #         // ¿La temperatura de la podadora es igual o mayor a 60 grados?
    #         if( operaciones operations.tooHot() >= 60 ){
    #             // Sí entonces deten su funcionamiento
    #             operaciones operations.stop();    
    #         }
            
    #         // ¿La podadora no se ha encontrado con un obstaculo?
    #         if( operaciones operations.emptyWay() == false){
                
    #             // Se ha encontrado obstaculo
    #             while ( [bool] isEmpty() == false ){
    #                 // entonces comenzarás a girar hasta tener el camino libre
    #                 operaciones operations.spin(90)   
    #             }
                
    #             // Se ha encontrado el camino libre (fin del ciclo)
    #             // Avanza de nuevo
    #             operaciones operations.go();
    #         }
            
    #         // distancia consumida
    #         distancia--;
    #     }
        
    #     // Al consumir su distancia total detener el
    #     operaciones operations.stop();
        
    # }//class
    # '''

    # resultado = analisis_sintactico(codigo)
     
    # def analizarCodigo (codigo):
    #     resultado = analisis_sintactico(codigo)
    #     return resultado
     
    
    print("Declaraciones:")
    for dec in declaracionesRegistro:
        print(dec)

    

    print("Errores encontrados:")
    for error in errores:
        print(error)

     # Construcción del arbol
    dot = Digraph(comment='AST')
    try:
        crearASA(resultado, dot)
    except Exception as e:
        print(f'Error crítico al construir el árbol: {e}')
    dot.render('ast', view=True)