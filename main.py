import flet as ft
import flet_geolocator as ftg
import webbrowser
import mysql.connector
from datetime import datetime

conexion = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="",
    database="ges_fugas"
)

async def main(page : ft.Page):
    page.title="BlueLeak"
    page.vertical_alignment=ft.MainAxisAlignment.CENTER
    page.horizontal_alignment=ft.CrossAxisAlignment.CENTER
    page.padding=0
    page.bgcolor = "#00B0C8"
    
    geo = ftg.Geolocator()
    page.services.append(geo)
    
    vista_contenedor = ft.Container(expand=True, alignment=ft.Alignment(0,0))
    
    latitud = None
    longitud = None
    
    async def abrir_mapa(e):
        nonlocal latitud, longitud
        ft.Text("Öbteniendo ubicacion, espere...")
        page.update()
        try: 
            await geo.request_permission()
            pos = await geo.get_current_position()
            if not pos:
                page.add(ft.Text("No se pudo obtener ubicación"))
                return
            latitud = pos.latitude
            longitud = pos.longitude
            url = (f"https://www.google.com/maps?q={latitud},{longitud}")
            webbrowser.open(url)
        except Exception as ex:
            page.add(ft.Text(f"Error al obtener ubicación: {ex}"))
            page.update()
            
    def inicio():
        return ft.Column(
            controls=[
                ft.Icon(ft.Icons.WATER_DROP, size=60, color=ft.Colors.BLUE_900),
                ft.Text("¡Bienvenido a BlueLeak!", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900),
                ft.ElevatedButton(content="Agregar reporte", bgcolor=ft.Colors.BLUE_400, color=ft.Colors.WHITE)
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True
        )   

        
    def informacion():
        return ft.Column(
            controls= [
            ft.Icon(ft.Icons.INFO, size=60, color=ft.Colors.WHITE),
            ft.Text("Información de la aplicación", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900),
            ft.Text("BlueLeak es una aplicación diseñada para ayudar a los usuarios a reportar fugas de agua en su área. Con esta aplicación, los usuarios pueden compartir información sobre la ubicación de las fugas, lo que permite a las autoridades locales tomar medidas rápidas para solucionar el problema y reducir el desperdicio de agua.", size=16, color=ft.Colors.WHITE),
            ft.Text("Que es una fuga de agua?", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900),
            ft.Text("Una fuga de agua es una pérdida no deseada de agua que ocurre cuando el agua se escapa de las tuberías, grifos, o cualquier otro sistema de plomería. Las fugas pueden ser causadas por una variedad de factores, como tuberías corroídas, conexiones sueltas, o daños físicos. Las fugas de agua pueden resultar en un desperdicio significativo de agua, así como en daños a la propiedad si no se abordan a tiempo.", size=16, color=ft.Colors.WHITE),
            ft.Text("Como ubicar una fuga de agua?", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900),
            ft.Text("Para ubicar una fuga de agua, es importante prestar atención a ciertos signos, como un aumento inexplicable en la factura de agua, manchas de humedad en las paredes o techos, o el sonido de agua corriendo cuando no debería haberlo. También se pueden utilizar herramientas como medidores de flujo o cámaras termográficas para identificar la ubicación exacta de la fuga.", size=16, color=ft.Colors.WHITE),
            ft.Text("¿Cómo reportar una fuga de agua?", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900),
            ft.Text("Cuando registre una fuga de agua aqui, con su ubicacion exacta, puede ir a levantar la queja en junta municipal de agua.", size=16, color=ft.Colors.WHITE),
            ft.Text("¡Gracias por ayudar a conservar el agua y proteger nuestro medio ambiente!", size=19, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,
            scroll=ft.ScrollMode.AUTO
            )

        
    def inicio_sesion():
        return ft.Column(
            controls=[
            ft.Text("Inicio de sesión", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900),
            ft.TextField(label="Usuario", width=200),
            ft.TextField(label="Contraseña", width=200, password=True),
            ft.Button("Iniciar sesión", bgcolor=ft.Colors.BLUE_400, color=ft.Colors.WHITE)
        ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True
        )


    def cambiar_pantalla(e):
        opcion = e.control.selected_index
        
        if opcion == 0:
            vista_contenedor.content=inicio()
        elif opcion == 1:
            vista_contenedor.content=informacion()
        elif opcion == 2:
            vista_contenedor.content=inicio_sesion()
        page.update()

    def mostrar_pantalla_principal(e):
        page.clean()
        page.appbar = ft.AppBar(
                title=ft.Text("Bienvenido a BlueLeak"),
                bgcolor=ft.Colors.BLUE_900,
                color=ft.Colors.WHITE,
                actions = [
                            ft.IconButton(ft.Icons.MAP, on_click=abrir_mapa, tooltip="Mapa"),
                ]
                )        
        page.navigation_bar=ft.NavigationBar(
            selected_index=0,
                destinations=[
                    ft.NavigationBarDestination(icon=ft.Icons.HOME, label="Inicio"),
                    ft.NavigationBarDestination(icon=ft.Icons.INFO, label="Informacion"),
                    ft.NavigationBarDestination(icon=ft.Icons.PERSON, label="Inicio de sesion"),
                ],
                on_change = cambiar_pantalla
            )
        vista_contenedor.content=inicio()
        page.add(
                vista_contenedor
                )
        page.update()
        

        
    page.add(vista_contenedor)
    page.update()
    
    page.add(
        ft.Column(
            controls=[
                ft.Icon(ft.Icons.WATER_DROP, size=60, color=ft.Colors.WHITE),
                ft.Text("¡Bienvenido a BlueLeak!", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                ft.Button("Entrar a la aplicacion", on_click=mostrar_pantalla_principal, bgcolor=ft.Colors.BLUE_400, color=ft.Colors.WHITE)             
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True 
        )
        )

    
ft.run(main)