# from flask import render_template, request
# import os
# from PIL import Image
# from datetime import datetime
# import pandas as pd
# import csv
#
# from pathlib import Path
# from typing import List, Any, Dict, Optional, Tuple, Set
#
# from app.utils import see_image, lets_recognise
#
# UPLOAD_FLODER = 'static/uploads'
#
#
# def faceapp():
#     return render_template('faceapp.html')
#
#
# def getwidth_height(path: Path):
#     img = Image.open(path)
#     size = img.size  # width and height
#     aspect = size[0] / size[1]  # width / height
#     w = 300 * aspect
#     h = 300 * aspect
#     return int(w), int(h)
#
#
# def memorize():
#     if request.method == "POST":
#         image1_object = request.files['image']
#         # assert f
#         global image1_path
#         # global filename
#         image1_name = image1_object.filename
#         image1_path = os.path.join(UPLOAD_FLODER, image1_name)
#         image1_object.save(image1_path)
#         w, h = getwidth_height(image1_path)
#
#         return render_template('faceapp.html', fileupload1=True, img_name=image1_name, w=w, h=h)
#
#     return render_template('faceapp.html', fileupload1=False, img_name="freeai.png")
#
#
# def recognize():
#     # controls if POST request
#     if request.method == "POST":
#         # if identify button clicked
#         if request.form.get('ayvos'):
#             if request.form['ayvos'] == 'Memorize':
#                 image1_object = request.files['image']
#                 # assert image2_name
#                 global image1_path
#                 # global filename
#                 image1_name = image1_object.filename
#                 image1_path = os.path.join(UPLOAD_FLODER, image1_name)
#                 image1_object.save(image1_path)
#                 w, h = getwidth_height(image1_path)
#
#                 return render_template('faceapp.html', fileupload1=True, img_name=image1_name, w=w, h=h)
#
#         image2_object = request.files['image']
#         # assert image2_name, "Where's my file?"
#         image2_name = image2_object.filename
#         image2_path = os.path.join(UPLOAD_FLODER, image2_name)
#         image2_object.save(image2_path)
#         w, h = getwidth_height(image2_path)
#
#         image, see_face_locations, see_encodings, known_faces, unique_image = see_image(image1_path)
#
#         rgb_img_path = lets_recognise(image2_path, known_faces)
#         un_file_name, file_extension = os.path.splitext(os.path.basename(rgb_img_path))
#
#         # record date
#         now = datetime.now()
#
#         # read .csv file and record date and first image path
#         with open('history.csv', 'a+', newline='') as csvfile:
#             writer = csv.writer(csvfile)
#             writer.writerow([now, image1_path])
#         df_history = pd.read_csv('history.csv')
#
#         df_history = df_history.sort_values("date", ascending=False)
#
#         if len(df_history) < 5:
#             front_date = df_history["date"].tolist()
#             front_path = df_history["image1"].tolist()
#         else:
#             front_date = df_history.iloc[:5, 0].tolist()
#             front_path = df_history.iloc[:5, 1].tolist()
#
#         empty_list = []
#         for index in range(len(front_path)):
#             empty_list.append([front_path[index], front_date[index]])
#
#         return render_template('faceapp.html', fileupload1=True, fileupload2=True, img_name=image1_name,
#                                img_name2=f"{un_file_name}{file_extension}", w=w, h=h, empty_list=empty_list)
#
#     return render_template('faceapp.html', fileupload2=False, img_name="static/assets/images/ayvos-white-logo.png")
