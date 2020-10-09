import cv2
import numpy as np
from tensorflow.keras.models import load_model


class Finder:
    @staticmethod
    def sort_points(points):
        points = sorted(points, key=lambda x: x[1])
        up = points[:2]
        down = points[2:]
        if up[0][0] > up[1][0]:
            up[0], up[1] = up[1], up[0]
        if down[0][0] > down[1][0]:
            down[0], down[1] = down[1], down[0]
        return np.stack(up + down)

    def get_board(self, path, preview=False, debug=False):
        model = load_model('src/models/model_cus.h5')
        image = cv2.imread(path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (1, 1), 3)
        blur = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 11, 17)
        _, contours, _ = cv2.findContours(blur, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        max_contour = sorted(contours, key=cv2.contourArea)[-1]
        epsilon = 0.1 * cv2.arcLength(max_contour, closed=True)
        points = cv2.approxPolyDP(max_contour, epsilon, True)
        points = np.squeeze(points, axis=1)
        points = self.sort_points(points)
        points = np.array(points, np.float32)
        pnt2 = np.array([[0, 0], [252, 0], [0, 252], [252, 252]], np.float32)
        # kernel1 = np.ones((2, 2), np.uint8)
        # opening = cv2.dilate(blur, kernel1, iterations=1)
        matrix = cv2.getPerspectiveTransform(points, pnt2)
        result = cv2.warpPerspective(blur, matrix, (252, 252))

        # print(points)
        mask = np.zeros_like(gray)
        cv2.drawContours(mask, [max_contour], 0, (255, 255, 255), -1)
        mask[mask == 255] = gray[mask == 255]
        prediction = []
        result = result / 255.0
        for i in range(11):
            cv2.line(result, (i*28, 0), (i*28, 252), (0, 0, 0), 5)
        for i in range(11):
            cv2.line(result, (0, i*28), (252, i*28), (0, 0, 0), 5)
        for i in range(9):
            for j in range(9):
                prediction.append(result[i * 28:(i + 1) * 28, j * 28:(j + 1) * 28].reshape(28, 28, 1))
        prediction = np.stack(prediction)
        prediction = prediction.reshape(81, 28, 28, 1)
        prediction = list(model.predict_classes(prediction))
        find = [prediction[i*9:(i+1)*9] for i in range(9)]
        # print(prediction)
        if preview:
            cv2.imshow('gray', gray)
            cv2.imshow('blur', blur)
            cv2.imshow('result', result)
            cv2.imshow('mask', mask)
            # cv2.imshow('opening', opening)
            cv2.waitKey(0)
        if debug:
            correct = [8, 0, 0, 0, 1, 0, 0, 0, 9, 0, 5, 0, 8, 0, 7, 0, 1, 0, 0, 0, 4, 0, 9, 0, 7, 0, 0, 0, 6, 0, 7, 0,
                       1, 0, 2, 0, 5, 0, 8, 0, 6, 0, 1, 0, 7, 0, 1, 0, 5, 0, 2, 0, 9, 0, 0, 0, 7, 0, 4, 0, 6, 0, 0, 0,
                       8, 0, 3, 0, 9, 0, 4, 0, 3, 0, 0, 0, 5, 0, 0, 0, 8]
            count = 0
            for i in zip(correct, prediction):
                if i[0] != i[1]:
                    print(f'Predicted : {i[1]}, Correct : {i[0]}')
                    count += 1
            print(f'Number of errors is {count}')
        return find

