# Archivo: src/controllers/report_controller.py

from typing import List, Dict, Any, Optional
from PySide6.QtCore import Slot
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtWidgets import QWidget
from utils import utils_db
from utils.utils_popup import _printv2
from models.report_model import ReportModel
from views.report_view import ReportView
from widgets.custom_chart_widget import CustomChartWidget


class ReportController:
    """
    Controlador que actúa como intermediario entre el modelo y la vista,
    gestionando la lógica de la aplicación y la interacción entre la base de datos y la interfaz de usuario.
    """

    def __init__(self, report_view: ReportView, report_model: ReportModel, popup_parent: Optional[QWidget] = None):
        """
        Inicializa el controlador, configurando la vista, el modelo y el gestor de popups.

        Parámetros:
        - report_view (ReportView): Vista para mostrar la interfaz de usuario.
        - report_model (ReportModel): Modelo de datos para interactuar con la base de datos.
        - popup_parent (QWidget | None): Widget padre opcional para asociar los popups a la ventana principal.
        """
        if not report_view or not report_model:
            raise ValueError("Se requieren tanto la vista como el modelo para inicializar el controlador.")

        self._view: ReportView = report_view
        self._model: ReportModel = report_model
        self._popup_parent: Optional[QWidget] = popup_parent

        # Conectar señales
        self._view.apply_filters_signal.connect(self._apply_filters)

        # Inicializar vista
        self._initialize_view()
    # __init__ (fin)

    def _initialize_view(self) -> None:
        """
        Inicializa la vista cargando los datos iniciales y las categorías.
        """
        try:
            # Cargar datos iniciales de la tabla "productos"
            model_data: Optional[Dict[str, Any]] = self._model._get_model(utils_db.EnumTablasDB.CANCIONES.value)
            if model_data:
                prepared_data: QStandardItemModel = self._prepare_table_data(model_data)
                self._view._set_model(prepared_data)

                # Configurar el gráfico inicial
                chart_data = self._prepare_chart_data(model_data)
                self._view._set_chart(chart_data)
            else:
                _printv2(show_popup=False, parent=self._popup_parent, message="No se encontraron datos en la tabla 'canciones'.")
                self._view._clear_chart()

            # Cargar generos
            genres_data: Optional[List[Dict[str, Any]]] = self._model._fetch_data(utils_db.EnumTablasDB.GENEROS.value)
            if genres_data:
                genres: List[str] = [row["nombre_genero"] for row in genres_data]
                self._view._set_categories(genres)
            else:
                _printv2(show_popup=False, parent=self._popup_parent, message="No se encontraron géneros.")
        except Exception as e:
            error_msg: str = f"Error al inicializar la vista: {e}"
            _printv2(show_popup=False, parent=self._popup_parent, message=error_msg)
    # _initialize_view (fin)

    @Slot(str, str)
    def _apply_filters(self, search_text: str, category: str) -> None:
        """
        Aplica los filtros recibidos desde la vista y actualiza los datos mostrados.

        Parámetros:
        - search_text (str): Texto ingresado en la barra de búsqueda.
        - category (str): Categoría seleccionada para filtrar.
        """
        try:
            model_data: Optional[List[Dict[str, Any]]] = self._model._fetch_data(utils_db.EnumTablasDB.CANCIONES.value)

            if not model_data:
                _printv2(show_popup=False, parent=self._popup_parent, message="No se encontraron datos para aplicar filtros.")
                self._view._clear_chart()
                self._view._set_model(QStandardItemModel())
                return

            # Filtrar datos
            filtered_data: List[Dict[str, Any]] = [
                row for row in model_data
                if search_text.lower() in row["producto"].lower() and (category == "Todas" or row["categoria"] == category)
            ]

            # Actualizar tabla
            prepared_data: QStandardItemModel = self._prepare_table_data({
                "columns": ["producto", "descripcion", "precio", "stock", "ventas"],
                "data": filtered_data,
            })
            self._view._set_model(prepared_data)

            # Actualizar gráfico
            chart_data = self._prepare_chart_data({
                utils_db.EnumEjes.EJE_X.value: [row["producto"] for row in filtered_data],
                utils_db.EnumEjes.EJE_Y.value: {"Ventas": [int(row["ventas"]) for row in filtered_data]},
            })
            self._view._set_chart(chart_data)
        except Exception as e:
            error_msg: str = f"Error al aplicar filtros: {e}"
            _printv2(show_popup=False, parent=self._popup_parent, message=error_msg)
    # _apply_filters (fin)

    def _prepare_table_data(self, model_data: Dict[str, Any]) -> QStandardItemModel:
        """
        Prepara los datos para ser usados en un QStandardItemModel, compatible con QTableView.

        Parámetros:
        - model_data (dict): Diccionario que contiene las columnas y los datos de la tabla.

        Retorno:
        - QStandardItemModel: Modelo de datos compatible con QTableView.
        """
        qt_model: QStandardItemModel = QStandardItemModel()

        # Configurar columnas
        columns: List[str] = model_data.get("columns", [])
        qt_model.setHorizontalHeaderLabels(columns)

        # Agregar filas
        for row in model_data.get("data", []):
            items: List[QStandardItem] = [QStandardItem(str(row.get(col, ""))) for col in columns]
            qt_model.appendRow(items)

        return qt_model
    # _prepare_table_data (fin)

    def _prepare_chart_data(self, model_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Prepara los datos estructurados para graficar en el CustomChartWidget.

        Parámetros:
        - model_data (dict): Diccionario que contiene los datos estructurados.

        Retorno:
        - dict: Datos en el formato esperado por CustomChartWidget.
        """
        eje_x: List[str] = model_data.get(utils_db.EnumEjes.EJE_X.value, [])
        barritas_datos: Dict[str, List[int]] = model_data.get(utils_db.EnumEjes.EJE_Y.value, {})

        return {
            utils_db.EnumEjes.EJE_X.value: eje_x,
            utils_db.EnumEjes.EJE_Y.value: barritas_datos
        }
    # _prepare_chart_data (fin)
# ReportController (fin)
