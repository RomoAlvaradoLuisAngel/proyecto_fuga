import flet as ft
import flet_geolocator as ftg
import webbrowser
import mysql.connector

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
    
    def mostrar_pantalla_principal(e):
        page.clean()
        
        page.navigation_bar=ft.NavigationBar(
                destinations=[
                    ft.NavigationBarDestination(icon=ft.Icons.HOME, label="Inicio"),
                    ft.NavigationBarDestination(icon=ft.Icons.INFO, label="Informacion"),
                    ft.NavigationBarDestination(icon=ft.Icons.PERSON, label="Inicio de sesion"),
                ],
                on_change = lambda e: print(f"Seleccionado: {e.control.selected_index}")
            )
        page.appbar = ft.AppBar(
                title=ft.Text("Panel principal"),
                bgcolor=ft.Colors.BLUE_900,
                color=ft.Colors.WHITE
                )
        page.add(
                ft.Text("¡Bienvenido a BlueLeak!", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900),
                ft.Button("Abrir mapa.", on_click=abrir_mapa, bgcolor=ft.Colors.BLUE_400, color=ft.Colors.WHITE)
            )
        page.update()
    
    page.add(
        ft.Icon(ft.Icons.WATER_DROP, size=60, color=ft.Colors.WHITE),
        ft.Text("¡Bienvenido a BlueLeak!", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
        ft.Button("Entrar a la aplicacion", on_click=mostrar_pantalla_principal, bgcolor=ft.Colors.BLUE_400, color=ft.Colors.WHITE)
    )

    
ft.run(main)