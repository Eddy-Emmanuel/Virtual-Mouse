import pyautogui
import mediapipe as mp

class Utilities:
    def __init__(self):
        return
    def arg_type(self, x):
        try:
            return int(x)
        except ValueError:
            return x
    @property
    def GetHands(self):
        return mp.solutions.hands
    @property
    def GetDrawingUtil(self):
        return mp.solutions.drawing_utils

    @property
    def GetScreenSize(self):
        return pyautogui.size()
    def MoveMouse(self, x, y):
        return pyautogui.moveTo(x, y)

    def MouseClick(self, x, y):
        return pyautogui.click(x, y)
