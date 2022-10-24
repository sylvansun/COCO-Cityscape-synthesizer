from pycocotools.coco import COCO
import numpy as np
import skimage.io as io
import matplotlib.pyplot as plt
import pylab
import cv2

pylab.rcParams['figure.figsize'] = (8.0, 10.0)

dataDir = '..'
dataType = 'val2017'
annFile = '{}/annotations/instances_{}.json'.format(dataDir, dataType)

# initialize COCO api for instance annotations
coco = COCO(annFile)

# learning COCO api for categories
cats = coco.loadCats(coco.getCatIds())

# display COCO categories and super categories
nms = [cat['name'] for cat in cats]
print('COCO categories: \n{}\n'.format(' '.join(nms)))
print(type(nms))
print(nms[1])

nms = set([cat['supercategory'] for cat in cats])
print('COCO super categories: \n{}'.format(' '.join(nms)))

# get all images containing given categories, select one at random
catIds = coco.getCatIds(catNms=['dog'])
print('catIDS:', catIds)
imgIds = coco.getImgIds(catIds=catIds)
print('imgIDS:', imgIds)
imgIds = coco.getImgIds(imgIds=[549220])
print('imgIDS:', imgIds)
img = coco.loadImgs(imgIds[np.random.randint(0, len(imgIds))])[0]

# load and display image
image = io.imread('%s/%s/%s'%(dataDir, dataType, img['file_name']))
# image_another = cv2.imread(dataDir + '/' + dataType + '/' + img['file_name'], cv2.IMREAD_COLOR)
# print("test of various reading methods", image == image_another)
# use url to load image
# image = io.imread(img['coco_url'])
# print("skimage.io.imread datatype: ", type(image))
# print(image.shape)
io.imsave('../figs_demo/' + img['file_name'][6:12] + '_original.png', image)

# load and display instance annotations
annIds = coco.getAnnIds(imgIds=img['id'], catIds=catIds, iscrowd=None)
anns = coco.loadAnns(annIds)
# for elem in anns:
#     print(type(elem))
#     print(elem.keys())
#     print(elem['area'])
#     print('category: ', elem['category_id'])
#     print('image: ', elem['image_id'])
#     print(elem['bbox'])
#     print(elem['id'])
mask = coco.polygon_extract(anns, image.shape[0], image.shape[1])
for ch in range(3):
    image[:, :, ch] *= mask
io.imsave('../figs_demo/' + img['file_name'][6:12] + '_masked.png', image)
