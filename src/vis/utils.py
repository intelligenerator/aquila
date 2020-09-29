def damage_color(encoding):
    # no-damage: green
    if encoding == [0, 0, 0]:
        return (0, 1, 0, 0.3)
    # light-damage: yellow
    elif encoding == [1, 0, 0]:
        return (1, 1, 0, 0.3)
    # major-damage: orange
    elif encoding == [1, 1, 0]:
        return (1, 0.6, 0, 0.3)
    # destroyed: red
    elif encoding == [1, 1, 1]:
        return (1, 0, 0, 0.3)
    # unclassified: gray
    else:
        return (0.5, 0.5, 0.5, 0.3)


def damage_str(encoding):
    if encoding == [0, 0, 0]:
        return 'no-damage'
    elif encoding == [1, 0, 0]:
        return 'minor-damage'
    elif encoding == [1, 1, 0]:
        return 'major-damage'
    elif encoding == [1, 1, 1]:
        return 'destroyed'
    else:
        return 'unclassified'


def clip(value, lower, upper):
    return lower if value < lower else upper if value > upper else value


def add_padding(box, padding=20, clip_max=512):
    tl, br = box
    xmin, ymin = tl
    xmax, ymax = br

    xmin -= padding
    xmin = clip(xmin, 0, clip_max)

    ymin -= padding
    ymin = clip(ymin, 0, clip_max)

    xmax += padding
    xmax = clip(xmax, 0, clip_max)

    ymax += padding
    ymax = clip(ymax, 0, clip_max)

    return [(xmin, ymin), (xmax, ymax)]
