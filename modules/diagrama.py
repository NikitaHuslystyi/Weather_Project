import PyQt6.QtCore as core
import PyQt6.QtWidgets as widgets
import PyQt6.QtGui as gui
import os


class WeatherDiagram:
    ICON_MAP = {
        "Clear": {"d": "media/p_weather/p_sun.png", "n": "media/p_weather/p_moon.png"},
        "Clouds": {"d": "media/p_weather/p_cloudy_sun.png", "n": "media/p_weather/p_cloudy_moon.png"},
        "Rain": {"d": "media/p_weather/p_rainy_sun.png", "n": "media/p_weather/p_rainy_moon.png"},
        "Drizzle": {"d": "media/p_weather/p_rainy_sun.png", "n": "media/p_weather/p_rainy_moon.png"},
        "Thunderstorm": {"d": "media/p_weather/p_thunderstorm_sun.png", "n": "media/p_weather/p_thunderstorm_moon.png"},
        "Snow": {"d": "media/p_weather/p_snowy_sun.png", "n": "media/p_weather/p_snowy_moon.png"},
    }
    DEFAULT_ICON = "media/p_weather/p_sun.png"
    MIN_TEMP = -10
    MAX_TEMP = 30
    PIXELS_PER_5_DEGREES = 13

    def __init__(self, weather_images_layout: widgets.QHBoxLayout, diagram_layout: widgets.QHBoxLayout, bar_count: int = 21):
        self.weather_images_layout = weather_images_layout
        self.diagram_layout = diagram_layout
        self.bar_count = bar_count
        self.weather_image_labels = []
        self.bar_frames = []

        self.diagram_layout.setSpacing(6)
        self.diagram_layout.setContentsMargins(0, 0, 0, 0)
        self.weather_images_layout.setSpacing(14)
        self.weather_images_layout.setContentsMargins(0, 0, 0, 0)

        for _ in range(self.bar_count):
            bar_frame = widgets.QFrame()
            bar_frame.setFixedSize(8, 8)
            bar_frame.setStyleSheet("background-color: qlineargradient(x1:1, y1:0, x2:0, y2:1, stop:0 rgba(255, 223, 86, 1), stop:1 rgba(135, 206, 250, 1)); border-radius: 0px;")
            self.bar_frames.append(bar_frame)
            self.diagram_layout.addWidget(bar_frame, alignment=core.Qt.AlignmentFlag.AlignBottom)

        for _ in range(self.bar_count):
            image_label = widgets.QLabel()
            image_label.setStyleSheet("background: transparent;")
            image_label.setFixedSize(16, 16)
            image_label.setPixmap(
                gui.QPixmap(self.DEFAULT_ICON).scaled(
                    16,
                    16,
                    core.Qt.AspectRatioMode.KeepAspectRatio,
                    core.Qt.TransformationMode.SmoothTransformation,
                )
            )
            self.weather_image_labels.append(image_label)
            self.weather_images_layout.addWidget(image_label)

    def _normalize_height(self, temperature: float) -> int:
        height = int((temperature - self.MIN_TEMP) * self.PIXELS_PER_5_DEGREES / 5)
        return max(4, min(106, height))

    def _icon_path(self, weather_type: str, pod: str) -> str:
        pod_flag = "n" if str(pod).lower().startswith("n") else "d"
        if weather_type in self.ICON_MAP:
            return self.ICON_MAP[weather_type].get(pod_flag, self.DEFAULT_ICON)
        return self.DEFAULT_ICON

    def update_forecast(self, forecast_list: list):
        count = min(len(forecast_list), self.bar_count)
        for index in range(self.bar_count):
            if index < count:
                item = forecast_list[index]
                temp = item.get("main", {}).get("temp", 0)
                height = self._normalize_height(temp)
                self.bar_frames[index].setFixedHeight(height)
                self.bar_frames[index].setVisible(True)

                weather_type = item.get("weather", [{}])[0].get("main", "Clear")
                pod = item.get("sys", {}).get("pod", "d")
                icon_path = self._icon_path(weather_type, pod)
                self.weather_image_labels[index].setPixmap(
                    gui.QPixmap(icon_path).scaled(
                        16,
                        16,
                        core.Qt.AspectRatioMode.KeepAspectRatio,
                        core.Qt.TransformationMode.SmoothTransformation,
                    )
                )
                self.weather_image_labels[index].setVisible(True)
            else:
                self.bar_frames[index].setVisible(False)
                self.weather_image_labels[index].setVisible(False)