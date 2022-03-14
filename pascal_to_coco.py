from src.lib.pascal_to_coco import PascalToCOCO
import config

if __name__ == "__main__":
    categories = ["grapes"]
    pascal_to_coco = PascalToCOCO(
        images_path=config.IMAGES_PATH,
        annotations_path=config.ANNOTATIONS_PATH,
        cat_list=categories
    )

    _ = pascal_to_coco.convert(config.OUTPUT_COVERSION_PATH)