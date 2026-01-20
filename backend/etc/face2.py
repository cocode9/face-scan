import face_recognition
from PIL import Image, ImageDraw

# Load the sample image
image_path = "./person1.jpg"
image = face_recognition.load_image_file(image_path)

# Find facial landmarks
face_landmarks_list = face_recognition.face_landmarks(image)
print(face_landmarks_list)  # prints coordinates of all features

# Draw the landmarks on the image
pil_image = Image.fromarray(image)
draw = ImageDraw.Draw(pil_image)

for face_landmarks in face_landmarks_list:
    for feature, points in face_landmarks.items():
        draw.line(points, fill="green", width=2)

# Show the image
pil_image.show()

# Optionally, save it to a file
pil_image.save("landmarks_result.png")