import face_recognition
import cv2
import dlib

# Get a reference to webcam #0 (the default one)
video_capture = cv2.VideoCapture(0)
class Sprite():
    def load_sprite(self,path):
        sprite = cv2.imread(path,-1)
        sprite = cv2.cvtColor(sprite, cv2.COLOR_BGR2BGRA)
        return sprite
    def resize_sprite(self, sprite, face_part):
        if face_part == 'chin':
            sprite = cv2.resize(sprite, ((int(elements[face_part][15][0])-int(elements[face_part][1][0])), 15+((int(elements[face_part][8][1]))-((int(elements[face_part][15][1])+int(elements[face_part][1][1]))//2))))
            return sprite
        if face_part == 'left_eye':
            sprite = cv2.resize(sprite, (7+int((max(elements[face_part], key=lambda x:x[0])[0]))-int((min(elements[face_part], key=lambda x:x[0])[0])),  (20+int((max(elements[face_part], key=lambda x:x[1])[1]))-int((min(elements[face_part], key=lambda x:x[1])[1])))))   
            return sprite
        if face_part == 'right_eye':
            sprite = cv2.resize(sprite, (7+int((max(elements[face_part], key=lambda x:x[0])[0]))-int((min(elements[face_part], key=lambda x:x[0])[0])),  (20+int((max(elements[face_part], key=lambda x:x[1])[1]))-int((min(elements[face_part], key=lambda x:x[1])[1])))))
            return sprite 
class Frame():
    def get_ret_frame(self,webcam):
        ret, frame = webcam.read()
        return ret, frame
    def get_offset(self, face_part):
        if face_part == 'chin':
            h_offset = ((int(elements[face_part][15][1])+int(elements[face_part][1][1]))//2)
            w_offset = int(elements[face_part][1][0])
            return h_offset, w_offset
        if face_part == 'left_eye':
            h_offset = int((min(elements[face_part],key=lambda x:x[1])[1]))-5
            w_offset = int((min(elements[face_part],key=lambda x:x[0])[0]))-5
            return h_offset, w_offset
        if face_part == 'right_eye':
            h_offset = int((min(elements[face_part],key=lambda x:x[1])[1]))-5
            w_offset = int((min(elements[face_part],key=lambda x:x[0])[0]))-5
            return h_offset, w_offset
    def draw_sprite(self, h_offset, w_offset, face_part, face_parth, face_partw, frame, frame_h, frame_w):
        for i in range(0, face_parth):
            if h_offset + i >= frame_h:
                break
            for j in range(0, face_partw):
                if face_part[i,j][3] != 0:
                    if w_offset + j >= frame_w:
                        break
                    else:
                        frame[h_offset + i,w_offset + j] = face_part[i,j]

# Initialize some variables
#face_locations = []
mask = Sprite().load_sprite('mask.png')
lefteye = Sprite().load_sprite('lefteye.png')
righteye = Sprite().load_sprite('righteye.png')

while True:
    # Grab a single frame of video
    ret, frame = Frame().get_ret_frame(video_capture)
    # Get shape of frame
    frame_h, frame_w, frame_c = frame.shape
    # Find all the faces and facial landmarks in the current frame of video
    facial_landmarks = face_recognition.face_landmarks(frame)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
    # Display the results
    for elements in facial_landmarks:
        mask = Sprite().resize_sprite(mask,'chin')
        lefteye = Sprite().resize_sprite(lefteye,'left_eye')
        righteye = Sprite().resize_sprite(righteye, 'right_eye')
        lefteye_h, lefteye_w, lefteye_c = lefteye.shape
        righteye_h, righteye_w, right_c = righteye.shape
        mask_h, mask_w, mask_c = mask.shape        
        h_offset, w_offset = Frame().get_offset('left_eye')
        Frame().draw_sprite(h_offset, w_offset, lefteye, lefteye_h, lefteye_w, frame, frame_h, frame_w)
        h_offset, w_offset = Frame().get_offset('right_eye')
        Frame().draw_sprite(h_offset, w_offset, righteye, righteye_h, righteye_w, frame, frame_h, frame_w)
        h_offset, w_offset = Frame().get_offset('chin')
        Frame().draw_sprite(h_offset, w_offset, mask, mask_h, mask_w, frame, frame_h, frame_w)
    # Display the resulting image
    cv2.imshow('Video', frame)
    mask = Sprite().load_sprite('mask.png')
    lefteye = Sprite().load_sprite('lefteye.png')
    righteye = Sprite().load_sprite('righteye.png')
    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
