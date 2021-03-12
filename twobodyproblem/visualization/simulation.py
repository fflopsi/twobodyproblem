from twobodyproblem.visualization import body
import vpython as vp
from scipy.constants import G
import signal
import os
import sys


class Simulation():
    """class used for the visualization of the simulation"""

    def __init__(self, values: dict, options: dict):
        self.values = values
        self.options = options

    def pause(self, button: vp.button):
        """pause and un-pause the simulation"""
        if button.text == "Pause":
            button.text = "Play"
        else:
            button.text = "Pause"

    def restart(self):
        """restart the program"""
        # does not work perfectly, especially on command line
        os.execl(sys.executable, sys.executable, *sys.argv)
        # os.execv(sys.executable, ["python"] + sys.argv)

    def adjust_radius(self, slider: vp.slider, sphere: body.Body):
        """adjust the visual size of the sphere according to the slider value"""
        sphere.radius = self.values[sphere.name + "_radius"] * slider.value

    def reset_slider(self, slider: vp.slider):
        """reset the slider to the default value"""
        slider.value = 1
        slider.bind()

    def start(self):
        """open the vpython window and start the simulation"""
        # set up important boolean values from options
        testing = bool(self.options["do_testing"])
        central_centered = bool(self.options["do_central_centered"])
        show_pointers = bool(self.options["show_pointers"])

        # set up canvas, bodies and pointers
        scene = vp.canvas(
            title="Simulation zum Zweikörperproblem",
            height=self.options["canvas"]["height"],
            width=self.options["canvas"]["width"]
        )
        central = body.Body(
            sim=self, name="central", mass=self.values["central_mass"],
            velocity=vp.vector(
                self.values["central_v0"]["x"],
                self.values["central_v0"]["y"],
                self.values["central_v0"]["z"]
            ),
            radius=self.values["central_radius"], make_trail=True,
            color=vp.vector(
                self.options["color"]["objects"]["r"] / 255,
                self.options["color"]["objects"]["g"] / 255,
                self.options["color"]["objects"]["b"] / 255
            )
        )
        sat = body.Body(
            sim=self, name="sat", mass=self.values["sat_mass"],
            velocity=vp.vector(
                self.values["sat_v0"]["x"],
                self.values["sat_v0"]["y"],
                self.values["sat_v0"]["z"]
            ),
            pos=vp.vector(
                self.values["distance"] +
                self.values["central_radius"] + self.values["sat_radius"], 0, 0),
            radius=self.values["sat_radius"], make_trail=True,
            color=vp.vector(
                self.options["color"]["objects"]["r"] / 255,
                self.options["color"]["objects"]["g"] / 255,
                self.options["color"]["objects"]["b"] / 255
            )
        )
        if show_pointers:
            central_pointer = vp.arrow(
                axis=vp.vector(
                    0,
                    -((self.values["distance"]+central.radius+sat.radius)/2),
                    0
                ),
                color=vp.vector(
                    self.options["color"]["pointer"]["r"],
                    self.options["color"]["pointer"]["g"],
                    self.options["color"]["pointer"]["b"]
                )
            )
            central_pointer.pos = central.pos - central_pointer.axis + \
                vp.vector(0, self.values["central_radius"], 0)
            sat_pointer = vp.arrow(
                axis=vp.vector(
                    0,
                    -((self.values["distance"]+central.radius+sat.radius)/2),
                    0
                ),
                color=vp.vector(
                    self.options["color"]["pointer"]["r"],
                    self.options["color"]["pointer"]["g"],
                    self.options["color"]["pointer"]["b"]
                )
            )
            sat_pointer.pos = sat.pos - sat_pointer.axis + \
                vp.vector(0, self.values["sat_radius"], 0)

        # set up buttons
        pause_sim = vp.button(text="Pause", bind=self.pause)
        vp.button(text="Stop", bind=lambda: os.kill(
            os.getpid(), signal.SIGINT))
        vp.button(text="Restart", bind=self.restart)
        scene.append_to_caption("\n")

        # set up sliders for changing the radius magnification of the two objects
        central_radius_slider: vp.slider = vp.slider(
            max=(self.values["distance"]+self.values["central_radius"])
            / self.values["central_radius"],
            min=1, value=1, top=12, bottom=12,
            bind=lambda: self.adjust_radius(
                slider=central_radius_slider, sphere=central)
        )
        vp.button(text="Reset", bind=lambda: self.reset_slider(
            central_radius_slider))
        scene.append_to_caption("\n")
        sat_radius_slider: vp.slider = vp.slider(
            max=(self.values["distance"]+self.values["sat_radius"])
            / self.values["sat_radius"],
            min=1, value=1, top=12, bottom=12,
            bind=lambda: self.adjust_radius(
                slider=sat_radius_slider, sphere=sat)
        )
        vp.button(text="Reset", bind=lambda: self.reset_slider(
            sat_radius_slider))

        # set up time variables
        t = 0
        t_max = self.options["update_rate"] * self.options["max_seconds"]
        # main simulation loop
        if central_centered:
            scene.camera.follow(central)
        while t < t_max:
            vp.rate(self.options["update_rate"])
            # vp.sleep(1/self.options["update_rate"])  # weird behaviour of those two
            if pause_sim.text == "Pause":
                r = sat.pos - central.pos
                if testing:
                    central.calculate(sat)
                    if show_pointers:
                        # move pointers
                        central_pointer.pos = central.pos - \
                            central_pointer.axis + \
                            vp.vector(0, central.radius, 0)
                        sat_pointer.pos = sat.pos - sat_pointer.axis + \
                            vp.vector(0, sat.radius, 0)
                else:
                    # calculate everything needed for the new positions
                    force_value = (G*central.mass*sat.mass) / (vp.mag(r)**2)
                    sat.force = force_value * vp.norm(-r)
                    central.force = force_value * vp.norm(r)
                    sat.acceleration = sat.force / sat.mass
                    central.acceleration = central.force / central.mass
                    sat.velocity = sat.acceleration*self.delta_t + sat.velocity
                    central.velocity = central.acceleration*self.delta_t + central.velocity
                    # reposition the objects
                    sat.pos = sat.velocity*self.delta_t + sat.pos
                    central.pos = central.velocity*self.delta_t + central.pos
                t += 1
        if bool(self.options["do_restart"]):
            self.restart()
