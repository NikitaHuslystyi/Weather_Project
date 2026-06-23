import PyQt6.QtCore as core
import PyQt6.QtWidgets as widgets
import PyQt6.QtGui as gui
import folium
import io
from utils import request
from PyQt6.QtWebEngineWidgets import QWebEngineView


class SettingsModal(widgets.QFrame):
    def __init__(self, weather_container):
        super().__init__(parent=weather_container)
        self.WC = weather_container
        self.selected_settings_language = None
        self.selected_settings_country = None
        self.selected_settings_city = None
        

        self.setGeometry(19, 56, 790, 688)
        self.setStyleSheet("background-color: #363636; border-radius: 10px; border: none;")
        self.setVisible(False)

        self.build_ui()
        self.raise_()

    def build_ui(self):
        self.whole_settings_layout = widgets.QVBoxLayout(self)
        self.whole_settings_layout.setContentsMargins(24, 24, 24, 24)
        self.whole_settings_layout.setSpacing(0)

        self.full_settings_string = widgets.QFrame()
        self.full_settings_string.setFixedSize(742, 28)
        self.full_settings_string.setStyleSheet("background-color: transparent")
        self.whole_settings_layout.addWidget(self.full_settings_string, alignment=core.Qt.AlignmentFlag.AlignTop)

        self.whole_settings_string_layout = widgets.QHBoxLayout(self.full_settings_string)
        self.whole_settings_string_layout.setContentsMargins(0, 0, 0, 0)

        self.settings_text_label = widgets.QLabel(text="Settings")
        self.settings_text_label.setStyleSheet("background-color: transparent; color: rgba(255, 255, 255, 1); font-size: 24px; font-weight: 500; ")

        self.close_whole_settings_frame = widgets.QPushButton()
        self.close_whole_settings_frame.setFixedSize(24, 24)
        self.close_whole_settings_frame.setIconSize(core.QSize(24, 24))
        self.close_whole_settings_frame.setStyleSheet("border: none; background-color: transparent;")
        close_frame_icon = gui.QIcon("media/title_bar/x.png")
        self.close_whole_settings_frame.setIcon(close_frame_icon)
        self.close_whole_settings_frame.clicked.connect(self.close)

        self.whole_settings_string_layout.addWidget(self.settings_text_label)
        self.whole_settings_string_layout.addStretch(1)
        self.whole_settings_string_layout.addWidget(self.close_whole_settings_frame)
        self.whole_settings_layout.addSpacing(34)

        self.settings_options_frame = widgets.QFrame()
        self.settings_options_frame.setFixedSize(742, 578)
        self.settings_options_frame.setStyleSheet("background-color: transparent; border-radius: 0px; border: 0px;")

        self.settings_options_layout = widgets.QHBoxLayout(self.settings_options_frame)
        self.settings_options_layout.setContentsMargins(0, 0, 0, 0)
        self.settings_options_layout.setSpacing(0)

        self.tabs_frame = widgets.QFrame()
        self.tabs_frame.setFixedSize(174, 578)
        self.tabs_frame.setStyleSheet("background-color: transparent; border-right: 1px solid rgba(255, 255, 255, 0.2); border-raidus: 0px")

        self.settings_options_layout.addWidget(self.tabs_frame, alignment=core.Qt.AlignmentFlag.AlignLeft)
        self.settings_options_layout.setSpacing(24)

        self.tabs_layout = widgets.QVBoxLayout(self.tabs_frame)
        self.tabs_layout.setContentsMargins(0, 0, 0, 0)
        self.tabs_layout.setSpacing(0)

        self.whole_tabs_frame = widgets.QFrame()
        self.whole_tabs_frame.setFixedSize(158, 140)
        self.whole_tabs_frame.setStyleSheet("background-color: transparent; border: none; border-radius: 0px")

        self.tabs_layout.addWidget(self.whole_tabs_frame, alignment=core.Qt.AlignmentFlag.AlignTop)

        self.whole_tabs_layout = widgets.QVBoxLayout(self.whole_tabs_frame)
        self.whole_tabs_layout.setContentsMargins(0, 0, 0, 0)
        self.whole_tabs_layout.setSpacing(0)

        self.tabs_city_finder_button = widgets.QPushButton()
        self.tabs_city_finder_button.setFixedSize(158, 35)
        self.tabs_city_finder_button.setStyleSheet("background-color: transparent; font-size: 16px; font-weight: 400; border: none;")

        self.tabs_city_finder_button_layout = widgets.QHBoxLayout(self.tabs_city_finder_button)
        self.tabs_city_finder_button_layout.setContentsMargins(8, 8, 8, 8)

        self.tabs_city_finder_button_label = widgets.QLabel(text="City search")
        self.tabs_city_finder_button_label.setStyleSheet("background-color: transparent; color: rgba(255, 255, 255, 1)")

        self.tabs_city_finder_button_layout.addWidget(self.tabs_city_finder_button_label, alignment=core.Qt.AlignmentFlag.AlignLeft)

        self.tabs_app_size_button = widgets.QPushButton()
        self.tabs_app_size_button.setFixedSize(158, 35)
        self.tabs_app_size_button.setStyleSheet("background-color: transparent; font-size: 16px; font-weight: 400; border: none;")

        self.tabs_app_size_layout = widgets.QHBoxLayout(self.tabs_app_size_button)
        self.tabs_app_size_layout.setContentsMargins(8, 8, 8, 8)

        self.tabs_app_size_label = widgets.QLabel(text="App size")
        self.tabs_app_size_label.setStyleSheet("background-color: transparent; color: rgba(255, 255, 255, 1)")

        self.tabs_app_size_layout.addWidget(self.tabs_app_size_label, alignment=core.Qt.AlignmentFlag.AlignLeft)

        self.tabs_app_language_button = widgets.QPushButton()
        self.tabs_app_language_button.setFixedSize(158, 35)
        self.tabs_app_language_button.setStyleSheet("background-color: transparent; font-size: 16px; font-weight: 400; border: none;")

        self.tabs_app_language_layout = widgets.QHBoxLayout(self.tabs_app_language_button)
        self.tabs_app_language_layout.setContentsMargins(8, 8, 8, 8)

        self.tabs_app_language_label = widgets.QLabel(text="App language")
        self.tabs_app_language_label.setStyleSheet("background-color: transparent; color: rgba(255, 255, 255, 1)")

        self.tabs_app_language_layout.addWidget(self.tabs_app_language_label, alignment=core.Qt.AlignmentFlag.AlignLeft)

        self.tabs_image_list_button = widgets.QPushButton()
        self.tabs_image_list_button.setFixedSize(158, 35)
        self.tabs_image_list_button.setStyleSheet("background-color: transparent; font-size: 16px; font-weight: 400; border: none;")

        self.tabs_image_list_layout = widgets.QHBoxLayout(self.tabs_image_list_button)
        self.tabs_image_list_layout.setContentsMargins(8, 8, 8, 8)

        self.tabs_image_list_label = widgets.QLabel(text="Image lists")
        self.tabs_image_list_label.setStyleSheet("background-color: transparent; color: rgba(255, 255, 255, 1)")

        self.tabs_image_list_layout.addWidget(self.tabs_image_list_label, alignment=core.Qt.AlignmentFlag.AlignLeft)

        self.whole_tabs_layout.addWidget(self.tabs_city_finder_button, alignment=core.Qt.AlignmentFlag.AlignLeft)
        self.whole_tabs_layout.addWidget(self.tabs_app_size_button, alignment=core.Qt.AlignmentFlag.AlignLeft)
        self.whole_tabs_layout.addWidget(self.tabs_app_language_button, alignment=core.Qt.AlignmentFlag.AlignLeft)
        self.whole_tabs_layout.addWidget(self.tabs_image_list_button, alignment=core.Qt.AlignmentFlag.AlignLeft)

        self.tabs_city_finder_button.clicked.connect(lambda: self.switch_settings_tab("city_finder"))
        self.tabs_app_language_button.clicked.connect(lambda: self.switch_settings_tab("language"))
        self.tabs_app_size_button.clicked.connect(lambda: self.switch_settings_tab("app_size"))
        self.tabs_image_list_button.clicked.connect(lambda: self.switch_settings_tab("image_list"))

        self.whole_settings_layout.addWidget(self.settings_options_frame)

        self.whole_city_finder_frame = widgets.QFrame()
        self.whole_city_finder_frame.setFixedSize(544, 578)
        self.whole_city_finder_layout = widgets.QVBoxLayout(self.whole_city_finder_frame)
        self.whole_city_finder_layout.setContentsMargins(0, 0, 0, 56)
        self.settings_options_layout.addWidget(self.whole_city_finder_frame)

        self.city_finder_action_frame = widgets.QFrame()
        self.city_finder_action_frame.setFixedSize(544, 301)
        self.whole_city_finder_layout.addWidget(self.city_finder_action_frame)
        self.whole_city_finder_layout.setSpacing(24)
        self.city_finder_action_layout = widgets.QHBoxLayout(self.city_finder_action_frame)
        self.city_finder_action_layout.setContentsMargins(0, 0, 0, 0)

        # Фрейм "Мова додатку"
        self.whole_language_frame = widgets.QFrame()
        self.whole_language_frame.setFixedSize(544, 578)
        self.whole_language_layout = widgets.QVBoxLayout(self.whole_language_frame)
        self.whole_language_layout.setContentsMargins(0, 0, 0, 0)
        self.whole_language_layout.setSpacing(16)
        self.settings_options_layout.addWidget(self.whole_language_frame)
        self.whole_language_frame.setVisible(False)

        self.language_title_label = widgets.QLabel(text="Choose app language")
        self.language_title_label.setStyleSheet("color: rgba(255, 255, 255, 1); font-size: 18px; font-weight: 400; background: transparent;")
        self.whole_language_layout.addWidget(self.language_title_label, alignment=core.Qt.AlignmentFlag.AlignTop)

        self.language_field_frame = widgets.QFrame()
        self.language_field_frame.setFixedSize(239, 56)
        self.language_field_layout = widgets.QVBoxLayout(self.language_field_frame)
        self.language_field_layout.setContentsMargins(0, 0, 0, 0)
        self.language_field_layout.setSpacing(8)
        self.whole_language_layout.addWidget(self.language_field_frame, alignment=core.Qt.AlignmentFlag.AlignTop)

        self.language_text_label = widgets.QLabel(text="App language")
        self.language_text_label.setFixedSize(239, 16)
        self.language_text_label.setStyleSheet("color: rgba(255, 255, 255, 1); font-size: 14px; font-weight: 500")
        self.language_field_layout.addWidget(self.language_text_label)

        self.language_input_frame = widgets.QFrame()
        self.language_field_layout.addWidget(self.language_input_frame)
        self.language_input_frame.setFixedSize(239, 32)
        self.language_input_frame.setStyleSheet("background-color: rgba(255, 255, 255, 1); border: none; border-radius: 4px;")
        language_input_layout = widgets.QHBoxLayout(self.language_input_frame)
        language_input_layout.setContentsMargins(10, 8, 10, 8)
        language_input_layout.setSpacing(5)

        self.language_search_input = widgets.QLineEdit()
        self.language_search_input.setStyleSheet("background-color: transparent; border: none; font-size: 12px; font-weight: 400; color: black;")
        self.language_search_input.setFixedSize(198, 16)
        self.language_search_input.setPlaceholderText("App language")
        self.language_search_input.setReadOnly(True)

        self.down_arrow_label3 = widgets.QLabel()
        self.down_arrow_label3.setFixedSize(16, 16)
        self.down_arrow_label3.setPixmap(gui.QPixmap("media/title_bar/chevron-down.png"))
        self.down_arrow_label3.setStyleSheet("background-color: transparent;")

        language_input_layout.addWidget(self.language_search_input, alignment=core.Qt.AlignmentFlag.AlignLeft)
        language_input_layout.addWidget(self.down_arrow_label3, alignment=core.Qt.AlignmentFlag.AlignRight)

        self.language_input_frame.mousePressEvent = self.on_language_input_clicked
        

        # Фрейм "Списки зображень"
        self.full_list_images_frame = widgets.QFrame()
        self.full_list_images_frame.setFixedSize(544, 578)
        self.full_list_images_layout = widgets.QVBoxLayout(self.full_list_images_frame)
        self.full_list_images_layout.setContentsMargins(0, 0, 0, 0)
        self.full_list_images_layout.setSpacing(0)
        self.full_list_images_layout.setAlignment(core.Qt.AlignmentFlag.AlignTop)
        self.settings_options_layout.addWidget(self.full_list_images_frame, alignment=core.Qt.AlignmentFlag.AlignTop)
        self.full_list_images_frame.setVisible(False)

        # Заголовок
        list_images_frame = widgets.QFrame()
        list_images_frame.setFixedSize(490, 21)
        list_images_layout = widgets.QHBoxLayout(list_images_frame)
        list_images_layout.setContentsMargins(0, 0, 0, 0)
        list_images_label = widgets.QLabel("Списки зображень")
        self.list_images_label = list_images_label
        list_images_label.setStyleSheet("color: rgba(255,255,255,1); font-size: 18px; font-weight: 400; background: transparent;")
        list_images_layout.addWidget(list_images_label, alignment=core.Qt.AlignmentFlag.AlignLeft)
        self.global_list_images_label = list_images_label
        self.full_list_images_layout.addWidget(list_images_frame, alignment=core.Qt.AlignmentFlag.AlignTop)

        self.full_list_images_layout.addSpacing(24)

        # Контейнер для паков
        all_packs_frame = widgets.QFrame()
        all_packs_frame.setFixedSize(490, 292)
        all_packs_layout = widgets.QVBoxLayout(all_packs_frame)
        all_packs_layout.setContentsMargins(0, 0, 0, 0)
        all_packs_layout.setSpacing(20)
        all_packs_layout.setAlignment(core.Qt.AlignmentFlag.AlignTop)
        self.full_list_images_layout.addWidget(all_packs_frame, alignment=core.Qt.AlignmentFlag.AlignTop)

        #Pack1
        list_images_pack1_button = widgets.QPushButton()
        list_images_pack1_button.setFixedSize(490, 136)
        list_images_pack1_button.setStyleSheet("background-color: rgba(0, 0, 0, 0.2); border-radius: 4px; border: none;")
        all_packs_layout.addWidget(list_images_pack1_button, alignment=core.Qt.AlignmentFlag.AlignTop)

        list_images_pack1_button_layout = widgets.QVBoxLayout(list_images_pack1_button)
        list_images_pack1_button_layout.setContentsMargins(16, 12, 16, 12)
        list_images_pack1_button_layout.setSpacing(8)

        pack1_label1 = widgets.QLabel("Список зображень №1")
        self.pack1_label1 = pack1_label1
        pack1_label1.setStyleSheet("color: rgba(255,255,255,1); font-size: 14px; font-weight: 500; background: transparent;")
        pack1_label1.setFixedHeight(18)
        list_images_pack1_button_layout.addWidget(pack1_label1, alignment=core.Qt.AlignmentFlag.AlignLeft)

        pack1_icons_frame = widgets.QFrame()
        pack1_icons_frame.setStyleSheet("background: transparent; border: none;")
        pack1_icons_layout = widgets.QHBoxLayout(pack1_icons_frame)
        pack1_icons_layout.setContentsMargins(0, 0, 0, 0)
        pack1_icons_layout.setSpacing(22)
        pack1_icons_layout.setAlignment(core.Qt.AlignmentFlag.AlignLeft)
        list_images_pack1_button_layout.addWidget(pack1_icons_frame)

        for icon_path in [
            "media/button_icons_pack/Pack1_Sunny.png",
            "media/button_icons_pack/Pack1_Cloudy.png",
            "media/button_icons_pack/Pack1_Rainy.png",
            "media/button_icons_pack/Pack1_few_Cloudy_Night.png",
            "media/button_icons_pack/Pack1_Cloudy_Night.png",
        ]:
            lbl = widgets.QLabel()
            lbl.setFixedSize(74, 74)
            lbl.setStyleSheet("background-color: transparent;")
            lbl.setPixmap(gui.QPixmap(icon_path).scaled(74, 74, core.Qt.AspectRatioMode.KeepAspectRatio, core.Qt.TransformationMode.SmoothTransformation))
            pack1_icons_layout.addWidget(lbl)

        #Pack2
        list_images_pack2_button = widgets.QPushButton()
        list_images_pack2_button.setFixedSize(490, 136)
        list_images_pack2_button.setStyleSheet("background-color: transparent; border-radius: 4px; border: none;")
        all_packs_layout.addWidget(list_images_pack2_button, alignment=core.Qt.AlignmentFlag.AlignTop)

        list_images_pack2_button_layout = widgets.QVBoxLayout(list_images_pack2_button)
        list_images_pack2_button_layout.setContentsMargins(16, 12, 16, 12)
        list_images_pack2_button_layout.setSpacing(8)

        pack2_label = widgets.QLabel("Список зображень №2")
        self.pack2_label = pack2_label
        pack2_label.setStyleSheet("color: rgba(255,255,255,1); font-size: 14px; font-weight: 500; background: transparent;")
        pack2_label.setFixedHeight(18)
        list_images_pack2_button_layout.addWidget(pack2_label, alignment=core.Qt.AlignmentFlag.AlignLeft)

        pack2_icons_frame = widgets.QFrame()
        pack2_icons_frame.setStyleSheet("background: transparent; border: none;")
        pack2_icons_layout = widgets.QHBoxLayout(pack2_icons_frame)
        pack2_icons_layout.setContentsMargins(0, 0, 0, 0)
        pack2_icons_layout.setSpacing(22)
        pack2_icons_layout.setAlignment(core.Qt.AlignmentFlag.AlignLeft)
        list_images_pack2_button_layout.addWidget(pack2_icons_frame)

        for icon_path in [
            "media/button_icons_pack/Pack2_Sunny.png",
            "media/button_icons_pack/Pack2_few_Cloudy.png",
            "media/button_icons_pack/Pack2_Rainy.png",
            "media/button_icons_pack/Pack2_Moon.png",
            "media/button_icons_pack/Pack2_Cloudy.png",
        ]:
            lbl = widgets.QLabel()
            lbl.setFixedSize(74, 74)
            lbl.setStyleSheet("background-color: transparent;")
            lbl.setPixmap(gui.QPixmap(icon_path).scaled(74, 74, core.Qt.AspectRatioMode.KeepAspectRatio, core.Qt.TransformationMode.SmoothTransformation))
            pack2_icons_layout.addWidget(lbl)

        self.use_second_icon_pack = False
        list_images_pack1_button.clicked.connect(self.select_pack1)
        list_images_pack2_button.clicked.connect(self.select_pack2)
        self.icon_pack1_button = list_images_pack1_button
        self.icon_pack2_button = list_images_pack2_button

        self.full_list_images_layout.addSpacing(24)

        save_pack_frame = widgets.QFrame()
        save_pack_frame.setFixedSize(105, 38)
        save_pack_frame.setStyleSheet("background-color: #2b2b2b; border-radius: 4px")
        save_pack_layout = widgets.QHBoxLayout(save_pack_frame)
        save_pack_layout.setContentsMargins(16, 8, 16, 8)

        save_pack_btn = widgets.QPushButton(text="Save")
        save_pack_btn.setStyleSheet("background-color: transparent; color: rgba(255,255,255,1); font-size: 14px; font-weight: 400")
        save_pack_layout.addWidget(save_pack_btn)
        self.save_pack_frame = save_pack_frame
        save_pack_btn.clicked.connect(self.on_icon_pack_save)
        self.save_pack_btn = save_pack_btn
        self.full_list_images_layout.addWidget(save_pack_frame, alignment=core.Qt.AlignmentFlag.AlignTop)

        # Фрейм "Розмір додатку"
        self.whole_app_size_frame = widgets.QFrame()
        self.whole_app_size_frame.setFixedSize(544, 578)
        self.whole_app_size_layout = widgets.QVBoxLayout(self.whole_app_size_frame)
        self.whole_app_size_layout.setContentsMargins(0, 0, 0, 0)
        self.whole_app_size_layout.setSpacing(0)
        self.whole_app_size_layout.setAlignment(core.Qt.AlignmentFlag.AlignTop)
        self.settings_options_layout.addWidget(self.whole_app_size_frame)
        self.whole_app_size_frame.setVisible(False)

        full_container = widgets.QFrame()
        full_container.setFixedSize(239, 219)
        full_container_layout = widgets.QVBoxLayout(full_container)
        full_container_layout.setContentsMargins(0, 0, 0, 0)
        full_container_layout.setSpacing(0)
        full_container_layout.setAlignment(core.Qt.AlignmentFlag.AlignTop)
        self.whole_app_size_layout.addWidget(full_container, alignment=core.Qt.AlignmentFlag.AlignTop)

        # Заголовок
        title_frame = widgets.QFrame()
        title_frame.setFixedSize(239, 21)
        title_layout = widgets.QHBoxLayout(title_frame)
        title_layout.setContentsMargins(0, 0, 0, 0)
        title_label = widgets.QLabel("Оберіть розмір додатку")
        title_label.setStyleSheet("color: rgba(255,255,255,1); font-size: 18px; font-weight: 400; background: transparent;")
        title_layout.addWidget(title_label, alignment=core.Qt.AlignmentFlag.AlignLeft)
        self.app_size_title_label = title_label
        full_container_layout.addWidget(title_frame)
        full_container_layout.setSpacing(24)

        full_sizes_frame  = widgets.QFrame()
        full_sizes_frame.setFixedSize(239, 112)
        full_container_layout.addWidget(full_sizes_frame)
        full_sizes_layout = widgets.QVBoxLayout(full_sizes_frame)
        full_sizes_layout.setContentsMargins(0, 0, 0, 0)
        
        #1
        size_frame1 = widgets.QFrame()
        size_frame1.setFixedSize(96, 16)
        full_sizes_layout.addWidget(size_frame1, alignment=core.Qt.AlignmentFlag.AlignTop)
        size_layout1 = widgets.QHBoxLayout(size_frame1)
        size_layout1.setContentsMargins(0, 0, 7, 0)
        
        circle_button_frame1 = widgets.QFrame()
        size_layout1.addWidget(circle_button_frame1, alignment = core.Qt.AlignmentFlag.AlignLeft)
        circle_button_frame1.setFixedSize(16, 16)
        
        circle_button_layout1 = widgets.QHBoxLayout(circle_button_frame1)
        circle_button_layout1.setContentsMargins(0, 0, 0, 0)
        circle_button_layout1.setSpacing(0)
        
        filled_circle_button1 = widgets.QPushButton()
        filled_circle_button1 .setFixedSize(16, 16)
        filled_circle_button1 .setIconSize(core.QSize(16,16))
        filled_circle_button1 .setStyleSheet("border: none; background-color: transparent;")
        
        circle_button_layout1.addWidget(filled_circle_button1)
        circle_button_layout1.setAlignment(core.Qt.AlignmentFlag.AlignCenter)
        circle_btn_icon1 = gui.QIcon("media/title_bar/Filled_Circle_btn.png")
        filled_circle_button1 .setIcon(circle_btn_icon1)
        
        
        size_label1 = widgets.QLabel(text = "1200x840")
        size_label1.setFixedSize(63, 14)
        size_label1.setStyleSheet("color: rgba(255, 255, 255, 1); font-size: 14px; font-weight: 400;")
        size_layout1.addWidget(size_label1, alignment = core.Qt.AlignmentFlag.AlignRight)
        
        
        #2
        size_frame2 = widgets.QFrame()
        size_frame2.setFixedSize(96, 16)
        full_sizes_layout.addWidget(size_frame2, alignment=core.Qt.AlignmentFlag.AlignTop)
        size_layout2 = widgets.QHBoxLayout(size_frame2)
        size_layout2.setContentsMargins(0, 0, 0, 0)
        
        circle_button_frame2 = widgets.QFrame()
        size_layout2.addWidget(circle_button_frame2, alignment = core.Qt.AlignmentFlag.AlignLeft)
        circle_button_frame2.setFixedSize(16, 16)
        
        circle_button_layout2 = widgets.QHBoxLayout(circle_button_frame2)
        circle_button_layout2.setContentsMargins(0, 0, 0, 0)
        circle_button_layout2.setSpacing(0)
        
        not_filled_circle_button2 = widgets.QPushButton()
        not_filled_circle_button2.setFixedSize(16, 16)
        not_filled_circle_button2.setIconSize(core.QSize(16,16))
        not_filled_circle_button2.setStyleSheet("border: none; background-color: transparent;")
        
        circle_button_layout2.addWidget(not_filled_circle_button2)
        circle_button_layout2.setAlignment(core.Qt.AlignmentFlag.AlignCenter)
        circle_btn_icon2 = gui.QIcon("media/title_bar/Circle_btn.png")
        not_filled_circle_button2.setIcon(circle_btn_icon2)
        
        
        size_label2 = widgets.QLabel(text = "1440x1024")
        size_label2.setFixedSize(72, 14)
        size_label2.setStyleSheet("color: rgba(255, 255, 255, 1); font-size: 14px; font-weight: 400;")
        size_layout2.addWidget(size_label2, alignment = core.Qt.AlignmentFlag.AlignRight)
        
        
        #3
        size_frame3 = widgets.QFrame()
        size_frame3.setFixedSize(96, 16)
        full_sizes_layout.addWidget(size_frame3, alignment=core.Qt.AlignmentFlag.AlignTop)
        size_layout3 = widgets.QHBoxLayout(size_frame3)
        size_layout3.setContentsMargins(0, 0, 7, 0)
        
        circle_button_frame3 = widgets.QFrame()
        size_layout3.addWidget(circle_button_frame3, alignment = core.Qt.AlignmentFlag.AlignLeft)
        circle_button_frame3.setFixedSize(16, 16)
        
        circle_button_layout3 = widgets.QHBoxLayout(circle_button_frame3)
        circle_button_layout3.setContentsMargins(0, 0, 0, 0)
        circle_button_layout3.setSpacing(0)
        
        not_filled_circle_button3 = widgets.QPushButton()
        not_filled_circle_button3.setFixedSize(16, 16)
        not_filled_circle_button3.setIconSize(core.QSize(16,16))
        not_filled_circle_button3.setStyleSheet("border: none; background-color: transparent;")
        
        circle_button_layout3.addWidget(not_filled_circle_button3)
        circle_button_layout3.setAlignment(core.Qt.AlignmentFlag.AlignCenter)
        circle_btn_icon3 = gui.QIcon("media/title_bar/Circle_btn.png")
        not_filled_circle_button3.setIcon(circle_btn_icon3)
        
        
        size_label3 = widgets.QLabel(text = "1512x982")
        size_label3.setFixedSize(63, 14)
        size_label3.setStyleSheet("color: rgba(255, 255, 255, 1); font-size: 14px; font-weight: 400;")
        size_layout3.addWidget(size_label3, alignment = core.Qt.AlignmentFlag.AlignRight)
        
        
        #4
        size_frame4 = widgets.QFrame()
        size_frame4.setFixedSize(96, 16)
        full_sizes_layout.addWidget(size_frame4, alignment=core.Qt.AlignmentFlag.AlignTop)
        size_layout4 = widgets.QHBoxLayout(size_frame4)
        size_layout4.setContentsMargins(0, 0, 0, 0)
        
        circle_button_frame4 = widgets.QFrame()
        size_layout4.addWidget(circle_button_frame4, alignment = core.Qt.AlignmentFlag.AlignLeft)
        circle_button_frame4.setFixedSize(16, 16)
        
        circle_button_layout4 = widgets.QHBoxLayout(circle_button_frame4)
        circle_button_layout4.setContentsMargins(0, 0, 0, 0)
        circle_button_layout4.setSpacing(0)
        
        not_filled_circle_button4 = widgets.QPushButton()
        not_filled_circle_button4.setFixedSize(16, 16)
        not_filled_circle_button4.setIconSize(core.QSize(16,16))
        not_filled_circle_button4.setStyleSheet("border: none; background-color: transparent;")
        
        circle_button_layout4.addWidget(not_filled_circle_button4)
        circle_button_layout4.setAlignment(core.Qt.AlignmentFlag.AlignCenter)
        circle_btn_icon4 = gui.QIcon("media/title_bar/Circle_btn.png")
        not_filled_circle_button4.setIcon(circle_btn_icon4)
        
        
        size_label4 = widgets.QLabel(text = "1728x1117")
        size_label4.setFixedSize(72, 14)
        size_label4.setStyleSheet("color: rgba(255, 255, 255, 1); font-size: 14px; font-weight: 400;")
        size_layout4.addWidget(size_label4, alignment = core.Qt.AlignmentFlag.AlignRight)
        
        
        
        self.app_size_options = [
            {"button": filled_circle_button1, "frame": size_frame1, "width": 1200, "height": 840},
            {"button": not_filled_circle_button2, "frame": size_frame2, "width": 1440, "height": 1024},
            {"button": not_filled_circle_button3, "frame": size_frame3, "width": 1512, "height": 982},
            {"button": not_filled_circle_button4, "frame": size_frame4, "width": 1728, "height": 1117},
        ]

        for opt in self.app_size_options:
            opt["frame"].setCursor(core.Qt.CursorShape.PointingHandCursor)
            opt["button"].setCursor(core.Qt.CursorShape.PointingHandCursor)
            opt["button"].clicked.connect(lambda checked, o=opt: self.on_app_size_selected(o))
            opt["frame"].mousePressEvent = lambda event, o=opt: self.on_app_size_selected(o)

        self.selected_app_size = (1200, 840)

        # Кнопка зберегти
        save_size_frame = widgets.QFrame()
        save_size_frame.setFixedSize(105, 38)
        save_size_frame.setStyleSheet("background-color: #2b2b2b; border-radius: 4px")
        save_size_layout = widgets.QHBoxLayout(save_size_frame)
        save_size_layout.setContentsMargins(16, 8, 16, 8)

        save_size_btn = widgets.QPushButton(text="Save")
        save_size_btn.setStyleSheet("background-color: transparent; color: rgba(255,255,255,1); font-size: 14px; font-weight: 400")
        save_size_layout.addWidget(save_size_btn)
        self._save_size_btn = save_size_btn
        self._save_size_frame = save_size_frame

        save_size_btn.clicked.connect(self.on_app_size_save)

        full_container_layout.addWidget(save_size_frame)

        # Дропдаун мов
        self.language_dropdown = widgets.QFrame(self)
        self.language_dropdown.setFixedSize(239, 80)
        self.language_dropdown.setStyleSheet("background-color: #363636; border-radius: 6px; border: none;")
        self.language_dropdown.setVisible(False)
        language_dd_layout = widgets.QVBoxLayout(self.language_dropdown)
        language_dd_layout.setContentsMargins(0, 0, 0, 0)
        language_dd_layout.setSpacing(0)

        for lang_code, lang_label in [("ua", "Українська"), ("en", "English")]:
            card = self._make_settings_dd_card(
                lang_label, self.language_dropdown,
                lambda c, code=lang_code: self.on_language_selected(code, c)
            )
            language_dd_layout.addWidget(card)

        # Кнопка Зберегти для мови
        language_save_button_frame = widgets.QFrame()
        language_save_button_frame.setFixedSize(105, 38)
        language_save_button_frame.setStyleSheet("background-color: #2b2b2b; border-radius: 4px")
        language_save_button_layout = widgets.QHBoxLayout(language_save_button_frame)
        language_save_button_layout.setContentsMargins(16, 8, 16, 8)

        self.language_save_button = widgets.QPushButton(text="Save")
        self.language_save_button.setStyleSheet("background-color: transparent; color: rgba(255, 255, 255, 1); font-size: 14px; font-weight: 400")
        language_save_button_layout.addWidget(self.language_save_button)
        self.language_save_button.clicked.connect(self.on_language_save)

        self.whole_language_layout.addWidget(language_save_button_frame, alignment=core.Qt.AlignmentFlag.AlignTop)
        self.whole_language_layout.addStretch()

        self.city_finder_functions_frame = widgets.QFrame()
        self.city_finder_functions_frame.setFixedSize(239, 301)
        self.city_finder_action_layout.addWidget(self.city_finder_functions_frame)
        self.city_finder_action_layout.setSpacing(16)
        self.city_finder_functions_layout = widgets.QVBoxLayout(self.city_finder_functions_frame)
        self.city_finder_functions_layout.setContentsMargins(0, 0, 0, 0)
        self.city_finder_functions_layout.setSpacing(0)

        # Пошук міста
        self.city_finder_text_frame = widgets.QFrame()
        self.city_finder_functions_layout.addWidget(self.city_finder_text_frame, alignment=core.Qt.AlignmentFlag.AlignTop)
        self.city_finder_text_frame.setFixedSize(239, 21)
        self.city_finder_text_layout = widgets.QHBoxLayout(self.city_finder_text_frame)
        self.city_finder_text_layout.setContentsMargins(0, 0, 0, 0)
        self.city_finder_text_label = widgets.QLabel(text="City search")
        self.city_finder_text_label.setStyleSheet("color: rgba(255, 255, 255, 1); font-size: 18px; font-weight: 400")
        self.city_finder_text_layout.addWidget(self.city_finder_text_label, alignment=core.Qt.AlignmentFlag.AlignLeft)

        # Контейнер со всеми функц cвязанные с картой
        self.map_funcs_frame = widgets.QFrame()
        self.city_finder_functions_layout.addWidget(self.map_funcs_frame)
        self.city_finder_functions_layout.setSpacing(24)
        self.map_funcs_layout = widgets.QVBoxLayout(self.map_funcs_frame)
        self.map_funcs_layout.setContentsMargins(0, 0, 0, 0)
        self.map_funcs_frame.setFixedSize(239, 194)

        # КРАЇНА
        self.country_finder_frame = widgets.QFrame()
        self.map_funcs_layout.addWidget(self.country_finder_frame, alignment=core.Qt.AlignmentFlag.AlignTop)
        self.map_funcs_layout.setSpacing(16)
        self.country_finder_frame.setFixedSize(239, 56)
        self.country_finder_layout = widgets.QVBoxLayout(self.country_finder_frame)
        self.country_finder_layout.setContentsMargins(0, 0, 0, 0)
        self.country_finder_layout.setSpacing(8)

        self.country_text_label = widgets.QLabel(text="Country")
        self.country_text_label.setFixedSize(239, 16)
        self.country_text_label.setStyleSheet("color: rgba(255, 255, 255, 1); font-size: 14px; font-weight: 500")
        self.country_finder_layout.addWidget(self.country_text_label)

        self.country_input_frame = widgets.QFrame()
        self.country_finder_layout.addWidget(self.country_input_frame)
        self.country_input_frame.setFixedSize(239, 32)
        self.country_input_frame.setStyleSheet("background-color: rgba(255, 255, 255, 1); border: none; border-radius: 4px;")
        country_input_layout = widgets.QHBoxLayout(self.country_input_frame)
        country_input_layout.setContentsMargins(10, 8, 10, 8)
        country_input_layout.setSpacing(5)

        self.country_search_input = widgets.QLineEdit()
        self.country_search_input.setStyleSheet("background-color: transparent; border: none; font-size: 12px; font-weight: 400; color: black;")
        self.country_search_input.setFixedSize(198, 16)
        self.country_search_input.setPlaceholderText("Search country")

        self.down_arrow_label1 = widgets.QLabel()
        self.down_arrow_label1.setFixedSize(16, 16)
        self.down_arrow_label1.setPixmap(gui.QPixmap("media/title_bar/chevron-down.png"))
        self.down_arrow_label1.setStyleSheet("background-color: transparent;")

        country_input_layout.addWidget(self.country_search_input, alignment=core.Qt.AlignmentFlag.AlignLeft)
        country_input_layout.addWidget(self.down_arrow_label1, alignment=core.Qt.AlignmentFlag.AlignRight)
        # Дропдаун країни
        self.country_dropdown = widgets.QFrame(self)
        self.country_dropdown.setFixedSize(239, 200)
        self.country_dropdown.setStyleSheet("background-color: #363636; border-radius: 6px; border: none;")
        self.country_dropdown.setVisible(False)
        country_dd_layout = widgets.QVBoxLayout(self.country_dropdown)
        country_dd_layout.setContentsMargins(0, 0, 0, 0)
        country_dd_layout.setSpacing(0)
        self.country_dd_scroll = widgets.QScrollArea()
        self.country_dd_scroll.setWidgetResizable(True)
        self.country_dd_scroll.setVerticalScrollBarPolicy(core.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.country_dd_scroll.setHorizontalScrollBarPolicy(core.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.country_dd_scroll.setFrameShape(widgets.QFrame.Shape.NoFrame)
        self.country_dd_scroll.setStyleSheet("background: transparent; border: none;")
        self.country_dd_content = widgets.QFrame()
        self.country_dd_content.setStyleSheet("background: transparent; border: none;")
        self.country_dd_layout = widgets.QVBoxLayout(self.country_dd_content)
        self.country_dd_layout.setContentsMargins(0, 0, 0, 0)
        self.country_dd_layout.setSpacing(0)
        self.country_dd_layout.setAlignment(core.Qt.AlignmentFlag.AlignTop)
        self.country_dd_scroll.setWidget(self.country_dd_content)
        country_dd_layout.addWidget(self.country_dd_scroll)
        self.country_search_input.textChanged.connect(self.on_country_search_changed)
        # МІСТО
        self.city_finder_frame = widgets.QFrame()
        self.map_funcs_layout.addWidget(self.city_finder_frame)
        self.city_finder_frame.setFixedSize(239, 56)
        self.city_finder_layout = widgets.QVBoxLayout(self.city_finder_frame)
        self.city_finder_layout.setContentsMargins(0, 0, 0, 0)
        self.city_finder_layout.setSpacing(8)

        self.city_text_label = widgets.QLabel(text="City")
        self.city_text_label.setFixedSize(239, 16)
        self.city_text_label.setStyleSheet("color: rgba(255, 255, 255, 1); font-size: 14px; font-weight: 500")
        self.city_finder_layout.addWidget(self.city_text_label)

        self.city_input_frame = widgets.QFrame()
        self.city_finder_layout.addWidget(self.city_input_frame)
        self.city_input_frame.setFixedSize(239, 32)
        self.city_input_frame.setStyleSheet("background-color: rgba(255, 255, 255, 1); border: none; border-radius: 4px;")
        city_input_layout = widgets.QHBoxLayout(self.city_input_frame)
        city_input_layout.setContentsMargins(10, 8, 10, 8)
        city_input_layout.setSpacing(5)

        self.city_search_input = widgets.QLineEdit()
        self.city_search_input.setStyleSheet("background-color: transparent; border: none; font-size: 12px; font-weight: 400; color: black;")
        self.city_search_input.setFixedSize(198, 16)
        self.city_search_input.setPlaceholderText("Search city")

        self.down_arrow_label2 = widgets.QLabel()
        self.down_arrow_label2.setFixedSize(16, 16)
        self.down_arrow_label2.setPixmap(gui.QPixmap("media/title_bar/chevron-down.png"))
        self.down_arrow_label2.setStyleSheet("background-color: transparent;")

        city_input_layout.addWidget(self.city_search_input, alignment=core.Qt.AlignmentFlag.AlignLeft)
        city_input_layout.addWidget(self.down_arrow_label2, alignment=core.Qt.AlignmentFlag.AlignRight)

        # Дропдаун міста
        self.city_dropdown = widgets.QFrame(self)
        self.city_dropdown.setFixedSize(239, 200)
        self.city_dropdown.setStyleSheet("background-color: #363636; border-radius: 6px; border: none;")
        self.city_dropdown.setVisible(False)
        city_dd_layout = widgets.QVBoxLayout(self.city_dropdown)
        city_dd_layout.setContentsMargins(0, 0, 0, 0)
        city_dd_layout.setSpacing(0)
        self.city_dd_scroll = widgets.QScrollArea()
        self.city_dd_scroll.setWidgetResizable(True)
        self.city_dd_scroll.setVerticalScrollBarPolicy(core.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.city_dd_scroll.setHorizontalScrollBarPolicy(core.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.city_dd_scroll.setFrameShape(widgets.QFrame.Shape.NoFrame)
        self.city_dd_scroll.setStyleSheet("background: transparent; border: none;")
        self.city_dd_content = widgets.QFrame()
        self.city_dd_content.setStyleSheet("background: transparent; border: none;")
        self.city_dd_layout = widgets.QVBoxLayout(self.city_dd_content)
        self.city_dd_layout.setContentsMargins(0, 0, 0, 0)
        self.city_dd_layout.setSpacing(0)
        self.city_dd_layout.setAlignment(core.Qt.AlignmentFlag.AlignTop)
        self.city_dd_scroll.setWidget(self.city_dd_content)
        city_dd_layout.addWidget(self.city_dd_scroll)
        self.city_search_input.textChanged.connect(self.on_city_search_changed)

        # Координати
        self.coord_finder_frame = widgets.QFrame()
        self.map_funcs_layout.addWidget(self.coord_finder_frame)
        self.coord_finder_frame.setFixedSize(239, 56)
        self.coord_finder_layout = widgets.QVBoxLayout(self.coord_finder_frame)
        self.coord_finder_layout.setContentsMargins(0, 0, 0, 0)

        self.coord_text_label = widgets.QLabel(text="Coordinates")
        self.coord_text_label.setFixedSize(239, 16)
        self.coord_text_label.setStyleSheet("color: rgba(255, 255, 255, 1); font-size: 14px; font-weight: 500 ")
        self.coord_finder_layout.addWidget(self.coord_text_label)
        self.coord_finder_layout.setSpacing(8)

        self.coord_find_input_frame = widgets.QFrame()
        self.coord_finder_layout.addWidget(self.coord_find_input_frame)
        self.coord_find_input_frame.setFixedSize(239, 32)
        self.coord_find_input_frame.setStyleSheet("background-color: rgba(255, 255, 255, 1); border: none; border-radius: 4px;")
        self.coord_find_input_layout = widgets.QHBoxLayout()
        self.coord_find_input_layout.setContentsMargins(10, 8, 10, 8)
        self.coord_find_input_frame.setLayout(self.coord_find_input_layout)

        self.coord_search_input = widgets.QLineEdit()
        self.coord_search_input.setStyleSheet("background-color: transparent; border: none; font-size: 12px; font-weight: 400; color: black;")
        self.coord_search_input.setFixedSize(219, 16)
        self.coord_search_input.setPlaceholderText("(WGS 84,UTM,MGRS)")

        self.coord_find_input_layout.addWidget(self.coord_search_input, alignment=core.Qt.AlignmentFlag.AlignCenter)

        # Кнопка Зберегти
        save_button_frame = widgets.QFrame()
        save_button_frame.setFixedSize(105, 38)
        save_button_frame.setStyleSheet("background-color: #2b2b2b; border-radius: 4px")
        save_button_layout = widgets.QHBoxLayout(save_button_frame)
        save_button_layout.setContentsMargins(16, 8, 16, 8)

        self.save_button = widgets.QPushButton(text="Save")
        self.save_button.setStyleSheet("background-color: transparent; color: rgba(255, 255, 255, 1); font-size: 14px; font-weight: 400")
        save_button_layout.addWidget(self.save_button)
        self.save_button.clicked.connect(self.on_settings_save)

        self.city_finder_functions_layout.addWidget(save_button_frame)

        self.map_frame = widgets.QFrame()
        self.map_frame.setFixedSize(289, 301)
        self.map_frame.setStyleSheet("background-color: transparent; border-radius: 4px; border: none;")
        self.city_finder_action_layout.addWidget(self.map_frame)
        self.map_layout = widgets.QVBoxLayout(self.map_frame)
        self.map_layout.setContentsMargins(0, 45, 0, 0)

        self.web_view = QWebEngineView()
        self.web_view.setFixedSize(289, 256)
        self.web_view.setStyleSheet("border-radius: 4px;")

        path = gui.QPainterPath()
        path.addRoundedRect(0, 0, 289, 256, 4, 4)
        region = gui.QRegion(path.toFillPolygon().toPolygon())
        self.web_view.setMask(region)

        default_map = folium.Map(width=289, height=256, location=[50, 50], tiles="CartoDB Positron")
        data = io.BytesIO()
        default_map.save(data, close_file=False)
        html = data.getvalue().decode()
        self.web_view.setHtml(html)
        self.map_layout.addWidget(self.web_view)

        # Фрейм (Додані міста)
        self.added_cities_frame = widgets.QFrame()
        self.added_cities_frame.setFixedSize(544, 197)
        self.added_cities_layout = widgets.QVBoxLayout(self.added_cities_frame)
        self.added_cities_layout.setContentsMargins(0, 0, 0, 0)

        self.added_cities_text_frame = widgets.QFrame()
        self.added_cities_layout.addWidget(self.added_cities_text_frame, alignment=core.Qt.AlignmentFlag.AlignTop)
        self.added_cities_text_frame.setFixedSize(544, 21)
        self.added_cities_text_frame.setStyleSheet("background-color: transparent;")
        self.added_cities_text_layout = widgets.QHBoxLayout(self.added_cities_text_frame)
        self.added_cities_text_layout.setContentsMargins(0, 0, 0, 0)

        self.added_cities_text_label = widgets.QLabel(text="Added cities")
        self.added_cities_text_label.setStyleSheet("background-color: transparent; color: rgba(255, 255, 255, 1); font-size: 18px; font-weight: 400")
        self.added_cities_text_layout.addWidget(self.added_cities_text_label, alignment=core.Qt.AlignmentFlag.AlignLeft)

        self.added_cities_scroll_area = widgets.QScrollArea()
        self.added_cities_scroll_area.setFixedSize(544, 160)
        self.added_cities_scroll_area.setWidgetResizable(True)
        self.added_cities_scroll_area.setVerticalScrollBarPolicy(core.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.added_cities_scroll_area.setHorizontalScrollBarPolicy(core.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.added_cities_scroll_area.setFrameShape(widgets.QFrame.Shape.NoFrame)
        self.added_cities_scroll_area.setStyleSheet("background: #2b2b2b; border-radius: 6px; border: none;")

        self.added_cities_scroll_content = widgets.QFrame()
        self.added_cities_scroll_content.setStyleSheet("background: transparent; border: none;")
        self.added_cities_scroll_layout = widgets.QVBoxLayout(self.added_cities_scroll_content)
        self.added_cities_scroll_layout.setContentsMargins(16, 8, 16, 8)
        self.added_cities_scroll_layout.setSpacing(0)
        self.added_cities_scroll_layout.setAlignment(core.Qt.AlignmentFlag.AlignTop)

        self.added_cities_scroll_area.setWidget(self.added_cities_scroll_content)
        self.added_cities_layout.addWidget(self.added_cities_scroll_area)

        self.whole_city_finder_layout.addWidget(self.added_cities_frame)
        
        
        
        
        
        self._tab_buttons = {
            "city_finder": self.tabs_city_finder_button_label,
            "language":    self.tabs_app_language_label,
            "app_size":    self.tabs_app_size_label,
            "image_list":  self.tabs_image_list_label,
        }
        self.switch_settings_tab("city_finder")

    def show_modal(self):
        self.setVisible(True)
        self.raise_()

    def add_city_to_list(self, city_name):
        for i in range(self.added_cities_scroll_layout.count()):
            w = self.added_cities_scroll_layout.itemAt(i).widget()
            if w and w.property("city_name") == city_name:
                return

        card = widgets.QFrame()
        card.setFixedSize(512, 32)
        card.setProperty("city_name", city_name)
        card.setStyleSheet("background: transparent; border: none;")
        card_layout = widgets.QHBoxLayout(card)
        card_layout.setContentsMargins(0, 0, 0, 0)
        card_layout.setSpacing(0)

        display_name = self.WC._get_city_display_name(city_name, self.WC.current_language)
        city_label = widgets.QLabel(display_name)
        city_label.setStyleSheet("color: rgba(255,255,255,1); font-size: 14px; font-weight: 400; background: transparent; border: none;")
        card_layout.addWidget(city_label)
        card.city_label_ref = city_label
        card_layout.addStretch()

        delete_btn = widgets.QPushButton()
        delete_btn.setFixedSize(16, 16)
        delete_btn.setStyleSheet("background: transparent; border: none;")
        delete_btn.setIcon(gui.QIcon("media/title_bar/trash.png"))
        delete_btn.setIconSize(core.QSize(16, 16))
        delete_btn.setCursor(core.Qt.CursorShape.PointingHandCursor)
        delete_btn.clicked.connect(lambda checked, c=city_name, w=card: self._remove_city(c, w))
        card_layout.addWidget(delete_btn)

        self.added_cities_scroll_layout.addWidget(card)

    def remove_city_from_list(self, city_name):
        for i in range(self.added_cities_scroll_layout.count()):
            w = self.added_cities_scroll_layout.itemAt(i).widget()
            if w and w.property("city_name") == city_name:
                w.deleteLater()
                break

    def update_language(self):
        t = self.WC.TRANSLATIONS
        lang = self.WC.current_language

        self.settings_text_label.setText(t["settings_title"][lang])
        self.tabs_city_finder_button_label.setText(t["tab_city_finder"][lang])
        self.tabs_app_size_label.setText(t["tab_app_size"][lang])
        self.tabs_app_language_label.setText(t["tab_language"][lang])
        self.tabs_image_list_label.setText(t["tab_image_list"][lang])
        self.save_button.setText(t["save_button"][lang])
        self.save_pack_btn.setText(t["save_button"][lang])
        self.language_save_button.setText(t["save_button"][lang])

        self.city_finder_text_label.setText(t["city_finder_title"][lang])
        self.country_text_label.setText(t["country_label"][lang])
        self.city_text_label.setText(t["city_label"][lang])
        self.coord_text_label.setText(t["coord_label"][lang])
        self.added_cities_text_label.setText(t["added_cities_title"][lang])
        self.list_images_label.setText(t["list_images_label"][lang])
        self.pack1_label1.setText(t["pack1_label1"][lang])
        self.pack2_label.setText(t["pack2_label"][lang])

        self.app_size_title_label.setText(t["app_size_title"][lang])
        self._save_size_btn.setText(t["save_button"][lang])

        self.language_title_label.setText(t["language_title"][lang])
        self.language_text_label.setText(t["language_label"][lang])

        self.country_search_input.setPlaceholderText(t["search_country_placeholder"][lang])
        self.city_search_input.setPlaceholderText(t["search_city_placeholder"][lang])

        self.update_added_cities_language()

    def update_added_cities_language(self):
        for i in range(self.added_cities_scroll_layout.count()):
            card = self.added_cities_scroll_layout.itemAt(i).widget()
            if card and hasattr(card, "city_label_ref"):
                city_name = card.property("city_name")
                display_name = self.WC._get_city_display_name(city_name, self.WC.current_language)
                card.city_label_ref.setText(display_name)

    def switch_settings_tab(self, tab_name):
        self.whole_city_finder_frame.setVisible(tab_name == "city_finder")
        self.whole_language_frame.setVisible(tab_name == "language")
        self.whole_app_size_frame.setVisible(tab_name == "app_size")
        self.full_list_images_frame.setVisible(tab_name == "image_list")

        self.language_dropdown.setVisible(False)

        active_style   = "background-color: rgba(255,255,255,0.2); color: rgba(255,255,255,1); border-radius: 6px;"
        inactive_style = "background-color: transparent; color: rgba(255,255,255,1); border-radius: 6px;"

        for key, label in self._tab_buttons.items():
            btn = label.parent()
            btn.setStyleSheet(
                f"background-color: {'rgba(255,255,255,0.2)' if key == tab_name else 'transparent'};"
                f"font-size: 16px; font-weight: {'500' if key == tab_name else '400'};"
                f"border: none; border-radius: 6px;"
            )
            label.setStyleSheet(
                f"background-color: transparent; color: {'rgba(255,255,255,1)' if key == tab_name else 'rgba(255,255,255,0.2)'};"
            )

    def on_language_input_clicked(self, event):
        if self.language_dropdown.isVisible():
            self.language_dropdown.setVisible(False)
            return
        pos = self.language_input_frame.mapTo(self, core.QPoint(0, 32))
        self.language_dropdown.move(pos)
        self.language_dropdown.setVisible(True)
        self.language_dropdown.raise_()

    def on_language_selected(self, lang_code, label_text):
        self.selected_settings_language = lang_code
        self.language_search_input.setText(label_text)
        self.language_dropdown.setVisible(False)

    def on_language_save(self):
        if not self.selected_settings_language:
            return
        self.WC.apply_language(self.selected_settings_language)

    def on_country_search_changed(self, text):
        text = text.strip()
        while self.country_dd_layout.count():
            item = self.country_dd_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        if not text:
            self.country_dropdown.setVisible(False)
            return

        all_data = self.WC._get_cities_list()
        countries = sorted(set(c["country"] for c in all_data))
        matched = [c for c in countries if c.lower().startswith(text.lower())][:15]
        if not matched:
            self.country_dropdown.setVisible(False)
            return

        for country in matched:
            card = self._make_settings_dd_card(country, self.country_dd_content, lambda c: self.on_country_selected(c))
            self.country_dd_layout.addWidget(card)

        pos = self.country_input_frame.mapTo(self, core.QPoint(0, 32))
        self.country_dropdown.move(pos)
        self.country_dropdown.setVisible(True)
        self.country_dropdown.raise_()

    def on_country_selected(self, country_name):
        self.selected_settings_country = country_name
        self.country_search_input.setText(country_name)
        self.country_dropdown.setVisible(False)
        self.city_search_input.clear()
        self.selected_settings_city = None

    def on_city_search_changed(self, text):
        text = text.strip()
        while self.city_dd_layout.count():
            item = self.city_dd_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        if not text:
            self.city_dropdown.setVisible(False)
            return

        all_data = self.WC._get_cities_list()

        if self.selected_settings_country:
            filtered = [c for c in all_data if c["country"] == self.selected_settings_country]
        else:
            filtered = all_data

        matched = []
        for c in filtered:
            eng_name = c["city"].lower()
            uk_name = self.WC._get_city_display_name(c["city"], "ua").lower()
            if eng_name.startswith(text.lower()) or uk_name.startswith(text.lower()):
                matched.append(c)
        matched = matched[:15]

        if not matched:
            self.city_dropdown.setVisible(False)
            return

        for item in matched:
            display_name = self.WC._get_city_display_name(item["city"])
            card = self._make_settings_dd_card(display_name, self.city_dd_content, lambda c: self.on_settings_city_selected(c))
            self.city_dd_layout.addWidget(card)

        pos = self.city_input_frame.mapTo(self, core.QPoint(0, 32))
        self.city_dropdown.move(pos)
        self.city_dropdown.setVisible(True)
        self.city_dropdown.raise_()

    def on_settings_city_selected(self, city_name):
        self.selected_settings_city = city_name
        self.city_search_input.setText(city_name)
        self.city_dropdown.setVisible(False)

    def on_settings_save(self):
        city = self.selected_settings_city
        if not city:
            return
        self.WC._fetch_city_translation(city)
        if self.WC.left_container_ref:
            self.WC.left_container_ref.add_city_card(city)
        self.add_city_to_list(city)
        self._update_minimap(city)
        self.country_search_input.clear()
        self.city_search_input.clear()
        self.selected_settings_country = None
        self.selected_settings_city = None

    def on_app_size_selected(self, option):
            for opt in self.app_size_options:
                icon_name = "Filled_Circle_btn.png" if opt is option else "Circle_btn.png"
                opt["button"].setIcon(gui.QIcon(f"media/title_bar/{icon_name}"))
            self.selected_app_size = (option["width"], option["height"])
            self._save_size_frame.setStyleSheet("background-color: #000000; border-radius: 4px")

    def select_pack1(self):
        self.use_second_icon_pack = False
        self.icon_pack1_button.setStyleSheet("background-color: rgba(0, 0, 0, 0.2); border-radius: 4px; border: none;")
        self.icon_pack2_button.setStyleSheet("background-color: transparent; border-radius: 4px; border: none;")

    def select_pack2(self):
        self.use_second_icon_pack = True
        self.icon_pack2_button.setStyleSheet("background-color: rgba(0, 0, 0, 0.2); border-radius: 4px; border: none;")
        self.icon_pack1_button.setStyleSheet("background-color: transparent; border-radius: 4px; border: none;")

    def on_icon_pack_save(self):
        self.WC.apply_icon_pack(self.use_second_icon_pack)

    def on_app_size_save(self):
        width, height = self.selected_app_size
        self.WC.apply_app_size(width, height)

    def _make_settings_dd_card(self, text, parent, callback):
        card = widgets.QFrame(parent)
        card.setFixedSize(239, 32)
        card.setStyleSheet("background: transparent; border: none;")
        card.setCursor(core.Qt.CursorShape.PointingHandCursor)
        layout = widgets.QHBoxLayout(card)
        layout.setContentsMargins(8, 4, 8, 4)
        label = widgets.QLabel(text)
        label.setStyleSheet("color: rgba(255,255,255,1); font-size: 13px; background: transparent; border: none;")
        layout.addWidget(label)

        def press(event, t=text):
            callback(t)
        card.mousePressEvent = press
        return card

    def _remove_city(self, city_name, card_widget):
        card_widget.deleteLater()
        if self.WC.left_container_ref:
            self.WC.left_container_ref.remove_city_card(city_name)

    def _update_minimap(self, city_name):
        try:
            data = request(city_name=city_name, request_type="current_weather")
            lat = data["coord"]["lat"]
            lon = data["coord"]["lon"]
            self.coord_search_input.setText(f"{lat}, {lon}")

            m = folium.Map(width=289, height=256, location=[lat, lon], zoom_start=10, tiles="CartoDB Positron")
            folium.Marker([lat, lon], tooltip=city_name).add_to(m)
            buf = io.BytesIO()
            m.save(buf, close_file=False)
            self.web_view.setHtml(buf.getvalue().decode())
            path = gui.QPainterPath()
            path.addRoundedRect(0, 0, 289, 256, 4, 4)
            region = gui.QRegion(path.toFillPolygon().toPolygon())
            self.web_view.setMask(region)
        except Exception:
            pass