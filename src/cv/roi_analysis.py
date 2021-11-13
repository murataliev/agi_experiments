import numpy as np

class RoiAnalysis:

    def while_quadrant(self, roi, p1, p2):
        dx_1 = roi[0] - p1[0]
        dy_1 = roi[1] - p1[1]
        dx_2 = roi[0] - p2[0]
        dy_2 = roi[1] - p2[1]

        if dx_1 + dx_2 == 1 or dy_1 + dy_2 == 1:
            return 5
        elif dx_1 > 0:
            if dy_1 > 0:
                return 1
            else:
                return 2
        elif dy_1 > 0:
            return 0
        else:
            return 3

    def get_mass(self, value):
        if value >= 0.4:
            return 2
        return 1

    def get_corner(self, p1, p2):
        if p1[1] > p2[1]:
            p1, p2 = p2, p1
        a = np.array([p2[0] - p1[0], p2[1] - p1[1]], dtype=np.float32)
        b = np.array([5, 0])
        return round((180 / np.arccos(-1)) * np.arccos(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))))

    def into_segment(self, list_x, list_y, p1, p2):
        x = p1[0]
        y = p2[0]

        if x > y:
            x, y = y, x

        res_x = []
        res_y = []
        res_x.append(x)

        for elem in list_x:
            if x < elem < y:
                res_x.append(elem)

        res_x.append(y)

        x = p1[1]
        y = p2[1]

        if x > y:
            x, y = y, x

        res_y.append(x)

        for elem in list_y:
            if x < elem < y:
                res_y.append(elem)

        res_y.append(y)
        return res_x, res_y

    def into_roi_square(self, points, x_left, x_right, y_bottom, y_top):
        return x_left <= points[0] <= x_right and y_bottom <= points[1] <= y_top

    def quadrant_roi_analysis(self, roi, approx_contour, quadrant_size):
        quadrant_norm = 1.42 * quadrant_size
        result = {}

        try:
            result['roi'] = roi.args
        except AttributeError:
            pass

        result['quadrants'] = [[], [], [], []]

        try:
            x_left = roi[0] - quadrant_size
            x_right = roi[0] + quadrant_size - 1
            y_top = roi[1] + quadrant_size - 1
            y_bottom = roi[1] - quadrant_size
            list_x = sorted([x_left, x_right, roi[0] - 1, roi[0]])
            list_y = sorted([y_bottom, y_top, roi[1] - 1, roi[1]])

            res = []

            a = list(approx_contour[0])
            approx_contour = list(approx_contour)
            approx_contour.append(a)

            for ind in range(1, len(approx_contour)):

                min_res = []
                p1_flag = self.into_roi_square(approx_contour[ind - 1], x_left, x_right, y_bottom, y_top)
                p2_flag = self.into_roi_square(approx_contour[ind], x_left, x_right, y_bottom, y_top)

                if p1_flag or p2_flag:
                    if p1_flag:
                        min_res.append(tuple(approx_contour[ind - 1]))
                    if p2_flag:
                        min_res.append(tuple(approx_contour[ind]))

                    approx_list_x, approx_list_y = self.into_segment(
                        list_x,
                        list_y,
                        approx_contour[ind - 1],
                        approx_contour[ind]
                    )

                    if approx_list_x[0] == approx_contour[ind][0]:
                        start_point = approx_contour[ind]
                        end_point = approx_contour[ind - 1]
                    else:
                        start_point = approx_contour[ind - 1]
                        end_point = approx_contour[ind]

                    for x in approx_list_x[1:-1]:
                        dx = x - start_point[0]
                        y = (dx / (end_point[0] - start_point[0])) * (end_point[1] - start_point[1]) + start_point[1]
                        min_res.append((x, round(y)))

                    for y in approx_list_y[1:-1]:
                        dy = y - start_point[1]
                        x = (dy / (end_point[1] - start_point[1])) * (end_point[0] - start_point[0]) + start_point[0]
                        min_res.append((round(x), y))

                    min_res.sort()
                    res.extend(min_res)
                    res.append(0)

            for ind in range(1, len(res)):
                if res[ind] == 0 or res[ind - 1] == 0:
                    continue

                quadrant_number = self.while_quadrant(roi, res[ind - 1], res[ind])

                if quadrant_number == 5:
                    continue

                if res[ind] == res[ind - 1]:
                    continue

                our_line = {}
                our_line['angle'] = self.get_corner(res[ind - 1], res[ind])
                our_line['mass'] = self.get_mass(np.linalg.norm(np.array([res[ind][0] - res[ind - 1][0],
                                                                          res[ind][1] - res[ind - 1][1]],
                                                                         dtype=np.float32)) / quadrant_norm)
                result['quadrants'][quadrant_number].append(our_line)
        except ValueError:
            pass
        return result
