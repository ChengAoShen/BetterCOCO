# -*- coding: utf-8 -*-
"""
show_mask.py

This script displays images and their associated COCO annotations. It loads the specified
images and annotations, and visualizes the annotations on the images using Matplotlib.

Copyright (C) 2024 DVA Lab All rights reserved.

Usage:
    For script usage: import and call the function `show_mask`.
    For command line usage: run the script with parameters, e.g.,
    `python show_mask.py --annotation_file path/to/annotations.json 
    --image_dir path/to/images --img_id 1`.


Author: ChengAo Shen
Date: 2024-05-20
"""

import os
import cv2
import matplotlib.pyplot as plt
from pycocotools.coco import COCO
import argparse


def show_mask(annotation_file: str, image_dir: str, img_id: int | list[int]):
    coco = COCO(annotation_file)

    # Convert single image ID to list if necessary
    if isinstance(img_id, int):
        img_id = [img_id]

    for i in img_id:
        img_info = coco.loadImgs([i])[0]
        img_filename = img_info["file_name"]
        image_path = os.path.join(image_dir, img_filename)

        # Load the image using OpenCV and convert from BGR to RGB
        img = cv2.imread(image_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Get annotation IDs and load annotations for the image
        ann_ids = coco.getAnnIds(imgIds=[i])
        anns = coco.loadAnns(ann_ids)

        # Display the image with annotations using Matplotlib
        plt.imshow(img)
        coco.showAnns(anns)
        plt.axis("off")
        plt.show()


def main():
    parser = argparse.ArgumentParser(description="Display COCO annotations on images.")
    parser.add_argument(
        "--annotation_file",
        type=str,
        required=True,
        help="Path to the COCO annotation JSON file.",
    )
    parser.add_argument(
        "--image_dir", type=str, required=True, help="Directory containing the images."
    )
    parser.add_argument(
        "--img_id",
        type=int,
        nargs="+",
        required=True,
        help="Image ID(s) to display annotations for.",
    )

    args = parser.parse_args()

    show_mask(args.annotation_file, args.image_dir, args.img_id)


if __name__ == "__main__":
    main()
