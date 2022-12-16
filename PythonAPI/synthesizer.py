from pycocotools.coco import COCO
import numpy as np
import skimage.io as io
from utils.ood_category import load_category

def get_city_filename(index):
    imagename = "zurich_{}_000019_leftImg8bit.png".format(format(index, "06d"))
    labelname = "zurich_{}_000019_gtFine_labelTrainIds.png".format(format(index, "06d"))
    name_dict = {"image":imagename, "label":labelname}
    return name_dict

def get_citycut_filename(index,pos):
    imagename = "zurich_{}_{}_000019_leftImg8bit.png".format(format(index, "06d"),pos)
    labelname = "zurich_{}_{}_000019_gtFine_labelTrainIds.png".format(format(index, "06d"),pos)
    name_dict = {"image":imagename, "label":labelname}
    return name_dict

def load_city_pair(index):
    name_dict = get_city_filename(index)
    image = io.imread("../figs/zurich/image/{}".format(name_dict["image"]))
    label = io.imread("../figs/zurich/label/{}".format(name_dict["label"]))
    return image,label

def save_city_pair(index, image, label):
    name_dict = get_city_filename(index)
    io.imsave("../figs/zurich/image_syn/{}".format(name_dict["image"]), image)
    io.imsave("../figs/zurich/label_syn/{}".format(name_dict["label"]), label)
    
def save_citycut_pair(index, pos, image, label):
    name_dict = get_citycut_filename(index,pos)
    io.imsave("../figs/zurich/image_cut/{}".format(name_dict["image"]), image)
    io.imsave("../figs/zurich/label_cut/{}".format(name_dict["label"]), label)

def main(cats, num_each_cat=10, num_cityscape_img=100, ood_id=254, crop_size=480):
    dataDir = '..'
    dataType = 'val2017'
    annFile = '{}/annotations/instances_{}.json'.format(dataDir, dataType)

    coco = COCO(annFile)
    cityscape_count = 0
    for cat in cats:
        print(cat)
        catIds = coco.getCatIds(catNms=[cat])
        imgIds = coco.getImgIds(catIds=catIds)
        img_count = idx = 0
        while img_count < num_each_cat:
            img = coco.loadImgs(imgIds[idx])[0]
            idx += 1
            image = io.imread('%s/%s/%s' % (dataDir, dataType, img['file_name']))
            annIds = coco.getAnnIds(imgIds=img['id'], catIds=catIds, iscrowd=None)
            anns = coco.loadAnns(annIds)
            mask = coco.polygon_extract(anns, image.shape[0], image.shape[1])
            if mask is None:
                continue
            else:
                H,W = image.shape[0], image.shape[1]
                mask_city = np.ones((1024,2048)).astype(np.uint8)
                unmask = np.ones(mask.shape) - mask
                
                Hpos, Wpos = np.random.randint(970,1024), np.random.randint(1000,2048)
                mask_city[Hpos-H:Hpos,Wpos-W:Wpos] = unmask
                
                city,label = load_city_pair(cityscape_count % num_cityscape_img)
                
                cityscape_count += 1
                img_count += 1

                for ch in range(3):
                    image[:, :, ch] *= mask
                    city[:, :, ch] *= mask_city
                label *= mask_city
                city[Hpos-H:Hpos,Wpos-W:Wpos,:] += image
                label[Hpos-H:Hpos,Wpos-W:Wpos] += (ood_id * mask).astype(np.uint8)
                save_city_pair(cityscape_count, city, label)
                cutted_img_labels = []
                cutted_img_labels.append((city[Hpos-720:Hpos-240,Wpos-720:Wpos-240,:], label[Hpos-720:Hpos-240,Wpos-720:Wpos-240]))
                cutted_img_labels.append((city[Hpos-2*crop_size:Hpos-crop_size,Wpos-2*crop_size:Wpos-crop_size,:], label[Hpos-2*crop_size:Hpos-crop_size,Wpos-2*crop_size:Wpos-crop_size]))
                cutted_img_labels.append((city[Hpos-2*crop_size:Hpos-crop_size,Wpos-crop_size:Wpos,:], label[Hpos-2*crop_size:Hpos-crop_size,Wpos-crop_size:Wpos]))
                cutted_img_labels.append((city[Hpos-crop_size:Hpos,Wpos-2*crop_size:Wpos-crop_size,:], label[Hpos-crop_size:Hpos,Wpos-2*crop_size:Wpos-crop_size]))
                cutted_img_labels.append((city[Hpos-crop_size:Hpos,Wpos-crop_size:Wpos,:], label[Hpos-crop_size:Hpos,Wpos-crop_size:Wpos]))
                for i in range(5):
                    save_citycut_pair(cityscape_count, i + 1, cutted_img_labels[i][0], cutted_img_labels[i][1])
 
if __name__ == "__main__":
    category = load_category("./utils/category.json")
    main(category)
    