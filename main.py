import flet as ft
from alert import AlertManager
from deposito_strumenti import DepositoStrumenti

FILE_STRUMENTI = "strumenti.csv"

def main(page: ft.Page):
    page.title = "Lab05"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.DARK

    # --- ALERT ---
    alert = AlertManager(page)

    # --- LA LOGICA DELL'APPLICAZIONE E' PRESA DAL DEPOSITO DI STRUMENTI DEL LAB03 ---
    deposito = DepositoStrumenti("Deposito Strumenti Musicali", "Alessandro Visconti")
    try:
        deposito.carica_file_strumenti(FILE_STRUMENTI)  # Carica il file
    except FileNotFoundError as e:
        alert.show_alert(f"❌ {e}")  # Fa apparire una finestra che mostra l'errore

    # --- UI ELEMENTI ---

    # Text per mostrare il nome e il responsabile del deposito
    txt_titolo = ft.Text(value=deposito.nome, size=38, weight=ft.FontWeight.BOLD)
    txt_responsabile = ft.Text(
        value=f"Responsabile: {deposito.get_responsabile()}",
        size=16,
        weight=ft.FontWeight.BOLD
    )

    # TextField per responsabile
    input_responsabile = ft.TextField(value=deposito.get_responsabile(), label="Responsabile")

    # ListView per mostrare la lista di strumenti aggiornata
    lista_strumenti = ft.ListView(expand=True, spacing=5, padding=10, auto_scroll=True)

    # Tutti i TextField per le info necessarie per aggiungere un nuovo strumento (tipo, marca, anno, contatore posti)
    # TODO
    txt_strumenti = ft.Text("Aggiungi nuovo strumento", size=20, weight=ft.FontWeight.BOLD)

    input_tipo = ft.TextField(
        label="Tipo",
        height=40,
        width=200,
        dense=True,
        text_size=15
    )
    input_marca = ft.TextField(
        label="Marca",
        height=40,
        width=200,
        dense=True,
        text_size=15
    )
    input_anno = ft.TextField(
        label="Anno acquisto",
        height=40,
        width=200,
        dense=True,
        text_size=15
        )
    casella_valore = ft.TextField(
        value = "0",
        text_align = ft.TextAlign.CENTER,
        height=40,
        width=50,
        dense=True,
        text_size=15
    )

    # --- FUNZIONI APP ---
    def aggiorna_lista_strumenti():
        lista_strumenti.controls.clear()
        for strumento in deposito.strumenti_ordinati_per_marca():
            stato = "✅" if strumento.disponibile else "⛔"
            lista_strumenti.controls.append(ft.Text(f"{stato} {strumento}"))
    # --- HANDLERS APP ---
    def cambia_tema(e):
        page.theme_mode = ft.ThemeMode.DARK if toggle_cambia_tema.value else ft.ThemeMode.LIGHT
        toggle_cambia_tema.label = "Tema scuro" if toggle_cambia_tema.value else "Tema chiaro"

    def conferma_responsabile(e):
        deposito.set_responsabile(input_responsabile.value)
        txt_responsabile.value = f"Responsabile: {deposito.get_responsabile()}"

    # Handlers per la gestione dei pulsanti utili all'inserimento di un nuovo strumento
    # TODO
    def counter_meno(e):
        valore = int(casella_valore.value)
        if valore>0:
            casella_valore.value = str(valore-1)
            page.update()

    def counter_piu(e):
        valore = int(casella_valore.value)
        casella_valore.value = str(valore+1)
        page.update()

    def agg_strumento(e):
        tipo = input_tipo.value
        marca = input_marca.value
        anno = input_anno.value
        n_tot = int(casella_valore.value)
        n=0
        if anno.isdigit():
            if n_tot > n:
                if tipo and marca and anno:
                    deposito.aggiungi_strumento(
                        tipo=tipo,
                        marca=marca,
                        anno_acquisto=anno,
                        valore = None
                        )
                    n_tot = n_tot - 1
                    aggiorna_lista_strumenti()
                    page.update()
            if n_tot == n:
                input_tipo.value = ""
                input_marca.value = ""
                input_anno.value = ""
                casella_valore.value = "0"
                page.update()
        else:
            alert.show_alert("Errore: inserire valori numerici validi per anno e posti")


    # --- EVENTI ---
    toggle_cambia_tema = ft.Switch(label="Tema scuro", value=True, on_change=cambia_tema)
    pulsante_conferma_responsabile = ft.Button("Conferma", on_click=conferma_responsabile)

    # Pulsanti per la gestione dell'inserimento di un nuovo strumento
    # TODO
    pulsante_aggiungi_strumento = ft.Button("Aggiungi strumento", on_click=agg_strumento)

    # --- LAYOUT ---
    page.add(
        toggle_cambia_tema,

        # Sezione 1
        txt_titolo,
        txt_responsabile,
        ft.Divider(),

        # Sezione 2
        ft.Text("Modifica Informazioni", size=20),
        ft.Row(spacing=200,
               controls=[input_responsabile, pulsante_conferma_responsabile],
               alignment=ft.MainAxisAlignment.CENTER),

        # Sezione 3
        # TODO
        txt_strumenti,
        ft.Row(controls=[
            input_tipo,
            input_marca,
            input_anno,
            ft.IconButton(icon=ft.Icons.REMOVE, on_click=counter_meno, icon_color=ft.Colors.RED),
            casella_valore,
            ft.IconButton(icon=ft.Icons.ADD, on_click=counter_piu, icon_color=ft.Colors.GREEN),
            ],
            alignment=ft.MainAxisAlignment.CENTER
        ),
        pulsante_aggiungi_strumento,

        # Sezione 4
        ft.Divider(),
        ft.Text("Strumenti", size=20),
        lista_strumenti,
    )
    aggiorna_lista_strumenti()

ft.run(main)
