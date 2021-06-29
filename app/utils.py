import face_recognition
import os
import cv2
import numpy as np
import imagehash
from PIL import Image


# resize image in order to prevent any error
def resize_image(image_path):
    file_name, file_extension = os.path.splitext(os.path.basename(image_path))

    img = cv2.imread(image_path)
    height, width = img.shape[:2]
    max_height = 900
    max_width = 900

    # only shrink if img is bigger than required
    if max_height < height or max_width < width:
        # get scaling factor
        scaling_factor = max_height / float(height)
        if max_width / float(width) < scaling_factor:
            scaling_factor = max_width / float(width)
        # resize image
        img = cv2.resize(img, None, fx=scaling_factor, fy=scaling_factor, interpolation=cv2.INTER_AREA)
        cv2.imwrite(os.path.join("static/processed_uploads/", f"{file_name}{file_extension}"), img)
        img_path = f"static/processed_uploads/{file_name}{file_extension}"
        return img_path

    return image_path


# this function reads first image to encoding
def see_image(know_img_path):
    know_img_path = resize_image(know_img_path)
    known_faces = []
    known_names = []

    # File_name = os.path.splitext(os.path.basename(know_img_path))[0]
    file_name, file_extension = os.path.splitext(os.path.basename(know_img_path))
    known_names.append(file_name)

    print('Loading known face...')
    image = face_recognition.load_image_file(know_img_path)

    see_face_locations = face_recognition.face_locations(image, number_of_times_to_upsample=0)

    see_encodings = face_recognition.face_encodings(image, see_face_locations)[0]
    known_faces.append(see_encodings)

    im_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    rgb_img_path = f"static/uploads/{file_name}{file_extension}"
    return im_rgb, see_face_locations, see_encodings, known_faces, rgb_img_path


# This function read second image, hash the image, encode faces and the above function's face.
def lets_recognise(un_img_path, known_faces,
                   TOLERANCE=0.6, FRAME_THICKNESS=3,
                   FONT_THICKNESS=3):
    un_img_path = resize_image(un_img_path)
    # Read image
    print('Loading unknown faces...')
    image_unknown = face_recognition.load_image_file(un_img_path)

    # Split file name and it's extension
    un_file_name, file_extension = os.path.splitext(os.path.basename(un_img_path))

    # Hashing image
    unique_image_name = str(imagehash.average_hash(Image.open(un_img_path)))

    # This time we first grab face locations - we'll need them to draw boxes
    locations_unknown = face_recognition.face_locations(image_unknown, number_of_times_to_upsample=0)

    # Encode all faces in image
    encodings_unknown = face_recognition.face_encodings(image_unknown, locations_unknown)

    face_names = []

    for face_encoding, face_location in zip(encodings_unknown, locations_unknown):
        matches = face_recognition.compare_faces(known_faces, face_encoding, TOLERANCE)
        distances = face_recognition.face_distance(known_faces, face_encoding)

        top_left = (face_location[3], face_location[0])
        bottom_right = (face_location[1], face_location[2])
        # match = None
        if True in matches:
            first_match_index = matches.index(True)
            name = known_faces[first_match_index]

            face_names.append(name)

            color = (0, 0, 255)
            # Paint frame
            cv2.rectangle(image_unknown, top_left, bottom_right, color, FRAME_THICKNESS)
            cv2.putText(image_unknown, str(np.round(distances, 3)), (face_location[3] + 10, face_location[2] + 15),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8, (255, 255, 255), FONT_THICKNESS)

        else:
            top_left = (face_location[3], face_location[0])
            bottom_right = (face_location[1], face_location[2])

            color = (255, 255, 0)
            # Paint frame
            cv2.rectangle(image_unknown, top_left, bottom_right, color, FRAME_THICKNESS)
            cv2.putText(image_unknown, str(np.round(distances, 3)), (face_location[3] + 10, face_location[2] + 15),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8, (255, 255, 255), FONT_THICKNESS)

    im_rgb = cv2.cvtColor(image_unknown, cv2.COLOR_BGR2RGB)
    cv2.imwrite(os.path.join("static/predict/", f"{unique_image_name}_{un_file_name}{file_extension}"), im_rgb)
    rgb_img_path = f"static/predict/{unique_image_name}_{un_file_name}{file_extension}"
    return rgb_img_path
