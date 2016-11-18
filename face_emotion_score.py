# This python program helps you interprete facial expressions from pictures

import httplib
import cv2
import json

def read_file(filename):
	with open(filename, 'rb') as rf:
		content = rf.read()
	return content

def get_emotion_score(image):
	headers = {
		'Content-Type': 'application/octet-stream',
		'Ocp-Apim-Subscription-Key': '<<api-key-here>>'
	}
	conn = httplib.HTTPSConnection('api.projectoxford.ai')
	conn.request("POST", "/emotion/v1.0/recognize?%s", image, headers)
	response = conn.getresponse()
	score = response.read()
	score = json.loads(score)
	print type(score)
	conn.close()
	return score

def overlay_score_on_image(score, filename):
	image = cv2.imread(filename, cv2.IMREAD_COLOR)

	for face in score:
		fR = face['faceRectangle']
		eS = face['scores']
		emotion_score = max(eS.iteritems(), key=lambda k: k[1])
		emotion, score_rounded = emotion_score[0], str(emotion_score[1])[:4]
		cv2.putText(image, emotion, (fR['left'], fR['top']), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255,255,255), 1)
		cv2.putText(image, score_rounded, (fR['left'], fR['top']+15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1)
		cv2.imwrite(filename[0:-4]+'.scored'+filename[-4:], image)

def interprete_facial_expression(filename):
	image = read_file(filename)
	score = get_emotion_score(image)
	overlay_score_on_image(score, filename)

interprete_facial_expression('group2.jpg')