# BetterCOCO🚀

COCO format is widely used in many places as a common data format in the field of object detection and instance segmentation in deep learning. However, in the process of use, the officially provided `pycocotools` often do not meet all needs. So in this repository, we include a series of very useful scripts to facilitate the use of COCO-formatted datasets, which are constantly updated.

**Script List**

* `convert_labelme_to_coco.py`: This script converts annotation data from Labelme format to COCO format. It processes a directory containing `Labelme` JSON files and corresponding images and generates a new COCO format JSON file with updated image references and annotations.
* `fix_COCO_bb_problem.py`: This script repairs COCO annotation polygons that have fewer than 5 points by duplicating the last point until there are exactly 5 points. This is a common issue when converting annotations from other formats to COCO format and this problem will cause `bb` error.
* `show_mask.py`: This script displays images and their associated COCO annotations. It loads the specified images and annotations, and visualizes the annotations on the images using `Matplotlib`.
* `split_coco_json.py`: This script splits a COCO-format dataset into training and validation subsets, facilitating machine learning model training and evaluation. 