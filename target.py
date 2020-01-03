# -*- coding: utf-8 -*-
# @Time    : 2020/1/1 18:29
# @Author  : zhanghao
# @FileName: target.py
# @Software: PyCharm

from location import Location, NewLocation, Position


# Target is a class that represent a person
# @id unique identity for everyone
# @frame_length is the total number of frames this person appears
# @locations is the list of locations, location has two attribute, frame_index and position
# @trajectory is the trajectory of the target, so it only frame number information of the target
class Target:
    def __init__(self, id=-1, first_frame=-1):
        self.id = id
        self.frame_length = 0
        self.locations = []
        self.trajectory = []
        self.first_frame = first_frame

    def json2obj(self, target_json):
        id = target_json['id']
        frame_length = target_json['frame_length']
        trajectory = target_json['trajectory']
        first_frame = target_json['first_frame']
        locations = []
        for loc in target_json['locations']:
            frame_index = loc['frame_index']
            position = Position().json2obj(loc['position'])
            location = Location(frame_index, position)
            locations.append(location)

        temp_target = Target(id, first_frame)
        temp_target.set_frame_length(frame_length)
        temp_target.set_locations(locations)
        temp_target.set_trajectory(trajectory)
        return temp_target

    def add_frame(self, frame_index, position):
        location = Location(frame_index, position)
        self.frame_length += 1
        self.trajectory.append(frame_index)
        self.locations.append(location)

    def set_frame_length(self, frame_length):
        self.frame_length = frame_length

    def get_frame_length(self):
        return self.frame_length

    def set_trajectory(self, trajectory):
        self.trajectory = trajectory

    def get_trajectory(self):
        return self.trajectory

    def set_locations(self, locations):
        self.locations = locations

class NewTarget:
    def __init__(self, target, new_first_frame=-1, confirm=False):
        self.target = target
        self.new_first_frame = new_first_frame
        self.flag = confirm

    def set_first_frame(self, new_first_frame):
        self.new_first_frame = new_first_frame
        self.flag = True

    def confirm(self):
        self.flag = True
