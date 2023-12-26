## Color-SHINE-MAPPING

It is an implementation to use MLP decoder to regress the color value using the same structure as the sdf regression in [SHINE_MAPPING](https://github.com/PRBonn/SHINE_mapping/issues/24).For the colored point cloud,I use [R3LIVE](https://github.com/hku-mars/r3live/) to obtain colored point cloud and the sensor pose.And I record rosbag and play it to a script to convert it to kitti format.

### Usage

1. Run the r3live to obtain the colored point cloud and the sensor pose.If you haven't install r3live,you can download this rosbag and try it first.[rosbag data](https://drive.google.com/file/d/1CccP_ii59UB_HPr5pQj-noFEpS86zUe7/view?usp=drive_link)
  
2. Run the script to convert the rosbag to kitti format.
   ```
   python dataset/colorpoints_to kitti_format.py
   ```

3. Modify your dataset path in color_incre_reg.yaml in the  config directory. And run the shine_incre.py,since the batch is not implemented yet.
   ```
   python shine_incre.py config config/color_incre_reg.yaml
   ```

### Result 

