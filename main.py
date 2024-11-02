
from MainApp import MainApp

if __name__ == "__main__":
    from multiprocessing import freeze_support
    freeze_support()
    app = MainApp()
    app.mainloop()
