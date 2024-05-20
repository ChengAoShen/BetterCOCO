# -*- coding: utf-8 -*-
"""
fix_COCO_bb_problem.py

This script repairs COCO annotation polygons that have fewer than 5 points by 
duplicating the last point until there are exactly 5 points.
This is a common issue when converting annotations from other formats to COCO format
and this problems will cause `bb` error.


Copyright (C) 2024 DVA Lab All rights reserved.

Usage:
    For script usage: import and call the function `repair_polygon_annotations`.
    For command line usage: run the script with parameters, e.g.,
    `python repair_polygon_annotations.py --json_file path/to/input.json 
    --new_json_file path/to/output.json`.

Author: ChengAo Shen
Date: 2024-05-20
"""

import json
import argparse


def repair_polygon_annotations(json_file, new_json_file=None):
    if new_json_file is None:
        new_json_file = json_file

    # Read the JSON file
    with open(json_file, "r") as f:
        data = json.load(f)

    # Check and repair each annotation
    for annotation in data["annotations"]:
        for segmentation in annotation["segmentation"]:
            # In COCO, segmentation can be RLE or polygons, we only handle polygons (lists)
            if isinstance(segmentation, list):
                # Check each polygon, if the number of points is less than 5, repair it
                num_points = len(segmentation) // 2
                if num_points < 5:
                    print(
                        f"Repairing polygon in annotation ID {annotation['id']} with {num_points} points."
                    )
                    last_point = segmentation[
                        -2:
                    ]  # Get the coordinates of the last point
                    # Supplement the missing points
                    while len(segmentation) // 2 < 5:
                        segmentation.extend(last_point)

    # Write the repaired data back to the original or a new file
    with open(new_json_file, "w") as f:
        json.dump(data, f, indent=4)


def main():
    parser = argparse.ArgumentParser(
        description="Repair COCO polygons with fewer than 5 points."
    )
    parser.add_argument(
        "--json_file",
        type=str,
        required=True,
        help="Path to the input JSON file with annotations.",
    )
    parser.add_argument(
        "--new_json_file",
        type=str,
        help="Path to the output JSON file where repaired annotations will be saved.",
    )

    args = parser.parse_args()

    repair_polygon_annotations(args.json_file, args.new_json_file)


if __name__ == "__main__":
    main()
