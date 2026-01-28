from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtCore import QThread, pyqtSignal
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import colorsys


class GanttUpdateThread(QThread):
    time_updated = pyqtSignal(float)

    def __init__(self, speed=1.0, interval=100, parent=None):
        super().__init__(parent)
        self.speed = speed
        self.interval = interval
        self.current_time = 0.0
        self._running = False
        self._paused = False

    def run(self):
        self._running = True
        while self._running:
            if not self._paused:
                self.current_time += self.speed * (self.interval / 1000.0)
                self.time_updated.emit(self.current_time)
            self.msleep(self.interval)

    def pause(self):
        self._paused = True

    def resume(self):
        self._paused = False

    def stop(self):
        self._running = False
        self.wait()

    def reset(self):
        self.current_time = 0.0

    def set_speed(self, speed):
        self.speed = speed


class GanttChart(QWidget):
    MACHINE_TIMES = {
        'm1': 5.3, 'm2': 5.8, 'm3': 4.8, 'm4': 5.8, 'm5': 4.2,
        'm6': 8.1, 'm6_adj': 2.0, 'm7': 4.8, 'm8': 6.3, 'm9': 4.9,
        'm10': 6.8, 'm11': 5.8
    }
    START_DELAYS = {
        'cover': 1.6, 'doors': 1.6, 'shelves': 2.0,
        'cooling': 1.6, 'lights': 2.0
    }
    TRANSITION_GAP = 0.3

    def __init__(self, tasks=None):
        super().__init__()
        self.fridge_tasks = []
        self.current_time = 0.0
        self.view_window = 30.0
        self.update_thread = None
        self.fridge_colors = {}
        self.color_index = 0
        self.task_gap = 1.0
        self.machine_available_time = {f"M{i}": 0.0 for i in range(1, 12)}

        layout = QVBoxLayout(self)
        self.figure = Figure(figsize=(6, 4), facecolor="#2e2e2e")
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        self.plot_gantt()
        self.start_animation(speed=1.0)

    def _generate_color(self, fridge_id):
        if fridge_id in self.fridge_colors:
            return self.fridge_colors[fridge_id]
        
        hue = (self.color_index * 0.618033988749895) % 1.0
        rgb = colorsys.hsv_to_rgb(hue, 0.7, 0.9)
        color = '#{:02x}{:02x}{:02x}'.format(int(rgb[0]*255), int(rgb[1]*255), int(rgb[2]*255))
        self.fridge_colors[fridge_id] = color
        self.color_index += 1
        return color

    def start_animation(self, speed=1.0):
        if self.update_thread is not None:
            return
        self.update_thread = GanttUpdateThread(speed=speed, interval=100)
        self.update_thread.time_updated.connect(self.on_time_update)
        self.update_thread.start()

    def stop_animation(self):
        if self.update_thread is not None:
            self.update_thread.stop()
            self.update_thread = None

    def pause_animation(self):
        if self.update_thread is not None:
            self.update_thread.pause()

    def resume_animation(self):
        if self.update_thread is not None:
            self.update_thread.resume()

    def reset_animation(self):
        self.current_time = 0.0
        if self.update_thread is not None:
            self.update_thread.reset()
        self.fridge_tasks = []
        self.fridge_colors = {}
        self.color_index = 0
        self.machine_available_time = {f"M{i}": 0.0 for i in range(1, 12)}
        self.plot_gantt()

    def set_animation_speed(self, speed):
        if self.update_thread is not None:
            self.update_thread.set_speed(speed)

    def on_time_update(self, time_value):
        self.current_time = time_value
        self.plot_gantt()

    def _get_fridge_attribute(self, item, *path, default=False):
        if isinstance(item, dict):
            result = item
            for key in path:
                result = result.get(key, {})
            return result if result != {} else default
        obj = item
        for attr in path:
            obj = getattr(obj, attr, None)
            if obj is None:
                return default
        return obj

    def _calculate_tasks_for_fridge(self, item, base_time):
        mt = self.MACHINE_TIMES
        sd = self.START_DELAYS
        gap = self.TRANSITION_GAP
        raw_tasks = []
        
        cover_end = sd['cover'] + mt['m1']
        paint_end = cover_end + gap + mt['m2']
        
        doors_end = sd['doors'] + mt['m3']
        machine_end = doors_end + gap + mt['m4']
        
        front_panel = self._get_fridge_attribute(item, 'doors', 'front_panel')
        panel_end = machine_end + gap + (mt['m5'] if front_panel else 0)
        
        adjustable = self._get_fridge_attribute(item, 'shelves', 'adjustable')
        shelf_time = mt['m6'] + (mt['m6_adj'] if adjustable else 0)
        shelves_end = sd['shelves'] + shelf_time
        
        frost_end = sd['cooling'] + mt['m7']
        freezer_end = frost_end + gap + mt['m8']
        energy_end = freezer_end + gap + mt['m9']
        
        lights_end = sd['lights'] + mt['m10']
        
        parallel_max = max(paint_end, panel_end, shelves_end, energy_end, lights_end)
        assembly_start = parallel_max + gap
        
        task_specs = [
            ("M1", sd['cover'], sd['cover'] + mt['m1']),
            ("M2", cover_end + gap, paint_end),
            ("M3", sd['doors'], sd['doors'] + mt['m3']),
            ("M4", doors_end + gap, machine_end),
            ("M5", machine_end + gap, panel_end),
            ("M6", sd['shelves'], shelves_end),
            ("M7", sd['cooling'], frost_end),
            ("M8", frost_end + gap, freezer_end),
            ("M9", freezer_end + gap, energy_end),
            ("M10", sd['lights'], lights_end),
            ("M11", assembly_start, assembly_start + mt['m11']),
        ]
        
        for machine, rel_start, rel_end in task_specs:
            raw_tasks.append({
                "machine": machine,
                "relative_start": rel_start,
                "relative_end": rel_end,
                "duration": rel_end - rel_start
            })

        scheduled_tasks = []
        for task in raw_tasks:
            machine = task["machine"]
            duration = task["duration"]
            
            if duration <= 0:
                scheduled_tasks.append({
                    "machine": machine,
                    "start": base_time + task["relative_start"],
                    "end": base_time + task["relative_end"]
                })
                continue

            earliest_start = base_time + task["relative_start"]
            machine_ready = self.machine_available_time.get(machine, 0.0)
            actual_start = max(earliest_start, machine_ready + self.task_gap)
            actual_end = actual_start + duration
            self.machine_available_time[machine] = actual_end

            scheduled_tasks.append({
                "machine": machine,
                "start": actual_start,
                "end": actual_end
            })

        return scheduled_tasks

    def _extract_fridge_id(self, fridge_item):
        if isinstance(fridge_item, dict):
            fridge_id = fridge_item.get('id')
            if fridge_id is None:
                body = fridge_item.get('body')
                if isinstance(body, dict):
                    fridge_id = body.get('id')
            return fridge_id
        return getattr(fridge_item, 'id', None)

    def add_fridge(self, fridge_item, fridge_id=None):
        if fridge_id is None:
            fridge_id = self._extract_fridge_id(fridge_item)
        if fridge_id is None:
            fridge_id = len(self.fridge_tasks) + 1

        self.fridge_tasks.append({
            "fridge_id": fridge_id,
            "color": self._generate_color(fridge_id),
            "tasks": self._calculate_tasks_for_fridge(fridge_item, self.current_time),
            "start_time": self.current_time
        })
        self.plot_gantt()

    def update_from_fridges(self, fridges, selected_index: int = 0):
        if not fridges:
            return
        if 1 <= selected_index <= len(fridges):
            idx = selected_index - 1
        elif 0 <= selected_index < len(fridges):
            idx = selected_index
        else:
            idx = 0
        self.add_fridge(fridges[idx])

    def clear_chart(self):
        self.stop_animation()
        self.fridge_tasks = []
        self.current_time = 0.0
        self.fridge_colors = {}
        self.color_index = 0
        self.machine_available_time = {f"M{i}": 0.0 for i in range(1, 12)}
        
        self.figure.clf()
        ax = self.figure.add_subplot(111)
        ax.set_facecolor("#2e2e2e")
        ax.set_title("")
        ax.set_xlabel("")
        ax.set_ylabel("")
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_visible(False)
        self.canvas.draw_idle()

    def _draw_task_bar(self, ax, y_pos, start, end, color):
        ax.barh(y_pos, end - start, left=start, color=color, zorder=3, height=0.6)

    def _render_fridge_tasks(self, ax, machine_positions, view_left, view_right):
        for fridge_data in self.fridge_tasks:
            color = fridge_data["color"]
            for task in fridge_data["tasks"]:
                start, end = task["start"], task["end"]
                duration = end - start

                if duration <= 0 or end < view_left or start > view_right:
                    continue

                visible_start = max(start, view_left)
                visible_end = min(end, view_right)
                if visible_end - visible_start <= 0:
                    continue

                y_pos = machine_positions.get(task["machine"], 0)

                if self.current_time >= end:
                    self._draw_task_bar(ax, y_pos, visible_start, visible_end, color)
                elif self.current_time <= start:
                    self._draw_task_bar(ax, y_pos, visible_start, visible_end, "#555555")
                else:
                    completed_start = max(visible_start, start)
                    completed_end = min(self.current_time, visible_end)
                    if completed_end > completed_start:
                        self._draw_task_bar(ax, y_pos, completed_start, completed_end, color)
                    
                    pending_start = max(self.current_time, visible_start)
                    if visible_end > pending_start:
                        self._draw_task_bar(ax, y_pos, pending_start, visible_end, "#555555")

    def _style_axes(self, ax, machines, view_left, view_right):
        ax.axvline(x=self.current_time, color="#ff4444", linewidth=2, linestyle='-', zorder=5)
        ax.set_xlim(left=view_left, right=view_right)
        ax.set_ylim(-0.5, len(machines) - 0.5)
        ax.set_yticks(range(len(machines)))
        ax.set_yticklabels(machines)
        ax.set_xlabel("Time", color="#00ffff")
        ax.set_ylabel("Machine", color="#00ffff")
        ax.set_title("Production Timeline", color="#00ffff")
        ax.invert_yaxis()
        ax.grid(True, zorder=1, color="#00ffff", alpha=0.3, linewidth=1.5)
        ax.tick_params(axis='x', colors='#00ffff')
        ax.tick_params(axis='y', colors='#00ffff')
        for spine in ax.spines.values():
            spine.set_color("#00ffff")

    def plot_gantt(self):
        self.figure.clf()
        ax = self.figure.add_subplot(111)
        ax.set_facecolor("#2e2e2e")

        machines = [f"M{i}" for i in range(1, 12)]
        machine_positions = {m: i for i, m in enumerate(machines)}
        view_left = self.current_time - self.view_window
        view_right = self.current_time

        if self.fridge_tasks:
            self.fridge_tasks = [
                f for f in self.fridge_tasks 
                if max(t["end"] for t in f["tasks"]) >= view_left
            ]
            self._render_fridge_tasks(ax, machine_positions, view_left, view_right)

        self._style_axes(ax, machines, view_left, view_right)
        self.canvas.draw_idle()
