
## Auto Image Annotation Tool

The pre-trained inception model (Open Image Dataset V4) is used in annotating each one second frame of the video.

When docker is running, put the input videos in ```/data/video```.

The result for each video will be saved separatly in ```/inception/output``` with the csv names same as csv names.


### steps 
1. docker build and run 
```
docker build -t yyyyteng/inception_ffmpeg .
docker run docker_run.sh
```
2. run annotation job on the example video, mountain_lake.MOV, in ```/inception/data/video```
```
bash start.sh
```
4. all the one second frames will be extracted and saved in ```/inception/data/video_frames``` 

5. annotation result will be saved under ```/inception/output``` in a csv with the same name as that of the input video



### this tool can also be used on images directly.
1. put the input images in one folder under video_frames and run the following
```
python classify_folder.py /inception/data/video_frames/input_imgs
```

2. annotation result for each image will be saved in a csv called input_imgs.csv under  ```/inception/output``` 


### example result 
the following frame 

<img src="https://github.com/yueying-teng/auto_image_annotation_tool/blob/master/data/video_frames/mountain_lake/mountain_lake007.jpg" height="300">

has the following labls 
```
3353: /m/04h4w - lake (score = 0.85)
4648: /m/09d_r - mountain (score = 0.79)
3745: /m/05h0n - nature (score = 0.78)
3450: /m/04p25 - loch (score = 0.63)
4334: /m/07j7r - tree (score = 0.61)
2860: /m/03ktm1 - body of water (score = 0.58)
1403: /m/023bbt - wilderness (score = 0.53)
2: /g/11jxkqbpp - mountainous landforms (score = 0.49)
4592: /m/093shy - reservoir (score = 0.43)
1475: /m/025s3q0 - landscape (score = 0.43)
```

### reference
https://github.com/openimages/dataset