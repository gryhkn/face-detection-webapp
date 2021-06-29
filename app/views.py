from flask import render_template, request
import os
from PIL import Image
from datetime import datetime
import pandas as pd
import csv

from app.utils import see_image, lets_recognise

UPLOAD_FLODER = 'static/uploads'


def faceapp():
    return render_template('faceapp.html')


def getwidth_height(path):
    img = Image.open(path)
    size = img.size  # width and height
    aspect = size[0] / size[1]  # width / height
    w = 300 * aspect
    h = 300 * aspect
    return int(w), int(h)


def memorize():
    if request.method == "POST":
        f = request.files['image']
        assert f
        global path1
        global filename
        filename = f.filename
        path1 = os.path.join(UPLOAD_FLODER, filename)
        f.save(path1)
        w, h = getwidth_height(path1)

        return render_template('faceapp.html', fileupload1=True, img_name=filename, w=w, h=h)

    return render_template('faceapp.html', fileupload1=False, img_name="freeai.png")


def recognize():
    # controls if POST request
    if request.method == "POST":
        # if identify button clicked
        if request.form.get('ayvos'):
            if request.form['ayvos'] == 'Memorize':
                f = request.files['image']
                assert f
                global path1
                global filename
                filename = f.filename
                path1 = os.path.join(UPLOAD_FLODER, filename)
                f.save(path1)
                w, h = getwidth_height(path1)

                return render_template('faceapp.html', fileupload1=True, img_name=filename, w=w, h=h)

        f = request.files['image']
        assert f, "Where's my file?"
        filename2 = f.filename
        path2 = os.path.join(UPLOAD_FLODER, filename2)
        f.save(path2)
        w, h = getwidth_height(path2)

        image, see_face_locations, see_encodings, known_faces, unique_image = see_image(path1)

        rgb_img_path = lets_recognise(path2, known_faces)
        un_file_name, file_extension = os.path.splitext(os.path.basename(rgb_img_path))

        # record date
        now = datetime.now()

        # read .csv file and record date and first image path
        with open('history.csv', 'a+', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([now, path1])
        df_history = pd.read_csv('history.csv')

        df_history = df_history.sort_values("date", ascending=False)

        if len(df_history) < 5:
            front_date = df_history["date"].tolist()
            front_path = df_history["image1"].tolist()
        else:
            front_date = df_history.iloc[:5, 0].tolist()
            front_path = df_history.iloc[:5, 1].tolist()

        bos_liste = []
        for index in range(len(front_path)):
            bos_liste.append([front_path[index], front_date[index]])

        return render_template('faceapp.html', fileupload1=True, fileupload2=True, img_name=filename,
                               img_name2=f"{un_file_name}{file_extension}", w=w, h=h, bos_liste=bos_liste)

    return render_template('faceapp.html', fileupload2=False, img_name="static/assets/images/ayvos-white-logo.png")
