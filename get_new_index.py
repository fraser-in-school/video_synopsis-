# -*- coding: utf-8 -*-
# @Time    : 2020/1/1 18:29
# @Author  : zhanghao
# @FileName: get_new_index
# @Software: PyCharm

from location import NewLocation, Position
from target import Target, NewTarget


import json


# a function that detect collision
def collision_detect(location1, location2):
    x1, y1 = location1.get_centeroid()
    x2, y2 = location2.get_centeroid()
    if abs(x1 - x2) <= 145 and abs(y1 - y2) <= 300:
        return True
    return False


class NewFrame:
    def __init__(self, frame_index):
        self.new_frame_index = frame_index
        self.locations = []
        self.locations_account = 0

    def add_new_location(self, new_location):
        self.locations.append(new_location)
        self.locations_account += 1

    def collision_detect(self, new_location):
        for location in self.locations:
            if collision_detect(location, new_location):
                return True
        return False


def create():
    json_file = open('./temp_file/targets.json', 'r')
    target_list = json.load(json_file)
    list_without_None = list(filter(None, target_list))
    video_index = [None] * 9000
    new_target_list = []

    # frame_num 原来是 frame_index, 与前面保持一致， 表示的帧号
    # 但为了不与 video_index 产生奇怪的联系，更名为 frame_num
    frame_num = 0

    # account 是所有未找到新的第一帧的 target 计数
    account = len(list_without_None)

    # 将所有 target 换成新的 NewTarget
    for target_dict in list_without_None:
        target_obj = Target().json2obj(target_json=target_dict)
        new_target = NewTarget(target_obj)
        new_target_list.append(new_target)

    while account > 0:
        new_frame = NewFrame(frame_num)
        video_index[frame_num] = new_frame

        print(frame_num)
        # 第一遍遍历找到所有帧号等于 frame_num 的 target
        for new_target in new_target_list:
            if not new_target.flag and new_target.target.first_frame == frame_num:
                # 需要做三件事
                # 1. 将 new_target 的 first_frame 设置好
                # 2. 将 这个 new_location 要放入 new_frame 中
                # 3. account-1
                new_target.set_first_frame(frame_num)

                # 因为 new_first_frame = （原来的 target）first_frame
                new_location = NewLocation(origin_frame=frame_num, position=new_target.target.locations[0].position, target_id=new_target.target.id)
                video_index[frame_num].add_new_location(new_location)
                account -= 1

        # 第二遍遍历找到在后面时刻的 target，但不会引发冲突的
        for new_target in new_target_list:
            if not new_target.flag:
                temp_location = NewLocation(origin_frame=new_target.target.first_frame,
                                            position=new_target.target.locations[0].position, target_id=new_target.target.id)
                if not video_index[frame_num].collision_detect(temp_location):
                    # 也是三件事
                    new_target.set_first_frame(frame_num)
                    video_index[frame_num].add_new_location(temp_location)
                    account -= 1

        frame_num += 1

    """
    # 检验性工作，查看每个目标的新的第一帧的帧号
    for new_target in new_target_list:
        print(new_target.new_first_frame)
    """

    # 前面的工作已经使得所有目标获得了新的第一帧的帧号
    # 接下来是对每个目标的 trajectory[i] - (new_first_frame - first_frame)
    # 变成新的 trajectory
    for new_target in new_target_list:
        # step 为步数差， new_first_frame >= first_frame
        step = new_target.target.first_frame - new_target.new_first_frame
        for loc in new_target.target.locations:
            temp_loc = NewLocation(origin_frame=loc.frame_index, position=loc.position, target_id=new_target.target.id)
            new_frame_num = loc.frame_index - step

            # 判断是否为空
            if not video_index[new_frame_num]:
                new_frame = NewFrame(frame_index=new_frame_num)
                video_index[new_frame_num] = new_frame

            video_index[new_frame_num].add_new_location(temp_loc)

    video_index = list(filter(None, video_index))
    # 冲突计数
    for frame in video_index:
        for i in range(0, len(frame.locations)):
            for j in range(i + 1, len(frame.locations)):
                if collision_detect(frame.locations[i], frame.locations[j]):
                    frame.locations[i].add_recorder()
                    frame.locations[j].add_recorder()

    new_index_txt = open('./temp_file/new_index.json', 'w')
    new_index_txt.write(json.dumps(video_index, default=lambda obj: obj.__dict__, sort_keys=True, indent=4))

create()