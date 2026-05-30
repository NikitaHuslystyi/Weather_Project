import PyQt6.QtCore as core
import PyQt6.QtWidgets as widgets
import PyQt6.QtGui as gui
from datetime import datetime, timedelta
from utils import request
from utils import json_write

class Cards(widgets.QFrame):
    def __init__(self, parent, city_name):
        super().__init__(parent)
        self.city_name = city_name
        self.selected = False
        self.on_select_callback = None
        
        self.setStyleSheet("background-color: qlineargradient(x1:1, y1:0, x2:0, y2:1, stop:0 #FFDF56, stop:1 #87CEFA); background: transparent; border-radius: 0px; border-bottom: 1px solid rgba(255, 255, 255, 0.2)")
        self.setFixedSize(330, 90)
        card_frame_layout = widgets.QHBoxLayout()
        self.setLayout(card_frame_layout)
        
        left_layout = widgets.QVBoxLayout()
        left_layout.setSpacing(2)
        left_layout.setContentsMargins(5,1,5,10)
        left_frame = widgets.QFrame()
        left_frame.setFixedSize(180, 90)
        
        self.left_label1 = widgets.QLabel(text = city_name)
        self.left_label1.setStyleSheet("color: rgba(255, 255, 255, 1); font-size: 24px; font-weight: 500;")
        self.left_label2 = widgets.QLabel(text = "")
        self.left_label2.setStyleSheet("color: rgba(255, 255, 255, 0.8); font-size: 14px; font-weight: 500;")
        self.left_label3 = widgets.QLabel(text = "")
        self.left_label3.setStyleSheet("color: rgba(255, 255, 255, 0.8); font-size: 14px; font-weight: 500;")
        
        self.icon_label = widgets.QLabel()
        self.icon_label.setFixedSize(16, 16)
        self.icon_label.setPixmap(gui.QPixmap("media/title_bar/navigation.png").scaled(16, 16))
        self.icon_label.setVisible(False)
        self.title_layout = widgets.QHBoxLayout()
        self.title_layout.setSpacing(5)
        self.title_layout.setContentsMargins(0, 0, 0, 0)
        self.title_layout.addWidget(self.icon_label)
        self.title_layout.setSpacing(10)
        self.title_layout.addWidget(self.left_label1)
        title_container = widgets.QFrame()
        title_container.setLayout(self.title_layout)

        left_frame.setStyleSheet("""
                                QFrame{
                                    background: transparent;
                                    border-bottom: none;
                                    color: white
                                }
                                QLabel{
                                    border: none;
                                    color: white;
                                    
                                }
                            """)

        left_layout.addWidget(title_container, alignment = core.Qt.AlignmentFlag.AlignLeft)
        left_layout.addSpacing(3)
        left_layout.addWidget(self.left_label2, alignment = core.Qt.AlignmentFlag.AlignLeft)
        left_layout.addSpacing(8)
        left_layout.addWidget(self.left_label3, alignment = core.Qt.AlignmentFlag.AlignLeft)
        left_frame.setLayout(left_layout)
        
        right_layout = widgets.QVBoxLayout()
        right_layout.setSpacing(14)
        right_layout.setContentsMargins(5,5,0,10)
        
        right_frame = widgets.QFrame()
        self.right_label1 = widgets.QLabel(text = "")
        self.right_label2 = widgets.QLabel(text = "")

        self.right_label1.setStyleSheet("color: rgba(255, 255, 255, 0.8); font-size: 44px; font-weight: 500;")
        self.right_label2.setStyleSheet("color: rgba(255, 255, 255, 0.8); font-weight: 500; font-size: 12px;")
        right_frame.setStyleSheet("""
                                QFrame{
                                    background: transparent;
                                    border-bottom: none;
                                }
                                QLabel{
                                    border: none;
                                }
                            """)
        right_frame.setFixedSize(160,90)
        right_layout.setAlignment(core.Qt.AlignmentFlag.AlignCenter)
        right_layout.addWidget(self.right_label1, alignment = core.Qt.AlignmentFlag.AlignRight)
        right_layout.addWidget(self.right_label2, alignment = core.Qt.AlignmentFlag.AlignRight)
        right_frame.setLayout(right_layout)

        card_frame_layout.addWidget(left_frame)
        card_frame_layout.setSpacing(10)
        card_frame_layout.setContentsMargins(5,5,5,5)
        card_frame_layout.addStretch(1)
        card_frame_layout.addWidget(right_frame, alignment = core.Qt.AlignmentFlag.AlignRight)



        self.timezone_offset = 0

        self.update_timer = core.QTimer(self)
        self.update_timer.timeout.connect(self.refresh_weather1)
        self.update_timer.start(60000)

        self.time_timer = core.QTimer(self)
        self.time_timer.timeout.connect(self.update_local_time)
        self.time_timer.start(1000)

        self.refresh_weather1()
        self.update_local_time()

    def refresh_weather1(self):
        weather_data = request(city_name=self.city_name, request_type="current_weather")
        json_write("weather.json", weather_data)

        self.left_label1.setText(weather_data['name'])
        self.timezone_offset = weather_data['timezone']
        self.left_label3.setText(weather_data['weather'][0]['description'].capitalize())
        self.right_label1.setText(f"{int(weather_data['main']['temp'])}°")
        self.right_label2.setText(f"Макс.:{int(weather_data['main']['temp_max'])}°, мін.:{int(weather_data['main']['temp_min'])}°")
        self.update_local_time()

    def update_local_time(self):
        local_time = (datetime.utcnow() + timedelta(seconds=self.timezone_offset)).strftime("%H:%M")
        self.left_label2.setText(local_time)

    def mousePressEvent(self, event):
        if self.on_select_callback:
            self.on_select_callback(self)

    def set_selected(self, value: bool):
        self.selected = value
        if self.selected:
            self.icon_label.setVisible(True)
            self.setStyleSheet("""
                background-color: rgba(0, 0, 0, 0.2);
                border-radius: 10px;
                border-bottom: none;
            """)
        else:
            self.icon_label.setVisible(False)
            self.setStyleSheet("""
                background: transparent;
                border-radius: 0px;
                border-bottom: 1px solid rgba(255, 255, 255, 0.2);
            """)