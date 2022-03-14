# Configuration for COCO dataset reducer

INPUT_ANNS_FILE_PATH = "resources/instances_val2017.json"
OUTPUT_ANNS_FILE_PATH = "resources/new_instances_val2017.json"


REDUCED_DATASET_PARAMS = {
    "num_classes": 20,
    "max_samples_class": 100
}

# Configuration Pascal -> COCO conversor

IMAGES_PATH = "/Dades/ubuntuold/UPC/TFM/datasets/grapes_dataset/0"
ANNOTATIONS_PATH = "/Dades/ubuntuold/UPC/TFM/datasets/grapes_dataset/0"
OUTPUT_COVERSION_PATH = "/Dades/ubuntuold/UPC/TFM/CustomCOCO/resources/pascal_to_coco.json"

# Configuration Grapes dataset

GRAPES_DATASET = {
    "path": "/Dades/ubuntuold/UPC/TFM/datasets/grapes_dataset",
    "output_ann_path": "/Dades/ubuntuold/UPC/TFM/CustomCOCO/resources"
}