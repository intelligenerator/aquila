import torch
from PIL import Image
import torchvision.transforms.functional as TF


def crop(img, target_size=512):
    cutouts = TF.five_crop(img, target_size)
    return [TF.to_tensor(img) for img in cutouts]


def pad_maps(parts, input_size=512, output_size=1024, fill=0):
    pad = (output_size - input_size)
    results = []

    for i, img in enumerate(parts):
        padding = (pad//2, pad//2, pad//2, pad//2)

        # tl image: pad right and bottom
        if i == 0:
            padding = (0, 0, pad, pad)
        # tr image: pad left and bottom
        elif i == 1:
            padding = (pad, 0, 0, pad)
        # bl image: pad right and top
        elif i == 2:
            padding = (0, pad, pad, 0)
        # br image: pad left and top
        elif i == 3:
            padding = (pad, pad, 0, 0)

        img = TF.to_pil_image(img)
        img = TF.pad(img, padding, fill=fill)
        img = TF.to_tensor(img)
        results.append(img)

    return results


def combine_maps(maps, **kwargs):
    maps = pad_maps(maps, **kwargs)
    result = torch.zeros_like(maps[0], dtype=torch.int32)

    for segmap in maps:
        result = result.bitwise_or(segmap.int())

    return result
