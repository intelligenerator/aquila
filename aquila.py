#                    _ _
#   __ _  __ _ _   _(_) | __ _
#  / _` |/ _` | | | | | |/ _` |
# | (_| | (_| | |_| | | | (_| |
#  \__,_|\__, |\__,_|_|_|\__,_|
#           |_|
#

import matplotlib.pyplot as plt
import numpy as np

import torch
import torch.nn as nn
import torch.nn.functional as F

import torchvision
import torchvision.transforms.functional as TF

from PIL import Image

from inundatio import get_houses, pad_bbox
from perses.dnet import Net as Perses
from unet import UNet

from src.cli import opt
from src.data import combine_maps, crop
from src.vis import add_padding, draw_bbox


THEIA_MODEL = opt.theia
PERSES_MODEL = opt.perses

PRE = opt.pre
POST = opt.post


before = Image.open(PRE)
after = Image.open(POST)

assert before.size == after.size

SIZE = before.size[0]

dev = torch.device('cuda' if (torch.cuda.is_available()
                              and not opt.no_cuda) else 'cpu')
print('Using device "%s" for calculation' % dev)

# theia
theia = UNet(in_channels=3, out_channels=1, padding=True)
theia.load_state_dict(torch.load(THEIA_MODEL))
theia.eval()
theia = theia.to(dev)

# perses
perses = Perses()
perses.load_state_dict(torch.load(PERSES_MODEL))
perses.eval()
perses = perses.to(dev)


before = crop(before)

seg_maps = []
for img in before:
    seg_map = theia(img.unsqueeze(0).to(dev))
    seg_map = torch.sigmoid(seg_map).squeeze().detach().to('cpu')

    seg_map[seg_map < opt.threshhold] = 0
    seg_map[seg_map > 0] = 1

    seg_maps.append(seg_map)


seg_map = combine_maps(seg_maps).squeeze().detach().numpy()

coords = get_houses(seg_map)
coords = [add_padding(box, clip_max=SIZE) for box in coords]

fig, ax = plt.subplots(1)

ax.imshow(after)

for bbox in coords:
    bbox_image = after.crop((bbox[0][0], bbox[0][1], bbox[1][0], bbox[1][1]))

    x = TF.resize(bbox_image, (75, 75))
    x = TF.to_tensor(x)

    damage = perses(x.to(dev).unsqueeze(0))
    damage = torch.sigmoid(damage).detach().squeeze().to('cpu')

    draw_bbox(ax, bbox, damage)

if opt.save:
    plt.savefig(opt.save)
else:
    plt.show()
