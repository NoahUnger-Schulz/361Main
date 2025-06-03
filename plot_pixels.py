"""import matplotlib.pyplot as plt

# Create a figure and axes
fig, ax = plt.subplots()

# Plot some data
ax.plot([1, 2, 3], [4, 5, 6])

# Ensure Gtk backend is used
import matplotlib
print(matplotlib.get_backend())
matplotlib.use('gtk4agg')  # Or 'GTK4Agg'

# Get the window manager
mngr = plt.get_current_fig_manager()
print(mngr)
print(geom = mngr.window.geometry())"""

"""import matplotlib.pyplot as plt

import matplotlib
print(matplotlib.get_backend())


# Create a figure
fig = plt.figure()
mngr = plt.get_current_fig_manager()
print(mngr)"""

"""# Get the Tk window
window = fig.canvas.manager.window
print(window)"""


"""import matplotlib.pyplot as plt

fig, ax = plt.subplots()
mngr = plt.get_current_fig_manager()
# to put it into the upper left corner for example:
mngr.window.setGeometry(50,100,640, 545)"""

"""import matplotlib
matplotlib.use('GTK4Agg')
import matplotlib.pyplot as plt


def move_figure(f, x, y):
    backend = matplotlib.get_backend()
    print(backend)
    if backend == 'TkAgg':
        f.canvas.manager.window.wm_geometry("+%d+%d" % (x, y))
    elif backend == 'WXAgg':
        f.canvas.manager.window.SetPosition((x, y))
    else:
        # This works for QT and GTK
        # You can also use window.setGeometry
        f.canvas.manager.window.move(x, y)

f, ax = plt.subplots()
move_figure(f, 500, 500)
plt.show()"""

"""import matplotlib.pyplot as plt
from matplotlib.backends.backend_gtk4agg import FigureCanvasGTK4Agg
import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk


# Create a matplotlib figure and axes
fig, ax = plt.subplots()

# Create a GTK window
window = Gtk.Window()
window.set_title("Matplotlib Window Position Example")

# Create a FigureCanvasGTK4Agg widget and add it to the window
canvas = FigureCanvasGTK4Agg(fig)
window.set_child(canvas)

# Get the Gtk.Window object from the canvas
gtk_window = canvas.get_window()

# Get the position of the window
if gtk_window:
    x, y = gtk_window.get_position()
    print(f"Window position: x={x}, y={y}")
else:
    print("Could not get Gtk.Window object")

window.show()"""

"""
import gi

gi.require_version('Gtk', '4.0')
from gi.repository import Gtk

import numpy as np

from matplotlib.backends.backend_gtk4agg import \
    FigureCanvasGTK4Agg as FigureCanvas
from matplotlib.figure import Figure


def on_activate(app):
    win = Gtk.ApplicationWindow(application=app)
    win.set_default_size(800, 300)
    win.set_title("Embedded in GTK4")

    fig = Figure(figsize=(5, 4), dpi=100)
    ax = fig.add_subplot()
    t = np.arange(0.0, 3.0, 0.01)
    s = np.sin(2*np.pi*t)
    ax.plot(t, s)

    # A scrolled margin goes outside the scrollbars and viewport.
    sw = Gtk.ScrolledWindow(margin_top=10, margin_bottom=10,
                            margin_start=10, margin_end=10)
    win.set_child(sw)

    canvas = FigureCanvas(fig)  # a Gtk.DrawingArea
    canvas.set_size_request(800, 600)
    sw.set_child(canvas)

    win.show()


app = Gtk.Application(application_id='org.matplotlib.examples.EmbeddingInGTK4')
app.connect('activate', on_activate)
app.run(None)"""

import matplotlib.pyplot as plt
from pynput import mouse
import ctypes

#PROCESS_PER_MONITOR_DPI_AWARE = 2
#ctypes.windll.shcore.SetProcessDpiAwareness(PROCESS_PER_MONITOR_DPI_AWARE)

fig, ax = plt.subplots()
ax.plot([1, 2, 3], [4, 5, 8])  # Example plot
def on_click(x, y, button, pressed):
    if pressed:

        # Convert from display (pixel) coordinates to data coordinates
        data_coords = ax.transData.inverted().transform((x, y))
        print(f"Clicked at data coordinates: {data_coords}")
        ax.plot([1, 2, 3], [4, 5, 6])
mouse_listener = mouse.Listener(on_click=on_click)

mouse_listener.start()

try:
    plt.show()
except KeyboardInterrupt:
    print("Program terminated!")
finally:
    mouse_listener.stop()
    mouse_listener.join()