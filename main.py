import flet as ft
import flet_geolocator as ftg
import webbrowser
import mysql.connector
from datetime import datetime

def conexion():
    return mysql.connector.connect(
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
        def abrir_dialog(e):
            txt_descripcion = ft.TextField(label="Escriba una descripcion de la fuga.", multiline=True, color=ft.Colors.BLUE_900)
            txt_direccion = ft.TextField(label="Escriba la direccion de la fuga.", multiline=True, color=ft.Colors.BLUE_900)
            txt_estado = ft.Dropdown(label = "Estado de la fuga", options=[
                ft.dropdown.Option("Completamente rota"),
                ft.dropdown.Option("Un poco rota"),
                ft.dropdown.Option("Mal mantenimiento"),
            ])
            mensaje = ft.Text("", color=ft.Colors.RED_400)
            
            def enviar_repo(e):
                if not txt_descripcion.value or not txt_direccion.value or not txt_estado.value:
                    mensaje.value = "Por favor acompleta todos los campos."
                    page.update()
                    return
                try:
                    db = conexion()
                    cursor = db.cursor()
                    cursor.execute(
                        "INSERT INTO reporte_fugas (descripcion, direccion, estado, latitud, longitud, fecha_reporte) VALUES (%s, %s, %s, %s, %s)",
                        (txt_descripcion.value, txt_direccion.value, txt_estado.value, latitud.value, longitud.value, datetime.now()))
                    db.commit()
                    db.close()
                    mensaje.color = ft.Colors.GREEN_400
                    mensaje.value = "Reporte enviado con exito" 
                except Exception as ex:
                    mensaje.value = f"Error al enviar reporte: {ex}" 
                    page.update()
                    
            def cerrar_dialogo(e):
                carta.open = False
                page.update()        
                    
            carta = ft.AlertDialog(
            title=ft.Text("Crear reporte", color=ft.Colors.BLUE_900),
            content=ft.Column(
                controls=[txt_descripcion, txt_direccion, txt_estado, mensaje],
                tight=True
            ),
    

    actions=[
        ft.Button(content="Agregar", on_click=enviar_repo, bgcolor=ft.Colors.GREEN_400, color=ft.Colors.WHITE),

        ft.Button(content="Cerrar", bgcolor=ft.Colors.RED_400, color=ft.Colors.WHITE, on_click = cerrar_dialogo)
    ]
)
            page.overlay.append(carta) 
            carta.open = True
            page.update()
                                
        return ft.Column(
            controls=[
                ft.Icon(ft.Icons.WATER_DROP, size=60, color=ft.Colors.BLUE_900),
                ft.Text("¡Bienvenido a BlueLeak!", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900),
                ft.Button(content="Agregar reporte", bgcolor=ft.Colors.BLUE_400, color=ft.Colors.WHITE, on_click=abrir_dialog),
                ft.Text("Nota: El reporte se visualiza en reportes.", size=12)
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
            ft.Text("¿Qué es una fuga de agua?", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900),
            ft.Text("Una fuga de agua es una pérdida no deseada de agua que ocurre cuando el agua se escapa de las tuberías, grifos, o cualquier otro sistema de plomería. Las fugas pueden ser causadas por una variedad de factores, como tuberías corroídas, conexiones sueltas, o daños físicos. Las fugas de agua pueden resultar en un desperdicio significativo de agua, así como en daños a la propiedad si no se abordan a tiempo.", size=16, color=ft.Colors.WHITE),
            ft.Text("¿Comó ubicar una fuga de agua?", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900),
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

        
    def repo():
        def eliminar(id_reporte):
            conn = None
            cursor = None
            try:
                conn = conexion()
                cursor = conn.cursor()
                cursor.execute(
                    "DELETE FROM reporte_fugas WHERE id_reporte = %s",
                    (id_reporte,)
                )
                conn.commit()
                conn.close()
                vista_contenedor.content = repo()
                page.update()

            except Exception as e:
                print("ERROR ELIMINAR reporte:", e)
                return False

            finally:
                if cursor:
                    cursor.close()
                if conn:
                    conn.close()
                    
        def modificar(id_reporte):
            pass
                    
        def cargar():
            tarjetas = []
            try:
                db = conexion()
                cursor = db.cursor()
                cursor.execute("""
                    SELECT id_reporte, descripcion, direccion, estado, fecha_reporte
                    FROM reporte_fugas
                """)
                reportes = cursor.fetchall()
                db.close()

                if reportes:
                    for reporte in reportes:
                        id_reporte = reporte[0]
                        descripcion = reporte[1]
                        direccion = reporte[2]
                        estado = reporte[3]
                        fecha = reporte[4]

                        tarjeta = ft.Card(elevation=8,margin=10,
                            content=ft.Container(
                                bgcolor=ft.Colors.WHITE,
                                border_radius=15,
                                padding=15,
                                content=ft.Column(spacing=10,controls=[ft.Row(
                                            controls=[
                                                ft.Icon(
                                                    ft.Icons.WATER_DROP,
                                                    color=ft.Colors.BLUE_400,
                                                    size=30
                                                ),

                                                ft.Text(
                                                    "Reporte de fuga",
                                                    size=20,
                                                    weight=ft.FontWeight.BOLD,
                                                    color=ft.Colors.BLUE_900
                                                )
                                            ]
                                        ),
                                        ft.Divider(),

                                        ft.Text( f"Descripción:",
                                            weight=ft.FontWeight.BOLD,
                                            color=ft.Colors.BLUE_900
                                        ),

                                        ft.Text(
                                            descripcion,
                                            size=15,
                                            color=ft.Colors.BLACK
                                        ),

                                        ft.Text(
                                            "Dirección:",
                                            weight=ft.FontWeight.BOLD,
                                            color=ft.Colors.BLUE_900
                                        ),

                                        ft.Text(
                                            direccion,
                                            size=15,
                                            color=ft.Colors.BLACK
                                        ),
                                        
                                        ft.Text(
                                            "Estado de la fuga",
                                            weight=ft.FontWeight.BOLD,
                                            color=ft.Colors.BLUE_900
                                        ),
                                        
                                        ft.Text(
                                            estado,
                                            size=15,
                                            color=ft.Colors.BLACK
                                        ),

                                        ft.Text(
                                            "Fecha:",
                                            weight=ft.FontWeight.BOLD,
                                            color=ft.Colors.BLUE_900
                                        ),

                                        ft.Text(
                                            str(fecha),
                                            size=13,
                                            color=ft.Colors.GREY_700
                                        ),
                                        ft.Row([
                                            ft.Button("Eliminar reporte", on_click=lambda e, id=id_reporte: eliminar(id), bgcolor=ft.Colors.RED_400, color=ft.Colors.WHITE),
                                            ft.Button("Modificar reporte", bgcolor = ft.Colors.CYAN_400, color=ft.Colors.WHITE)
                                        ])
                                    ]
                                )
                            )
                        )
                        
                        

                        tarjetas.append(tarjeta)

                else:

                    tarjetas.append(

                        ft.Text(
                            "No hay reportes registrados",
                            color=ft.Colors.WHITE,
                            size=18
                        )
                    )

            except Exception as ex:

                tarjetas.append(

                    ft.Text(
                        f"Error: {ex}",
                        color=ft.Colors.RED
                    )
                )

            return ft.Column(

                controls=[

                    ft.Text(
                        "Visualizador de reportes",
                        size=28,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.WHITE
                    ),

                    ft.Column(
                        controls=tarjetas,
                        scroll=ft.ScrollMode.AUTO,
                        expand=True
                    )
                ],
                expand=True,
                scroll=ft.ScrollMode.AUTO,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        return cargar()



    def cambiar_pantalla(e):
        opcion = e.control.selected_index
        
        if opcion == 0:
            vista_contenedor.content=inicio()
        elif opcion == 1:
            vista_contenedor.content=informacion()
        elif opcion == 2:
            vista_contenedor.content=repo()
        page.update()

    def mostrar_pantalla_principal(e):
        page.clean()
        page.appbar = ft.AppBar(
                title=ft.Text("Bienvenido a BlueLeak"),
                bgcolor=ft.Colors.BLUE_900,
                color=ft.Colors.WHITE,
                actions = [
                            ft.IconButton(ft.Icons.MAP, on_click=abrir_mapa, tooltip="Mapa", icon_size=40 ),
                ]
                )        
        page.navigation_bar=ft.NavigationBar(
            selected_index=0,
                destinations=[
                    ft.NavigationBarDestination(icon=ft.Icons.HOME, label="Inicio"),
                    ft.NavigationBarDestination(icon=ft.Icons.INFO, label="Informacion"),
                    ft.NavigationBarDestination(icon=ft.Icons.PERSON, label="Reportes"),
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
