import PyQt6.QtCore as core
import PyQt6.QtWidgets as widgets
import PyQt6.QtGui as gui

class Header(widgets.QFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.setStyleSheet("background-color: qlineargradient(x1:1, y1:0, x2:0, y2:1, stop:0 #FFDF56, stop:1 #87CEFA); border-top-left-radius: 20px; border-top-right-radius: 20px;")

        self.setFixedSize(self.window().width(), 40)
        
        layout = widgets.QHBoxLayout()
        
        layout.setAlignment(core.Qt.AlignmentFlag.AlignLeft)
        
        self.setLayout(layout)
        
        close_button = widgets.QPushButton(parent= self)
        close_button.setStyleSheet("background-color: transparent; border: none")
        close_icon = gui.QIcon("media/title_bar/Close_Button.svg")
        close_button.setIcon(close_icon)
        layout.addWidget(close_button)
        close_button.clicked.connect(self.window().close)
        
        minimize_button = widgets.QPushButton(parent= self)
        minimize_icon = gui.QIcon("media/title_bar/Minimize_Button.svg")
        minimize_button.setIcon(minimize_icon)
        layout.addWidget(minimize_button)
        minimize_button.setStyleSheet("background-color: transparent; border: none")
        minimize_button.clicked.connect(self.window().showMinimized)
        
        self.window()
        
        max_button = widgets.QPushButton(parent = self)
        max_button.setObjectName("MaxButton")
        
        max_close_icon = gui.QIcon("media/title_bar/Maximize_Button.svg")
        max_button.setIcon(max_close_icon)
        layout.addWidget(max_button)
        max_button.setStyleSheet("background-color: transparent; border: none")
        def toggle_maximize():
            if self.window().isMaximized():
                self.window().showNormal()
            else:
                self.window().showMaximized()
        max_button.clicked.connect(toggle_maximize)

    def mousePressEvent(self, event: gui.QMouseEvent):
        if event.button() == core.Qt.MouseButton.LeftButton:
            self.CLICK_COORD = event.position().toPoint()
        else:
            self.CLICK_COORD = None

    def mouseMoveEvent(self, event: gui.QMouseEvent):
        window = self.window()
        
        if self.CLICK_COORD:
            coord = event.position().toPoint() - self.CLICK_COORD
            
            print(window.x() + coord.x(), window.y() + coord.y())
            
            window.move(
                window.x() + coord.x(), 
                window.y() + coord.y()
            )

    def apply_theme_header(self, is_dark):
        if is_dark:
            self.setStyleSheet("""
                background-color: qlineargradient(x1:1, y1:0, x2:0, y2:1, stop:0 rgba(128, 128, 128, 1), stop:1 rgba(93, 173, 226, 1));
                border-top-left-radius: 20px;
                border-top-right-radius: 20px;
            """)
        else:
            self.setStyleSheet("""
                background-color: qlineargradient(x1:1, y1:0, x2:0, y2:1, stop:0 #FFDF56, stop:1 #87CEFA);
                border-top-left-radius: 20px;
                border-top-right-radius: 20px;
            """)