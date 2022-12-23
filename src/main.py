from src.ui.graphical_ui import GraphicalUI
from src.ui.console_ui import ConsoleUI
from jproperties import Properties

if __name__ == '__main__':
    config = Properties()
    with open('settings.properties', 'rb') as fread:
        config.load(fread)
        settings = config['ui_type'].data
    match settings:
        case 'graphical_ui':
            GraphicalUI()
        case 'console_ui':
            ConsoleUI()
    exit()
