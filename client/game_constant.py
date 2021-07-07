import configparser

config = configparser.ConfigParser()
config.read("env")

APP_HOST = config.get("app", "APP_HOST")
APP_PORT = config.get("app", "APP_PORT")

SCREEN_W = int(config.get("game", "WIDTH"))
SCREEN_H = int(config.get("game", "HEIGHT"))

# Color https://chir.ag/projects/name-that-color :)
CLR_ProvincialPink = (254, 243, 243)
CLR_Parchment = (238, 228, 208)
CLR_Tan = (207, 166, 124)
CLR_Paarl = (160, 93, 49)
CLR_SpicyMix = (148, 91, 69)
CLR_KenyanCopper = (109, 31, 9)
CLR_Stonewall = (149, 137, 123)
CLR_Black = (0,0,0)
CLR_White = (255,255,255)


# MENU
## Button
MENU_BTN_BORDER=2
MENU_BTN_EDGE=21
MENU_BTN_W=606
MENU_BTN_H=100
MENU_INPUT_W=500


CLR_BG_MENU=(238,228,208)
CLR_DEFAULT_BUTTON= CLR_BG_MENU;
CLR_ACTIVE_BUTTON= (207, 166, 124);
CLR_ACTIVE_BUTTON_TEXT= (254, 243, 243);
CLR_DEFAULT_BUTTON_TEXT= (207, 166, 124);
CLR_DEFAULT_BUTTON_BORDER= (207, 166, 124);
CLR_HTP= (160, 93, 49);
CLR_TTL= (109, 31, 9,1);
BLACK= (0, 0, 0,0.5);

