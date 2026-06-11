import PyQt6.QtCore as core
import PyQt6.QtWidgets as widgets
import PyQt6.QtGui as gui
from datetime import datetime, timedelta
from utils import request
from utils import json_write


class ForecastCard(widgets.QFrame):
    def __init__(self, parent, city_name):
        super().__init__(parent)

        self.city_name = city_name
        self.timezone_offset = 0
        self.setFixedSize(60, 82)
        self.setStyleSheet("background: transparent; color: white")
        forecastCard_layout = widgets.QVBoxLayout()
        forecastCard_layout.setContentsMargins(0, 0, 0, 0)
        forecastCard_layout.setSpacing(0)
        
        self.time_label = widgets.QLabel(text = "15")
        self.time_label.setStyleSheet("color: rgba(255, 255, 255, 1); font-size: 16px; font-weight: 500;")
        self.image_weather_label = widgets.QLabel()
        self.image_weather_label.setFixedSize(24, 24)
        self.image_weather_label.setPixmap(gui.QPixmap("media/p_weather/p_cloudy_sun.png").scaled(24, 24, core.Qt.AspectRatioMode.KeepAspectRatio, core.Qt.TransformationMode.SmoothTransformation))
        self.weather_temp_label = widgets.QLabel(text = "11°".capitalize())
        self.weather_temp_label.setStyleSheet("color: rgba(255, 255, 255, 1); font-size: 16px; font-weight: 500;")
        
        self.time_label.setAlignment(core.Qt.AlignmentFlag.AlignCenter)
        self.image_weather_label.setAlignment(core.Qt.AlignmentFlag.AlignCenter)
        self.weather_temp_label.setAlignment(core.Qt.AlignmentFlag.AlignCenter)
        
        forecastCard_layout.addWidget(self.time_label, alignment = core.Qt.AlignmentFlag.AlignHCenter)
        forecastCard_layout.addSpacing(10)
        forecastCard_layout.addWidget(self.image_weather_label, alignment = core.Qt.AlignmentFlag.AlignHCenter)
        forecastCard_layout.addSpacing(10)
        forecastCard_layout.addWidget(self.weather_temp_label, alignment = core.Qt.AlignmentFlag.AlignHCenter)
        
        self.setLayout(forecastCard_layout)

    def update_forecast_item(self, forecast_item, timezone_offset=0, index=0):
        self.timezone_offset = timezone_offset

        dt_ts = forecast_item.get("dt", 0)
        local_ts = dt_ts + timezone_offset
        dt_local = datetime.utcfromtimestamp(local_ts)
        
        if index == 0:
            self.time_label.setText("Зараз")
        else:
            self.time_label.setText(dt_local.strftime("%H"))

        temp = forecast_item.get("main", {}).get("temp")
        if temp is not None:
            self.weather_temp_label.setText(f"{int(round(temp))}°")
        else:
            self.weather_temp_label.setText("--°")

        weather = forecast_item.get("weather", [])
        weather_main = weather[0].get("main") if weather else None

        hour = dt_local.hour
        is_night = hour >= 18 or hour < 6

        icon_name = "p_cloudy_sun"
        if weather_main == "Clear":
            icon_name = "p_sun"
        elif weather_main == "Clouds":
            icon_name = "p_cloudy"
        elif weather_main in {"Rain", "Drizzle"}:
            icon_name = "p_rainy"
        elif weather_main == "Thunderstorm":
            icon_name = "p_thunderstorm"
        elif weather_main == "Snow":
            icon_name = "p_snowy"
        
        if is_night:
            suffix = "_moon"
        else:
            suffix = "_sun"
        icon_path = f"media/p_weather/{icon_name}{suffix}.png"
        pixmap = gui.QPixmap(icon_path)
        if pixmap.isNull():
            pixmap = gui.QPixmap("media/p_weather/p_cloudy_sun.png")
        self.image_weather_label.setPixmap(pixmap.scaled(24, 24, core.Qt.AspectRatioMode.KeepAspectRatio, core.Qt.TransformationMode.SmoothTransformation))

class SunCard(widgets.QFrame):
    def __init__(self, parent, sun_time, sun_type):
        super().__init__(parent)

        self.setFixedSize(92, 82)
        self.setStyleSheet("background: transparent; color: white")

        layout = widgets.QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.time_label = widgets.QLabel(text=sun_time)
        self.time_label.setStyleSheet("color: rgba(255, 255, 255, 1); font-size: 16px; font-weight: 500;")
        self.time_label.setAlignment(core.Qt.AlignmentFlag.AlignCenter)

        self.image_label = widgets.QLabel()
        self.image_label.setFixedSize(24, 24)
        icon_path = "media/title_bar/Sunrise.png" if sun_type == "sunrise" else "media/title_bar/Sunset.png"
        self.image_label.setPixmap(gui.QPixmap(icon_path).scaled(24, 24, core.Qt.AspectRatioMode.KeepAspectRatio, core.Qt.TransformationMode.SmoothTransformation))
        self.image_label.setAlignment(core.Qt.AlignmentFlag.AlignCenter)

        self.text_label = widgets.QLabel(text="Схід сонця" if sun_type == "sunrise" else "Захід сонця")
        self.text_label.setFixedSize(90, 20)
        self.text_label.setStyleSheet("color: rgba(255, 255, 255, 1); font-size: 16px; font-weight: 500;")
        self.text_label.setAlignment(core.Qt.AlignmentFlag.AlignCenter)
        self.text_label.setWordWrap(False)

        layout.addWidget(self.time_label, alignment=core.Qt.AlignmentFlag.AlignHCenter)
        layout.addSpacing(10)
        layout.addWidget(self.image_label, alignment=core.Qt.AlignmentFlag.AlignHCenter)
        layout.addSpacing(10)
        layout.addWidget(self.text_label, alignment=core.Qt.AlignmentFlag.AlignHCenter)

        self.setLayout(layout)

    def update_forecast_city(self, city_name):
        self.city_name = city_name
        self.setVisible(True)

    def refresh_forecast_data(self):
        forecast_data = request(city_name=self.city_name, request_type="daily_forecast")
        return forecast_data
        