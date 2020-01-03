这是一个视频浓缩的项目

但这个项目是在前人的工作上完成的， 请了解 https://github.com/Qidian213/deep_sort_yolov3
前辈们的 README.md 我更名为 SENIOR_README.md 这个文件仍然在项目目录下，我觉得你也很有必要去看看
这个文件

这个视频浓缩主要分为以下的几个步骤

1、多目标检测+跟踪，确定序号和轨迹
形成每个跟踪对象轨迹的索引
2、确定视频编辑的背景
3、检查跟踪轨迹的重合，避免多个对象在同一时刻出现在同一位置，造成重叠
4、形成一个新的索引，并依据这个索引生成视频浓缩

# 一些必要的准备工作
必要的库
opencv
TensorFlow 1.5 以下
以及一些其他的库
需要下载 yolo.h5 model, 将其放到 model_data 文件夹下
首先需要将 constant.py 里面的视频路径改成自己的


# 正式开始
第一步确定目标轨迹的索引，基本由前人的工作完成 
python demo
或者在 pycahrm 直接运行 demo.py
在 temp_file 文件夹下会生成 tracking.txt, 后面用到的是 tracking_result.txt 文件是指拿到完整的 tracking.txt 更名为 tracking_result.txt 即可

第二步生成视频背景
运行 get_background.py
觉得背景可以了，按下 q 退出
在 temp_file 文件夹下会生成 background.jpg

第三步生成新的索引我没有找到好的算法和方法，后面是我自己想的办法，处理方式比较粗糙，目标重合比较严重，详情可以见 some_message.txt
这里有两步
运行 read_frame.py
在 temp_file 文件夹下会生成 target.json, 相当于目标原来的轨迹索引了
在 targets_image 文件夹下会生成每个目标的在各个帧的裁剪图片

运行 get_new_index.py
在 temp_file 文件夹下会生成 new_index.json 文件，相当于新的索引了

第四步生成新的索引和视频
运行 get_video.py 生成最后的视频

联系方式：
201250397@qq.com
这是我的小号的 QQ 邮箱，可能会看到，也可能看不到

