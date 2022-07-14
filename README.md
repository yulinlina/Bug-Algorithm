# Bug algorithm in ROS 
## 演示
[如何使用Gazebo实现Bug](https://www.bilibili.com/video/BV15a411n7ju?vd_source=77f197efc9e66a13ad8a2235a6cb34be)
## 效果图
![image](https://user-images.githubusercontent.com/77262518/178882651-fd6176b0-b127-4f8f-8a67-7f04f4cbe699.png)  
![image](https://user-images.githubusercontent.com/77262518/178882608-e91fe28f-54de-48db-9df5-11ea884a5cf3.png)  
![image](https://user-images.githubusercontent.com/77262518/178882686-daca6889-e1c7-485f-b382-2434b86590cf.png)

## Requirement  
***pakename*** `wk2Assignment_3`
*  launch folder: contains launch files
*  scripts folder: contains your python code
* urdf folder: contains the model files describing your robot
* srv folder: contains your custom ROS services 
* CMakeLists.txt: list of cmake rules for compilation
* Package.xml: Package information and dependencies
## Usage
use the command `roslaunch wk2Assignment wk2Assignment.launch`  
then type the number of the bug algorithm you want to use  
0: bug0  
1: bug1  
2: bug2  
### 1. Urdf xacro.py  
The tutorials can be found in [here](https://www.yuque.com/yulinlin-rf5a0/qfbvb9/xyctsx#E6cgE)  
The topic used: 
laser : `/wk2Bot3/laser/scan`
cmd_vel: `wk2Bot3/cmd_vel`
odom:  `odom` 
### 2. Service.py
1.  Service HomingSignal.srv: 指定docking station，面对的朝向 发出信息"My wk2Bot reaches the charging station located at (xx, xx)"   
2.  SetBugBehaviour.srv: 指定机器人移动速度  
## 3. Bug1,Bug2 and Client.py  
name : `Bug1.py`  
name : `Bug2.py`   
client.py : 实现选择算法bug1或bug2，
在bug12中判断传的req是否为true再决定要不要调用  
##  4.GoToPoint.py and followWall.py
go_to_point_switch和wall_follower_switch改srv的类型  
## 5.wk2AssignmentWorld.world
建世界,bug1 algorithm is better than Bug2 algorithm
