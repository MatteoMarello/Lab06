import flet as ft


class View(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        # page stuff
        self._page = page
        self._page.title = "Analizza vendite"
        self._page.horizontal_alignment = 'CENTER'
        self._page.theme_mode = ft.ThemeMode.DARK
        # controller (it is not initialized. Must be initialized in the main, after the controller is created)
        self._controller = None
        # graphical elements
        self._title = None
        self.txt_name = None
        self.btn_hello = None
        self.txt_result = None
        self.txt_container = None

    def load_interface(self):
        # title
        self._title = ft.Text("Analizza vendite", color="blue", size=24)
        self._page.controls.append(self._title)

        #ROW with some controls

        self.dropdown1 = ft.Dropdown(label="Anno",  # Etichetta
                                     width=400,  # Larghezza in pixel
                                     height=60,  # Altezza in pixel
                                     options=[ft.dropdown.Option(key=0, text=" Nessun filtro")],
                                     hint_text="Seleziona un anno")

        self._controller.populate_dropdown1()

        self.dropdown2 = ft.Dropdown(label="Brand",  # Etichetta
                                     width=400,  # Larghezza in pixel
                                     height=60,  # Altezza in pixel
                                     options=[ft.dropdown.Option(key=0, text=" Nessun filtro")],
                                     hint_text="Seleziona un brand")

        self._controller.populate_dropdown2()

        self.dropdown3 = ft.Dropdown(label="Retailer",  # Etichetta
                                     width=400,  # Larghezza in pixel
                                     height=60,  # Altezza in pixel
                                     options=[ft.dropdown.Option(key=0, text=" Nessun filtro")],
                                     hint_text="Seleziona un retailer",
                                     on_change = self._controller.read_retailer)

        self.bottone1= ft.ElevatedButton(
            text="Top Vendite",
            icon=ft.icons.SEARCH,
            style=ft.ButtonStyle(
                color=ft.colors.WHITE,
                bgcolor=ft.colors.BLUE_700,
                overlay_color=ft.colors.BLUE_900,
                padding=20,
                shape=ft.RoundedRectangleBorder(radius=12),
                elevation=6,
            ),
            on_click=self._controller.handle_topVendita
        )

        self.bottone2 = ft.ElevatedButton(
            text="Analizza Vendite",
            icon=ft.icons.SEARCH,
            style=ft.ButtonStyle(
                color=ft.colors.WHITE,
                bgcolor=ft.colors.BLUE_700,
                overlay_color=ft.colors.BLUE_900,
                padding=20,
                shape=ft.RoundedRectangleBorder(radius=12),
                elevation=6,
            ),
            on_click=self._controller.handle_analizzaVendite
        )

        row1 = ft.Row([self.dropdown1, self.dropdown2, self.dropdown3],
                      alignment=ft.MainAxisAlignment.CENTER, expand=True)

        row2 = ft.Row([self.bottone1, self.bottone2],
                      alignment=ft.MainAxisAlignment.CENTER, expand=True)

        self._page.controls.append(row1)
        self._page.controls.append(row2)
        self._controller.populate_dropdown3()
        # List View where the reply is printed
        self.txt_result = ft.ListView(expand=1, spacing=10, padding=0, auto_scroll=True)
        self._page.controls.append(self.txt_result)
        self._page.update()

    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, controller):
        self._controller = controller

    def set_controller(self, controller):
        self._controller = controller

    def create_alert(self, message):
        dlg = ft.AlertDialog(title=ft.Text(message))
        self._page.dialog = dlg
        dlg.open = True
        self._page.update()

    def update_page(self):
        self._page.update()

