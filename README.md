# RigifyToUnity
Converts Rigify rig to Humanoid compatible  

**_Installation:_** 
- Download this repo as zip archive
- In Blender Open Edit tab -> Preferences... -> Add-ons -> Instal... -> choose the downloaded zip archive
- You can find the Addon under Rigging category, there should be "Rigify to Unity" addon

**_Usage:_** 
1) Create Basic Human Rig
2) Press "Generate Rig" from Rigify tab
3) Make sure newly generated rig is selected (named just "rig")
4) Press "Prepare rig for unity" from Rigify to Unity converter tab
> :warning: Do it before weight painting as some deform bones will be removed
5) Do something cool!
6) p.s. Check "Only Deform Bones" when exporting to exclude unnecessary bones from fbx

![Before and after](https://github.com/AlexLemminG/RigifyToUnity/raw/master/HowTo/6%20-%20diff.png)
This script basicaly follows this tutorial  
https://docs.unity3d.com/560/Documentation/Manual/BlenderAndRigify.html

Script inspired by legacy https://github.com/trynyty/Rigify_DeformBones  
