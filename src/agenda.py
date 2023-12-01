"""
27/11/2023

Práctica del examen para realizar en casa
-----------------------------------------

* El programa debe estar correctamente documentado.

* Debes intentar ajustarte lo máximo que puedas a lo que se pide en los comentarios TODO.

* Tienes libertad para desarrollar los métodos o funciones que consideres, pero estás obligado a usar como mínimo todos los que se solicitan en los comentarios TODO.

* Además, tu programa deberá pasar correctamente las pruebas unitarias que se adjuntan en el fichero test_agenda.py, por lo que estás obligado a desarrollar los métodos que se importan y prueban en la misma: pedir_email(), validar_email() y validar_telefono()

"""

import os
import pathlib
import copy
from os import path


# Constantes globales
RUTA = pathlib.Path(__file__).parent.absolute() 

NOMBRE_FICHERO = 'contactos.csv'

RUTA_FICHERO = path.join(RUTA, NOMBRE_FICHERO)

#TODO: Crear un conjunto con las posibles opciones del menú de la agenda -> DONE
OPCIONES_MENU = {1, 2, 3, 4, 5, 6, 7, 8}
#TODO: Utiliza este conjunto en las funciones agenda() y pedir_opcion()


def borrar_consola():
    """ Limpia la consola
    """
    if os.name == "posix":
        os.system ("clear")
    elif os.name == "ce" or os.name == "nt" or os.name == "dos":
        os.system ("cls")


def cargar_contactos(contactos: list):
    """ Carga los contactos iniciales de la agenda desde un fichero
    ...
    """
    #TODO: Controlar los posibles problemas derivados del uso de ficheros... -> DONE
    lista_fichero = []
    try:
        with open(RUTA_FICHERO, 'r') as fichero:
                for linea in fichero:
                    lista_fichero.append(linea.strip().split("\n"))
        for i in range(len(lista_fichero)):
            lista_fichero[i] = lista_fichero[i][0].split(";")
    except Exception:
        print("El fichero dado no existe.")

    for dato in lista_fichero:
        diccionario_datos = {}
        diccionario_datos["nombre"] = dato[0]
        diccionario_datos["apellido"] = dato[1]
        diccionario_datos["email"] = dato[2]
        diccionario_datos["telefonos"] = [dato[i] for i in range(3, len(dato))]
        contactos.append(diccionario_datos)

    return contactos


def buscar_contacto(contactos: list, email: str) -> int:
    #pytest
    pos = None

    for num_contacto in range(len(contactos)):
        if contactos[num_contacto]["email"] == email:
            pos = num_contacto
    
    return pos

    
def eliminar_contacto(contactos: list, email: str):
    """ Elimina un contacto de la agenda
    ...
    """
    try:
        #TODO: Crear función buscar_contacto para recuperar la posición de un contacto con un email determinado -> DONE
        pos = buscar_contacto(contactos, email)

        if pos != None:
            del contactos[pos]
            print("Se eliminó 1 contacto")
        else:
            print("No se encontró el contacto para eliminar")
    except Exception as e:
        print(f"**Error** {e}")
        print("No se eliminó ningún contacto")


def mostrar_menu():
    print("AGENDA")
    print("------")
    print("1. Nuevo contacto")
    print("2. Modificar contacto")
    print("3. Eliminar contacto")
    print("4. Vaciar agenda")
    print("5. Cargar agenda inicial")
    print("6. Mostrar contactos por criterio")
    print("7. Mostrar la agenda completa")
    print("8. Salir")


def pedir_opcion():

    try:
        opcion = int(input(">> Seleccione una opción: "))
        if 1 > opcion or 8 < opcion :
            opcion = -1    
    except ValueError:
        opcion = -1

    return opcion


def pedir_nombre_y_apellido() -> list:
    #pytest
    nombre = input("Introduzca su nombre y primer apellido: ").strip().split(" ")

    if len(nombre) < 2:
        raise Exception

    nombre, apellido = separar_nombre_y_apellido(nombre)

    return nombre, apellido


def separar_nombre_y_apellido(nombre: list):
    #pytest
    for elemento in range(len(nombre)):
        nombre[elemento] = nombre[elemento].capitalize()

    apellido = nombre[-1]
    nombre.pop()
    nombre = " ".join(nombre)

    return nombre, apellido


def validar_email(email: str, contactos: list, buscar_en_lista: bool):
    #No funciona
    if len(email.strip()) == 0:
        raise ValueError("el email no puede ser una cadena vacía")

    if "@" not in email or "." not in email.split("@")[1] or len(email.split("@")[0]) == 0 or len(email.split("@")[1].split(".")[0]) == 0 or len(email.split("@")[1].split(".")[1]) == 0:
        raise ValueError("el email no es un correo válido")

    if buscar_en_lista == True:
        posicion = buscar_contacto(contactos, email)
        if posicion != None:
            raise ValueError("el email ya existe en la agenda")
        
    return email


