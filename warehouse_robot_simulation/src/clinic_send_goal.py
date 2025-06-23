#!/usr/bin/env python3
import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import tf

WAYPOINTS = {
    "Storage": (-7.0, -7.0, 0.0),
    "Room1": (-7.0, 7.0, 0.0),
    "Room2": (-7.0, 2.0, 0.0),
    "Room3": (-7.0, -2.0, 0.0),
    "Room4": (1.5, -1.5, 0.0),
    "Room5": (6.0, -1.5, 0.0),
    "Room6": (6.0, -7.6, 0.0),
    "Room7": (1.5, -7.6, 0.0),
}

def send_goal(name):
    if name not in WAYPOINTS:
        rospy.logerr(f"No waypoint named '{name}'. Valid: {list(WAYPOINTS)}")
        return False

    x, y, yaw = WAYPOINTS[name]
    quaternion = tf.transformations.quaternion_from_euler(0, 0, yaw)

    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()
    goal.target_pose.pose.position.x = x
    goal.target_pose.pose.position.y = y
    goal.target_pose.pose.orientation.x = quaternion[0]
    goal.target_pose.pose.orientation.y = quaternion[1]
    goal.target_pose.pose.orientation.z = quaternion[2]
    goal.target_pose.pose.orientation.w = quaternion[3]

    client = actionlib.SimpleActionClient("move_base", MoveBaseAction)
    rospy.loginfo("Waiting for move_base server...")
    if not client.wait_for_server(timeout=rospy.Duration(10)):
        rospy.logerr("move_base server not available!")
        return False

    client.send_goal(goal)
    rospy.loginfo(f"Sent goal: {name} -> {x:.2f}, {y:.2f}, yaw {yaw:.2f}")
    client.wait_for_result()
    result = client.get_state()
    rospy.loginfo(f"Goal result: {result}")
    return result == actionlib.GoalStatus.SUCCEEDED

if __name__ == "__main__":
    rospy.init_node("send_goal_by_name")
    rate = rospy.Rate(0.5)
    rospy.loginfo("Goal sender ready. Type location names to send goals.")
    while not rospy.is_shutdown():
        name = input("Enter location name (or 'list'): ")
        if name == "list":
            print("Available:", ", ".join(WAYPOINTS.keys()))
            continue
        send_goal(name)
        rate.sleep()

