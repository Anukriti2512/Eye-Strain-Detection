from Blink_detection import blink_detection
import Notifier
from imutils.video import VideoStream
from flask import Response
from flask import Flask
from flask import render_template
import threading
import datetime
import imutils
import time
import cv2

app = Flask(__name__)

# initialize the output frame and a lock used to ensure thread-safe
# exchanges of the output frames
outputFrame = None
lock = threading.Lock()

# keep track of time
timediff = datetime.datetime.now()

# eye aspect ratio to indicate blink and
# range of consecutive frames the eye must be below the threshold
EYE_AR_THRESH = 0.22
EYE_AR_CONSEC_FRAMES_MIN = 2
EYE_AR_CONSEC_FRAMES_MAX = 5

# start the video stream thread
vs = VideoStream(src=0).start()
fileStream = False
time.sleep(1.0)

@app.route("/")
def index():
	return render_template("index.html")


def detect_blinks():

	global vs, outputFrame, lock

	# initialize the frame counter and the total number of blinks
	counter = 0
	totalBlinks = 0

	# loop over frames from the video stream
	while True:

		if fileStream and not vs.more():
			break
	 
		# read frame from the threaded video file stream, resize
		# and convert to grayscale
		frame = vs.read()
		frame = imutils.resize(frame, width=700)
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

		if(time_interval_passed()):
			if(totalBlinks < 12):
				Notifier.notify()
			totalBlinks = 0

		#Eye Aspect Ratio
		EAR = blink_detection.calculate_ear(frame, gray)

		if EAR is not None :
			
			# the eye aspect ratio is below the blink threshold
			if EAR < EYE_AR_THRESH:
				counter += 1

			# the eye aspect ratio is not below the blink threshold
			else:
				# if the eyes were closed for a sufficient range of frames
				# then increment the total number of blinks
				if counter >= EYE_AR_CONSEC_FRAMES_MIN and counter <= EYE_AR_CONSEC_FRAMES_MAX:
					totalBlinks += 1

				# reset the eye frame counter
				counter = 0

			cv2.putText(frame, "Blinks: {}".format(totalBlinks), (10, 30),
				cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
			cv2.putText(frame, "EAR: {:.2f}".format(EAR), (300, 30),
				cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
		
		# Acquire the lock to ensure that outputFrame variable is 
		#not accidentally being read by a client while we are trying to update it
		with lock:
			outputFrame = frame.copy()


def time_interval_passed():

	global timediff

	# Calculate time interval since last iteration
	time_delta = datetime.datetime.now() - timediff
	seconds_passed = time_delta.total_seconds()

	# Check if one minute interval has passed
	if(seconds_passed >= 60):
		timediff = datetime.datetime.now()
		return True


def generate():

	global outputFrame, lock

	# loop over frames from output stream
	while True:
		# wait until the lock is acquired
		# check if the output frame is available, otherwise skip
		# the iteration of the loop
		with lock:
			if outputFrame is None:
				continue

			# encode the frame in JPEG format
			#JPEG compression is performed here to reduce load on the network 
			#and ensure faster transmission of frames.
			(flag, encodedImage) = cv2.imencode(".jpg", outputFrame)

			# ensure the frame was successfully encoded
			if not flag:
				continue

		# yield the output frame in the byte format
		yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
			bytearray(encodedImage) + b'\r\n')


@app.route("/video_feed")
def video_feed():
	# return the response generated along with the specific media
	# type (mime type)
	return Response(generate(),
		mimetype = "multipart/x-mixed-replace; boundary=frame")

# check to see if this is the main thread of execution
if __name__ == '__main__':

	# start a thread that will perform blink detection
	t = threading.Thread(target=detect_blinks)
	t.daemon = True
	t.start()
	app.run(debug=True, threaded=True, use_reloader=False)


cv2.destroyAllWindows()
vs.stop()