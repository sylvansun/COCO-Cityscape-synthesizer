import numpy as np
import skimage.io as io

def show_label_max_class(img):
    img[img==255] = 0
    print(np.max(img))


if __name__ == '__main__':
    img = io.imread("../figs_demo/label_test.png")
    show_label_max_class(img)