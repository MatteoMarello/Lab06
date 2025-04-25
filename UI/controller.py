import flet as ft
from database.DAO import DAO


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._DAO = DAO()

    def populate_dropdown1(self):
        lista_anni= self._DAO.get_years()
        options=[ft.dropdown.Option(key="", text="nessun filtro")]
        options.extend([ft.dropdown.Option(key = str(anno), text = str(anno)) for anno in lista_anni])
        # Assegna le opzioni al Dropdown
        self._view.dropdown1.options = options
        self._view.update_page()


    def populate_dropdown2(self):
        lista_brand = self._DAO.get_brands()
        options = [ft.dropdown.Option(key="", text="nessun filtro")]
        options.extend([ft.dropdown.Option(key = string, text = string) for string in lista_brand])
        # Assegna le opzioni al Dropdown
        self._view.dropdown2.options = options
        self._view.update_page()

    def populate_dropdown3(self):
        retailers = self._DAO.get_retailer() or []  # Recupera i retailer
        # Crea le opzioni con key, text, e data
        options=[ft.dropdown.Option(key="", text="nessun filtro")]
        options.extend([
            ft.dropdown.Option(
                key=str(ret.retailer_code),  # Assicuriamoci che il key sia una stringa
                text=ret.retailer_name,
                data=ret  # L'oggetto completo
            )
            for ret in retailers
        ])

        # Assegna le opzioni al Dropdown
        self._view.dropdown3.options = options
        self._view.update_page()

    def read_retailer(self, e):
        selected_key = e.control.value  # Il 'key' è la stringa selezionata
        # Troviamo l'opzione selezionata
        opt = None
        for o in e.control.options:
            if o.key == selected_key:
                opt = o
                break

        if not opt:
            return

        r = opt.data  # L'oggetto completo del retailer
        # Pulisci la ListView e aggiungi il testo
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text(f"Nome: {r.retailer_name}  Paese: {r.country}  Tipo: {r.type}")
        )
        self._view.update_page()

    def handle_topVendita(self, e):
        chiave_dropdown1 = self._view.dropdown1.value
        chiave_dropdown2 = self._view.dropdown2.value
        chiave_dropdown3 = self._view.dropdown3.value

        risultati = self._model.set_filtri(chiave_dropdown1, chiave_dropdown2, chiave_dropdown3)
        self._view.txt_result.controls.clear()
        self._view.update_page()
        for r in risultati:
            data = r[0].strftime("%d/%m/%Y")
            ricavo = f"{r[1]:.2f}€"
            riga = f"{data} | Ricavo: {ricavo} | Retailer: {r[2]} | Prodotto: {r[3]}"
            self._view.txt_result.controls.append(ft.Text(riga))

        if len(risultati) == 0:
            self._view.txt_result.controls.append(ft.Text("Non ci sono vendite che corrispondono ai criteri di ricerca"))
        self._view.update_page()


    def handle_analizzaVendite(self, event=None):
            # 1️⃣ Prendo i valori dai drop-down della view
            raw1 = self._view.dropdown1.value
            raw2 = self._view.dropdown2.value
            raw3 = self._view.dropdown3.value

            # 2️⃣ Se sono None o "", li sostituisco con 'nessun filtro'
            chiave1 = raw1 or "nessun filtro"
            chiave2 = raw2 or "nessun filtro"
            chiave3 = raw3 or "nessun filtro"

            # 3️⃣ Chiamo il model/DAO
            risultati = self._model.getAnalisi(chiave1, chiave2, chiave3)

            # 4️⃣ Aggiorno la UI esattamente come prima
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("📊 Statistiche rilevate:\n"))

            if risultati and risultati[0]:
                r = risultati[0]
                ricavo = r[0] if r[0] is not None else 0
                nv = r[1] if r[1] is not None else 0
                nr = r[2] if r[2] is not None else 0
                np = r[3] if r[3] is not None else 0

                self._view.txt_result.controls.append(
                    ft.Text(
                        f"Giro d'affari: {ricavo:,.2f} €\n"
                        f"Numero vendite: {nv}\n"
                        f"Retailer coinvolti: {nr}\n"
                        f"Prodotti distinti venduti: {np}\n"
                    )
                )
            else:
                self._view.txt_result.controls.append(
                    ft.Text("⚠️ Nessuna vendita trovata con i filtri selezionati.")
                )

            self._view.update_page()
