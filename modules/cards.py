import PyQt6.QtCore as core
import PyQt6.QtWidgets as widgets
import PyQt6.QtGui as gui

class Cards(widgets.QFrame):
    def __init__(self, parent, city):
        super().__init__(parent)
        self.setStyleSheet("background-color: qlineargradient(x1:1, y1:0, x2:0, y2:1, stop:0 #FFDF56, stop:1 #87CEFA); background: transparent; border-radius: 10px; border-bottom: 1px solid white")
        self.setFixedSize(330, 90)
        card_frame_layout = widgets.QHBoxLayout()
        self.setLayout(card_frame_layout)
        
        
        left_layout = widgets.QVBoxLayout()
        left_layout.setSpacing(2)
        left_layout.setContentsMargins(5,10,5,10)
        left_frame = widgets.QFrame()
        left_frame.setFixedSize(130, 80)
        
        left_label1 = widgets.QLabel(city)
        left_label2 = widgets.QLabel(text = "time")
        left_label3 = widgets.QLabel(text = "weather")
        
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
        left_layout.setAlignment(core.Qt.AlignmentFlag.AlignTop)
        left_layout.addWidget(left_label1, alignment = core.Qt.AlignmentFlag.AlignLeft)
        left_layout.addWidget(left_label2, alignment = core.Qt.AlignmentFlag.AlignLeft)
        left_layout.addWidget(left_label3, alignment = core.Qt.AlignmentFlag.AlignLeft)
        left_frame.setLayout(left_layout)
        
        
        
        right_layout = widgets.QVBoxLayout()
        right_layout.setSpacing(2)
        right_layout.setContentsMargins(5,10,5,10)
        
        right_frame = widgets.QFrame()
        right_label1 = widgets.QLabel(text = "15°C")
        right_label2 = widgets.QLabel(text = "Макс.:17°, мін.: 0°")

        right_label1.setStyleSheet("color: white")
        right_label2.setStyleSheet("color: white")
        right_frame.setStyleSheet("""
                                QFrame{
                                    background: transparent;
                                    border-bottom: none;
                                }
                                QLabel{
                                    border: none;
                                    color: white;
                                }
                            """)
        right_frame.setFixedSize(130,80)
        right_layout.setAlignment(core.Qt.AlignmentFlag.AlignCenter)
        right_layout.addWidget(right_label1, alignment = core.Qt.AlignmentFlag.AlignHCenter)
        right_layout.addWidget(right_label2, alignment = core.Qt.AlignmentFlag.AlignBottom)
        right_frame.setLayout(right_layout)


        card_frame_layout.addWidget(left_frame)
        card_frame_layout.setSpacing(10)
        card_frame_layout.setContentsMargins(5,5,5,5)
        card_frame_layout.addStretch(1)
        card_frame_layout.addWidget(right_frame)
