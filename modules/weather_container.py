import PyQt6.QtCore as core
import PyQt6.QtWidgets as widgets

import json

from utils import request


class WeatherContainer(widgets.QFrame):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.setFixedSize(828, 800)
        self.setStyleSheet("background-color: qlineargradient(x1:1, y1:0, x2:0, y2:1, stop:0 #FFDF56, stop:1 #87CEFA)")
        
        self.WEATHER_CONTEINER_LAYOUT = widgets.QVBoxLayout(self)
        self.setLayout(self.WEATHER_CONTEINER_LAYOUT)
        
        self.TOP_FRAME = widgets.QFrame(self)
        self.TOP_FRAME.setFixedSize(788, 36)
        self.TOP_FRAME.setStyleSheet("background-color: grey")
        self.WEATHER_CONTEINER_LAYOUT.addWidget(self.TOP_FRAME)
        
        
        # response = request("Sydney")
        
        # print(json.dumps(response, indent=4))
        
        # if response["cod"] != 404:
        #     label = widgets.QLabel(self.CETRAL_FRAME, text = str(response["main"]["temp"]))
        #     self.CENTRAL_LAYOUT.addWidget(label)
            
            
        #     city_label = widgets.QLabel(self.CETRAL_FRAME, text = str(response["name"]))
        #     self.CENTRAL_LAYOUT.addWidget(city_label)
        
        
        self.CETRAL_FRAME = widgets.QFrame(self)
        self.CETRAL_FRAME.setFixedSize(788, 303)
        self.CETRAL_FRAME.setStyleSheet("background-color: grey")
        self.WEATHER_CONTEINER_LAYOUT.addWidget(self.CETRAL_FRAME)
        
        self.CENTRAL_LAYOUT = widgets.QHBoxLayout(self.CETRAL_FRAME)
        self.CETRAL_FRAME.setLayout(self.CENTRAL_LAYOUT)
        
        self.FOOTER = widgets.QFrame(parent = self)
        self.FOOTER.setFixedSize(788, 364)
        self.FOOTER.setStyleSheet("background-color: grey")
        self.WEATHER_CONTEINER_LAYOUT.addWidget(self.FOOTER)
