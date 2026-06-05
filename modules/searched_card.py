import PyQt6.QtCore as core
import PyQt6.QtWidgets as widgets
import PyQt6.QtGui as gui


class SearchCityCard(widgets.QFrame):
    def __init__(self, parent, city_name):
        super().__init__(parent)

        self.city_name = city_name
        self.on_select_callback = None
        self.setFixedSize(261, 32)

        searched_card_layout = widgets.QHBoxLayout(self)
        searched_card_layout.setContentsMargins(8, 8, 8, 8)

        searched_card_label = widgets.QLabel(city_name)
        searched_card_label.setStyleSheet("color: rgba(255, 255, 255, 1); font-size: 14px; font-weight: 400; border: none; background: transparent; border-radius: 0px;")
        searched_card_layout.addWidget(searched_card_label)

        self.setStyleSheet("background: transparent; border: none; border-radius: 0px;")

    def mousePressEvent(self, event):
        if self.on_select_callback:
            self.on_select_callback(self.city_name)