from modules import application, main_window


def main():
    try:
        main_window.show()
        application.exec()
    except Exception as error:
        print(f"Помилка під час запуску проєкту: {error}")



if __name__ == "__main__":
    main()

