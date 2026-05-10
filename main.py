import flet as ft

def main(page: ft.Page):
    page.title = "Proyecto Fuga"
    page.add(ft.Text("¡Bienvenido al Proyecto Fuga!"))
    
ft.app(target=main)