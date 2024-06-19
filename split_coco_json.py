# -*- coding: utf-8 -*-
"""
split_coco_json.py

This script splits a COCO dataset into training and validation sets. It processes a 
COCO format JSON file and generates two new JSON files for the train and validation sets.

Copyright (C) 2024 DVA Lab All rights reserved.

Usage:
    For script usage: import and call the function `split_coco_json`.
    For command line usage: run the script with parameters, e.g.,
    `python split_coco_json.py --json_path ./coco_annotations.json --output_train_json 
    ./train_annotations.json --output_val_json ./val_annotations.json --val_size 0.2`.

Author: ChengAo Shen
Date: 2024-06-19
"""

import json
import argparse
from pycocotools.coco import COCO
from sklearn.model_selection import train_test_split


def split_coco_json(json_path, output_train_json, output_val_json, val_size=0.2):
    """
    Splits a COCO dataset into training and validation sets based on the specified validation size.

    Args:
        json_path (str): Path to the original COCO JSON file.
        output_train_json (str): Path to save the training subset JSON.
        output_val_json (str): Path to save the validation subset JSON.
        val_size (float): Proportion of the dataset to include in the validation split.
    """
    coco = COCO(json_path)
    image_ids = list(coco.imgs.keys())
    train_ids, val_ids = train_test_split(
        image_ids, test_size=val_size, random_state=42
    )

    def generate_subset(ids):
        imgs = [coco.imgs[id] for id in ids]
        ann_ids = coco.getAnnIds(imgIds=ids)
        anns = coco.loadAnns(ann_ids)
        return {
            "info": coco.dataset["info"],
            "licenses": coco.dataset["licenses"],
            "images": imgs,
            "annotations": anns,
            "categories": coco.dataset["categories"],
        }

    train_data = generate_subset(train_ids)
    val_data = generate_subset(val_ids)

    with open(output_train_json, "w") as f:
        json.dump(train_data, f, indent=4)
    with open(output_val_json, "w") as f:
        json.dump(val_data, f, indent=4)

    print("Train and validation JSON files have been created.")


def main():
    parser = argparse.ArgumentParser(
        description="Split a COCO-style JSON file into train and validation sets."
    )
    parser.add_argument(
        "--json_path", required=True, help="Path to the input COCO JSON file"
    )
    parser.add_argument(
        "--output_train_json",
        required=True,
        help="Path where the training set JSON will be saved",
    )
    parser.add_argument(
        "--output_val_json",
        required=True,
        help="Path where the validation set JSON will be saved",
    )
    parser.add_argument(
        "--val_size",
        type=float,
        default=0.2,
        help="Proportion of data to be used as the validation set",
    )

    args = parser.parse_args()
    split_coco_json(
        args.json_path, args.output_train_json, args.output_val_json, args.val_size
    )


if __name__ == "__main__":
    main()
