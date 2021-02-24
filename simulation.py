import vpython
import input


class Simulation():
    """class used for the visualization of the simulation"""

    def __init__(self, window: input.MainWindow, values: dict, options: dict = None):
        self.parent = window
        self.values = values
        self.options = options

    def pause(self, pause: bool) -> bool:
        """pause and un-pause the simulation"""
        pass

    def adjust_radius(self, slider: str, value: float):
        """adjust the visual size of the spheres according to the slidere values"""
        pass

    def reset_slider(self, slider: str):
        """reset the sliders to default values"""
        pass

    def start(self):
        """start the simulation and open the vpython window"""
        pass
