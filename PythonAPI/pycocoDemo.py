from pycocotools.coco import COCO
import numpy as np
import skimage.io as io
import matplotlib.pyplot as plt
import pylab
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
catIds = coco.getCatIds(catNms=['person', 'dog', 'skateboard'])
print(catIds)
imgIds = coco.getImgIds(catIds=catIds)
print(imgIds)
imgIds = coco.getImgIds(imgIds=[549220])
print(imgIds)
img = coco.loadImgs(imgIds[np.random.randint(0, len(imgIds))])[0]

# load and display image
# I = io.imread('%s/images/%s/%s'%(dataDir,dataType,img['file_name']))
# use url to load image
I = io.imread(img['coco_url'])
# plt.axis('off')
plt.imshow(I)
plt.savefig('./demo.png')
plt.show()


# load and display instance annotations
# annIds = coco.getAnnIds(imgIds=img['id'], catIds=catIds, iscrowd=None)
# anns = coco.loadAnns(annIds)
# print(type(anns))
# print(len(anns))
# for elem in anns:
#     print(type(elem))
#     print(elem.keys())
#     print(elem['area'])
#     print('category: ', elem['category_id'])
#     print('image: ', elem['image_id'])
#     print(elem['bbox'])
#     print(elem['id'])
# coco.showAnns(anns)