def pedir_email(contactos: list, buscar_en_lista: bool) -> str:
    #No funciona
    email = input("Ingrese su correo: ").lower().strip()

    email = validar_email(email, contactos, buscar_en_lista)
    
    return email


def validar_telefono(telefono: str) -> bool:
    
    telefono = telefono.replace(" ", "")

    if len(telefono) == 9 and telefono.isdecimal():
        return True
    elif len(telefono) == 12 and telefono[:3] == "+34" and telefono[1:].isdecimal():
        return True
    else:
        return False


def pedir_telefono():

    telefono = input()

    if not telefono:
        return None
    else:
        if not validar_telefono(telefono):
            raise Exception
            
        return telefono.replace(" ", "")
        

def agregar_contacto(contactos: list):
    try:
        diccionario_datos = {}
        diccionario_datos["nombre"], diccionario_datos["apellido"] = pedir_nombre_y_apellido()
        diccionario_datos["email"] = pedir_email(contactos, True)

        lista_telefonos = []
        todo_ok = False
        contador_telefono = 0
        print("Ingresa los telefonos:")
        while not todo_ok:
            print(f"({contador_telefono})==> ", end="")
            telefono = pedir_telefono()
            if telefono == None:
                todo_ok = True
            else:
                lista_telefonos.append(telefono)
                contador_telefono += 1
        diccionario_datos["telefonos"] = lista_telefonos

        contactos.append(diccionario_datos)
    except Exception as e:
        print(e)
        print("Error, no se agregó ningún contacto.")


def vaciar_agenda(contactos: list):
    contactos = []
    return contactos


def mostrar_menu_limitado(msj: str):
    print("------")
    print(f"1. {msj} nombre")
    print(f"2. {msj} apellido")
    print(f"3. {msj} email")
    print(f"4. {msj} telefonos")
    print(f"5. Salir")


def pedir_opcion_limitado():

    todo_ok = False
    
    while not todo_ok:
        try:
            opcion = int(input(">> Seleccione una opción: "))
            if opcion not in OPCIONES_MENU - {6, 7, 8}:
                opcion = -1
            todo_ok = True    
        except ValueError:
            print("Error, por favor introduzca solo números enteros del 1 al 5.")

    return opcion


def modificar_contacto(contactos: list):
    borrar_consola()
    contactos_temporal = copy.deepcopy(contactos)
    try:
        email = pedir_email(contactos, False)

        pos_contacto = buscar_contacto(contactos, email)
        if pos_contacto == None:
            raise ValueError("el email no existe en la agenda")
        else:
            opcion = None
            contactos[pos_contacto]
            while opcion != 5:
                borrar_consola()
                mostrar_menu_limitado("Modificar")
                opcion = pedir_opcion_limitado()

                if opcion == 1:
                    contactos[pos_contacto]["nombre"] = input("Introduzca un nuevo nombre: ").strip().capitalize()
                    if len(contactos[pos_contacto]["nombre"]) == 0:
                        raise ValueError("Error, no se admiten nombres vacíos.")
                    pulse_tecla_para_continuar()
                elif opcion == 2: 
                    contactos[pos_contacto]["apellido"] = input("Introduzca un nuevo apellido: ").replace(" ", "").capitalize()
                    if len(contactos[pos_contacto]["nombre"]) == 0:
                        raise ValueError("Error, no se admiten apellidos vacíos.")
                    pulse_tecla_para_continuar()
                elif opcion == 3: 
                    nuevo_email = pedir_email(contactos_temporal, False)
                    pos = None

                    for num_contacto in range(len(contactos)):
                        if contactos[num_contacto]["email"] == nuevo_email:
                            pos = num_contacto

                    if pos == None:        
                        contactos[pos_contacto]["email"]
                    else:
                        raise ValueError("Error, el correo introducido ya esta en la agenda.")
                    pulse_tecla_para_continuar()
                else:
                    lista_telefonos = []
                    todo_ok = False
                    contador_telefono = 0
                    print("Ingresa los telefonos:")
                    while not todo_ok:
                        print(f"({contador_telefono})==> ", end="")
                        telefono = pedir_telefono()
                        if telefono == None:
                            todo_ok = True
                        else:
                            lista_telefonos.append(telefono)
                            contador_telefono += 1
                    contactos[pos_contacto]["telefonos"] = lista_telefonos

    except Exception as e:
        print(e)
        contactos = contactos_temporal
        print("Debido al error no se modificó ningún contacto.")


