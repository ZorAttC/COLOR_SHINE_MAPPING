import rospy
from sensor_msgs.msg import PointCloud2,PointField
from sensor_msgs import point_cloud2
from nav_msgs.msg import Odometry
import message_filters
import open3d as o3d
from open3d import io as o3d_io
import numpy as np
import os
from scipy.spatial.transform import Rotation
class KittiWriter:
    def __init__(self):
        self.pointcloud_data = None
        self.odometry_data = None
        self.sequence_number = 0

        # 创建时间同步器
        self.ts = message_filters.ApproximateTimeSynchronizer(
            [message_filters.Subscriber("/render_pts", PointCloud2),
             message_filters.Subscriber("/aft_mapped_to_init", Odometry)],
            queue_size=10,
            slop=0.1
        )
        self.ts.registerCallback(self.callback)
        print("KittiWriter init success.")

    def callback(self, pointcloud_msg, odometry_msg):
        pts = point_cloud2.read_points(pointcloud_msg, field_names=["x", "y", "z"], skip_nans=True)
        xyz_points=list(pts)
        pointcloud_msg.fields = [
            PointField(name="r", offset=16, datatype=PointField.UINT8, count=1),
            PointField(name="g", offset=17, datatype=PointField.UINT8, count=1),
            PointField(name="b", offset=18, datatype=PointField.UINT8, count=1),
        ]
        colors = point_cloud2.read_points(pointcloud_msg, field_names=["r", "g", "b"], skip_nans=True)
        colors=list(colors)

        q = odometry_msg.pose.pose.orientation
        dcm = Rotation.from_quat(np.array([q.x, q.y, q.z, q.w])).as_matrix() 
        trans = odometry_msg.pose.pose.position
        trans = np.array([trans.x, trans.y, trans.z])
        pose = np.eye(4)
        pose[:3, :3] = dcm
        pose[:3, 3] = trans
        #r3live的彩色点云是世界坐标系下的，需要转换到相机坐标系下
        xyz_points=(xyz_points-pose[:3,3])@ pose[:3,:3]
        cloud = o3d.geometry.PointCloud()
        cloud.points = o3d.utility.Vector3dVector(np.array(xyz_points).reshape(-1,3))
        cloud.colors = o3d.utility.Vector3dVector(np.array(colors).reshape(-1,3)/255)
        self.pointcloud_data = cloud
        self.odometry_data = pose
        self.save_kitti_format()

    def save_kitti_format(self):
        if self.pointcloud_data is not None and self.odometry_data is not None:
            
            pose=self.odometry_data
            kitti_pose=np.concatenate((pose[0,:4],pose[1,:4],pose[2,:4]))
            save_path="data/r3live_d/velodyne/"
            if  not os.path.exists(os.path.join(os.path.curdir,save_path)):
                os.makedirs(save_path)
            with open("data/r3live_d/poses.txt", 'a') as f:
                f.write(' '.join(map(str, kitti_pose)) + '\n')
            o3d_io.write_point_cloud(f"{save_path}{self.sequence_number:06d}.ply", self.pointcloud_data)

            self.sequence_number += 1

            rospy.loginfo("Kitti format saved successfully.")
        else:
            rospy.logwarn("PointCloud2 or Odometry data is missing.")

if __name__ == "__main__":
    rospy.init_node("kitti_converter")
    kitti_writer = KittiWriter()
    rospy.spin()