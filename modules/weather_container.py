from urllib import response
import PyQt6.QtCore as core
import PyQt6.QtWidgets as widgets
import PyQt6.QtGui as gui
from datetime import datetime, timedelta
import json
import requests
import os
import folium
import io
import sys
import threading
from utils import request
from utils import json_write
from .weather_scroll import ForecastCard, SunCard
from .diagrama import WeatherDiagram
from .searched_card import SearchCityCard
from PyQt6.QtWebEngineWidgets import QWebEngineView

class WeatherContainer(widgets.QFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.city_name = "Dnipro"
        self.selected_search_city = None
        self.left_container_ref = None

        self.setFixedSize(828, 828)
        self.setStyleSheet("background-color: qlineargradient(x1:1, y1:0, x2:0, y2:1, stop:0 #FFDF56, stop:1 #87CEFA)")
        
        self.WEATHER_CONTEINER_LAYOUT = widgets.QVBoxLayout(self)
        self.WEATHER_CONTEINER_LAYOUT.setContentsMargins(20, 10, 20, 80)
        self.WEATHER_CONTEINER_LAYOUT.setSpacing(0)
        self.setLayout(self.WEATHER_CONTEINER_LAYOUT)
        
        self.TOP_FRAME = widgets.QFrame(self)
        self.TOP_FRAME.setFixedSize(788, 36)
        self.TOP_FRAME.setStyleSheet("background-color: transparent; border-radius: 10px; border-bottom: none;")
        
        self.top_layout = widgets.QHBoxLayout()
        self.top_layout.setContentsMargins(0, 0, 0, 0)
        self.TOP_FRAME.setLayout(self.top_layout)
        
        self.full_settings_frame = widgets.QFrame()
        self.full_settings_frame.setFixedSize(144, 36)
        self.full_settings_frame.setStyleSheet("background-color: transparent; border: none;")
        self.full_settings_layout = widgets.QHBoxLayout()
        self.full_settings_layout.setContentsMargins(0, 0, 0, 0)
        self.full_settings_frame.setLayout(self.full_settings_layout)
        
        
        self.setting_button_frame = widgets.QFrame()
        self.full_settings_layout.addWidget(self.setting_button_frame, alignment = core.Qt.AlignmentFlag.AlignLeft)
        self.setting_button_frame.setFixedSize(36, 36)
        self.setting_button_frame.setStyleSheet("background-color: rgba(0, 0, 0, 0.2); border-radius: 4px; border-bottom: none;")
        
        self.setting_button_layout = widgets.QHBoxLayout()
        self.setting_button_layout.setContentsMargins(10, 10, 10, 10)
        self.setting_button_layout.setSpacing(0)
        
        self.setting_button = widgets.QPushButton()
        self.setting_button.setFixedSize(16, 16)
        self.setting_button.setIconSize(core.QSize(36,36))
        self.setting_button.setStyleSheet("border: none; background-color: transparent;")
        
        self.setting_button_layout.addWidget(self.setting_button)
        self.setting_button_layout.setAlignment(core.Qt.AlignmentFlag.AlignCenter)
        self.setting_button_frame.setLayout(self.setting_button_layout)
        setting_icon = gui.QIcon("media/title_bar/settings.png")
        self.setting_button.setIcon(setting_icon)
        self.setting_button_frame.setStyleSheet("background-color: rgba(0, 0, 0, 0.2); border-radius: 10px; border: none;}")
        
        self.settings_label = widgets.QLabel(text = "Налаштування")
        self.settings_label.setFixedSize(98, 16)
        self.settings_label.setStyleSheet("color: rgba(255, 255, 255, 1); font-size: 14px; font-weight: 500;")
        self.full_settings_layout.addWidget(self.settings_label, alignment = core.Qt.AlignmentFlag.AlignRight)
        
        
        #New task(settings frame)
        self.whole_settings_frame = widgets.QFrame(self)
        self.whole_settings_frame.setGeometry(19, 56, 790, 688)
        self.whole_settings_frame.setStyleSheet("background-color: #363636; border-radius: 10px; border: none;")
        
        self.whole_settings_frame.setVisible(False)
        self.setting_button.clicked.connect(self.show_settings_frame)
        
        self.whole_settings_layout = widgets.QVBoxLayout(self.whole_settings_frame)
        self.whole_settings_layout.setContentsMargins(24, 24, 24, 24)
        self.whole_settings_layout.setSpacing(0)
        
        self.full_settings_string = widgets.QFrame()
        self.full_settings_string.setFixedSize(742,28)
        self.full_settings_string.setStyleSheet("background-color: transparent")
        self.whole_settings_layout.addWidget(self.full_settings_string, alignment = core.Qt.AlignmentFlag.AlignTop)
        
        self.whole_settings_string_layout = widgets.QHBoxLayout(self.full_settings_string)
        self.whole_settings_string_layout.setContentsMargins(0, 0, 0, 0)
        
        self.settings_text_label = widgets.QLabel(text="Налаштування")
        self.settings_text_label.setStyleSheet("background-color: transparent; color: rgba(255, 255, 255, 1); font-size: 24px; font-weight: 500; ")
        
        self.close_whole_settings_frame = widgets.QPushButton()
        self.close_whole_settings_frame.setFixedSize(24,24)
        self.close_whole_settings_frame.setIconSize(core.QSize(24,24))
        self.close_whole_settings_frame.setStyleSheet("border: none; background-color: transparent;")
        close_frame_icon = gui.QIcon("media/title_bar/x.png")
        self.close_whole_settings_frame.setIcon(close_frame_icon)
        self.close_whole_settings_frame.clicked.connect(self.whole_settings_frame.close)
        
        
        
        self.whole_settings_string_layout.addWidget(self.settings_text_label)
        self.whole_settings_string_layout.addStretch(1)
        self.whole_settings_string_layout.addWidget(self.close_whole_settings_frame)
        self.whole_settings_layout.addSpacing(34)
        
        
        self.settings_options_frame = widgets.QFrame()
        self.settings_options_frame.setFixedSize(742, 578)
        self.settings_options_frame.setStyleSheet("background-color: transparent; border-radius: 0px; border: 0px;")

        
        self.settings_options_layout = widgets.QHBoxLayout(self.settings_options_frame)
        self.settings_options_layout.setContentsMargins(0, 0, 0, 0)
        self.settings_options_layout.setSpacing(0)
        
        self.tabs_frame = widgets.QFrame()
        self.tabs_frame.setFixedSize(174, 578)
        self.tabs_frame.setStyleSheet("background-color: transparent; border-right: 1px solid rgba(255, 255, 255, 0.2); border-raidus: 0px")
        
        self.settings_options_layout.addWidget(self.tabs_frame, alignment = core.Qt.AlignmentFlag.AlignLeft)
        self.settings_options_layout.setSpacing(24)
        
        self.tabs_layout = widgets.QVBoxLayout(self.tabs_frame)
        self.tabs_layout.setContentsMargins(0, 0, 0, 0)
        self.tabs_layout.setSpacing(0)
        
        self.whole_tabs_frame = widgets.QFrame()
        self.whole_tabs_frame.setFixedSize(158, 140)
        self.whole_tabs_frame.setStyleSheet("background-color: transparent; border: none; border-radius: 0px")
        
        self.tabs_layout.addWidget(self.whole_tabs_frame, alignment = core.Qt.AlignmentFlag.AlignTop)
        
        self.whole_tabs_layout = widgets.QVBoxLayout(self.whole_tabs_frame)
        self.whole_tabs_layout.setContentsMargins(0, 0, 0, 0)
        self.whole_tabs_layout.setSpacing(0)
        
        self.tabs_city_finder_button = widgets.QPushButton()
        self.tabs_city_finder_button.setFixedSize(158, 35)
        self.tabs_city_finder_button.setStyleSheet("background-color: transparent; font-size: 16px; font-weight: 400; border: none;")
        
        self.tabs_city_finder_button_layout = widgets.QHBoxLayout(self.tabs_city_finder_button)
        self.tabs_city_finder_button_layout.setContentsMargins(8, 8, 8, 8)
        
        self.tabs_city_finder_button_label = widgets.QLabel(text = "Пошук міста")
        self.tabs_city_finder_button_label.setStyleSheet("background-color: transparent; color: rgba(255, 255, 255, 1)")
        
        self.tabs_city_finder_button_layout.addWidget(self.tabs_city_finder_button_label, alignment = core.Qt.AlignmentFlag.AlignLeft)
        
        
        self.tabs_app_size_button = widgets.QPushButton()
        self.tabs_app_size_button.setFixedSize(158, 35)
        self.tabs_app_size_button.setStyleSheet("background-color: transparent; font-size: 16px; font-weight: 400; border: none;")

        self.tabs_app_size_layout= widgets.QHBoxLayout(self.tabs_app_size_button)
        self.tabs_app_size_layout.setContentsMargins(8, 8, 8, 8)
        
        self.tabs_app_size_label = widgets.QLabel(text = "Розмір додатку")
        self.tabs_app_size_label.setStyleSheet("background-color: transparent; color: rgba(255, 255, 255, 1)")
        
        self.tabs_app_size_layout.addWidget(self.tabs_app_size_label, alignment = core.Qt.AlignmentFlag.AlignLeft)
        
        self.tabs_app_language_button = widgets.QPushButton()
        self.tabs_app_language_button.setFixedSize(158, 35)
        self.tabs_app_language_button.setStyleSheet("background-color: transparent; font-size: 16px; font-weight: 400; border: none;")

        self.tabs_app_language_layout = widgets.QHBoxLayout(self.tabs_app_language_button)
        self.tabs_app_language_layout.setContentsMargins(8, 8, 8, 8)
        
        self.tabs_app_language_label = widgets.QLabel(text = "Пошук міста")
        self.tabs_app_language_label.setStyleSheet("background-color: transparent; color: rgba(255, 255, 255, 1)")
        
        self.tabs_app_language_layout.addWidget(self.tabs_app_language_label, alignment = core.Qt.AlignmentFlag.AlignLeft)
        
        self.tabs_image_list_button = widgets.QPushButton()
        self.tabs_image_list_button.setFixedSize(158, 35)
        self.tabs_image_list_button.setStyleSheet("background-color: transparent; font-size: 16px; font-weight: 400; border: none;")
        
        self.tabs_image_list_layout = widgets.QHBoxLayout(self.tabs_image_list_button)
        self.tabs_image_list_layout.setContentsMargins(8, 8, 8, 8)
        
        self.tabs_image_list_label = widgets.QLabel(text = "Списки зображень")
        self.tabs_image_list_label.setStyleSheet("background-color: transparent; color: rgba(255, 255, 255, 1)")
        
        self.tabs_image_list_layout.addWidget(self.tabs_image_list_label, alignment = core.Qt.AlignmentFlag.AlignLeft)
        
        self.whole_tabs_layout.addWidget(self.tabs_city_finder_button, alignment = core.Qt.AlignmentFlag.AlignLeft)
        self.whole_tabs_layout.addWidget(self.tabs_app_size_button, alignment = core.Qt.AlignmentFlag.AlignLeft)
        self.whole_tabs_layout.addWidget(self.tabs_app_language_button, alignment = core.Qt.AlignmentFlag.AlignLeft)
        self.whole_tabs_layout.addWidget(self.tabs_image_list_button, alignment = core.Qt.AlignmentFlag.AlignLeft)
        
        self.whole_settings_layout.addWidget(self.settings_options_frame)
        
        
        self.whole_city_finder_frame = widgets.QFrame()
        self.whole_city_finder_frame.setFixedSize(544, 578)
        self.whole_city_finder_layout = widgets.QVBoxLayout(self.whole_city_finder_frame)
        self.whole_city_finder_layout.setContentsMargins(0, 0, 0, 56)
        self.settings_options_layout.addWidget(self.whole_city_finder_frame)
        
        self.city_finder_action_frame = widgets.QFrame()
        self.city_finder_action_frame.setFixedSize(544, 301)
        self.whole_city_finder_layout.addWidget(self.city_finder_action_frame)
        self.whole_city_finder_layout.setSpacing(24)
        self.city_finder_action_layout = widgets.QHBoxLayout(self.city_finder_action_frame)
        self.city_finder_action_layout.setContentsMargins(0, 0, 0, 0)
        
        
        
        self.city_finder_functions_frame = widgets.QFrame()
        self.city_finder_functions_frame.setFixedSize(239, 301)
        self.city_finder_action_layout.addWidget(self.city_finder_functions_frame)
        self.city_finder_action_layout.setSpacing(16)
        self.city_finder_functions_layout = widgets.QVBoxLayout(self.city_finder_functions_frame)
        self.city_finder_functions_layout.setContentsMargins(0, 0, 0, 0)
        self.city_finder_functions_layout.setSpacing(0)
        
        #Пошук міста
        self.city_finder_text_frame = widgets.QFrame()
        self.city_finder_functions_layout.addWidget(self.city_finder_text_frame, alignment = core.Qt.AlignmentFlag.AlignTop)
        self.city_finder_text_frame.setFixedSize(239, 21)
        self.city_finder_text_layout = widgets.QHBoxLayout(self.city_finder_text_frame)
        self.city_finder_text_layout.setContentsMargins(0, 0, 0, 0)
        self.city_finder_text_label = widgets.QLabel(text = "Пошук міста")
        self.city_finder_text_label.setStyleSheet("color: rgba(255, 255, 255, 1); font-size: 18px; font-weight: 400")
        self.city_finder_text_layout.addWidget(self.city_finder_text_label, alignment = core.Qt.AlignmentFlag.AlignLeft)
        
        #Контейнер со всеми функц cвязанные с картой
        self.map_funcs_frame = widgets.QFrame()
        self.city_finder_functions_layout.addWidget(self.map_funcs_frame)
        self.city_finder_functions_layout.setSpacing(24)
        self.map_funcs_layout = widgets.QVBoxLayout(self.map_funcs_frame)
        self.map_funcs_layout.setContentsMargins(0, 0, 0, 0)
        self.map_funcs_frame.setFixedSize(239, 194)
        
        
# КРАЇНА
        self.country_finder_frame = widgets.QFrame()
        self.map_funcs_layout.addWidget(self.country_finder_frame, alignment=core.Qt.AlignmentFlag.AlignTop)
        self.map_funcs_layout.setSpacing(16)
        self.country_finder_frame.setFixedSize(239, 56)
        self.country_finder_layout = widgets.QVBoxLayout(self.country_finder_frame)
        self.country_finder_layout.setContentsMargins(0, 0, 0, 0)
        self.country_finder_layout.setSpacing(8)

        self.country_text_label = widgets.QLabel(text="Країна")
        self.country_text_label.setFixedSize(239, 16)
        self.country_text_label.setStyleSheet("color: rgba(255, 255, 255, 1); font-size: 14px; font-weight: 500")
        self.country_finder_layout.addWidget(self.country_text_label)

        self.country_input_frame = widgets.QFrame()
        self.country_finder_layout.addWidget(self.country_input_frame)
        self.country_input_frame.setFixedSize(239, 32)
        self.country_input_frame.setStyleSheet("background-color: rgba(255, 255, 255, 1); border: none; border-radius: 4px;")
        country_input_layout = widgets.QHBoxLayout(self.country_input_frame)
        country_input_layout.setContentsMargins(10, 8, 10, 8)
        country_input_layout.setSpacing(5)

        self.country_search_input = widgets.QLineEdit()
        self.country_search_input.setStyleSheet("background-color: transparent; border: none; font-size: 12px; font-weight: 400; color: black;")
        self.country_search_input.setFixedSize(198, 16)
        self.country_search_input.setPlaceholderText("Виберіть країну")

        self.down_arrow_label1 = widgets.QLabel()
        self.down_arrow_label1.setFixedSize(16, 16)
        self.down_arrow_label1.setPixmap(gui.QPixmap("media/title_bar/chevron-down.png"))
        self.down_arrow_label1.setStyleSheet("background-color: transparent;")

        country_input_layout.addWidget(self.country_search_input, alignment=core.Qt.AlignmentFlag.AlignLeft)
        country_input_layout.addWidget(self.down_arrow_label1, alignment=core.Qt.AlignmentFlag.AlignRight)

        # Дропдаун країни
        self.country_dropdown = widgets.QFrame(self.whole_settings_frame)
        self.country_dropdown.setFixedSize(239, 200)
        self.country_dropdown.setStyleSheet("background-color: #363636; border-radius: 6px; border: none;")
        self.country_dropdown.setVisible(False)
        country_dd_layout = widgets.QVBoxLayout(self.country_dropdown)
        country_dd_layout.setContentsMargins(0, 0, 0, 0)
        country_dd_layout.setSpacing(0)
        self.country_dd_scroll = widgets.QScrollArea()
        self.country_dd_scroll.setWidgetResizable(True)
        self.country_dd_scroll.setVerticalScrollBarPolicy(core.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.country_dd_scroll.setHorizontalScrollBarPolicy(core.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.country_dd_scroll.setFrameShape(widgets.QFrame.Shape.NoFrame)
        self.country_dd_scroll.setStyleSheet("background: transparent; border: none;")
        self.country_dd_content = widgets.QFrame()
        self.country_dd_content.setStyleSheet("background: transparent; border: none;")
        self.country_dd_layout = widgets.QVBoxLayout(self.country_dd_content)
        self.country_dd_layout.setContentsMargins(0, 0, 0, 0)
        self.country_dd_layout.setSpacing(0)
        self.country_dd_layout.setAlignment(core.Qt.AlignmentFlag.AlignTop)
        self.country_dd_scroll.setWidget(self.country_dd_content)
        country_dd_layout.addWidget(self.country_dd_scroll)
        self.country_search_input.textChanged.connect(self.on_country_search_changed)

        # МІСТО
        self.city_finder_frame = widgets.QFrame()
        self.map_funcs_layout.addWidget(self.city_finder_frame)
        self.city_finder_frame.setFixedSize(239, 56)
        self.city_finder_layout = widgets.QVBoxLayout(self.city_finder_frame)
        self.city_finder_layout.setContentsMargins(0, 0, 0, 0)
        self.city_finder_layout.setSpacing(8)

        self.city_text_label = widgets.QLabel(text="Місто")
        self.city_text_label.setFixedSize(239, 16)
        self.city_text_label.setStyleSheet("color: rgba(255, 255, 255, 1); font-size: 14px; font-weight: 500")
        self.city_finder_layout.addWidget(self.city_text_label)

        self.city_input_frame = widgets.QFrame()
        self.city_finder_layout.addWidget(self.city_input_frame)
        self.city_input_frame.setFixedSize(239, 32)
        self.city_input_frame.setStyleSheet("background-color: rgba(255, 255, 255, 1); border: none; border-radius: 4px;")
        city_input_layout = widgets.QHBoxLayout(self.city_input_frame)
        city_input_layout.setContentsMargins(10, 8, 10, 8)
        city_input_layout.setSpacing(5)

        self.city_search_input = widgets.QLineEdit()
        self.city_search_input.setStyleSheet("background-color: transparent; border: none; font-size: 12px; font-weight: 400; color: black;")
        self.city_search_input.setFixedSize(198, 16)
        self.city_search_input.setPlaceholderText("Виберіть місто")

        self.down_arrow_label2 = widgets.QLabel()
        self.down_arrow_label2.setFixedSize(16, 16)
        self.down_arrow_label2.setPixmap(gui.QPixmap("media/title_bar/chevron-down.png"))
        self.down_arrow_label2.setStyleSheet("background-color: transparent;")

        city_input_layout.addWidget(self.city_search_input, alignment=core.Qt.AlignmentFlag.AlignLeft)
        city_input_layout.addWidget(self.down_arrow_label2, alignment=core.Qt.AlignmentFlag.AlignRight)

        # Дропдаун міста
        self.city_dropdown = widgets.QFrame(self.whole_settings_frame)
        self.city_dropdown.setFixedSize(239, 200)
        self.city_dropdown.setStyleSheet("background-color: #363636; border-radius: 6px; border: none;")
        self.city_dropdown.setVisible(False)
        city_dd_layout = widgets.QVBoxLayout(self.city_dropdown)
        city_dd_layout.setContentsMargins(0, 0, 0, 0)
        city_dd_layout.setSpacing(0)
        self.city_dd_scroll = widgets.QScrollArea()
        self.city_dd_scroll.setWidgetResizable(True)
        self.city_dd_scroll.setVerticalScrollBarPolicy(core.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.city_dd_scroll.setHorizontalScrollBarPolicy(core.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.city_dd_scroll.setFrameShape(widgets.QFrame.Shape.NoFrame)
        self.city_dd_scroll.setStyleSheet("background: transparent; border: none;")
        self.city_dd_content = widgets.QFrame()
        self.city_dd_content.setStyleSheet("background: transparent; border: none;")
        self.city_dd_layout = widgets.QVBoxLayout(self.city_dd_content)
        self.city_dd_layout.setContentsMargins(0, 0, 0, 0)
        self.city_dd_layout.setSpacing(0)
        self.city_dd_layout.setAlignment(core.Qt.AlignmentFlag.AlignTop)
        self.city_dd_scroll.setWidget(self.city_dd_content)
        city_dd_layout.addWidget(self.city_dd_scroll)
        self.city_search_input.textChanged.connect(self.on_city_search_changed)

        self.selected_settings_country = None
        self.selected_settings_city = None

        #Координати
        self.coord_finder_frame = widgets.QFrame()
        self.map_funcs_layout.addWidget(self.coord_finder_frame)
        self.coord_finder_frame.setFixedSize(239, 56)
        self.coord_finder_layout = widgets.QVBoxLayout(self.coord_finder_frame)
        self.coord_finder_layout.setContentsMargins(0, 0, 0, 0)
        
        self.coord_text_label = widgets.QLabel(text = "Координати")
        self.coord_text_label.setFixedSize(239, 16)
        self.coord_text_label.setStyleSheet("color: rgba(255, 255, 255, 1); font-size: 14px; font-weight: 500 ")
        self.coord_finder_layout.addWidget(self.coord_text_label)
        self.coord_finder_layout.setSpacing(8)
        
        self.coord_find_input_frame = widgets.QFrame()
        self.coord_finder_layout.addWidget(self.coord_find_input_frame)
        self.coord_find_input_frame.setFixedSize(239, 32)
        self.coord_find_input_frame.setStyleSheet("background-color: rgba(255, 255, 255, 1); border: none; border-radius: 4px;")
        self.coord_find_input_layout = widgets.QHBoxLayout()
        self.coord_find_input_layout.setContentsMargins(10, 8, 10, 8)
        self.coord_find_input_frame.setLayout(self.coord_find_input_layout)
        
        
        self.coord_search_input = widgets.QLineEdit()
        self.coord_search_input.setStyleSheet("background-color: transparent; border: none; font-size: 12px; font-weight: 400; color: black;")
        self.coord_search_input.setFixedSize(219, 16)
        self.coord_search_input.setPlaceholderText("(WGS 84,UTM,MGRS)")
        
        
        self.coord_find_input_layout.addWidget(self.coord_search_input, alignment = core.Qt.AlignmentFlag.AlignCenter)
        
        #Кнопка Зберегти
        save_button_frame = widgets.QFrame()
        save_button_frame.setFixedSize(105, 38)
        save_button_frame.setStyleSheet("background-color: #2b2b2b; border-radius: 4px")
        save_button_layout = widgets.QHBoxLayout(save_button_frame)
        save_button_layout.setContentsMargins(16, 8, 16, 8)
        
        save_button = widgets.QPushButton(text = "Зберегти")
        save_button.setStyleSheet("background-color: transparent; color: rgba(255, 255, 255, 1); font-size: 14px; font-weight: 400")
        save_button_layout.addWidget(save_button)
        save_button.clicked.connect(self.on_settings_save)
        
        self.city_finder_functions_layout.addWidget(save_button_frame)
        
        
        self.map_frame = widgets.QFrame()
        self.map_frame.setFixedSize(289, 301)
        self.map_frame.setStyleSheet("background-color: transparent; border-radius: 4px; border: none;")
        self.city_finder_action_layout.addWidget(self.map_frame)
        self.map_layout = widgets.QVBoxLayout(self.map_frame)
        self.map_layout.setContentsMargins(0, 45, 0, 0)
        
        self.web_view = QWebEngineView()
        self.web_view.setStyleSheet("background-color: transparent; border: none; border-radius: 4px;")
        map = folium.Map(width = 289, height = 256,location = [50, 50], tiles = "CartoDB Positron")
        data = io.BytesIO()
        map.save(data, close_file = False)
        html = data.getvalue().decode()
        self.web_view.setHtml(html)
        
        self.map_layout.addWidget(self.web_view)

        #Фрейм(Додані міста)
        self.added_cities_frame = widgets.QFrame()
        self.added_cities_frame.setFixedSize(544, 197)
        self.added_cities_layout = widgets.QVBoxLayout(self.added_cities_frame)
        self.added_cities_layout.setContentsMargins(0, 0, 0, 0)
        
        #Текст Додані міста
        self.added_cities_text_frame = widgets.QFrame()
        self.added_cities_layout.addWidget(self.added_cities_text_frame, alignment =core.Qt.AlignmentFlag.AlignTop)
        self.added_cities_text_frame.setFixedSize(544, 21)
        self.added_cities_text_frame.setStyleSheet("background-color: transparent;")
        self.added_cities_text_layout = widgets.QHBoxLayout(self.added_cities_text_frame)
        self.added_cities_text_layout.setContentsMargins(0, 0, 0, 0)
        
        self.added_cities_text_label = widgets.QLabel(text = "Додані міста")
        self.added_cities_text_label.setStyleSheet("background-color: transparent; color: rgba(255, 255, 255, 1); font-size: 18px; font-weight: 400")
        self.added_cities_text_layout.addWidget(self.added_cities_text_label, alignment = core.Qt.AlignmentFlag.AlignLeft)
        
        #Фрейм та скрол доданих міст
        # Скрол доданих міст
        self.added_cities_scroll_area = widgets.QScrollArea()
        self.added_cities_scroll_area.setFixedSize(544, 160)
        self.added_cities_scroll_area.setWidgetResizable(True)
        self.added_cities_scroll_area.setVerticalScrollBarPolicy(core.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.added_cities_scroll_area.setHorizontalScrollBarPolicy(core.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.added_cities_scroll_area.setFrameShape(widgets.QFrame.Shape.NoFrame)
        self.added_cities_scroll_area.setStyleSheet("background: #2b2b2b; border-radius: 6px; border: none;")

        self.added_cities_scroll_content = widgets.QFrame()
        self.added_cities_scroll_content.setStyleSheet("background: transparent; border: none;")
        self.added_cities_scroll_layout = widgets.QVBoxLayout(self.added_cities_scroll_content)
        self.added_cities_scroll_layout.setContentsMargins(16, 8, 16, 8)
        self.added_cities_scroll_layout.setSpacing(0)
        self.added_cities_scroll_layout.setAlignment(core.Qt.AlignmentFlag.AlignTop)

        self.added_cities_scroll_area.setWidget(self.added_cities_scroll_content)
        self.added_cities_layout.addWidget(self.added_cities_scroll_area)
        
        
        
        
        
        self.whole_city_finder_layout.addWidget(self.added_cities_frame)
        
        self.top_layout.addWidget(self.full_settings_frame, alignment = core.Qt.AlignmentFlag.AlignLeft)
        
        
        
        
        self.full_searching_frame = widgets.QFrame()
        self.full_searching_frame.setFixedSize(261, 36)
        self.full_searching_frame.setStyleSheet("background-color: rgba(0, 0, 0, 0.2); border: none; border-radius: 4px;")
        self.full_searching_layout = widgets.QHBoxLayout()
        self.full_searching_layout.setContentsMargins(7, 8, 7, 8)
        self.full_searching_frame.setLayout(self.full_searching_layout)
        
        self.search_gryph_label = widgets.QLabel()
        self.search_gryph_label.setFixedSize(25, 22)
        self.search_gryph_label.setPixmap(gui.QPixmap("media/title_bar/Search Glyph.png"))
        self.search_gryph_label.setStyleSheet("background-color: transparent;")
        
        
        self.search_input = widgets.QLineEdit()
        self.search_input.setStyleSheet("background-color: transparent; border: none; font-size: 17px; font-weight: 400; color: rgba(255, 255, 255, 1);")
        self.search_input.setFixedSize(220, 22)
        self.search_input.setPlaceholderText("Пошук")
        
        # Кнопка очищення поля пошуку
        self.clear_search_button = widgets.QPushButton()
        self.clear_search_button.setFixedSize(16, 16)
        self.clear_search_button.setStyleSheet("border: none; background-color: transparent;")
        self.clear_search_button.setCursor(core.Qt.CursorShape.PointingHandCursor)
        clear_icon = gui.QIcon("media/title_bar/Clear.png")
        self.clear_search_button.setIcon(clear_icon)
        self.clear_search_button.clicked.connect(self.clear_search_field)
        
        self.full_searching_layout.addWidget(self.search_gryph_label, alignment = core.Qt.AlignmentFlag.AlignRight)
        self.full_searching_layout.setSpacing(0)
        self.full_searching_layout.addWidget(self.search_input, alignment = core.Qt.AlignmentFlag.AlignRight)
        self.full_searching_layout.addWidget(self.clear_search_button, alignment = core.Qt.AlignmentFlag.AlignRight)
        
        #add button
        self.add_button = widgets.QPushButton()
        self.add_button.setFixedSize(97, 36)
        self.add_button.setStyleSheet("background-color: rgba(0, 0, 0, 0.2); border-radius: 4px; border: none;")
        button_layout = widgets.QHBoxLayout(self.add_button)
        button_layout.setContentsMargins(7, 8, 7, 8)
        button_layout.setSpacing(6)
        
        add_icon_label = widgets.QLabel()
        add_icon_label.setFixedSize(16, 16)
        add_icon_label.setStyleSheet("background-color: transparent;")
        add_icon_label.setPixmap(gui.QPixmap("media/title_bar/plus-circle.png").scaled(16, 16, core.Qt.AspectRatioMode.KeepAspectRatio, core.Qt.TransformationMode.SmoothTransformation))
        text_label = widgets.QLabel("Додати")
        text_label.setFixedSize(58, 22)
        text_label.setStyleSheet("color: white; background-color: transparent; font-size: 17px; font-weight: 400;")
        button_layout.addWidget(add_icon_label, alignment = core.Qt.AlignmentFlag.AlignLeft)
        button_layout.addWidget(text_label)
        button_layout.addStretch()
        
        self.top_layout.addWidget(self.full_settings_frame, alignment = core.Qt.AlignmentFlag.AlignLeft)
        self.top_layout.addStretch()
        self.top_layout.addWidget(self.add_button)
        self.top_layout.addSpacing(0)
        self.top_layout.addWidget(self.full_searching_frame)
        
        self.add_button.setVisible(False)
        


        # Подключаем сигналы
        self.search_input.textChanged.connect(self.on_search_text_changed)
        self.add_button.clicked.connect(self.on_add_city)

        # Dropdown фрейм
        self.search_dropdown_frame = widgets.QFrame(self)
        self.search_dropdown_frame.setGeometry(547, 56, 261, 200)
        self.search_dropdown_frame.setStyleSheet("background-color: #363636; border-radius: 10px; border: none;")
        self.search_dropdown_frame.setVisible(False)

        dropdown_main_layout = widgets.QVBoxLayout(self.search_dropdown_frame)
        dropdown_main_layout.setContentsMargins(0, 0, 0, 0)
        dropdown_main_layout.setSpacing(0)

        # Заголовок
        self.dropdown_header = widgets.QLabel("Результати пошуку")
        self.dropdown_header.setFixedSize(261, 32)
        self.dropdown_header.setAlignment(core.Qt.AlignmentFlag.AlignLeft)
        self.dropdown_header.setStyleSheet("""
            color: rgba(255, 255, 255, 0.8);
            font-size: 12px;
            font-weight: 400;
            background: transparent;
            border: none;
            border-radius: 0px;
            padding-left: 6px;
            padding-top: 8px;
            padding-right: px;
        """)
        dropdown_main_layout.addWidget(self.dropdown_header)

        # Скролл-область
        self.dropdown_scroll_area = widgets.QScrollArea()
        self.dropdown_scroll_area.setStyleSheet("background: transparent; border: none; border-radius: 0px;")
        self.dropdown_scroll_area.setWidgetResizable(True)
        self.dropdown_scroll_area.setVerticalScrollBarPolicy(core.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.dropdown_scroll_area.setHorizontalScrollBarPolicy(core.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.dropdown_scroll_area.setFrameShape(widgets.QFrame.Shape.NoFrame)

        self.dropdown_scroll_content = widgets.QFrame()
        self.dropdown_scroll_content.setStyleSheet("background: transparent; border: none; border-radius: 0px;")
        self.dropdown_scroll_layout = widgets.QVBoxLayout(self.dropdown_scroll_content)
        self.dropdown_scroll_layout.setContentsMargins(0, 0, 0, 0)
        self.dropdown_scroll_layout.setSpacing(0)
        self.dropdown_scroll_layout.setAlignment(core.Qt.AlignmentFlag.AlignTop)

        self.dropdown_scroll_area.setWidget(self.dropdown_scroll_content)
        dropdown_main_layout.addWidget(self.dropdown_scroll_area)

        self.search_dropdown_frame.raise_()

        
        self.WEATHER_CONTEINER_LAYOUT.addWidget(self.TOP_FRAME)
        self.WEATHER_CONTEINER_LAYOUT.addSpacing(10)

        self.CENTRAL_FRAME = widgets.QFrame(self)
        self.CENTRAL_FRAME.setFixedSize(788, 303)
        self.CENTRAL_FRAME.setStyleSheet("background-color: transparent")
        self.WEATHER_CONTEINER_LAYOUT.addWidget(self.CENTRAL_FRAME)
        self.WEATHER_CONTEINER_LAYOUT.addSpacing(4)
        self.CENTRAL_LAYOUT = widgets.QHBoxLayout(self.CENTRAL_FRAME)
        self.CENTRAL_LAYOUT.setSpacing(10)
        self.CENTRAL_LAYOUT.setContentsMargins(0, 0, 0, 0)
        self.CENTRAL_FRAME.setLayout(self.CENTRAL_LAYOUT)
        
        self.weather_right_frame = widgets.QFrame()
        self.weather_right_frame.setFixedSize(390, 303)
        self.weather_right_frame.setStyleSheet("background-color: rgba(0, 0, 0, 0.2); border-radius: 10px; border-bottom: none;")
        self.weather_right_layout1 = widgets.QVBoxLayout()
        self.weather_right_layout1.setContentsMargins(16, 8, 16, 16)
        self.weather_right_layout1.setSpacing(10)
        
        self.today_wrap = widgets.QFrame()
        self.today_wrap.setStyleSheet("background: transparent; border: none;")
        self.today_wrap_layout = widgets.QVBoxLayout()
        self.today_wrap_layout.setContentsMargins(0, 10, 0, 10)
        self.today_wrap_layout.setSpacing(0)
        self.today_wrap.setLayout(self.today_wrap_layout)
        
        self.today_right_label = widgets.QLabel(text="Сьогодні")
        self.today_right_label.setStyleSheet("""
            background-color: transparent;
            border-radius: 0px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.2);
            color: rgba(255, 255, 255, 1);
            font-size: 16px;
            font-weight: 500;
            padding-bottom: 10px;
        """)
        self.text_day_label = widgets.QLabel(text="Понеділок")
        self.text_day_label.setStyleSheet("color: rgba(255, 255, 255, 1); font-size: 24px; font-weight: 500;")
        self.text_data_label = widgets.QLabel(text="24.03.2025")
        self.text_data_label.setStyleSheet("color: rgba(255, 255, 255, 1); font-size: 24px; font-weight: 500;")
        self.watch_label = widgets.QLabel()
        self.watch_label.setStyleSheet("""
            background-color: transparent;
            border-radius: 0px;
            border-bottom: none;
            color: rgba(0, 0, 0, 0.2);
        """)
        self.watch_label.setFixedSize(168, 168)
        self.watch_label.setPixmap(gui.QPixmap("media/title_bar/Frame 55.png").scaled(168, 168))
        self.right_frame1 = widgets.QFrame()
        self.right_frame1.setStyleSheet("""
            background-color: transparent;
            border-radius: 0px;
            border-bottom: none;
        """)
        
        self.time_label = widgets.QLabel(text = '15:24')
        self.time_label.setStyleSheet("background-color: transparent; font-size: 29px; font-weight: 500; color: rgba(255, 255, 255, 1)")
        self.time_label_layout = widgets.QVBoxLayout()
        self.watch_label.setLayout(self.time_label_layout)
        self.time_label_layout.addWidget(self.time_label, alignment = core.Qt.AlignmentFlag.AlignCenter)

        self.weather_right_layout2 = widgets.QHBoxLayout()
        self.weather_right_layout2.setContentsMargins(0, 0, 0, 0)
        self.weather_right_layout2.setSpacing(0)
        self.right_frame1.setLayout(self.weather_right_layout2)
        self.weather_right_layout2.addWidget(self.text_day_label, alignment=core.Qt.AlignmentFlag.AlignLeft)
        self.weather_right_layout2.addStretch()
        self.weather_right_layout2.addWidget(self.text_data_label, alignment=core.Qt.AlignmentFlag.AlignRight)
        
        self.today_wrap_layout.addWidget(self.today_right_label)
        self.weather_right_layout1.addWidget(self.today_wrap)
        self.weather_right_layout1.addWidget(self.right_frame1)
        self.weather_right_layout1.addSpacing(0)
        self.weather_right_layout1.addWidget(self.watch_label, alignment = core.Qt.AlignmentFlag.AlignHCenter)
        self.weather_right_frame.setLayout(self.weather_right_layout1)
        
        
        self.weather_left_frame = widgets.QFrame()
        self.weather_left_frame.setFixedSize(390, 303)
        self.weather_left_frame.setStyleSheet("""
            background-color: rgba(0, 0, 0, 0.2);
            border-radius: 10px;
            border-bottom: none;
        """)
        
        self.weather_left_layout = widgets.QVBoxLayout()
        self.weather_left_layout.setContentsMargins(16, 8, 16, 8)
        self.weather_left_frame.setLayout(self.weather_left_layout)
        
        self.left_frame1 = widgets.QFrame()
        self.left_frame1.setStyleSheet("""
                                QFrame{
                                    background: transparent;
                                    border-bottom: 1px solid rgba(255, 255, 255, 0.2);;
                                    border-radius: 0px;
                                }
                                QLabel{
                                    border: none;
                                    background: transparent;
                                    
                                }
                            """)

        self.left_layout1 = widgets.QVBoxLayout()
        self.left_layout1.setContentsMargins(0, 10, 0, 10)
        self.left_layout1.setSpacing(0)
        self.left_frame1.setLayout(self.left_layout1)

        self.top_location_frame = widgets.QFrame()
        self.top_location_frame.setStyleSheet("""
            background-color: transparent;
            border-radius: 0px;
            border-bottom: none;
        """)
        self.top_location_layout = widgets.QHBoxLayout()
        self.top_location_layout.setContentsMargins(0, 0, 0, 0)
        self.top_location_layout.setSpacing(6)
        self.top_location_frame.setLayout(self.top_location_layout)
        
        self.geolocation_label = widgets.QLabel()
        self.geolocation_label.setFixedSize(16, 16)
        self.geolocation_label.setPixmap(gui.QPixmap("media/title_bar/navigation.png").scaled(16, 16))
        
        self.position_label = widgets.QLabel(text = "Поточна позиція")
        self.position_label.setStyleSheet("color: rgba(255, 255, 255, 1); font-size: 16px; font-weight: 500;")
        
        self.town_name_label = widgets.QLabel(text = "Дніпро")
        self.town_name_label.setStyleSheet("""
            background-color: transparent;
            border-radius: 0px;
            border-bottom: none;
            color: rgba(255, 255, 255, 1);
            font-size: 44px;
            font-weight: 500;
        """)
        
        self.weather_picture_label = widgets.QLabel()
        self.weather_picture_label.setStyleSheet("background: transparent;")
        self.weather_picture_label.setFixedSize(74, 74)
        self.weather_picture_label.setPixmap(gui.QPixmap("media/title_bar/Frame 1.png").scaled(74, 74, core.Qt.AspectRatioMode.KeepAspectRatio, core.Qt.TransformationMode.SmoothTransformation))
        
        self.temperature_label = widgets.QLabel(text = "11°".capitalize())
        self.temperature_label.setStyleSheet("color: rgba(255, 255, 255, 1); font-size: 67px; font-weight: 500;")
        
        self.weather_information_label = widgets.QLabel(text = "Хмарно")
        self.weather_information_label.setStyleSheet("color: rgba(255, 255, 255, 1); font-size: 24px; font-weight: 500;")
        
        self.min_max_label = widgets.QLabel(text = "Макс.:11°, мін.:0°")
        self.min_max_label.setStyleSheet("color: rgba(255, 255, 255, 0.8); font-size: 16px; font-weight: 500;")
        
        self.top_location_layout.addWidget(self.geolocation_label)
        self.top_location_layout.addWidget(self.position_label)
        self.top_location_layout.addStretch()
        self.left_layout1.addWidget(self.top_location_frame)
        
        self.left_frame2 = widgets.QFrame()
        self.left_frame2.setStyleSheet("""
            background-color: transparent;
            border-radius: 0px;
            border-bottom: none;
        """)
        
        self.left_layout2 = widgets.QHBoxLayout()
        self.left_layout2.setContentsMargins(0, 0, 0, 0)
        self.left_layout2.setSpacing(8)
        self.left_layout2.setAlignment(core.Qt.AlignmentFlag.AlignCenter)
        self.left_frame2.setLayout(self.left_layout2)
        self.left_layout2.addWidget(self.weather_picture_label, alignment = core.Qt.AlignmentFlag.AlignCenter)
        self.left_layout2.addWidget(self.temperature_label, alignment = core.Qt.AlignmentFlag.AlignCenter)
        
        self.left_frame3 = widgets.QFrame()
        self.left_frame3.setStyleSheet("""
            background-color: transparent;
            border-radius: 0px;
            border-bottom: none;
        """)
        self.left_layout3 = widgets.QVBoxLayout()
        self.left_frame3.setLayout(self.left_layout3)
        self.left_layout3.addWidget(self.weather_information_label, alignment = core.Qt.AlignmentFlag.AlignHCenter)
        self.left_layout3.addWidget(self.min_max_label, alignment = core.Qt.AlignmentFlag.AlignHCenter)
        
        self.weather_left_layout.addWidget(self.left_frame1)
        self.weather_left_layout.addSpacing(10)
        self.weather_left_layout.addWidget(self.town_name_label, alignment = core.Qt.AlignmentFlag.AlignHCenter)
        self.weather_left_layout.addSpacing(6)
        self.weather_left_layout.addWidget(self.left_frame2, alignment = core.Qt.AlignmentFlag.AlignHCenter)
        self.weather_left_layout.addWidget(self.left_frame3, alignment = core.Qt.AlignmentFlag.AlignHCenter)
        
        
        #New task
        
        self.forecast_weather_frame = widgets.QFrame()
        self.WEATHER_CONTEINER_LAYOUT.addWidget(self.forecast_weather_frame)
        self.forecast_weather_frame.setFixedSize(788, 157)
        self.forecast_weather_frame.setStyleSheet("""
            background: rgba(0, 0, 0, 0.2);
            border-bottom: none;
            border-radius: 10px;
        """)
        
        self.forecast_weather_layout = widgets.QVBoxLayout()
        self.forecast_weather_layout.setContentsMargins(16, 8, 16, 8)
        self.forecast_weather_layout.setSpacing(10)
        self.forecast_weather_frame.setLayout(self.forecast_weather_layout)
        
        self.information_weather_frame1 = widgets.QFrame()
        self.information_weather_frame1.setStyleSheet("""
            background: transparent;
            border: none;
        """)
        self.information_weather_layout1 = widgets.QVBoxLayout()
        self.information_weather_layout1.setContentsMargins(0, 8, 0, 0)
        self.information_weather_layout1.setSpacing(0)
        self.information_weather_frame1.setLayout(self.information_weather_layout1)
        self.forecast_weather_layout.addWidget(self.information_weather_frame1, alignment = core.Qt.AlignmentFlag.AlignTop)
        
        self.information_weather_label = widgets.QLabel(text = "Хмарна погода до кінця дня")
        self.information_weather_label.setStyleSheet("""
            background-color: transparent;
            border-radius: 0px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.2);
            color: rgba(255, 255, 255, 1);
            font-size: 16px;
            font-weight: 500;
            padding-bottom: 10px;
        """)
        self.information_weather_layout1.addWidget(self.information_weather_label)
        
        self.information_weather_frame2 = widgets.QFrame()
        self.information_weather_frame2.setStyleSheet("""
            background: transparent;
            border: none;
        """)
        self.information_weather_layout2 = widgets.QVBoxLayout()
        self.information_weather_layout2.setContentsMargins(0, 8, 0, 0)
        self.information_weather_layout2.setSpacing(0)
        self.information_weather_frame2.setLayout(self.information_weather_layout2)
        
        self.forecast_weather_layout.addWidget(self.information_weather_frame2)
        
        self.scroll_area = widgets.QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(core.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.setHorizontalScrollBarPolicy(core.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.setFrameShape(widgets.QFrame.Shape.NoFrame)
        self.scroll_area.setStyleSheet("""
            background: transparent;
            border: none;
        """)
        self.scroll_content = widgets.QFrame()
        self.scroll_content.setStyleSheet("""
            background: transparent;
            border: none;
        """)
        self.scroll_layout = widgets.QHBoxLayout()
        self.scroll_layout.setContentsMargins(8, 0, 8, 16)
        self.scroll_layout.setSpacing(10)
        self.scroll_content.setLayout(self.scroll_layout)
        self.scroll_area.setWidget(self.scroll_content)
        self.scroll_area.setMinimumHeight(82)
        
        self.scroll_controls_frame = widgets.QFrame()
        self.scroll_controls_frame.setStyleSheet("background: transparent; border: none;")
        self.scroll_controls_layout = widgets.QHBoxLayout()
        self.scroll_controls_layout.setContentsMargins(6, 0, 6, 16)
        self.scroll_controls_layout.setSpacing(28)
        self.scroll_controls_frame.setLayout(self.scroll_controls_layout)
        
        self.prev_button = widgets.QPushButton()
        self.prev_button.setFixedSize(16, 16)
        self.prev_button.setStyleSheet("""
            QPushButton {
                background: transparent;;
                color: rgba(255, 255, 255, 1);
                font-size: 16px;
            }
        """)
        left_icon = gui.QIcon("media/title_bar/chevron-left.png")
        self.prev_button.setIcon(left_icon)
        self.prev_button.clicked.connect(self.scroll_left)
        
        self.next_button = widgets.QPushButton()
        self.next_button.setFixedSize(16, 16)
        self.next_button.setStyleSheet("""
            QPushButton {
                background: transparent;;
                color: rgba(255, 255, 255, 1);
                font-size: 16px;
            }
        """)
        right_icon = gui.QIcon("media/title_bar/chevron-right.png")
        self.next_button.setIcon(right_icon)
        self.next_button.clicked.connect(self.scroll_right)
        
        self.scroll_controls_layout.addWidget(self.prev_button, alignment=core.Qt.AlignmentFlag.AlignVCenter)
        self.scroll_controls_layout.addWidget(self.scroll_area)
        self.scroll_controls_layout.addWidget(self.next_button, alignment=core.Qt.AlignmentFlag.AlignVCenter)
        self.information_weather_layout2.addWidget(self.scroll_controls_frame)
        

        
        self.WEATHER_CONTEINER_LAYOUT.addWidget(self.forecast_weather_frame)
        self.WEATHER_CONTEINER_LAYOUT.addSpacing(5)
        
        # Діаграма погоди
        self.weather_sheet_frame = widgets.QFrame()
        self.weather_sheet_frame.setFixedSize(788, 197)
        self.weather_sheet_frame.setStyleSheet("background-color: rgba(0, 0, 0, 0.2); border-radius: 10px; border-bottom: none;")
        
        
        self.text_diagram_layout1 = widgets.QVBoxLayout()
        self.text_diagram_layout1.setContentsMargins(16, 8, 16, 8)
        self.text_diagram_layout1.setSpacing(10)
        self.weather_sheet_frame.setLayout(self.text_diagram_layout1)
        
        
        self.text_diagram_frame = widgets.QFrame()
        self.text_diagram_frame.setStyleSheet("""
            background: transparent;
            border: none;
        """)

        self.text_diagram_layout2 = widgets.QVBoxLayout()
        self.text_diagram_layout2.setContentsMargins(0, 8, 0, 0)
        self.text_diagram_layout2.setSpacing(0)
        self.text_diagram_frame.setLayout(self.text_diagram_layout2)        
        
        self.text_diagram_layout1.addWidget(self.text_diagram_frame, alignment = core.Qt.AlignmentFlag.AlignTop)
        self.text_diagram_layout1.setSpacing(0)
        
        self.information_diagram_label = widgets.QLabel(text = "Прогноз на 36 годин")
        self.information_diagram_label.setStyleSheet("""
            background-color: transparent;
            border-radius: 0px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.2);
            color: rgba(255, 255, 255, 1);
            font-size: 16px;
            font-weight: 500;
            padding-bottom: 10px;
        """)
        self.text_diagram_layout2.addWidget(self.information_diagram_label)
        
        self.weather_images_frame = widgets.QFrame()
        self.weather_images_frame.setFixedSize(728, 24)
        self.weather_images_frame.setStyleSheet("""
            background: transparent;
            border: none;
            border-radius: 0px;
        """)
        self.weather_images_layout = widgets.QHBoxLayout()
        self.weather_images_layout.setSpacing(14)
        self.weather_images_layout.setContentsMargins(0, 0, 0, 0)
        self.weather_images_frame.setLayout(self.weather_images_layout)
        self.text_diagram_layout1.addWidget(self.weather_images_frame)
        
        self.diagram_frame = widgets.QFrame()
        self.diagram_frame.setFixedSize(755, 106)
        self.diagram_frame.setStyleSheet("""
            background: transparent;
            border: none;
            border-radius: 0px;
        """)
        self.all_diagram_layout = widgets.QHBoxLayout()
        self.all_diagram_layout.setContentsMargins(0, 0, 0, 0)
        self.all_diagram_layout.setSpacing(6)
        self.diagram_frame.setLayout(self.all_diagram_layout)
        
        self.diagram_frame2 = widgets.QFrame()
        self.diagram_frame2.setStyleSheet("""
            border-image: url(media/title_bar/Diagram.png) 0 0 0 0 stretch stretch;
            """)
        self.diagram_frame2.setFixedSize(727, 106)
        self.diagram_layout = widgets.QHBoxLayout()
        self.diagram_frame2.setLayout(self.diagram_layout)

        self.weather_diagram = WeatherDiagram(
            weather_images_layout=self.weather_images_layout,
            diagram_layout=self.diagram_layout,
            bar_count=21,
        )
        
        self.diagram_temp_frame = widgets.QFrame()
        self.diagram_temp_frame.setFixedSize(24, 106)
        temp_layout = widgets.QVBoxLayout()
        temp_layout.setContentsMargins(0, 2, 0, 2)
        temp_layout.setSpacing(0)
        temp_layout.setAlignment(core.Qt.AlignmentFlag.AlignLeft)
        self.diagram_temp_frame.setLayout(temp_layout)
        
        temps = [25, 20, 15, 10, 5, 0, -5, -10]
        for t in temps:
            label = widgets.QLabel(f"{t}°")
            label.setStyleSheet("""
                color: rgba(255, 255, 255, 1);
                font-size: 12px;
                font-weight: 400;
                background: transparent;
            """)
            temp_layout.addWidget(label)
        
        
        
        self.all_diagram_layout.addWidget(self.diagram_frame2)
        self.all_diagram_layout.addWidget(self.diagram_temp_frame)
        
        self.text_diagram_layout1.addWidget(self.diagram_frame)
        
        
        self.WEATHER_CONTEINER_LAYOUT.addWidget(self.weather_sheet_frame)
        
        self.CENTRAL_LAYOUT.addWidget(self.weather_left_frame)
        self.CENTRAL_LAYOUT.addWidget(self.weather_right_frame)
        
        self.watch_timezone_offset = 0

        self.whole_settings_frame.raise_()

        self.time_timer = core.QTimer(self)
        self.time_timer.timeout.connect(self.update_watch_time)
        self.time_timer.start(10000)
        
        
    def update_city(self, city_name):
        self.city_name = city_name
        self.refresh_weather2()
        
    def refresh_weather2(self):
        data = request(city_name=self.city_name, request_type="current_weather")
        self.town_name_label.setText(data["name"])
        self.temperature_label.setText(f"{int(data['main']['temp'])}°")
        self.weather_information_label.setText(data["weather"][0]["description"].capitalize())
        self.min_max_label.setText(f"Макс.:{int(data['main']['temp_max'])}°, мін.:{int(data['main']['temp_min'])}°")
        
        days = ["Понеділок","Вівторок","Середа","Четвер","П’ятниця","Субота","Неділя"]
        now = datetime.now()
        self.text_day_label.setText(days[now.weekday()])
        self.text_data_label.setText(now.strftime("%d.%m.%Y"))
        
        city_time = datetime.utcnow() + timedelta(seconds=data['timezone'])
        hour = city_time.hour
        is_night = hour >= 18 or hour < 6
        
        weather_type = data["weather"][0]["main"]
        
        day_icons = {
            "Clear": "media/title_bar/Sunny.png",
            "Clouds": "media/title_bar/Cloudy.png",
            "Rain": "media/title_bar/Rainy.png",
            "Drizzle": "media/title_bar/Rainy.png",
            "Thunderstorm": "media/title_bar/Thunderstorm.png",
            "Snow": "media/title_bar/Snowy.png"
        }
        night_icons = {
            "Clear": "media/title_bar/Moon.png",
            "Clouds": "media/title_bar/Cloudy_night.png",
            "Rain": "media/title_bar/Rainy_night.png",
            "Drizzle": "media/title_bar/Rainy_night.png",
            "Thunderstorm": "media/title_bar/Thunderstorm.png",
            "Snow": "media/title_bar/Snowy_night.png"
        }
        if is_night:
            icon_path = night_icons.get(weather_type, "media/title_bar/Cloudy_night.png")
        else:
            icon_path = day_icons.get(weather_type, "media/title_bar/Cloudy.png")
        self.weather_picture_label.setPixmap(gui.QPixmap(icon_path).scaled(74, 74, core.Qt.AspectRatioMode.KeepAspectRatio, core.Qt.TransformationMode.SmoothTransformation))
        
        self.watch_timezone_offset = data['timezone']
        self.update_watch_time()
        self.refresh_scroll_weather()

    def update_watch_time(self):
        correct_time = (datetime.utcnow() + timedelta(seconds=self.watch_timezone_offset)).strftime("%H:%M")
        self.time_label.setText(correct_time)

    def scroll_left(self):
        scrollbar = self.scroll_area.horizontalScrollBar()
        scrollbar.setValue(max(0, scrollbar.value() - 120))

    def scroll_right(self):
        scrollbar = self.scroll_area.horizontalScrollBar()
        scrollbar.setValue(min(scrollbar.maximum(), scrollbar.value() + 120))

    def refresh_scroll_weather(self):
        forecast_data = request(city_name=self.city_name, request_type="daily_forecast")
        json_write("forecast.json", forecast_data)

        forecast_list = forecast_data.get("list", [])
        timezone_offset = forecast_data.get("city", {}).get("timezone", 0)
        sunrise_ts = forecast_data.get("city", {}).get("sunrise", 0)
        sunset_ts = forecast_data.get("city", {}).get("sunset", 0)

        self.weather_diagram.update_forecast(forecast_list)
        
        while self.scroll_layout.count():
            item = self.scroll_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        sunrise_local = datetime.utcfromtimestamp(sunrise_ts + timezone_offset)
        sunset_local = datetime.utcfromtimestamp(sunset_ts + timezone_offset)
        sunrise_str = sunrise_local.strftime("%H:%M")
        sunset_str = sunset_local.strftime("%H:%M")

        sunrise_inserted = False
        sunset_inserted = False

        for index, forecast_item in enumerate(forecast_list[:12]):
            dt_ts = forecast_item.get("dt", 0)
            local_ts = dt_ts + timezone_offset
            dt_local = datetime.utcfromtimestamp(local_ts)

            if not sunrise_inserted and dt_local.time() >= sunrise_local.time():
                sun_card = SunCard(parent=self.scroll_content, sun_time=sunrise_str, sun_type="sunrise")
                self.scroll_layout.addWidget(sun_card)
                sunrise_inserted = True

            if not sunset_inserted and dt_local.time() >= sunset_local.time():
                sun_card = SunCard(parent=self.scroll_content, sun_time=sunset_str, sun_type="sunset")
                self.scroll_layout.addWidget(sun_card)
                sunset_inserted = True

            card = ForecastCard(parent=self.scroll_content, city_name=self.city_name)
            card.update_forecast_item(forecast_item, timezone_offset, index)
            self.scroll_layout.addWidget(card)
        
    def clear_search_field(self):
        self.search_input.clear()
        self.search_input.setFocus()

    def load_cities(self):
        response = requests.get("https://countriesnow.space/api/v0.1/countries")
        data = response.json()
        result = []
        for country in data["data"]:
            for city in country["cities"]:
                result.append({
                    "city": city,
                    "country": country["country"]
                })
        result = sorted(result, key=lambda x: x["city"])
        path = os.path.join(os.path.dirname(__file__), "..", "json", "cities.json")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as file:
            json.dump(result, file, ensure_ascii=False, indent=4)
        print(f"Збережено {len(result)} міст")
        return result

    def on_search_text_changed(self, text):
        text = text.strip()
        if not text:
            self.search_dropdown_frame.setVisible(False)
            self.add_button.setVisible(False)
            self.selected_search_city = None
            return

        all_cities = self._get_cities_list()
        matched = [c for c in all_cities if c["city"].lower().startswith(text.lower())][:15]

        while self.dropdown_scroll_layout.count():
            item = self.dropdown_scroll_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        if not matched:
            self.search_dropdown_frame.setVisible(False)
            return

        for item in matched:
            card = SearchCityCard(
                parent=self.dropdown_scroll_content,
                city_name=item["city"],
                country_name=item["country"]
            )
            card.on_select_callback = self.on_dropdown_city_selected
            self.dropdown_scroll_layout.addWidget(card)

        self.search_dropdown_frame.setVisible(True)
        self.search_dropdown_frame.raise_()

    def on_dropdown_city_selected(self, city_name):
        self.selected_search_city = city_name
        self.search_input.setText(city_name)
        self.search_dropdown_frame.setVisible(False)
        self.add_button.setVisible(True)

    def on_add_city(self):
        if not self.selected_search_city:
            return
        if self.left_container_ref:
            self.left_container_ref.add_city_card(self.selected_search_city)
        self.search_input.clear()
        self.add_button.setVisible(False)
        self.selected_search_city = None

    def _get_cities_list(self):
        path = os.path.join(os.path.dirname(__file__), "..", "json", "cities.json")
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            # Перевірка формату — якщо старий (список рядків) перезавантажуємо
            if data and isinstance(data[0], str):
                return self.load_cities()
            return data
        except Exception:
            return [
                {"city": "Kyiv", "country": "Ukraine"},
                {"city": "Kharkiv", "country": "Ukraine"},
                {"city": "London", "country": "United Kingdom"},
                {"city": "Berlin", "country": "Germany"},
                {"city": "Paris", "country": "France"},
            ]
    
    def show_settings_frame(self):
        self.whole_settings_frame.setVisible(True)
        self.whole_settings_frame.raise_()
    
    def on_country_search_changed(self, text):
        text = text.strip()
        while self.country_dd_layout.count():
            item = self.country_dd_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        if not text:
            self.country_dropdown.setVisible(False)
            return

        all_data = self._get_cities_list()
        countries = sorted(set(c["country"] for c in all_data))
        matched = [c for c in countries if c.lower().startswith(text.lower())][:15]

        if not matched:
            self.country_dropdown.setVisible(False)
            return

        for country in matched:
            card = self._make_settings_dd_card(country, self.country_dd_content, lambda c: self.on_country_selected(c))
            self.country_dd_layout.addWidget(card)

        # Позиціонуємо дропдаун відносно country_input_frame
        pos = self.country_input_frame.mapTo(self.whole_settings_frame, core.QPoint(0, 32))
        self.country_dropdown.move(pos)
        self.country_dropdown.setVisible(True)
        self.country_dropdown.raise_()

    def on_country_selected(self, country_name):
        self.selected_settings_country = country_name
        self.country_search_input.setText(country_name)
        self.country_dropdown.setVisible(False)
        self.city_search_input.clear()
        self.selected_settings_city = None

    def on_city_search_changed(self, text):
        text = text.strip()
        while self.city_dd_layout.count():
            item = self.city_dd_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        if not text:
            self.city_dropdown.setVisible(False)
            return

        all_data = self._get_cities_list()

        if self.selected_settings_country:
            filtered = [c for c in all_data if c["country"] == self.selected_settings_country]
        else:
            filtered = all_data

        matched = [c for c in filtered if c["city"].lower().startswith(text.lower())][:15]

        if not matched:
            self.city_dropdown.setVisible(False)
            return

        for item in matched:
            label = f"{item['city']}"
            card = self._make_settings_dd_card(label, self.city_dd_content, lambda c: self.on_settings_city_selected(c))
            self.city_dd_layout.addWidget(card)

        pos = self.city_input_frame.mapTo(self.whole_settings_frame, core.QPoint(0, 32))
        self.city_dropdown.move(pos)
        self.city_dropdown.setVisible(True)
        self.city_dropdown.raise_()

    def on_settings_city_selected(self, city_name):
        self.selected_settings_city = city_name
        self.city_search_input.setText(city_name)
        self.city_dropdown.setVisible(False)

    def _make_settings_dd_card(self, text, parent, callback):
        card = widgets.QFrame(parent)
        card.setFixedSize(239, 32)
        card.setStyleSheet("background: transparent; border: none;")
        card.setCursor(core.Qt.CursorShape.PointingHandCursor)
        layout = widgets.QHBoxLayout(card)
        layout.setContentsMargins(8, 4, 8, 4)
        label = widgets.QLabel(text)
        label.setStyleSheet("color: rgba(255,255,255,1); font-size: 13px; background: transparent; border: none;")
        layout.addWidget(label)

        def press(event, t=text):
            callback(t)
        card.mousePressEvent = press
        return card
    def on_settings_save(self):
        city = self.selected_settings_city
        if not city:
            return

        # Додаємо в лівий контейнер
        if self.left_container_ref:
            self.left_container_ref.add_city_card(city)

        # Додаємо карточку в скрол доданих міст
        self._add_to_added_cities_scroll(city)

        # Оновлюємо мінімапу
        self._update_minimap(city)

        # Скидаємо поля
        self.country_search_input.clear()
        self.city_search_input.clear()
        self.selected_settings_country = None
        self.selected_settings_city = None

    def _add_to_added_cities_scroll(self, city_name):
        # Перевіряємо чи вже є
        for i in range(self.added_cities_scroll_layout.count()):
            w = self.added_cities_scroll_layout.itemAt(i).widget()
            if w and w.property("city_name") == city_name:
                return

        card = widgets.QFrame()
        card.setFixedSize(512, 32)
        card.setProperty("city_name", city_name)
        card.setStyleSheet("background: transparent; border: none;")
        card_layout = widgets.QHBoxLayout(card)
        card_layout.setContentsMargins(0, 0, 0, 0)
        card_layout.setSpacing(0)

        city_label = widgets.QLabel(city_name)
        city_label.setStyleSheet("color: rgba(255,255,255,1); font-size: 14px; font-weight: 400; background: transparent; border: none;")
        card_layout.addWidget(city_label)
        card_layout.addStretch()

        delete_btn = widgets.QPushButton()
        delete_btn.setFixedSize(16, 16)
        delete_btn.setStyleSheet("background: transparent; border: none;")
        delete_btn.setIcon(gui.QIcon("media/title_bar/trash.png"))
        delete_btn.setIconSize(core.QSize(16, 16))
        delete_btn.setCursor(core.Qt.CursorShape.PointingHandCursor)
        delete_btn.clicked.connect(lambda checked, c=city_name, w=card: self._remove_city(c, w))
        card_layout.addWidget(delete_btn)

        self.added_cities_scroll_layout.addWidget(card)

    def _remove_city(self, city_name, card_widget):
        # Видаляємо з скролу налаштувань
        card_widget.deleteLater()

        # Видаляємо з лівого контейнера
        if self.left_container_ref:
            self.left_container_ref.remove_city_card(city_name)

    def _update_minimap(self, city_name):
        try:
            data = request(city_name=city_name, request_type="current_weather")
            lat = data["coord"]["lat"]
            lon = data["coord"]["lon"]
            
            # Записуємо координати в поле
            self.coord_search_input.setText(f"{lat}, {lon}")
            
            m = folium.Map(width=289, height=256, location=[lat, lon], zoom_start=10, tiles="CartoDB Positron")
            folium.Marker([lat, lon], tooltip=city_name).add_to(m)
            buf = io.BytesIO()
            m.save(buf, close_file=False)
            self.web_view.setHtml(buf.getvalue().decode())
        except Exception:
            pass

    def _ensure_cities_loaded(self):
        path = os.path.join(os.path.dirname(__file__), "..", "json", "cities.json")
        needs_reload = False
        if not os.path.exists(path):
            needs_reload = True
        else:
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                if data and isinstance(data[0], str):
                    needs_reload = True
                    print("Старий формат, перегенеруємо...")
            except Exception:
                needs_reload = True
        if needs_reload:
            print("Завантажуємо міста у фоні...")
            thread = threading.Thread(target=self.load_cities, daemon=True)
            thread.start()

    def on_add_city(self):
        if not self.selected_search_city:
            return
        if self.left_container_ref:
            self.left_container_ref.add_city_card(self.selected_search_city)
        # Синхронізуємо з скролом доданих міст в налаштуваннях
        self._add_to_added_cities_scroll(self.selected_search_city)
        self.search_input.clear()
        self.add_button.setVisible(False)
        self.selected_search_city = None

    def _remove_from_added_cities_scroll(self, city_name):
        for i in range(self.added_cities_scroll_layout.count()):
            w = self.added_cities_scroll_layout.itemAt(i).widget()
            if w and w.property("city_name") == city_name:
                w.deleteLater()
                break