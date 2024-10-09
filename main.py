#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import sys
import numpy as np
import moveit_commander
from visualization_msgs.msg import Marker, MarkerArray
from geometry_msgs.msg import Point, Pose

def visualize_reachable_positions():
    rospy.init_node('visualize_reachable_positions')
    moveit_commander.roscpp_initialize(sys.argv)
    
    arm_group = moveit_commander.MoveGroupCommander("arm")
    arm_group.set_planning_time(1.0) 
    marker_pub = rospy.Publisher('reachable_positions', MarkerArray, queue_size=10)
    
    marker_array = MarkerArray()
    marker = Marker()
    marker.header.frame_id = "arm_base_link" #替换为机械臂基坐标系
    marker.type = marker.SPHERE_LIST
    marker.action = marker.ADD
    marker.scale.x = 0.01
    marker.scale.y = 0.01
    marker.scale.z = 0.01
    marker.color.a = 1.0
    marker.color.r = 0.0
    marker.color.g = 1.0
    marker.color.b = 0.0

    # 打开文件，准备写入
    with open("points.txt", "a") as f:
        # 定义目标姿态，注释部分为固定末端姿态
        pose_target = Pose()
        # pose_target.orientation.x = -0.000451616880183
        # pose_target.orientation.y = 0.7175795226
        # pose_target.orientation.z = 0.00635486614268
        # pose_target.orientation.w = 0.696447442714

        # 遍历位置
        step_size = 0.02
        for x in np.arange(0, 0.5, step_size):
            for y in np.arange(-0.3, 0.3, step_size):
                for z in np.arange(-0.3, 0.3, step_size):
                    pose_target.position.x = x
                    pose_target.position.y = y
                    pose_target.position.z = z

                    # 计算可达性，而不执行
                    waypoints = [pose_target]
                    (plan, fraction) = arm_group.compute_cartesian_path(waypoints, 0.01, 0)  # 计算路径

                    if fraction == 1.0:  # 如果路径的比例为1.0，说明可达
                        point = Point()
                        point.x, point.y, point.z = (x, y, z)
                        marker.points.append(point)
                        f.write("{} {} {}\n".format(x, y, z))
                        f.flush()  # 刷新文件内容
                        print("Reachable point: (%f, %f, %f)" % (x, y, z))
                    else:
                        print("Unreachable point: (%f, %f, %f)" % (x, y, z))

    marker_pub.publish(marker_array)  # 在循环结束后发布所有 Marker

    moveit_commander.roscpp_shutdown()

if __name__ == "__main__":
    visualize_reachable_positions()
