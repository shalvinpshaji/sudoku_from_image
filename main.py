import cv2
import numpy as np
from tensorflow.keras.models import load_model


class finder:

    @staticmethod
    def get():
        model = load_model('src/models/model_cus.h5')

        image = cv2.imread('images/2.png', 0)
        # image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        # cv2.imshow("Image", image)

        gray = image
        # cv2.imshow("gray", gray)

        blur = cv2.GaussianBlur(gray, (1, 1), 0)
        # cv2.imshow("blur", blur)

        thresh = cv2.adaptiveThreshold(blur, 255, 1, 1, 9, 2)
        # cv2.imshow("thresh", thresh)

        _, contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        max_area = 0
        c = 0
        for i in contours:
            area = cv2.contourArea(i)
            if area > 1000:
                if area > max_area:
                    max_area = area
                    best_cnt = i
                    image = cv2.drawContours(image, contours, c, (0, 255, 0), 3)
            c += 1

        mask = np.zeros(gray.shape, np.uint8)
        cv2.drawContours(mask, [best_cnt], 0, 255, -1)
        cv2.drawContours(mask, [best_cnt], 0, 0, 2)
        # cv2.imshow("mask", mask)

        out = np.zeros_like(gray)
        out[mask == 255] = gray[mask == 255]
        # cv2.imshow("New image", out)

        blur = cv2.GaussianBlur(out, (5, 5), 0)
        # cv2.imshow("blur1", blur)

        thresh = cv2.adaptiveThreshold(blur, 255, 1, 1, 11, 2)
        # cv2.imshow("thresh1", thresh)

        _, contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        c = 0
        for i in contours:
            area = cv2.contourArea(i)
            if area > 1000 / 2:
                cv2.drawContours(image, contours, c, (255, 255, 255), 3)
            c += 1
        image = (255 - image)
        # cv2.imshow("im", image)
        # cv2.waitKey(0)
        img = image
        img = img / 255.0
        l = []
        img = cv2.resize(img, (252, 252))
        img = img.reshape((252, 252, 1))
        for i in range(9):
            for j in range(9):
                l.append(img[i * 28:(i + 1) * 28, j * 28:(j + 1) * 28].reshape(28, 28, 1))
        l = np.stack(l)
        l = l.reshape(81, 28, 28, 1)
        pred = list(model.predict_classes(l))
        k = []
        for i in range(9):
            k.extend([pred[i * 9:(i + 1) * 9]])
        return k