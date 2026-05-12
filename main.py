import flet as ft

def main(page : ft.Page):
    page.title="BlueLeak"
    page.vertical_alignment=ft.MainAxisAlignment.CENTER
    page.horizontal_alignment=ft.CrossAxisAlignment.CENTER
    page.padding=30
    page.bgcolor = "#00B0C8"
    
    page.add(ft.Text("¡Bienvenido a blueLeak!"))
    
    def entrar_click(e): 
        page.add(ft.Text("Bienvenido"))
    
    btn_entrar = ft.ElevatedButton(
        content="Entrar a la aplicación",
        bgcolor=ft.Colors.GREEN_400,
        color=ft.Colors.WHITE,
        on_click=entrar_click
    )

    page.add(btn_entrar)
    
    def mostrar_pantalla_principal():
        page.clean()
        page.navigation_bar=ft.NavigationBar(
            destinations=[
                ft.NavigationBarDestination(icon=ft.Icons.HOME, label="Inicio"),
                ft.NavigationBarDestination(icon=ft.Icons.INFO, label="Informacion"),
                ft.NavigationBarDestination(icon=ft.Icons.PERSON, label="Inicio de sesion"),
            ],
            on_change = lambda e: print(f"Seleccionado: {e.control.selected_index}")
        )

    
ft.app(target=main)