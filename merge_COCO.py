# -*- coding: utf-8 -*-
"""
merge_coco.py

This script merges multiple COCO-format JSON files into a single JSON file. It combines images, annotations,
and categories from all input files, ensuring unique IDs across the combined dataset.

Copyright (C) 2024 DVA Lab All rights reserved.

Usage:
    Run the script from the command line with parameters, for example:
    `python merge_coco.py --json_paths ./annotations1.json ./annotations2.json --output_path ./merged_annotations.json`

Author: ChengAo Shen
Date: 2024-06-19
"""

import json
import argparse
from pycocotools.coco import COCO


def merge_coco_jsons(json_paths, output_path):
    """
    Merges multiple COCO-format JSON files into a single JSON file.

    Args:
        json_paths (list of str): Paths to the COCO JSON files to merge.
        output_path (str): Path where the merged COCO JSON file will be saved.
    """
    merged_data = {"images": [], "annotations": [], "categories": []}
    next_image_id = 1
    next_annotation_id = 1
    category_map = {}

    for json_path in json_paths:
        coco = COCO(json_path)

        # Update image IDs and add to merged list
        for image in coco.dataset["images"]:
            image["id"] = next_image_id
            merged_data["images"].append(image)
            next_image_id += 1

        # Update annotation IDs and map category IDs
        for annotation in coco.dataset["annotations"]:
            original_category_id = annotation["category_id"]
            if original_category_id not in category_map:
                category_map[original_category_id] = len(merged_data["categories"]) + 1
                merged_data["categories"].append(
                    {
                        "id": category_map[original_category_id],
                        "name": coco.cats[original_category_id]["name"],
                        "supercategory": coco.cats[original_category_id][
                            "supercategory"
                        ],
                    }
                )
            annotation["category_id"] = category_map[original_category_id]
            annotation["id"] = next_annotation_id
            annotation["image_id"] = annotation["image_id"]  # Remap if needed
            merged_data["annotations"].append(annotation)
            next_annotation_id += 1

    # Save the merged COCO dataset
    with open(output_path, "w") as f:
        json.dump(merged_data, f, indent=4)

    print("Merged COCO JSON file has been created at:", output_path)


def main():
    parser = argparse.ArgumentParser(
        description="Merge multiple COCO-format JSON files into one."
    )
    parser.add_argument(
        "--json_paths",
        nargs="+",
        required=True,
        help="Paths to the COCO JSON files to merge",
    )
    parser.add_argument(
        "--output_path", required=True, help="Path to save the merged COCO JSON file"
    )

    args = parser.parse_args()
    merge_coco_jsons(args.json_paths, args.output_path)


if __name__ == "__main__":
    main()
