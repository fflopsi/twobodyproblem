import os
import signal
import sys

import vpython as vp

from twobodyproblem.options import Options
from twobodyproblem.values import Values
from twobodyproblem.visualization.body import Body

def run_simulation(values: Values = Values(), options: Options = Options()): # TODO: fix indentation
    """Open the vpython window and start the simulation
    
    Arguments:
    values: Values object with physical values required for simulation
    options: Options object required for adjusting simulation
    """
    if not isinstance(values, Values) or not isinstance(options, Options):
        raise TypeError("values must be of type Values, options must be "
                        "of type Options")

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

    def change_rate(field: vp.winput):
        """Change the rate according to winput field number"""
        options.rate = field.number

    def change_delta_t(field: vp.winput):
        """Change the Δt factor according to winput field number"""
        options.delta_t = field.number

    def adjust_radius(slider: vp.slider, sphere: Body):
        """Adjust the visual size of the body according to the slider value

        Arguments:
        slider: vpython slider which was changed
        sphere: Body associated with the slider
        """
        sphere.radius = eval("values." + sphere.name + ".radius") \
                        * slider.value

    def reset_slider(slider: vp.slider):
        """Reset the slider to the default value"""
        slider.value = 1
        slider.bind()

    # set up canvas, bodies and pointers
    scene = vp.canvas(title="Simulation zum Zweikörperproblem",
                      height=options.canvas.height,
                      width=options.canvas.width)
    central = Body(name="central", mass=values.central.mass,
                   velocity=vp.vector(values.central.velocity.x,
                                      values.central.velocity.y,
                                      values.central.velocity.z),
                   radius=values.central.radius, make_trail=True,
                   color=vp.vector(options.colors.bodies.x / 255,
                                   options.colors.bodies.y / 255,
                                   options.colors.bodies.z / 255))
    sat = Body(name="sat", mass=values.sat.mass,
               velocity=vp.vector(values.sat.velocity.x,
                                  values.sat.velocity.y,
                                  values.sat.velocity.z),
               pos=vp.vector(values.distance + values.central.radius
                             + values.sat.radius, 0, 0),
               radius=values.sat.radius, make_trail=True,
               color=vp.vector(options.colors.bodies.x / 255,
                               options.colors.bodies.y / 255,
                               options.colors.bodies.z / 255))
    central_ptr = vp.arrow(axis=vp.vector(0,
                                        -((values.distance
                                            + central.radius
                                            + sat.radius) / 2),
                                        0),
                           color=vp.vector(
                               options.colors.pointers.x,
                               options.colors.pointers.y,
                               options.colors.pointers.z),
                           visible=options.pointers)
    central_ptr.pos = (central.pos - central_ptr.axis) + vp.vector(
        0, values.central.radius, 0)
    sat_ptr = vp.arrow(axis=vp.vector(0, -((values.distance +
                                            central.radius +
                                            sat.radius) / 2), 0),
                       color=vp.vector(
                           options.colors.pointers.x,
                           options.colors.pointers.y,
                           options.colors.pointers.z),
                       visible=options.pointers)
    sat_ptr.pos = sat.pos - sat_ptr.axis + vp.vector(0, values.sat.radius, 0)

    # set up buttons
    pause_sim = vp.button(text="Pause", bind=pause)
    vp.button(text="Stop",
            bind=lambda: os.kill(os.getpid(), signal.SIGINT))
    vp.button(text="Restart", bind=restart)
    vp.checkbox(text="Collision detection",
                bind=switch_collision_detection, checked=True)
    scene.append_to_caption("\n")

    # set up text fields for rate and Δt
    vp.winput(text=options.rate, prompt="Rate: ", bind=change_rate) # TODO: test prompt
    vp.winput(text=options.delta_t, prompt="Δt: ", bind=change_delta_t)

    # set up sliders for changing the radius of the two bodies
    central_slider = vp.slider(max=((values.distance +
                                    values.central.radius) /
                                    values.central.radius),
                            min=1, value=1, top=12, bottom=12,
                            bind=lambda: adjust_radius(
                                slider=central_slider, sphere=central))
    vp.button(text="Reset", bind=lambda: reset_slider(central_slider))
    scene.append_to_caption("\n")
    sat_slider = vp.slider(max=((values.distance +
                                values.sat.radius) /
                                values.sat.radius),
                        min=1, value=1, top=12, bottom=12,
                        bind=lambda: adjust_radius(slider=sat_slider,
                            sphere=sat))
    vp.button(text="Reset", bind=lambda: reset_slider(sat_slider))

    # set up time variables
    t = 0
    t_max = options.rate * options.sim_time
    # main simulation loop
    if options.central_centered:
        scene.camera.follow(central)
    while t <= t_max:
        # weird behaviour of those two
        vp.rate(options.rate)
        # vp.sleep(1/options["update_rate"])
        if pause_sim.text == "Pause":
            # physical calculations
            r = sat.pos - central.pos
            fv = (6.67430e-11 * central.mass * sat.mass) / (vp.mag(r) ** 2)
            central.force = fv * vp.norm(r)
            sat.force = fv * vp.norm(-r)
            central.calculate(options.delta_t)
            sat.calculate(options.delta_t)
            if options.pointers:
                # move pointers
                central_ptr.pos = central.pos - central_ptr.axis + \
                                vp.vector(0, central.radius, 0)
                sat_ptr.pos = sat.pos - sat_ptr.axis + vp.vector(
                    0, sat.radius, 0)
            if options.sim_time > 0:
                t += 1
            # collision detection
            if collision_detection and vp.mag(sat.pos - central.pos) < \
                    values.central.radius + values.sat.radius:
                pause_sim.text = "Collision detected (original radii)," + \
                                " click to continue"
    if bool(options.restart):
        restart()
