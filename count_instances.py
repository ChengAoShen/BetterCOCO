# -*- coding: utf-8 -*-
"""
count_instances.py

This script counts the number of instances in a specified image or calculates 
the average number of instances per image using a COCO-format JSON file. 
The script utilizes the pycocotools library to access and analyze the annotation data.


Copyright (C) 2024 DVA Lab All rights reserved.

Usage:
    To count instances for a specific image:
    `python count_instances.py --json_path ./annotations.json --image_id 12345`
    To calculate the average number of instances across all images:
    `python count_instances.py --json_path ./annotations.json`

Author: ChengAo Shen
Date: 2024-06-19
"""

import json
import argparse
from pycocotools.coco import COCO


def count_instances(json_path, image_id=None):
    """
    Counts the number of instances in the specified image or calculates the average number of instances per image
    using a COCO-format JSON file.

    Args:
        json_path (str): Path to the COCO JSON file.
        image_id (int, optional): ID of the image to analyze. If None, calculates the average instances per image.
    """
    coco = COCO(json_path)

    if image_id is not None:
        # Count instances for a specific image
        ann_ids = coco.getAnnIds(imgIds=[image_id])
        annotations = coco.loadAnns(ann_ids)
        instance_count = len(annotations)
        print(f"Number of instances in image ID {image_id}: {instance_count}")
        return instance_count
    else:
        # Calculate average instances per image across all images
        img_ids = coco.getImgIds()
        total_instances = 0
        for id in img_ids:
            ann_ids = coco.getAnnIds(imgIds=[id])
            annotations = coco.loadAnns(ann_ids)
            total_instances += len(annotations)
        average_instances = total_instances / len(img_ids) if img_ids else 0
        print(f"Average number of instances per image: {average_instances:.2f}")
        return average_instances


def main():
    parser = argparse.ArgumentParser(
        description="Count instances in a specified image or calculate average instances using a COCO-format JSON file."
    )
    parser.add_argument(
        "--json_path", type=str, required=True, help="Path to the COCO JSON file"
    )
    parser.add_argument(
        "--image_id", type=int, help="ID of the image to analyze (optional)"
    )

    args = parser.parse_args()
    count_instances(args.json_path, args.image_id)


if __name__ == "__main__":
    main()
