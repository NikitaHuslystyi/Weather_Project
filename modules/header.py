import PyQt6.QtCore as core
import PyQt6.QtWidgets as widgets
import PyQt6.QtGui as gui

class Header(widgets.QFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self.setStyleSheet("background-color: #FFF")
        self.setFixedSize(self.window().width(), 40)
        
        layout = widgets.QHBoxLayout()
        
        layout.setAlignment(core.Qt.AlignmentFlag.AlignLeft)
        
        self.setLayout(layout)
        
        # Настройки: Создать виджет, Добавить в лейаут, Настроить размеры 16х16, Указать иконку, Прикрепить метод
        
        # Егор Войтов. Создать кнопку close
        close_button = widgets.QPushButton(parent= self)
        close_icon = gui.QIcon("media/title_bar/Close_Button.svg")
        close_button.setIcon(close_icon)
        layout.addWidget(close_button)
        close_button.setStyleSheet("border: none")
        close_button.clicked.connect(self.window().close)
        
        # Полина. Создать кнопку minimize
        minimize_button = widgets.QPushButton(parent= self)
        minimize_icon = gui.QIcon("media/title_bar/Minimize_Button.svg")
        minimize_button.setIcon(minimize_icon)
        layout.addWidget(minimize_button)
        minimize_button.setStyleSheet("border: none")
        minimize_button.clicked.connect(self.window().showMinimized)
        
        # Получение окна
        self.window()
        
        # Егор Столяров. Создать кнопку maximize
        max_button = widgets.QPushButton(parent = self)
        max_button.setObjectName("MaxButton")
        
        max_close_icon = gui.QIcon("media/title_bar/Maximize_Button.svg")
        max_button.setIcon(max_close_icon)
        layout.addWidget(max_button)
        max_button.setStyleSheet("border: none")
        max_button.clicked.connect(self.window().showMaximized)
    
    def mousePressEvent(self, event: gui.QMouseEvent):
        
        if event.button() == core.Qt.MouseButton.LeftButton:
            self.CLICK_COORD = event.position().toPoint()
        else:
            self.CLICK_COORD = None
    
    def mouseMoveEvent(self, event: gui.QMouseEvent):
        window = self.window()
        
        if self.CLICK_COORD:
            # Получаем координаты курсора
            coord = event.position().toPoint() - self.CLICK_COORD
            
            print(window.x() + coord.x(), window.y() + coord.y())
            
            window.move(
                window.x() + coord.x(), 
                window.y() + coord.y()
            )
        
