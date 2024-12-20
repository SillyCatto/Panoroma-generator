#!/usr/bin/env python3

import os
import sys

import cv2


try:
    source_path = sys.argv[1]
except IndexError:
    sys.exit("\nERROR: Path must be provided.\n")

# get the output path if it exists or an empty subset
output_path = sys.argv[2:3]

def panaroma(images, stitch_mode):
    stitcher = cv2.Stitcher.create(stitch_mode)
    status, pano = stitcher.stitch(images)

    if status != cv2.Stitcher_OK:
        raise RuntimeError(f"Stitching failed (status_code: {status})")
    
    return pano


pano = panaroma(
    images=[cv2.imread(img) for img in os.scandir(source_path)],
    stitch_mode=cv2.STITCHER_PANORAMA,
)

if output_path:
    cv2.imwrite(output_path[0], pano)
else:
    cv2.imshow('output', pano)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
