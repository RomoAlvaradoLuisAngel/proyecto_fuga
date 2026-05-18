import flet as ft
from flet_geolocator import Geolocator
import webbrowser
import mysql.connector

conexion = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="",
    database="ges_fugas"
)

def main(page : ft.Page):
    page.title="BlueLeak"
    page.vertical_alignment=ft.MainAxisAlignment.CENTER
    page.horizontal_alignment=ft.CrossAxisAlignment.CENTER
    page.padding=30
    page.bgcolor = "#00B0C8"
    
    page.add(ft.Text("¡Bienvenido a blueLeak!"))
    
    def mostrar_pantalla_principal():
        page.clean()
        page.add(ft.Text("Hola de prueba"))
        page.navigation_bar=ft.NavigationBar(
            destinations=[
                ft.NavigationBarDestination(icon=ft.Icons.HOME, label="Inicio"),
                ft.NavigationBarDestination(icon=ft.Icons.INFO, label="Informacion"),
                ft.NavigationBarDestination(icon=ft.Icons.PERSON, label="Inicio de sesion"),
            ],
            on_change = lambda e: print(f"Seleccionado: {e.control.selected_index}")
        )
        
        page.add(
            ft.AppBar(
                title=ft.Text("Panel principal"),
                bgcolor=ft.Colors.BLUE_900,
                color=ft.Colors.WHITE,
                automatically_imply_leading=False
            ),
            ft.Column(
                [
                    ft.Icon(ft.Icons.BOLT, color=ft.Colors.YELLOW, size=100),
                    ft.Text("Bienvenido al sistema.", color=ft.Colors.WHITE),
                    ft.Text("Has iniciado sesion correctamente.", color=ft.Colors.WHITE)
                ],
                expand=True,
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        )
        page.update()
    
    btn_entrar = ft.ElevatedButton(
        content="Entrar a la aplicación",
        bgcolor=ft.Colors.GREEN_400,
        color=ft.Colors.WHITE,
        on_click=mostrar_pantalla_principal
    )

    page.add(btn_entrar)
    geo = Geolocator()
    page.services.append(geo)
    async def abrir_mapa(e):
        pos = await geo.get_current_position()
        if not pos:
            page.add(ft.Text("No se pudo obtener ubicación"))
            return
        url = (
            f"https://www.openstreetmap.org/"
            f"?mlat={pos.latitude}&mlon={pos.longitude}"
            f"#map=16/{pos.latitude}/{pos.longitude}"
        )
        webbrowser.open(url)
    page.add(
        ft.Button("Abrir mapa", on_click=abrir_mapa)
    )

    
ft.run(main)