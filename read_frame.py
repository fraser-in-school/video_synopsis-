from location import Location, Position
from target import Target
from constant import *
from PIL import Image

import cv2
import os
import operator
import json

target_set = set()
target_list = [None]*2000


class ReadFrame:
    def __init__(self, frame_string):
        # 读取帧号
        strs = frame_string.split('@')
        self.frame_index = int(strs[0].strip())

        # 得到(id, position) 的字符数组，并去掉跟踪目标计数[0]
        self.targets = strs[1].split('$')
        self.targets = self.targets[1:]

    def get_targets(self):
        # 得到这一帧的 target, 并加入到 target_list 中
        for target in self.targets:
            # 去掉空字符串和回车字符串
            li = [integer for integer in target.split(' ') if integer and integer != '\n']

            # 第一个整数为ID，后面的四元组为左上和右下坐标
            id = int(li[0])
            position = Position(li[1:])

            # id 已经在集合中出现，则不用创建对象，只需要 add_frame
            if id in target_set:
                target_list[id].add_frame(frame_index=self.frame_index, position=position)
            # id 没有出现，则将 id 加入集合作为标记，创建对象，并 add_frame
            else:
                target_set.add(id)
                target_list[id] = Target(id, first_frame=self.frame_index)
                target_list[id].add_frame(frame_index=self.frame_index, position=position)


def get_targets_image(lines):
    # 打开原视频
    video_capture = cv2.VideoCapture(VIDEO_PATH)
    frame_index = 0
    while True:
        if frame_index % 10 == 0:
            print(frame_index)

        # 读取新的一帧
        ret, frame = video_capture.read()
        if not ret:
            break

        # 读取新的一行
        line = lines[frame_index]
        locations_str = line.split('$')[1:]
        for loc_str in locations_str:
            quintuples = [integer for integer in loc_str.split(' ') if integer and integer != '\n']
            target_id = int(quintuples[0])
            temp_position = Position(quintuples[1:])
            temp_location = Location(frame_index, temp_position)
            bigger_tuple = temp_position.get_bigger_tuple()
            dst = frame[bigger_tuple[1]:bigger_tuple[3], bigger_tuple[0]:bigger_tuple[2]]

            folder_name = './targets_image/target_' + str(target_id)
            img_name = folder_name + '/' + str(frame_index) + '-' + str(temp_position.top_left_x) + '-' + str(temp_position.top_left_y) \
                       + '-' + str(temp_position.bottom_right_x) + '-' + str(temp_position.bottom_right_y) + '.jpg'

            if not os.path.exists(folder_name):
                os.makedirs(folder_name)
            print(img_name)
            cv2.imwrite(img_name, dst)

            # Press Q to stop!
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        # print(quintuples)

        frame_index += 1
        # cv2.imshow('frame', frame)
        # cv2.waitKey(5)


def test():
    # Frame('0 @7 $ 1 827 637 877 771 $ 2 129 572 201 696 $ 3 571 637 646 792 $ 4 0 540 34 637 $ 5 1093 488 1129 579 $ 6 604 623 667 776 $ 7 791 504 823 565')
    frame_txt = open('./temp_file/tracking_result.txt')
    frame_index = 1
    lines = []
    for frame_line in frame_txt:
        frame = ReadFrame(frame_line)
        lines.append(frame_line)
        frame.get_targets()

    print('begin!')
    # 下面一句代码用来生成独立的 target 小图片
    get_targets_image(lines)
    # 生成 JSON 文件
    targets_json = open('./temp_file/targets.json', 'w')
    targets_json.write(json.dumps(target_list, default=lambda obj: obj.__dict__, sort_keys=True, indent=4))

    '''
    # 此部分代码用来求取目标框的平均宽度和高度
    positions = []
    for target in target_list:
        if target:
            for loc in target.locations:
                positions.append(loc.position)
    ave_width = 0;
    ave_height = 0;
    for position in positions:
        ave_width += position.get_width()
        ave_height += position.get_height()

    ave_width = ave_width / len(positions)
    ave_height = ave_height / len(positions)

    print(ave_width, ave_height)
    '''

test()