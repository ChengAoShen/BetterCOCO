# -*- coding: utf-8 -*-
"""
convert_labelme_to_coco.py

This script converts annotation data from Labelme format to COCO format. It processes
a directory containing Labelme JSON files and corresponding images, and generates a
new COCO format JSON file with updated image references and annotations.

Copyright (C) 2024 DVA Lab All rights reserved.

Usage:
    For script usage: import and call the function `convert_labelme_to_coco`.
    For command line usage: run the script with parameters, e.g.,
    `python convert_labelme_to_coco.py --Labelme_dir ./Train --img_path 
    ./Train/Image --json_path ./coco_annotations.json`.

Author: ChengAo Shen
Date: 2024-05-20
"""

import json
import os
import shutil
from PIL import Image
from tqdm import tqdm
import argparse


def convert_labelme_to_coco(Labelme_dir, img_path, json_path):
    categories = ["car"]
    image_id = 0
    annotation_id = 0

    # Create the image path directory if it does not exist
    if not os.path.exists(img_path):
        os.makedirs(img_path)

    # Initialize the COCO format dictionary
    coco_format = {"images": [], "annotations": [], "categories": []}

    # Add category information to the COCO format
    for idx, category in enumerate(categories):
        coco_format["categories"].append(
            {"id": idx + 1, "name": category, "supercategory": "none"}
        )

    # Process each file in the Labelme directory
    for idx, filename in tqdm(enumerate(sorted(os.listdir(Labelme_dir)))):
        if filename.endswith(".json"):
            full_json_path = os.path.join(Labelme_dir, filename)
            image_name = filename.split(".")[0] + ".png"
            image_path = os.path.join(Labelme_dir, image_name)

            # Generate a new image file name
            new_image_name = f"{image_id + 1:04d}.png"

            # Copy and rename the image to the img_path folder
            shutil.copy(image_path, os.path.join(img_path, new_image_name))

            # Read the Labelme JSON file
            with open(full_json_path, "r") as f:
                labelme_data = json.load(f)

            # Add image information to COCO
            img = Image.open(os.path.join(img_path, new_image_name))
            width, height = img.size
            coco_format["images"].append(
                {
                    "file_name": new_image_name,
                    "height": height,
                    "width": width,
                    "id": image_id,
                }
            )

            # Process each annotation
            for shape in labelme_data["shapes"]:
                category_name = shape["label"]
                category_id = categories.index(category_name) + 1
                points = shape["points"]

                # Convert points to COCO format segmentation and bbox
                segmentation = [sum(points, [])]  # Flatten the list of points
                min_x = min([p[0] for p in points])
                max_x = max([p[0] for p in points])
                min_y = min([p[1] for p in points])
                max_y = max([p[1] for p in points])
                bbox = [min_x, min_y, max_x - min_x, max_y - min_y]

                # Add annotation information to COCO
                coco_format["annotations"].append(
                    {
                        "id": annotation_id,
                        "image_id": image_id,
                        "category_id": category_id,
                        "segmentation": segmentation,
                        "area": bbox[2] * bbox[3],
                        "bbox": bbox,
                        "iscrowd": 0,
                    }
                )
                annotation_id += 1
            image_id += 1

    # Write the final COCO JSON file
    with open(json_path, "w") as f:
        json.dump(coco_format, f, indent=4)


def main():
    parser = argparse.ArgumentParser(
        description="Convert Labelme annotations to COCO format."
    )
    parser.add_argument(
        "--Labelme_dir",
        type=str,
        required=True,
        help="Directory containing Labelme JSON files and images.",
    )
    parser.add_argument(
        "--img_path",
        type=str,
        required=True,
        help="Path where processed images will be stored.",
    )
    parser.add_argument(
        "--json_path",
        type=str,
        required=True,
        help="Path where the resulting COCO format JSON file will be saved.",
    )

    args = parser.parse_args()

    convert_labelme_to_coco(args.Labelme_dir, args.img_path, args.json_path)


if __name__ == "__main__":
    main()
