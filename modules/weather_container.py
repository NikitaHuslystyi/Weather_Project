from urllib import response
import PyQt6.QtCore as core
import PyQt6.QtWidgets as widgets
import PyQt6.QtGui as gui
from datetime import datetime, timedelta
import json
import requests
from utils import request
from utils import json_write
from .weather_scroll import ForecastCard
from .diagrama import WeatherDiagram


class WeatherContainer(widgets.QFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.city_name = "Dnipro"

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
        self.full_settings_frame.setStyleSheet("background: transparent; border: none;")
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
        
        self.settings_label = widgets.QLabel(text = "Налаштування")
        self.settings_label.setFixedSize(98, 16)
        self.settings_label.setStyleSheet("color: rgba(255, 255, 255, 1); font-size: 14px; font-weight: 500;")
        self.full_settings_layout.addWidget(self.settings_label, alignment = core.Qt.AlignmentFlag.AlignRight)
        
        self.top_layout.addWidget(self.full_settings_frame, alignment = core.Qt.AlignmentFlag.AlignLeft)
        
        self.full_searching_frame = widgets.QFrame()
        self.full_searching_frame.setFixedSize(261, 36)
        self.full_searching_frame.setStyleSheet("background: rgba(0, 0, 0, 0.2); border: none; border-radius: 4px;")
        self.full_searching_layout = widgets.QHBoxLayout()
        self.full_searching_layout.setContentsMargins(7, 8, 7, 8)
        self.full_searching_frame.setLayout(self.full_searching_layout)
        
        self.search_gryph_label = widgets.QLabel()
        self.search_gryph_label.setFixedSize(25, 22)
        self.search_gryph_label.setPixmap(gui.QPixmap("media/title_bar/Search Glyph.png"))
        self.search_gryph_label.setStyleSheet("background: transparent;")
        
        
        self.search_input = widgets.QLineEdit()
        self.search_input.setStyleSheet("background: transparent; border: none; font-size: 17px; font-weight: 400; color: rgba(255, 255, 255, 1);")
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
        self.add_button.setStyleSheet("background: rgba(0, 0, 0, 0.2); border-radius: 4px; border: none;")
        button_layout = widgets.QHBoxLayout(self.add_button)
        button_layout.setContentsMargins(7, 8, 7, 8)
        button_layout.setSpacing(6)
        
        add_icon_label = widgets.QLabel()
        add_icon_label.setFixedSize(16, 16)
        add_icon_label.setStyleSheet("background: transparent;")
        add_icon_label.setPixmap(gui.QPixmap("media/title_bar/plus-circle.png").scaled(16, 16, core.Qt.AspectRatioMode.KeepAspectRatio, core.Qt.TransformationMode.SmoothTransformation))
        text_label = widgets.QLabel("Додати")
        text_label.setFixedSize(58, 22)
        text_label.setStyleSheet("color: white; background: transparent; font-size: 17px; font-weight: 400;")
        button_layout.addWidget(add_icon_label, alignment = core.Qt.AlignmentFlag.AlignLeft)
        button_layout.addWidget(text_label)
        button_layout.addStretch()
        
        self.top_layout.addWidget(self.full_settings_frame, alignment = core.Qt.AlignmentFlag.AlignLeft)
        self.top_layout.addStretch()
        self.top_layout.addWidget(self.add_button)
        self.top_layout.addSpacing(0)
        self.top_layout.addWidget(self.full_searching_frame)
        
        self.add_button.setVisible(False)
        
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
        
        self.forecast_cards = []
        for i in range(12):
            forecast_card = ForecastCard(parent=self.scroll_content, city_name=self.city_name)
            self.forecast_cards.append(forecast_card)
            self.scroll_layout.addWidget(forecast_card)
        
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
        self.weather_diagram.update_forecast(forecast_list)
        visible_count = min(len(forecast_list), len(self.forecast_cards))

        for index, forecast_card in enumerate(self.forecast_cards):
            if index < visible_count:
                forecast_card.update_forecast_item(forecast_list[index], timezone_offset, index)
                forecast_card.setVisible(True)
            else:
                forecast_card.setVisible(False)
        
    def clear_search_field(self):
        self.search_input.clear()
        self.search_input.setFocus()

    def load_cities(self):
        response = requests.get("https://countriesnow.space/api/v0.1/countries")
        data = response.json()
        cities = []
        for country in data["data"]:
            cities.extend(country["cities"])
        cities = sorted(set(cities))
        with open("cities.json", "w", encoding="utf-8") as file:
            json.dump(cities, file, ensure_ascii=False, indent=4)
        return cities