def crear_lista_telefonos_formato(lista_telefonos_original: list) -> list:
    lista_telefonos_formato = []

    for num_elemento in range(len(lista_telefonos_original)):
        if len(lista_telefonos_original[num_elemento]) == 12:
            lista_telefonos_formato.append(lista_telefonos_original[num_elemento][:3] + "-" + lista_telefonos_original[num_elemento][3:])
        else:
            lista_telefonos_formato.append(lista_telefonos_original[num_elemento])

    return lista_telefonos_formato


def buscar_contacto_por_criterio(contactos: list, criterio: str, valor: str) -> list:
    #pytest
    pos = []

    for num_contacto in range(len(contactos)):
        if valor in contactos[num_contacto][criterio]:
            pos.append(num_contacto)
    
    return pos


def mostrar_contacto(contactos: list):
    borrar_consola()
    try:
        mostrar_menu_limitado("Buscar por")
        opcion = pedir_opcion_limitado()
        if opcion == -1:
            raise ValueError("Error, el valor introducido no se corresponde con ninguna de las opciones.")
        else:
            if opcion == 1:
                nombre = input("Introduzca un nombre: ").strip().capitalize()

                lista_pos_contacto = buscar_contacto_por_criterio(contactos, "nombre", nombre)
                if len(lista_pos_contacto) != 0:
                    borrar_consola()
                    for posicion in lista_pos_contacto:
                        print("------")
                        print(f"Nombre: {contactos[posicion]['nombre']} {contactos[posicion]['apellido']} ({contactos[posicion]['email']})")
                        print(f"Teléfonos: {' / '.join(crear_lista_telefonos_formato(contactos[posicion]['telefonos']))}")

            elif opcion == 2: 
                apellido = input("Introduzca un apellido: ").replace(" ", "").capitalize()

                lista_pos_contacto = buscar_contacto_por_criterio(contactos, "apellido", apellido)
                if len(lista_pos_contacto) != 0:
                    borrar_consola()
                    for posicion in lista_pos_contacto:
                        print("------")
                        print(f"Nombre: {contactos[posicion]['nombre']} {contactos[posicion]['apellido']} ({contactos[posicion]['email']})")
                        print(f"Teléfonos: {' / '.join(crear_lista_telefonos_formato(contactos[posicion]['telefonos']))}")

            elif opcion == 3: 
                email = input("Introduzca un email: ").lower()

                lista_pos_contacto = buscar_contacto_por_criterio(contactos, "email", email)
                if len(lista_pos_contacto) != 0:
                    borrar_consola()
                    for posicion in lista_pos_contacto:
                        print("------")
                        print(f"Nombre: {contactos[posicion]['nombre']} {contactos[posicion]['apellido']} ({contactos[posicion]['email']})")
                        print(f"Teléfonos: {' / '.join(crear_lista_telefonos_formato(contactos[posicion]['telefonos']))}")

            else:
                telefono = input("Introduzca un telefono: ").lower()

                lista_pos_contacto = buscar_contacto_por_criterio(contactos, "telefonos", telefono)
                if len(lista_pos_contacto) != 0:
                    borrar_consola()
                    for posicion in lista_pos_contacto:
                        print("------")
                        print(f"Nombre: {contactos[posicion]['nombre']} {contactos[posicion]['apellido']} ({contactos[posicion]['email']})")
                        print(f"Teléfonos: {' / '.join(crear_lista_telefonos_formato(contactos[posicion]['telefonos']))}")


    except Exception as e:
        print(e)
        print("Debido al error no se mostrara ningún contacto.")


def mostrar_contactos(contactos: list):

    lista_nombres = []

    for contacto in range(len(contactos)):
        lista_nombres.append(contactos[contacto]["nombre"])

    lista_nombres.sort()

    print(f"AGENDA ({len(contactos)})")
    for nombre in lista_nombres:
        for contacto in range(len(contactos)):
            if nombre == contactos[contacto]["nombre"]:
                print("------")
                print(f"Nombre: {contactos[contacto]['nombre']} {contactos[contacto]['apellido']} ({contactos[contacto]['email']})")
                print(f"Teléfonos: {' / '.join(crear_lista_telefonos_formato(contactos[contacto]['telefonos']))}")
    print("------")


def agenda(contactos: list):
    """ Ejecuta el menú de la agenda con varias opciones
    ...
    """
    #TODO: Crear un bucle para mostrar el menú y ejecutar las funciones necesarias según la opción seleccionada...

    opcion = None

    while opcion != 8:
        borrar_consola()
        mostrar_menu()
        opcion = pedir_opcion()

        #TODO: Se valorará que utilices la diferencia simétrica de conjuntos para comprobar que la opción es un número entero del 1 al 7
        if opcion in OPCIONES_MENU - {8}:
            if opcion == 1:
                agregar_contacto(contactos)
                pulse_tecla_para_continuar()
            elif opcion == 2: 
                modificar_contacto(contactos)
                pulse_tecla_para_continuar()
            elif opcion == 3: 
                eliminar_contacto(contactos, pedir_email(contactos, False))
                pulse_tecla_para_continuar()
            elif opcion == 4: 
                contactos = vaciar_agenda(contactos)
                pulse_tecla_para_continuar()
            elif opcion == 5: 
                cargar_contactos(contactos)
                pulse_tecla_para_continuar() 
            elif opcion == 6:
                mostrar_contacto(contactos)
                pulse_tecla_para_continuar()
            else: 
                mostrar_contactos(contactos)
                pulse_tecla_para_continuar()


