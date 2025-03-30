
def funcion(pais, estado, ciudad):
    print(pais, estado, ciudad)

lista = {"pais": "mexico", "estado":"san luis", "ciudad":"city"}
print(type(lista))
funcion(**lista)