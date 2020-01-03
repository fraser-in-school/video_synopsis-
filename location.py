# -*- coding: utf-8 -*-
# @Time    : 2020/1/1 18:29
# @Author  : zhanghao
# @FileName: location.py
# @Software: PyCharm

# 设置视频的宽度和高度
video_width = 1920
video_height = 1080


class Location:
    def __init__(self, frame_index, position):
        self.frame_index = frame_index
        self.position = position
        self.center_x, self.center_y = self.position.get_centroid()

    def get_centeroid(self):
        return self.center_x, self.center_y


# New_location is used to create new index
# 本来使用继承，但 python 继承太日了，不如重新写新类
class NewLocation:
    def __init__(self, origin_frame=-1, position=None, target_id=-1):
        self.origin_frame = origin_frame
        self.position = position
        self.recorder = 0
        self.target_id = target_id
        self.center_x, self.center_y = -1, -1

    # 本来是想重载构造函数的，但 python 不支持函数重载，只会认最后一个构造函数
    # 前面的构造函数是在生成 json 文件前使用的，下面的构造函数主要是用来读 json 的
    # python 读取 json 文件获取到的也是 dict 对象， 可以通过 dict['key'] 来使用
    # 但这不够所以重写读为类（其实是类似JS的函数）对象
    # 有个解决办法是上面的构造函数都设置 -1 的默认参数
    # 要读 json 时， NewLocation().under_function(loc_json)
    # def __init__(self, loc_json):
    def json2obj(self, loc_json):
        temp_recorder = loc_json['recorder']
        temp_position = Position().json2obj(position_json=loc_json['position'])
        temp_origin_frame = loc_json['origin_frame']
        temp_target_id = loc_json['target_id']

        # 构造函数是有返回值的，就是新对象本身，我们这里想实现类似构造函数的功能
        temp_new_location = NewLocation(origin_frame=temp_origin_frame, position=temp_position, target_id=temp_target_id)
        temp_new_location.recorder = temp_recorder
        return temp_new_location


    def add_recorder(self):
        self.recorder += 1

    def get_centeroid(self):
        self.center_x, self.center_y = self.position.get_centroid()
        return self.center_x, self.center_y

    # 因为截取图片是多截了 20%， 所以 poisson 融合相应的坐标要稍作变更
    def get_bigger_centeroid(self):
        # 考虑到边界，所以直接生成图片真正的坐标
        # 然后求 center
        x1, y1, x2, y2 = self.position.get_bigger_tuple()
        return (x1 + x2) // 2, (y1 + y2) // 2

    # 获取在 targets_image 文件夹下对应文件名
    def get_file_name(self):
        path = './targets_image/target_' + str(self.target_id)
        file_name = path + '/' + str(self.origin_frame) + '-' + str(self.position.top_left_x) + '-' + \
                    str(self.position.top_left_y) + '-' + str(self.position.bottom_right_x) + '-' \
                    + str(self.position.bottom_right_y) + '.jpg'
        return file_name


class Position:
    def __init__(self, str_list=['0', '0', '0', '0']):
        if len(str_list) != 4:
            print('the position is not legal')
            print(str_list)
        self.top_left_x = int(str_list[0])
        self.top_left_y = int(str_list[1])
        self.bottom_right_x = int(str_list[2])
        self.bottom_right_y = int(str_list[3])
        self.center = self.get_centroid()

    def set_tuple(self, x1, y1, x2, y2):
        self.top_left_x = x1
        self.top_left_y = y1
        self.bottom_right_x = x2
        self.bottom_right_y = y2

    def json2obj(self, position_json):
        top_left_x = position_json['top_left_x']
        top_left_y = position_json['top_left_y']
        bottom_right_x = position_json['bottom_right_x']
        bottom_right_y = position_json['bottom_right_y']
        temp_position = Position()
        temp_position.set_tuple(top_left_x, top_left_y, bottom_right_x, bottom_right_y)
        temp_position.center = temp_position.get_centroid()
        return temp_position

    def get_tuple(self):
        return self.top_left_x, self.top_left_y, self.bottom_right_x, self.bottom_right_y

    def get_centroid(self):
        return (self.top_left_x + self.bottom_right_x) // 2, (self.top_left_y + self.bottom_right_y) // 2

    def get_width(self):
        return self.bottom_right_x - self.top_left_x

    def get_height(self):
        return self.bottom_right_y - self.top_left_y

    def get_wh(self):
        return self.bottom_right_x - self.top_left_x, self.bottom_right_y - self.top_left_y

    def get_tlwh(self):
        return self.top_left_x, self.top_left_y, self.bottom_right_x - self.top_left_x, self.bottom_right_y - self.top_left_y

    # 获取更大的框， 注意越界问题
    # 6，12 这两个数值详情见 some_message.txt
    def get_bigger_tuple(self):
        x1 = self.top_left_x - 6
        y1 = self.top_left_y - 12
        x2 = self.bottom_right_x + 6
        y2 = self.bottom_right_y + 12
        if x1 < 0:
            x1 = 0
        if y1 < 0:
            y1 = 0
        if x2 >= video_width:
            x2 = video_width - 1
        if y2 >= video_height:
            y2 = video_height -1
        return x1, y1, x2, y2

    def get_bigger_tlwh(self):
        x1 = self.top_left_x - 6
        y1 = self.top_left_y - 12
        x2 = self.bottom_right_x + 6
        y2 = self.bottom_right_y + 12
        if x1 < 0:
            x1 = 0
        if y1 < 0:
            y1 = 0
        if x2 >= video_width:
            x2 = video_width - 1
        if y2 >= video_height:
            y2 = video_height -1
        return x1, y1, x2 - x1, y2 - y1