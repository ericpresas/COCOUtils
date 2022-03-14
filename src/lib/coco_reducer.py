import src.utils.utils as utils


class COCOReducer(object):
    def __init__(self, config):
        self.config = config

    def reduce(self):
        coco_tools = utils.load_ann_file(self.config.INPUT_ANNS_FILE_PATH)
        cats = coco_tools.loadCats(coco_tools.getCatIds())

        # Randomly sample classes
        cats = utils.random_sample(cats, self.config.REDUCED_DATASET_PARAMS['num_classes'])

        # Sample images from classes
        imgs = []
        anns = []
        for cat in cats:

            imgsIds = coco_tools.getImgIds(catIds=cat['id'])
            imgsInfo = coco_tools.loadImgs(imgsIds)

            imgsInfo = utils.random_sample(imgsInfo, self.config.REDUCED_DATASET_PARAMS['max_samples_class'])
            imgs += imgsInfo

            annotationsIds = coco_tools.getAnnIds(imgIds=imgsIds, catIds=cat['id'])
            annotationsInfo = coco_tools.loadAnns(annotationsIds)
            anns += annotationsInfo

        new_annotation_file = {
            "categories": cats,
            "images": imgs,
            "annotations": anns
        }

        utils.save_ann_file(new_annotation_file, self.config.OUTPUT_ANNS_FILE_PATH)
