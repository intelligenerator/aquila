import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

from .utils import damage_color, damage_str, add_padding


def draw_bbox(ax, bbox, damage, color=True, label=False):
    damage = damage.round().tolist()
    color = damage_color(damage) if color else (1, 0, 0, 0.3)

    x, y = bbox[0]  # top-left corner
    width = bbox[1][0] - x
    height = bbox[1][1] - y

    if label:
        ax.text(x, y, damage_str(damage), size=8)

    box = Rectangle((x, y), width, height, True, color=color, linewidth=4)
    ax.add_patch(box)
