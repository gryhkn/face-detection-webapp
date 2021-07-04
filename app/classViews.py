from flask import render_template, request
import os
from PIL import Image
from datetime import datetime
import pandas as pd
import csv

# import output types
from pathlib import Path
from typing import List, Optional, Tuple
from werkzeug.datastructures import FileStorage

# import functions
from app.utils import lets_recognise, see_image


class flaskApp:
    UPLOAD_FOLDER = 'static/uploads'

    def faceapp(self):
        return render_template('faceapp.html')

    def getwidth_height(self, image_path):
        img = Image.open(image_path)
        size = img.size  # width and height
        aspect = size[0] / size[1]  # width / height
        w = 300 * aspect
        h = 300 * aspect
        return int(w), int(h)

    def get_objects(self) -> Tuple[FileStorage, Optional[str], str, int, int]:
        image_object = request.files['image']
        image_name = image_object.filename
        image_path = os.path.join(self.UPLOAD_FOLDER, image_name)
        image_object.save(image_path)
        w, h = self.getwidth_height(image_path)
        return image_object, image_name, image_path, w, h

    def memorize(self):
        if request.method == "POST":
            image1_object, image1_name, image1_path, w1, h1 = self.get_objects()
            self.write_make_history(image1_path)
            return render_template('faceapp.html', fileupload1=True, img_name=image1_name, w=w1, h=h1)

        return render_template('faceapp.html', fileupload1=False, img_name="freeai.png")

    def write_make_history(self, image_path: Path):
        now = datetime.now()
        with open('history.csv', 'a+', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([now, image_path])
        csvfile.close()

    def read_make_history(self) -> List:
        df_history = pd.read_csv('history.csv')
        df_history = df_history.sort_values("date", ascending=False)

        if len(df_history) < 5:
            front_date = df_history["date"].tolist()
            front_path = df_history["image1"].tolist()
        else:
            front_date = df_history.iloc[:5, 0].tolist()
            front_path = df_history.iloc[:5, 1].tolist()

        images_list = []
        for index in range(len(front_path)):
            images_list.append([front_path[index], front_date[index]])

        return images_list

    def recognize(self):
        # controls if POST request
        if request.method == "POST":
            # if identify button clicked
            if request.form.get('ayvos'):
                if request.form['ayvos'] == 'Memorize':
                    image1_object, image12_name, image1_path, w1, h1 = self.get_objects()
                    self.write_make_history(image1_path)

                    return render_template('faceapp.html', fileupload1=True, img_name=image12_name, w=w1, h=h1)

            image2_object, image2_name, image2_path, w2, h2 = self.get_objects()

            path1_image = self.read_make_history()[0][0]
            image, see_face_locations, see_encodings, known_faces, rgb_img1_path = see_image(path1_image)
            un_file1_name, file1_extension = os.path.splitext(os.path.basename(rgb_img1_path))

            rgb_img_path = lets_recognise(image2_path, known_faces)
            un_file_name, file_extension = os.path.splitext(os.path.basename(rgb_img_path))

            history_images = self.read_make_history()
            return render_template('faceapp.html', fileupload1=True, fileupload2=True,
                                   img_name=f"{un_file1_name}{file1_extension}",
                                   img_name2=f"{un_file_name}{file_extension}", w=w2, h=h2,
                                   empty_list=history_images)

        return render_template('faceapp.html', fileupload2=False, img_name="static/assets/images/ayvos-white-logo.png")
