from sys import exit as sys_exit, argv as sys_argv
from main_windows import MainApp


if __name__ == "__main__":
    app = MainApp(sys_argv)
    sys_exit(app.exec())
