from pycocotools.coco import COCO
import numpy as np
import skimage.io as io
from utils.ood_category import load_category

def get_city_filename(index):
    imagename = "zurich_{}_000019_leftImg8bit.png".format(format(index, "06d"))
    labelname = "zurich_{}_000019_gtFine_labelTrainIds.png".format(format(index, "06d"))
    name_dict = {"image":imagename, "label":labelname}
    return name_dict

def load_city_pair(index):
    name_dict = get_city_filename(index)
    image = io.imread("../figs/zurich/image/{}".format(name_dict["image"]))
    label = io.imread("../figs/zurich/label/{}".format(name_dict["label"]))
    return image,label

def main(cats, num_each_cat=10):
    dataDir = '..'
    dataType = 'val2017'
    annFile = '{}/annotations/instances_{}.json'.format(dataDir, dataType)

    coco = COCO(annFile)
    for cat in cats:
        print(cat)
        catIds = coco.getCatIds(catNms=[cat])
        imgIds = coco.getImgIds(catIds=catIds)
        img_count = idx = 0
        while img_count < 10:
            img = coco.loadImgs(imgIds[idx])[0]
            idx += 1
            image = io.imread('%s/%s/%s' % (dataDir, dataType, img['file_name']))
            annIds = coco.getAnnIds(imgIds=img['id'], catIds=catIds, iscrowd=None)
            anns = coco.loadAnns(annIds)
            mask = coco.polygon_extract(anns, image.shape[0], image.shape[1])
            if mask is None:
                continue
            else:
                img_count += 1
                io.imsave('../figs/coco/' + img['file_name'][6:12] + cat + '_orig.png', image)
                for ch in range(3):
                    image[:, :, ch] *= mask
                io.imsave('../figs/coco/' + img['file_name'][6:12] + cat + '_mask.png', image)
            
    
    
    
if __name__ == "__main__":
    category = load_category("./utils/category.json")
    main(category)
