import PyQt6.QtWidgets as widgets
import PyQt6.QtGui as QtGui
import PyQt6.QtCore as core
from .cards import Cards 



class LeftContainer(widgets.QFrame):
    def __init__(self, parent, weather_container, header):
        super().__init__(parent)
        self.current_selected_card = None
        self.SWITCH_THEME_TOOGLE = False
        self.weather_container = weather_container
        self.header = header
        self.added_cities = set()

        self.setFixedSize(370, 828)
        self.setStyleSheet("background-color: qlineargradient(x1:1, y1:0, x2:0, y2:1, stop:0 #808080, stop:1 #5DADE2)")
        
        self.LAYOUT = widgets.QVBoxLayout()
        self.LAYOUT.addSpacing(0)
        self.setLayout(self.LAYOUT)
        
        switch_button_frame = widgets.QFrame(parent = self)
        switch_button_frame.setFixedSize(330, 44)
        switch_button_frame.setStyleSheet("background: transparent")
        
        self.LAYOUT.addWidget(switch_button_frame)
        self.LAYOUT.setAlignment(core.Qt.AlignmentFlag.AlignTop)
        
        switch_theme_button_layout = widgets.QHBoxLayout()
        switch_theme_button_layout.setContentsMargins(0, 0, 0, 0)
        switch_theme_button = widgets.QPushButton(parent = switch_button_frame)
        switch_theme_button.setFixedSize(52,24)
        switch_theme_button.setIconSize(core.QSize(52,24))
        switch_theme_button.setStyleSheet("border: none")
        switch_theme_button_layout.addWidget(switch_theme_button)
        switch_theme_button_layout.setAlignment(core.Qt.AlignmentFlag.AlignRight)
        switch_button_frame.setLayout(switch_theme_button_layout)
        switch_icon = QtGui.QIcon("media/title_bar/Property 1=light.svg")
        switch_theme_button.setIcon(switch_icon)
        
        def switch_icon():
            if self.SWITCH_THEME_TOOGLE == False:
                switch_theme_button.setIcon(QtGui.QIcon("media/title_bar/Property 1=dark.svg"))
                self.SWITCH_THEME_TOOGLE = True
                self.weather_container.apply_theme_weather_container(True)
                self.apply_theme_left_container(True)
                self.header.apply_theme_header(True)
            else:
                switch_theme_button.setIcon(QtGui.QIcon("media/title_bar/Property 1=light.svg"))
                self.SWITCH_THEME_TOOGLE = False
                self.weather_container.apply_theme_weather_container(False)
                self.apply_theme_left_container(False)
                self.header.apply_theme_header(False)

        switch_theme_button.clicked.connect(switch_icon)
        
        scroll_area = widgets.QScrollArea(parent= self)
        
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(core.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setFrameShape(widgets.QFrame.Shape.NoFrame)
        self.LAYOUT.addWidget(scroll_area)
        
        scroll_frame = widgets.QFrame(parent= scroll_area)
        scroll_frame_layout = widgets.QVBoxLayout()
        self.scroll_frame_layout = scroll_frame_layout
        self.scroll_frame = scroll_frame
        scroll_frame_layout.setAlignment(core.Qt.AlignmentFlag.AlignTop)
        scroll_frame_layout.setSpacing(10)
        self.weather_container.left_container_ref = self
        scroll_frame.setLayout(scroll_frame_layout)
        
        scroll_area.setWidget(scroll_frame)

        
    def add_city_card(self, city_name):
        if city_name in self.added_cities:
            for i in range(self.scroll_frame_layout.count()):
                widget = self.scroll_frame_layout.itemAt(i).widget()
                if isinstance(widget, Cards) and widget.city_name == city_name:
                    self._select_card(widget)
                    return
            return
        self.added_cities.add(city_name)
        card = Cards(parent=self.scroll_frame, city_name=city_name, weather_container=self.weather_container)
        card.on_select_callback = lambda clicked_card: self._select_card(clicked_card)
        self.scroll_frame_layout.addWidget(card)
        self._select_card(card)

    def _select_card(self, card):
        if self.current_selected_card:
            self.current_selected_card.set_selected(False)
        card.set_selected(True)
        self.current_selected_card = card
        self.weather_container.update_city(card.city_name)

    def remove_city_card(self, city_name):
        if city_name in self.added_cities:
            self.added_cities.discard(city_name)
        was_selected = False
        
        for i in range(self.scroll_frame_layout.count()):
            widget = self.scroll_frame_layout.itemAt(i).widget()
            if isinstance(widget, Cards) and widget.city_name == city_name:
                if self.current_selected_card == widget:
                    self.current_selected_card = None
                    was_selected = True
                widget.deleteLater()
                break
        self.weather_container._remove_from_added_cities_scroll(city_name)

        if was_selected:
            self.weather_container.clear_weather_display()

    def update_all_cards_language(self):
        for i in range(self.scroll_frame_layout.count()):
            widget = self.scroll_frame_layout.itemAt(i).widget()
            if isinstance(widget, Cards):
                widget.update_language()

    def apply_theme_left_container(self, is_dark):
        if is_dark:
            self.setStyleSheet("background-color: qlineargradient(x1:1, y1:0, x2:0, y2:1, stop:0 rgba(74, 74, 74, 1), stop:1 rgba(93, 173, 226, 1))")
        else:
            self.setStyleSheet("background-color: qlineargradient(x1:1, y1:0, x2:0, y2:1, stop:0 #808080, stop:1 #5DADE2)")