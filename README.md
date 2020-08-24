# Eye-Strain-Detection

## Problem 

Screen-time has exponentially increased for a lot of us ever since we started working from home. While it may not always be possible to minimize this screen-time, we can take conscious steps to take care of our eyes. Spending too many hours staring at a screen can cause eye strain. We tend to blink less while staring at the blue light from a screen, and the movement of the screen makes your eyes work harder to focus. We typically do not position the screen at an ideal distance or angle, which can cause added strain. All these issues add up and can lead to lasting effects on vision: eye fatigue, dry and irritated eyes, loss of focus flexibility, retinal damage, etc.

One of the steps you can take, is to blink regularly. The average adult blinks between 10-20 times per minute. On an average we only blink 3-8 times per minute when reading, watching TV, listening to a podcast, working on a computer, or another activity that requires intense focus. That’s roughly 60 percent less than our normal rate of blinking!


## Solution

Eye Strain Detector to the rescue! It is a computer-vision based webapp that continuously monitors your blinking rate, in real time. If you don't blink enough, it reminds you to do so through desktop notifications. 

### Key Features 

- Instantly see your eye blinking rate
- Realtime eye strain alerts (notification & sound)
- The Computer Vision models used are robust and error rate is very low for different expressions, angles and even for people wearing spectacles[2]
- Click on the notifications to see more information!
- The app will work in the background and send reminders even if you don't open the browser
- If your eyes are closed for a prolonged period of time (5-6 secs), blinks are not detected


## How To Use

Note: Currently, the webapp has not been deployed but this can be cloned and used easily. Further, only supports MacOS as of now. 

To clone and run this application, you'll need [Git](https://git-scm.com), [Python](https://www.python.org/) and Anaconda 3 installed on your computer. From your command line:

```bash
# Clone this repository
$ git clone https://github.com/Anukriti2512/Eye-Strain-Detection.git

# Go into the repository
$ cd Eye-Strain-Detection

# Create a virtual/conda environment and activate it: 
$ conda create --name myenv
$ conda activate myenv

# Install dependencies
$ pip install -r requirements.txt

# Run the app
$ python webstreaming.py

# Copy the IP Address on a web browser and use the application to see blink detection in real-time
```


## Approach

The blink detector computes a metric called the eye aspect ratio (EAR), introduced by Soukupová and Čech in their 2016 paper, Real-Time Eye Blink Detection Using Facial Landmarks[1]. The eye aspect ratio makes for an elegant algorithm that involves a very simple calculation based on the ratio of distances between facial landmarks of the eyes. 

Each eye is represented by 6 (x, y)-coordinates, starting at the left-corner of the eye, and then working clockwise around the remainder of the region:

![blink_detection_6_landmarks](https://user-images.githubusercontent.com/37685052/91079233-6ccfdf00-e661-11ea-8804-25269701d328.jpg) 

Based on this image, we can see find a relation between the width and the height of these coordinates. We can then derive an equation that reflects this relation called the eye aspect ratio (EAR): 

![blink_detection_equation](https://user-images.githubusercontent.com/37685052/91079328-8a04ad80-e661-11ea-90b7-01d89fad71d2.png)

The eye aspect ratio is approximately constant while the eye is open, but will rapidly fall to zero when a blink is taking place. Using this simple equation, we can avoid image processing techniques and simply rely on the ratio of eye landmark distances to determine if a person is blinking. A frame threshold range is used to ensure that the person actually blinked and that their eyes are not closed for a long time.

![blink_detection_plot](https://user-images.githubusercontent.com/37685052/91079315-87a25380-e661-11ea-9f03-9c32bee8f9cc.jpg)

In this project, I have used existing Deep Learning models that detect faces and facial landmarks from images/video streams. These return the coordinates of the facial features like left eye, right eye, nose, etc. which have been used to calculate EAR. Blinking rate is monitored per minute.


## Demo 

You can view a demo of this project here : https://youtu.be/Tt2DR8FvYDk

## Scope for improvement & future plans

1. Currenly, EAR is the only quantitative metric used to determine if a person has blinked. However, due to noise in a video stream, subpar facial landmark detections, or fast changes in viewing angle, it could produce a false-positive detection, reporting that a blink had taken place when in reality the person had not blinked. To improve the blink detector, Soukupová and Čech recommend constructing a 13-dim feature vector of eye aspect ratios (N-th frame, N – 6 frames, and N + 6 frames), followed by feeding this feature vector into a Linear SVM for classification.

2. The UI is still being improved, and the web-app will be deployed soon.

3. Currently, this only works for MacOS due to some library limilations. It will be made cross platform soon.

4. Visualizations will be added so users can see insights about their blinking habits.


### References

1. [Research Paper: Real-Time Eye Blink Detection Using Facial Landmarks](http://vision.fe.uni-lj.si/cvww2016/proceedings/papers/05.pdf)
2. [Facial and Landmark Recognition Models](http://dlib.net/)
3. [Creating web-application using Flask](https://towardsdatascience.com/designing-a-machine-learning-model-and-deploying-it-using-flask-on-heroku-9558ce6bde7b)
4. [HTML+CSS](https://templatemo.com/tag/video)
5. [Eye Health knowledge](https://visionsource.com/blog/are-you-blinking-enough/)
