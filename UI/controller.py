import flet as ft
from UI.view import View
from model.model import Model

'''
    CONTROLLER:
    - Funziona da intermediario tra MODELLO e VIEW
    - Gestisce la logica del flusso dell'applicazione
'''

class Controller:
    def __init__(self, view: View, model: Model):
        self._model = model
        self._view = view

        # Variabili per memorizzare le selezioni correnti
        self.biblioteca_selezionata = None
        self.genere_selezionato = None

    def popola_dropdowns(self):
        """ Popola i menu a tendina chiedendo i dati al Modello """
        # Aggiungiamo subito l'opzione di default in cima ad entrambi
        self._view.dd_biblioteca.options.append(ft.dropdown.Option("Nessun filtro"))
        self._view.dd_genere.options.append(ft.dropdown.Option("Nessun filtro"))

        # Recupera le biblioteche dal database e le aggiunge al Dropdown
        biblioteche = self._model.get_biblioteche()
        if biblioteche:
            for b in biblioteche:
                # b.nome corrisponde al nome della biblioteca nel DTO
                self._view.dd_biblioteca.options.append(ft.dropdown.Option(b.nome))

        # Recupera i generi e li aggiunge al Dropdown
        generi = self._model.get_generi()
        if generi:
            for g in generi:
                self._view.dd_genere.options.append(ft.dropdown.Option(g))

    def seleziona_biblioteca(self, e):
        valore = e.control.value
        # Se l'utente sceglie "Nessun filtro", salviamo None per farlo elaborare al COALESCE in SQL
        self.biblioteca_selezionata = None if valore == "Nessun filtro" else valore

    def seleziona_genere(self, e):
        valore = e.control.value
        self.genere_selezionato = None if valore == "Nessun filtro" else valore

    def mostra_libri(self, e):
        # Svuota i risultati precedenti
        self._view.lista_libri.controls.clear()

        # Interroga il Modello (e quindi il DB) passando i due filtri attuali
        libri = self._model.get_libri_filtrati(self.biblioteca_selezionata, self.genere_selezionato)

        # Gestione alert se la ricerca non produce risultati o se c'è un errore
        if not libri or len(libri) == 0:
            self._view.show_alert("Nessun libro soddisfa i criteri di filtraggio indicati.")
        else:
            for libro in libri:
                self._view.lista_libri.controls.append(ft.Text(str(libro)))

        # Aggiorna la vista
        self._view.update()