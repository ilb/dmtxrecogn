import cv2
import numpy as np
from pylibdmtx.pylibdmtx import decode
import os
from pdf2image import convert_from_path


class DatamatrixRecognizer:
    def __init__(self):
        self.resized_height = 2000
        self.resized_width = None
        self.zone_scale_x = 2
        self.zone_scale_y = 2
        self.timeout = 250
        self.count_x_segments = 3
        self.count_y_segments = 6

    @staticmethod
    def get_img_list(path):
        file_extension = os.path.splitext(path)[1]
        if file_extension == '.pdf':
            pages = convert_from_path(path)
            img_list = [np.array(page) for page in pages]
            return [cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) for img in img_list]
        else:
            return [cv2.imread(path, cv2.IMREAD_GRAYSCALE)]

    def contrast(self, img):
        img = cv2.convertScaleAbs(img, alpha=1, beta=5)
        _, img = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        return img;

    def img_preprocessing(self, img):
        img = self.erode(img)
        img = self.morphologyEx(img)
        return img

    def erode(self, img):
        _, thresholded = cv2.threshold(img, 200, 255, cv2.THRESH_BINARY)
        kernel = np.ones((3, 3), np.uint8)
        return cv2.erode(thresholded, kernel, iterations=1)

    def morphologyEx(self, img):
        kernel = np.ones((4, 4), np.uint8)
        img = cv2.bitwise_not(img)
        img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
        return cv2.bitwise_not(img)

    def resize_img(self, img):
        height, width = img.shape[:2]
        aspect_ratio = width / height
        self.resized_width = int(self.resized_height * aspect_ratio)
        return cv2.resize(img, (self.resized_width, self.resized_height))

    def crop_img(self, img, params):
        segment_height = self.resized_height / self.count_y_segments
        segment_width = self.resized_width / self.count_x_segments
        search_area_height = int(segment_height * self.zone_scale_y)
        search_area_width = int(segment_width * self.zone_scale_x)
        y = max(0, int(((params["segment"]["y"] - 1) * segment_height) - (
                (search_area_height - segment_height) / self.zone_scale_y)))
        x = max(0,
                int(((params["segment"]["x"] - 1) * segment_width) - (
                        (search_area_width - segment_width) / self.zone_scale_x)))
        crop_y = y + search_area_height
        crop_x = x + search_area_width
        return img[y:crop_y, x:crop_x]

    def get_dmtx_text(self, img):
        data = decode(img, timeout=self.timeout, max_count=1)
        if data:
            return [data[0].data.decode('utf-8')]
        else:
            return []

    def prepare_img1(self, img, params):
        img = self.resize_img(img)
        img = self.crop_img(img, params)
        img = self.contrast(img)
        img = self.img_preprocessing(img)
        return img

    def prepare_img2(self, img, params):
        img = self.crop_white(img)
        img = self.resize_img(img)
        img = self.crop_img(img, params)
        img = self.contrast(img)
        return img

    def prepare_img3(self, img, params):
        img = self.crop_white(img)
        img = self.resize_img(img)
        img = self.crop_img(img, params)
        return img

    def prepare_img4(self, img):
        return img

    def crop_white(self, img):
        height = img.shape[0]
        white_rows = np.all(img == 255, axis=1)[::-1]
        my_array = np.asarray(white_rows)
        count = 0
        for i in range(1, len(my_array)):
            if my_array[i]:
                count += 1
            else:
                break
        return img[0:(height - count), :]

    def process_img(self, img, params):
        prepared_img = self.prepare_img2(img, params)
        recognized_text = self.get_dmtx_text(prepared_img)
        if not len(recognized_text):
            prepared_img = self.prepare_img1(img, params)
            recognized_text = self.get_dmtx_text(prepared_img)
        if not len(recognized_text):
            prepared_img = self.prepare_img3(img, params)
            recognized_text = self.get_dmtx_text(prepared_img)
        if not len(recognized_text):
            prepared_img = self.prepare_img4(img)
            recognized_text = self.get_dmtx_text(prepared_img)
        return recognized_text

    def magick(self, path, params):
        img_list = self.get_img_list(path)
        result = {"pages": []}
        for img in img_list:
            recognized_text = self.process_img(img, params)
            result["pages"].append(recognized_text)
        return result
