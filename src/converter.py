from PIL import Image
import numpy
import matplotlib.pyplot as plt



class Converter():

    def __init__(self, raw_image):

        image = raw_image.convert("L")
        self.image_array = numpy.array(image, dtype=object)
        self.resized_image_array = numpy.zeros((28, 28))


    def split(self, img, rows, cols):

        cache = []
        try:
            img_r = img.shape[0]

            img_c = img.shape[1]
        except Exception as e:
            raise Exception(
                f'\nInform a \033[31mNumpy\033[37m array\n\n{str(e)}\n')

        for c, n in zip(range(0, img_r + 1, img_r // rows), range(img_r // rows, img_r + 1, img_r // rows)):
            for i, f in zip(range(0, img_c + 1, img_c // cols), range(img_c // cols, img_c + 1, img_r // cols)):
                cache.append(img[c:n, i:f])

        return cache


    def delete_extra_pixels(self):


        row_number = 0
        while self.image_array.shape[0] != 784:
            self.image_array = numpy.delete(self.image_array, row_number, 0)
            row_number += 1

        while self.image_array.shape[1] != 784:
            self.image_array = numpy.delete(self.image_array,0,1)



    def squeeze(self):

        for row in self.image_array:
            for pixel in row:
                if pixel==255:
                    pixel==0
                elif pixel==0:
                    pixel==1

        partitioned_array = self.split(self.image_array, 28, 28)
        sum = 0
        i_counter= 0
        j_counter= 0
        for i in range(28*28):
            for ibox in range(28):
                for jbox in range(28):
                    if(partitioned_array[i][ibox][jbox] == 0):
                        sum+=0.325255102

            self.resized_image_array[i_counter][j_counter] = sum
            sum = 0
            j_counter+=1
            if j_counter==28:
                i_counter += 1
                j_counter = 0


    def finalize(self):
        for r in range(28):
            for c in range(28):
                self.resized_image_array[r][c] = self.resized_image_array[r][c]/255
        self.resized_image_array = self.resized_image_array[numpy.newaxis, :, :]
        self.resized_image_array = self.resized_image_array.astype(numpy.float32)



    def draw(self):
        img = Image.fromarray(self.resized_image_array)
        figure = plt.figure(figsize =(4,4))
        plt.title("image")
        plt.axis("off")
        plt.imshow(img, cmap="gray")
        plt.show()


    def complete_convert(self):
        self.delete_extra_pixels()
        self.squeeze()
        #self.draw()
        self.finalize()
        return self.resized_image_array