import PyQt6.QtCore as core
import PyQt6.QtWidgets as widgets
import PyQt6.QtGui as gui
from datetime import datetime, timedelta
import json
from utils import request
from utils import json_write

class WeatherContainer(widgets.QFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.city_name = "Dnipro"

        self.setFixedSize(828, 800)
        self.setStyleSheet("background-color: qlineargradient(x1:1, y1:0, x2:0, y2:1, stop:0 #FFDF56, stop:1 #87CEFA)")
        
        self.WEATHER_CONTEINER_LAYOUT = widgets.QVBoxLayout(self)
        self.WEATHER_CONTEINER_LAYOUT.setContentsMargins(20, 20, 20, 40)
        self.WEATHER_CONTEINER_LAYOUT.setSpacing(0)
        self.setLayout(self.WEATHER_CONTEINER_LAYOUT)
        
        self.TOP_FRAME = widgets.QFrame(self)
        self.TOP_FRAME.setFixedSize(788, 36)
        self.TOP_FRAME.setStyleSheet("background-color: rgba(0, 0, 0, 0.2); border-radius: 10px; border-bottom: none;")
        self.WEATHER_CONTEINER_LAYOUT.addWidget(self.TOP_FRAME)
        self.WEATHER_CONTEINER_LAYOUT.addSpacing(20)


        self.CENTRAL_FRAME = widgets.QFrame(self)
        self.CENTRAL_FRAME.setFixedSize(788, 303)
        self.CENTRAL_FRAME.setStyleSheet("background-color: transparent")
        self.WEATHER_CONTEINER_LAYOUT.addWidget(self.CENTRAL_FRAME)
        self.WEATHER_CONTEINER_LAYOUT.addSpacing(10)
        self.CENTRAL_LAYOUT = widgets.QHBoxLayout(self.CENTRAL_FRAME)
        self.CENTRAL_LAYOUT.setSpacing(10)
        self.CENTRAL_LAYOUT.setContentsMargins(0, 0, 0, 0)
        self.CENTRAL_FRAME.setLayout(self.CENTRAL_LAYOUT)
        
        self.weather_right_frame = widgets.QFrame()
        self.weather_right_frame.setStyleSheet("""
            background-color: rgba(0, 0, 0, 0.2);
            border-radius: 10px;
            border-bottom: none;
        """)
        self.weather_right_layout1 = widgets.QVBoxLayout()
        self.weather_right_frame.setLayout(self.weather_right_layout1)
        self.today_right_label = widgets.QLabel(text="Сьогодні")
        self.today_right_label.setStyleSheet("""
            background-color: transparent;
            border-radius: 0px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.2);
            color: rgba(255, 255, 255, 1);
            font-size: 16px;
            font-weight: 500;
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
        self.right_frame1.setLayout(self.weather_right_layout2)
        self.weather_right_layout2.addWidget(self.text_day_label)
        self.weather_right_layout2.addSpacing(80)
        self.weather_right_layout2.addWidget(self.text_data_label)
        
        self.weather_right_layout1.addWidget(self.today_right_label)
        self.weather_right_layout1.addWidget(self.right_frame1)
        self.weather_right_layout1.addWidget(self.watch_label, alignment = core.Qt.AlignmentFlag.AlignHCenter)
        self.weather_right_frame.setLayout(self.weather_right_layout1)
        
        
        self.weather_left_frame = widgets.QFrame()
        self.weather_left_frame.setStyleSheet("""
            background-color: rgba(0, 0, 0, 0.2);
            border-radius: 10px;
            border-bottom: none;
        """)
        self.weather_left_layout = widgets.QVBoxLayout()
        self.weather_left_layout.setContentsMargins(16, 8, 16, 8)
        self.weather_left_frame.setLayout(self.weather_left_layout)
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
        self.weather_picture_label.setFixedSize(76, 76)
        self.weather_picture_label.setPixmap(gui.QPixmap("media/title_bar/Group 1.png").scaled(76, 76, core.Qt.AspectRatioMode.KeepAspectRatio, core.Qt.TransformationMode.SmoothTransformation))
        self.temperature_label = widgets.QLabel(text = "11°".capitalize())
        self.temperature_label.setStyleSheet("color: rgba(255, 255, 255, 1); font-size: 67px; font-weight: 500;")
        self.weather_information_label = widgets.QLabel(text = "Хмарно")
        self.weather_information_label.setStyleSheet("color: rgba(255, 255, 255, 1); font-size: 24px; font-weight: 500;")
        self.min_max_label = widgets.QLabel(text = "Макс.:11°, мін.:0°")
        self.min_max_label.setStyleSheet("color: rgba(255, 255, 255, 0.8); font-size: 16px; font-weight: 500;")
        self.left_frame1 = widgets.QFrame()
        self.left_frame1.setStyleSheet("""
                                QFrame{
                                    background: transparent;
                                    border-radius: 0px;
                                    border-bottom: 1px solid rgba(255, 255, 255, 0.2);
                                }
                                QLabel{
                                    border: none;
                                    background: transparent;
                                }
                            """)
        self.left_layout1 = widgets.QHBoxLayout()
        self.left_frame1.setLayout(self.left_layout1)
        self.left_layout1.addWidget(self.geolocation_label)
        self.left_layout1.addWidget(self.position_label)
        
        self.left_frame2 = widgets.QFrame()
        self.left_frame2.setStyleSheet("""
            background-color: transparent;
            border-radius: 0px;
            border-bottom: none;
        """)
        self.left_layout2 = widgets.QHBoxLayout()
        self.left_frame2.setLayout(self.left_layout2)
        self.left_layout2.addWidget(self.weather_picture_label, alignment = core.Qt.AlignmentFlag.AlignCenter)
        self.left_layout2.addWidget(self.temperature_label, alignment = core.Qt.AlignmentFlag.AlignHCenter)
        
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
        self.weather_left_layout.addWidget(self.left_frame2, alignment = core.Qt.AlignmentFlag.AlignHCenter)
        self.weather_left_layout.addWidget(self.left_frame3, alignment = core.Qt.AlignmentFlag.AlignHCenter)
        
        
        self.scroll_weather_frame = widgets.QFrame(parent = self)
        self.scroll_weather_frame.setFixedSize(788, 157)
        self.scroll_weather_frame.setStyleSheet("background-color: rgba(0, 0, 0, 0.2); border-radius: 10px; border-bottom: none;")
        self.WEATHER_CONTEINER_LAYOUT.addWidget(self.scroll_weather_frame)
        self.WEATHER_CONTEINER_LAYOUT.addSpacing(10)
        
        
        self.weather_sheet_frame = widgets.QFrame()
        self.weather_sheet_frame.setFixedSize(788, 197)
        self.weather_sheet_frame.setStyleSheet("background-color: rgba(0, 0, 0, 0.2); border-radius: 10px; border-bottom: none;")
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
        data = request(city_name=self.city_name)
        self.town_name_label.setText(data["name"])
        self.temperature_label.setText(f"{int(data['main']['temp'])}°")
        self.weather_information_label.setText(data["weather"][0]["description"].capitalize())
        self.min_max_label.setText(f"Макс.:{int(data['main']['temp_max'])}°, мін.:{int(data['main']['temp_min'])}°")
        
        days = ["Понеділок","Вівторок","Середа","Четвер","П’ятниця","Субота","Неділя"]
        now = datetime.now()
        self.text_day_label.setText(days[now.weekday()])
        self.text_data_label.setText(now.strftime("%d.%m.%Y"))
        
        weather_type = data["weather"][0]["main"]
        icons = {
            "Clear": "media/title_bar/Sunny.png",
            "Clouds": "media/title_bar/Cloudy.png",
            "Rain": "media/title_bar/Rainy.png",
            "Drizzle": "media/title_bar/Rainy.png",
            "Thunderstorm": "media/title_bar/Rainy.png",
            "Snow": "media/title_bar/Snowy.png"
        }
        icon_path = icons.get(weather_type, "media/title_bar/Cloudy.png")
        self.weather_picture_label.setPixmap(gui.QPixmap(icon_path).scaled(76, 76, core.Qt.AspectRatioMode.KeepAspectRatio, core.Qt.TransformationMode.SmoothTransformation))
        
        self.watch_timezone_offset = data['timezone']
        self.update_watch_time()
        
    def update_watch_time(self):
        correct_time = (datetime.utcnow() + timedelta(seconds=self.watch_timezone_offset)).strftime("%H:%M")
        self.time_label.setText(correct_time)