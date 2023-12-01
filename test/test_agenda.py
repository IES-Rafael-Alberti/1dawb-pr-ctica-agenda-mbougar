import copy
from os import path
import pathlib
import pytest

from src.agenda import(
    cargar_contactos,
    validar_email,
    pedir_email,
    validar_telefono,
    buscar_contacto,
    pedir_opcion,
    pedir_nombre_y_apellido,
    separar_nombre_y_apellido,
    vaciar_agenda,
    pedir_opcion_limitado,
    crear_lista_telefonos_formato,
    buscar_contacto_por_criterio
)


# Simulamos un archivo CSV con datos de contacto para las pruebas
RUTA = pathlib.Path(__file__).parent.absolute() 
NOMBRE_FICHERO = "contactos.csv"
RUTA_FICHERO = path.join(RUTA, NOMBRE_FICHERO)
CONTACTOS_PRUEBA = [
    {"nombre": "Laura", "apellido": "Iglesias", "email": "liglesias@gmail.com", "telefonos": ["666777333", "666888555", "607889988"]},
    {"nombre": "Antonio", "apellido": "Amargo", "email": "aamargo@gmail.com", "telefonos": []},
    {"nombre": "Marta", "apellido": "Copete", "email": "marcopete@gmail.com", "telefonos": ["+34600888800"]},
    {"nombre": "Rafael", "apellido": "Ciruelo", "email": "rciruelo@gmail.com", "telefonos": ["+34607212121", "655001122"]},
    {"nombre": "Daniela", "apellido": "Alba", "email": "danalba@gmail.com", "telefonos": ["+34600606060", "+34670898934"]},
    {"nombre": "Rogelio", "apellido": "Rojo", "email": "rogrojo@gmail.com", "telefonos": ["610000099", "645000013"]}
]


@pytest.fixture
def contactos_iniciales() -> list:
    return copy.deepcopy(CONTACTOS_PRUEBA)


def test_cargar_contactos(contactos_iniciales):
    contactos = []
    cargar_contactos(contactos)
    assert contactos == contactos_iniciales


def test_validar_email(contactos_iniciales):
    with pytest.raises(ValueError, match="el email no puede ser una cadena vacía"):
        validar_email("", contactos_iniciales, False)
    with pytest.raises(ValueError, match="el email no es un correo válido"):
        validar_email("correosinarroba.com", contactos_iniciales, False)
    with pytest.raises(ValueError, match="el email ya existe en la agenda"):
        validar_email("rogrojo@gmail.com", contactos_iniciales, True)


def test_pedir_email(monkeypatch, contactos_iniciales):
    monkeypatch.setattr("builtins.input", lambda _: "")
    with pytest.raises(ValueError, match="el email no puede ser una cadena vacía"):
        pedir_email(contactos_iniciales, False)
    monkeypatch.setattr("builtins.input", lambda _: "correosinarroba.com")
    with pytest.raises(ValueError, match="el email no es un correo válido"):
        pedir_email(contactos_iniciales, False)
    monkeypatch.setattr("builtins.input", lambda _: "marcopete@gmail.com")
    with pytest.raises(ValueError, match="el email ya existe en la agenda"):
        pedir_email(contactos_iniciales, True)


@pytest.mark.parametrize(
    "input_tel, expected",
    [
        ("123456789", True),
        ("+34607660290", True),
        ("12345", False),
        ("+33666777888", False),
        ("abcd", False),
        ("", False)
    ]
)
def test_validar_telefono(input_tel, expected):
    assert validar_telefono(input_tel) == expected


@pytest.mark.parametrize(
    "input_email, expected",
    [
        ("liglesias@gmail.com", 0),
        ("danalba@gmail.com", 4),
        ("no_existe@gmail.com", None),
        ("aamargo@gmail.com", 1),
        ("marcopete@gmail.com", 2),
        ("", None)
    ]
)
def test_buscar_contacto_params(contactos_iniciales, input_email, expected):
    assert buscar_contacto(contactos_iniciales, input_email) == expected


def test_pedir_opcion(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "3")
    resultado = pedir_opcion()
    assert resultado == 3
    monkeypatch.setattr("builtins.input", lambda _: "a")
    resultado = pedir_opcion()
    assert resultado == -1


#Principio de las funciones creadas por mi
def test_pedir_nombre_y_apellido(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "Manuel Carlos Bouza")
    resultado = pedir_nombre_y_apellido()
    assert resultado == ("Manuel Carlos", "Bouza")


def test_separar_nombre_y_apellido():
    resultado = separar_nombre_y_apellido(["Manuel", "Carlos", "Bouza"])
    assert resultado == ("Manuel Carlos", "Bouza")


def test_vaciar_agenda():
    contactos = CONTACTOS_PRUEBA
    resultado = vaciar_agenda(contactos)
    assert resultado == []


def test_pedir_opcion_limitado(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "3")
    resultado = pedir_opcion_limitado()
    assert resultado == 3
    monkeypatch.setattr("builtins.input", lambda _: "a")
    resultado = pedir_opcion_limitado()
    assert resultado == -1


def test_crear_lista_telefonos_formato():
    lista_telefonos_original = ["+34123456789", "+34987654321", "123123123"]
    resultado = crear_lista_telefonos_formato(lista_telefonos_original)
    assert resultado == ["+34-123456789", "+34-987654321", "123123123"]


def test_buscar_contacto_por_criterio():
    contactos = CONTACTOS_PRUEBA
    resultado = buscar_contacto_por_criterio(contactos, "apellido", "Amargo")
    assert resultado == [1]
    contactos = CONTACTOS_PRUEBA
    resultado = buscar_contacto_por_criterio(contactos, "telefonos", "610000099")
    assert resultado == [5]