def pulse_tecla_para_continuar():
    """ Muestra un mensaje y realiza una pausa hasta que se pulse una tecla
    """
    print("\n")
    os.system("pause")


def main():
    """ Función principal del programa
    """
    borrar_consola()

    #TODO: Asignar una estructura de datos vacía para trabajar con la agenda -> DONE
    contactos = []

    #TODO: Modificar la función cargar_contactos para que almacene todos los contactos del fichero en una lista con un diccionario por contacto (claves: nombre, apellido, email y telefonos)
    #TODO: Realizar una llamada a la función cargar_contacto con todo lo necesario para que funcione correctamente.
    cargar_contactos(contactos)

    #TODO: Crear función para agregar un contacto. Debes tener en cuenta lo siguiente:
    # - El nombre y apellido no pueden ser una cadena vacía o solo espacios y se guardarán con la primera letra mayúscula y el resto minúsculas (ojo a los nombre compuestos)
    # - El email debe ser único en la lista de contactos, no puede ser una cadena vacía y debe contener el carácter @.
    # - El email se guardará tal cuál el usuario lo introduzca, con las mayúsculas y minúsculas que escriba. 
    #  (CORREO@gmail.com se considera el mismo email que correo@gmail.com)
    # - Pedir teléfonos hasta que el usuario introduzca una cadena vacía, es decir, que pulse la tecla <ENTER> sin introducir nada.
    # - Un teléfono debe estar compuesto solo por 9 números, aunque debe permitirse que se introduzcan espacios entre los números.
    # - Además, un número de teléfono puede incluir de manera opcional un prefijo +34.
    # - De igual manera, aunque existan espacios entre el prefijo y los 9 números al introducirlo, debe almacenarse sin espacios.
    # - Por ejemplo, será posible introducir el número +34 600 100 100, pero guardará +34600100100 y cuando se muestren los contactos, el telófono se mostrará como +34-600100100. 
    #TODO: Realizar una llamada a la función agregar_contacto con todo lo necesario para que funcione correctamente.
    agregar_contacto(contactos)

    pulse_tecla_para_continuar()
    borrar_consola()

    #TODO: Realizar una llamada a la función eliminar_contacto con todo lo necesario para que funcione correctamente, eliminando el contacto con el email rciruelo@gmail.com
    eliminar_contacto(contactos, "rciruelo@gmail.com")

    pulse_tecla_para_continuar()
    borrar_consola()

    #TODO: Crear función mostrar_contactos para que muestre todos los contactos de la agenda con el siguiente formato:
    # ** IMPORTANTE: debe mostrarlos ordenados según el nombre, pero no modificar la lista de contactos de la agenda original **
    #
    # AGENDA (6)
    # ------
    # Nombre: Antonio Amargo (aamargo@gmail.com)
    # Teléfonos: niguno
    # ......
    # Nombre: Daniela Alba (danalba@gmail.com)
    # Teléfonos: +34-600606060 / +34-670898934
    # ......
    # Nombre: Laura Iglesias (liglesias@gmail.com)
    # Teléfonos: 666777333 / 666888555 / 607889988
    # ......
    # ** resto de contactos **
    #
    #TODO: Realizar una llamada a la función mostrar_contactos con todo lo necesario para que funcione correctamente.
    mostrar_contactos(contactos)

    pulse_tecla_para_continuar()
    borrar_consola()

    #TODO: Crear un menú para gestionar la agenda con las funciones previamente desarrolladas y las nuevas que necesitéis:
    # AGENDA
    # ------
    # 1. Nuevo contacto
    # 2. Modificar contacto
    # 3. Eliminar contacto
    # 4. Vaciar agenda
    # 5. Cargar agenda inicial
    # 6. Mostrar contactos por criterio
    # 7. Mostrar la agenda completa
    # 8. Salir
    #
    # >> Seleccione una opción: 
    #
    #TODO: Para la opción 3, modificar un contacto, deberás desarrollar las funciones necesarias para actualizar la información de un contacto.
    #TODO: También deberás desarrollar la opción 6 que deberá preguntar por el criterio de búsqueda (nombre, apellido, email o telefono) y el valor a buscar para mostrar los contactos que encuentre en la agenda.
    
    agenda(contactos)


if __name__ == "__main__":
    main()