import vpython as vp
import signal
import os


class Simulation():
    """class used for the visualization of the simulation"""

    def __init__(self, window, values: dict, options: dict):
        self.parent = window
        self.values = values
        self.options = options
        self.pause_sim: vp.button
        self.paused = False

    def pause(self):
        """pause and un-pause the simulation"""
        self.paused = not self.paused
        if self.paused:
            self.pause_sim.text = "Play"
        else:
            self.pause_sim.text = "Pause"

    def adjust_radius(self, slider: str, value: float):
        """adjust the visual size of the spheres according to the slider values"""
        pass

    def reset_slider(self, slider: str):
        """reset the sliders to default values"""
        pass

    def start(self):
        """start the simulation and open the vpython window"""
        t = 0
        t_max = self.options["update_rate"] * self.options["max_seconds"]
        testing = self.options["do_testing"]
        central_unmoving = self.options["do_central_unmoving"]
        central_centered = self.options["do_central_centered"]
        scene = vp.canvas(
            title="Simulation zum Zweikörperproblem",
            height=self.options["canvas"]["height"],
            width=self.options["canvas"]["width"]
        )
        central = vp.sphere(
            radius=self.values["central_radius"], make_trail=True,
            color=vp.vector(
                self.options["color"]["objects"]["r"] / 255,
                self.options["color"]["objects"]["g"] / 255,
                self.options["color"]["objects"]["b"] / 255
            )
        )
        sat = vp.sphere(
            pos=vp.vector(self.values["distance"], 0, 0),
            radius=self.values["central_radius"], make_trail=True,
            color=vp.vector(
                self.options["color"]["objects"]["r"] / 255,
                self.options["color"]["objects"]["g"] / 255,
                self.options["color"]["objects"]["b"] / 255
            )
        )
        self.pause_sim = vp.button(text="Pause", bind=self.pause)
        vp.button(text="Stop", bind=lambda: os.kill(
            os.getpid(), signal.SIGINT))
        vp.button(text="Restart", bind=self.parent.restart)
        scene.append_to_caption("\n")
        G = 6.67430e-11  # gravitational constant
        M = self.values["central_mass"]
        m = self.values["sat_mass"]
        delta_t = self.options["t_factor"]
        if not central_unmoving:
            pos1_s = sat.pos
            pos1_c = central.pos
            v_pos1_s = vp.vector(
                self.values["sat_v0"]["x"],
                self.values["sat_v0"]["y"],
                self.values["sat_v0"]["z"]
            )
            v_pos1_c = vp.vector(
                self.values["central_v0"]["x"],
                self.values["central_v0"]["y"],
                self.values["central_v0"]["z"]
            )
        else:
            pos1 = sat.pos
            v_pos1 = vp.vector(
                self.values["sat_v0"]["x"],
                self.values["sat_v0"]["y"],
                self.values["sat_v0"]["z"]
            )
        if self.options["do_central_centered"]:
            scene.camera.follow(central)

        while t < t_max:
            # vp.rate(self.options["update_rate"])  # does not work apparently
            vp.sleep(1/self.options["update_rate"])
            if not self.paused:
                r = sat.pos - central.pos
                if not central_unmoving:
                    F_s = ((G*M*m) / (vp.mag(r)**2)) * vp.norm(-r)
                    F_c = ((G*M*m) / (vp.mag(r)**2)) * vp.norm(r)
                    a_s = F_s / m
                    a_c = F_c / M
                    v_s = a_s*delta_t + v_pos1_s
                    v_c = a_c*delta_t + v_pos1_c

                    sat.pos = v_s*delta_t + pos1_s
                    central.pos = v_c*delta_t + pos1_c

                    v_pos1_s = v_s
                    v_pos1_c = v_c
                    pos1_s = sat.pos
                    pos1_c = central.pos
                else:
                    F = ((G*M*m) / (vp.mag(r)**2)) * vp.norm(-r)
                    a = F / m
                    v = a*delta_t + v_pos1
                    sat.pos = v*delta_t + pos1

                    v_pos1 = v
                    pos1 = sat.pos
                t += 1
        if self.options["do_restart"]:
            self.parent.restart()
