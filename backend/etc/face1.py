import dlib
import face_recognition

print("dlib version:", dlib.__version__)
print("face_recognition ready!")

# Quick test
image = face_recognition.load_image_file("person.jpg")
locations = face_recognition.face_locations(image)
print(locations)