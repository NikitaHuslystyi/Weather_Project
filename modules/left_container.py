import PyQt6.QtWidgets as widgets
import PyQt6.QtGui as QtGui
import PyQt6.QtCore as core
import PyQt6.QtWebEngineWidgets as WebEngine
from .cards import Cards 

import folium 
import io


class LeftContainer(widgets.QFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.current_selected_card = None
        self.SWITCH_THEME_TOOGLE = False
        
        self.setFixedSize(370, 800)
        self.setStyleSheet("background-color: qlineargradient(x1:1, y1:0, x2:0, y2:1, stop:0 #808080, stop:1 #5DADE2)")
        
        self.LAYOUT = widgets.QVBoxLayout()
        self.setLayout(self.LAYOUT)
        
        switch_button_frame = widgets.QFrame(parent = self)
        switch_button_frame.setFixedSize(330, 44)
        switch_button_frame.setStyleSheet("background: transparent")
        
        self.LAYOUT.addWidget(switch_button_frame)
        self.LAYOUT.setAlignment(core.Qt.AlignmentFlag.AlignTop)
        
        switch_theme_button_layout = widgets.QHBoxLayout()
        switch_theme_button = widgets.QPushButton(parent = switch_button_frame)
        switch_theme_button.setFixedSize(52,24)
        switch_theme_button.setIconSize(core.QSize(52,24))
        switch_theme_button.setStyleSheet("border: none")
        switch_theme_button_layout.addWidget(switch_theme_button)
        switch_theme_button_layout.setAlignment(core.Qt.AlignmentFlag.AlignRight)
        switch_button_frame.setLayout(switch_theme_button_layout)
        switch_icon = QtGui.QIcon("media/title_bar/Property 1=dark.svg")
        switch_theme_button.setIcon(switch_icon)
        
        def switch_icon():
            if self.SWITCH_THEME_TOOGLE == True:
                switch_icon1 = QtGui.QIcon("media/title_bar/Property 1=dark.svg")
                switch_theme_button.setIcon(switch_icon1)
                self.SWITCH_THEME_TOOGLE = False
            elif self.SWITCH_THEME_TOOGLE == False:
                switch_icon2 = QtGui.QIcon("media/title_bar/Property 1=light.svg")
                switch_theme_button.setIcon(switch_icon2)
                self.SWITCH_THEME_TOOGLE = True
        
        switch_theme_button.clicked.connect(switch_icon)
        
        # Указываем родителя QScrollArea
        scroll_area = widgets.QScrollArea(parent= self)
        
        # Указывает адаптивность размеров QScrollArea
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(core.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setFrameShape(widgets.QFrame.Shape.NoFrame)
        self.LAYOUT.addWidget(scroll_area)
        
        scroll_frame = widgets.QFrame(parent= scroll_area)
        scroll_frame_layout = widgets.QVBoxLayout()
        scroll_frame_layout.setAlignment(core.Qt.AlignmentFlag.AlignTop)
        scroll_frame_layout.setSpacing(10)
        scroll_frame.setLayout(scroll_frame_layout)
        
        scroll_area.setWidget(scroll_frame)
        
        cities = [
            "Kyiv",
            "Kharkiv",
            "Odesa",
            "Dnipro",
            "Lviv",
            "Zaporizhzhia",
            "Kryvyi Rih",
            "Mykolaiv",
            "Vinnytsia",
            "Kherson",
            "Poltava",
            "Chernihiv",
            "Sumy",
            "Zhytomyr",
            "Cherkasy",
            "Khmelnytskyi",
            "Rivne",
            "Ivano-Frankivsk",
            "Ternopil",
            "Lutsk",
            "Uzhhorod",
            "Crimea",
            "Donetsk",
            "Luhansk",
            "Copenhagen"
        ]
        
        for city in cities:
            card = Cards(
                parent=scroll_frame,
                city_name=city
            )
            def on_card_selected(clicked_card):
                if self.current_selected_card:
                    self.current_selected_card.set_selected(False)
                clicked_card.set_selected(True)
                self.current_selected_card = clicked_card
            card.on_select_callback = on_card_selected
            scroll_frame_layout.addWidget(card)
        
        
        # self.open_modal_button = widgets.QPushButton(parent = self, text = "Открыть окно")
        # self.open_modal_button.setGeometry(50,50,150,40)
        # self.open_modal_button.clicked.connect(self.open_modal)

    def open_modal(self):
        # Получаем главное окно (объект)
        main_window = self.window()
        
        self.MODAL = widgets.QWidget(main_window)
        self.MODAL.setGeometry(10,10, 790, 688)
        self.MODAL.setStyleSheet("background-color: white")
        modal_layout = widgets.QVBoxLayout()
        modal_layout.setAlignment(core.Qt.AlignmentFlag.AlignTop)
        
        # Объекты выравнивания
        # core.Qt.AlignmentFlag.AlignTop
        
        self.MODAL.setLayout(modal_layout)
        
        header_frame = widgets.QFrame(parent = self.MODAL)
        frame_layout = widgets.QHBoxLayout()
        frame_layout.setAlignment(core.Qt.AlignmentFlag.AlignRight)
        header_frame.setLayout(frame_layout)
        header_frame.setFixedSize(742, 28)
        modal_layout.addWidget(header_frame)
        header_frame.setStyleSheet("background-color: cyan")
        
        close_button = widgets.QPushButton(parent = header_frame)
        frame_layout.addWidget(close_button)
        close_button.setFixedSize(24, 24)
        
        icon = QtGui.QIcon("media/close.svg")
        close_button.setIcon(icon)
        close_button.clicked.connect(self.MODAL.hide)
        
        data = io.BytesIO()

        map = folium.Map(location = (50, 50))
        #save() - сохраняет данные карты в дате обьекта
        #close_file - =False(оставляем дата обьекта открытым для будущих обновлений карты)
        map.save(data,close_file = False)

        self.MODAL.show()
        web_engine_view = WebEngine.QWebEngineView(parent = self.MODAL)
        web_engine_view.setFixedSize(289,256)
        modal_layout.addWidget(web_engine_view)
        
        html = data.getvalue().decode()
        
        web_engine_view.setHtml(html)
        
