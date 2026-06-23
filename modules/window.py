import PyQt6.QtCore as core
import PyQt6.QtWidgets as widgets
import PyQt6.QtGui as gui
from .header import Header
from .app import application
from .left_container import LeftContainer
from .weather_container import WeatherContainer


class MainWindow(widgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(core.Qt.WindowType.FramelessWindowHint)
        self.setAttribute(core.Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(core.Qt.WidgetAttribute.WA_NoSystemBackground)
        self.setStyleSheet("background: transparent;")

        window_width = 1200
        window_height = 840

        screen = application.primaryScreen()
        screen_size = screen.size()
        center_x = (screen_size.width() - window_width) // 2
        center_y = (screen_size.height() - window_height) // 2
        self.setGeometry(center_x, center_y, window_width, window_height)
        self.setMinimumSize(1200, 840)
        self.setWindowTitle("Project")

        self.content_container = widgets.QFrame(parent=self)
        self.content_container.setStyleSheet("background: transparent;")
        self.content_container.setGeometry(0, 0, window_width, window_height)

        content_layout = widgets.QVBoxLayout()
        content_layout.setSpacing(0)
        content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_container.setLayout(content_layout)

        self.HEADER = Header(parent=self.content_container)
        content_layout.addWidget(self.HEADER)

        central_widget = widgets.QFrame(self.content_container)
        central_widget.setStyleSheet("background: transparent;")
        central_widget.setSizePolicy(
            widgets.QSizePolicy.Policy.Expanding,
            widgets.QSizePolicy.Policy.Expanding
        )
        content_layout.addWidget(central_widget)

        center_widget_layout = widgets.QHBoxLayout()
        center_widget_layout.setSpacing(0)
        center_widget_layout.setContentsMargins(0, 0, 0, 0)
        central_widget.setLayout(center_widget_layout)

        self.WEATHER_CONTAINER = WeatherContainer(parent=central_widget)
        self.LEFT_CONTAINER = LeftContainer(
            parent=central_widget,
            weather_container=self.WEATHER_CONTAINER,
            header=self.HEADER
        )

        center_widget_layout.addWidget(self.LEFT_CONTAINER, stretch=370)
        center_widget_layout.addWidget(self.WEATHER_CONTAINER, stretch=830)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.content_container.setGeometry(0, 0, event.size().width(), event.size().height())

    def mousePressEvent(self, event: gui.QMouseEvent):
        if event.button() == core.Qt.MouseButton.RightButton:
            print("Правая кнопка")

    def keyPressEvent(self, event: gui.QKeyEvent):
        if event.key() == core.Qt.Key.Key_K:
            print(event.text())
            print(event.key())

    def mouseReleaseEvent(self, event: gui.QMouseEvent):
        if event.button() == core.Qt.MouseButton.RightButton:
            print("right: works")

    def keyReleaseEvent(self, event: gui.QKeyEvent):
        if event.key() == core.Qt.Key.Key_K:
            print(f"Key: {event.key()}")
            print(f"Text: {event.text()}")

    def set_app_size(self, width, height):
            screen = application.primaryScreen()
            screen_size = screen.size()
            center_x = (screen_size.width() - width) // 2
            center_y = (screen_size.height() - height) // 2

            self.setMinimumSize(width, height)
            self.setGeometry(center_x, center_y, width, height)
            self.content_container.setGeometry(0, 0, width, height)


main_window = MainWindow()