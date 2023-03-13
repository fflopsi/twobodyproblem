import os
import signal
import sys

import vpython as vp

from twobodyproblem.options import Options
from twobodyproblem.values import Values
from twobodyproblem.visualization.body import Body


class Simulation:
    """Visualization of the simulation
    
    Attributes:
    values: Values object with physical values required for simulation
    options: Options object required for adjusting simulation
    """

    def __init__(self, values: Values, options: Options):
        """Initialize a Simulation with required values and options"""
        if isinstance(values, Values) and isinstance(options, Options):
            self.values = values
            self.options = options
        else:
            raise TypeError("values must be of type Values, options must be "
                            "of type Options")

    def start(self): # TODO: rename
        """Open the vpython window and start the simulation"""
        # set up important boolean values from options
        testing = self.options.testing
        central_centered = self.options.central_centered
        show_pointers = self.options.pointers

        collision_detection = True

        def pause(button: vp.button):
            """Pause and un-pause the simulation

            Arguments:
            button: Pause vpython button itself
            """
            if button.text == "Pause":
                button.text = "Play"
            else:
                button.text = "Pause"

        def restart():
            """Restart the program"""
            # does not work perfectly, especially on command line
            os.execl(sys.executable, sys.executable, *sys.argv)
            # os.execv(sys.executable, ["python"] + sys.argv)

        def switch_collision_detection(button: vp.button):
            """Activate and deactivate collision detection"""
            if button.checked:
                collision_detection = True
            else:
                collision_detection = False

        def adjust_radius(slider: vp.slider, sphere: Body):
            """Adjust the visual size of the body according to the slider value

            Arguments:
            slider: vpython slider which was changed
            sphere: Body associated with the slider
            """
            sphere.radius = eval("self.values." + sphere.name
                                 + ".radius") * slider.value

        def reset_slider(slider: vp.slider):
            """Reset the slider to the default value"""
            slider.value = 1
            slider.bind()

        # set up canvas, bodies and pointers
        scene = vp.canvas(title="Simulation zum Zweikörperproblem",
                          height=self.options.canvas.height,
                          width=self.options.canvas.width)
        central = Body(sim=self, name="central", mass=self.values.central.mass,
                       velocity=vp.vector(self.values.central.velocity.x,
                                          self.values.central.velocity.y,
                                          self.values.central.velocity.z),
                       radius=self.values.central.radius, make_trail=True,
                       color=vp.vector(self.options.colors.bodies.x / 255,
                                       self.options.colors.bodies.y / 255,
                                       self.options.colors.bodies.z / 255))
        sat = Body(sim=self, name="sat", mass=self.values.sat.mass,
                   velocity=vp.vector(self.values.sat.velocity.x,
                                      self.values.sat.velocity.y,
                                      self.values.sat.velocity.z),
                   pos=vp.vector(self.values.distance
                                 + self.values.central.radius
                                 + self.values.sat.radius, 0, 0),
                   radius=self.values.sat.radius, make_trail=True,
                   color=vp.vector(self.options.colors.bodies.x / 255,
                                   self.options.colors.bodies.y / 255,
                                   self.options.colors.bodies.z / 255))
        central_ptr = vp.arrow()
        sat_ptr = vp.arrow()
        if show_pointers:
            central_ptr = vp.arrow(axis=vp.vector(0,
                                                  -((self.values.distance
                                                     + central.radius
                                                     + sat.radius) / 2),
                                                  0),
                                   color=vp.vector(
                                       self.options.colors.pointers.x,
                                       self.options.colors.pointers.y,
                                       self.options.colors.pointers.z))
            central_ptr.pos = (central.pos - central_ptr.axis) + vp.vector(
                0, self.values.central.radius, 0)
            sat_ptr = vp.arrow(axis=vp.vector(0, -((self.values.distance +
                                                    central.radius +
                                                    sat.radius) / 2), 0),
                               color=vp.vector(
                                   self.options.colors.pointers.x,
                                   self.options.colors.pointers.y,
                                   self.options.colors.pointers.z))
            sat_ptr.pos = sat.pos - sat_ptr.axis + vp.vector(
                0, self.values.sat.radius, 0)

        # set up buttons
        pause_sim = vp.button(text="Pause", bind=pause)
        vp.button(text="Stop",
                  bind=lambda: os.kill(os.getpid(), signal.SIGINT))
        vp.button(text="Restart", bind=restart)
        vp.checkbox(text="Collision detection",
                    bind=switch_collision_detection, checked=True)
        scene.append_to_caption("\n")

        # set up sliders for changing the radius of the two bodies
        central_slider = vp.slider(max=((self.values.distance +
                                         self.values.central.radius) /
                                        self.values.central.radius),
                                   min=1, value=1, top=12, bottom=12,
                                   bind=lambda: adjust_radius(
                                       slider=central_slider, sphere=central))
        vp.button(text="Reset", bind=lambda: reset_slider(central_slider))
        scene.append_to_caption("\n")
        sat_slider = vp.slider(max=((self.values.distance +
                                     self.values.sat.radius) /
                                    self.values.sat.radius),
                               min=1, value=1, top=12, bottom=12,
                               bind=lambda: adjust_radius(slider=sat_slider,
                                   sphere=sat))
        vp.button(text="Reset", bind=lambda: reset_slider(sat_slider))

        # set up time variables
        t = 0
        t_max = self.options.rate * self.options.sim_time
        # main simulation loop
        if central_centered:
            scene.camera.follow(central)
        while t <= t_max:
            # weird behaviour of those two
            vp.rate(self.options.rate)
            # vp.sleep(1/self.options["update_rate"])
            if pause_sim.text == "Pause":
                # physical calculations
                r = sat.pos - central.pos
                fv = (6.67430e-11 * central.mass * sat.mass) / (vp.mag(r) ** 2)
                central.force = fv * vp.norm(r)
                sat.force = fv * vp.norm(-r)
                central.calculate(self.options.delta_t)
                sat.calculate(self.options.delta_t)
                if show_pointers:
                    # move pointers
                    central_ptr.pos = central.pos - central_ptr.axis + \
                                      vp.vector(0, central.radius, 0)
                    sat_ptr.pos = sat.pos - sat_ptr.axis + vp.vector(
                        0, sat.radius, 0)
                if self.options.sim_time > 0:
                    t += 1
                # collision detection
                if collision_detection and vp.mag(sat.pos - central.pos) < \
                        self.values.central.radius + self.values.sat.radius:
                    pause_sim.text = "Collision detected (original radii)," + \
                                     " click to continue"
        if bool(self.options.restart):
            restart()
