#!/usr/bin/python
# encoding=utf8
from django.core.management.base import BaseCommand, CommandError

from drf_exercise.models.song import Song
from drf_exercise.models.song import Tag

from django.conf import settings
import os
import json

class Command(BaseCommand):

    def handle(self, *args, **options):
        c= 0
        o = 0
        json_dataset_location = settings.BASE_DIR + "/lastfm_subset"

        for root, dirs, files in os.walk(json_dataset_location):
            for file in files:
                fname = os.path.join(root, file)
                # data = json.load(open(fname))
                try:
                    with open(fname, encoding='utf-8') as json_data:
                        d = json.load(json_data)
                        print (d["artist"])
                        print (d["timestamp"])

                        print(d["similars"])
                        songs_by_scores = sorted(d["similars"], key=lambda x: x[1], reverse=True)

                        # print(d["tags"])
                        # print(d["title"])
                        # print(d["track_id"])
                        s = Song(artist_name=d["artist"],timestamp=d["timestamp"],similars=songs_by_scores ,title=d["title"],track_id=d["track_id"])
                        print (s)
                        s.save()
                        # import pdb; pdb.set_trace()
                        for each_tag in d["tags"]:
                            t = Tag(tag_name=each_tag[0],score=each_tag[1])
                            t.save()
                            t.songs.add(s)
                    c+=1
                except:
                    o+=1
                    pass
        print ("c")
        print (c)            
        print ("0")
        print (o)            
        # import pdb; pdb.set_trace()
        # wb = load_workbook(filename=dest_filename)
        # sheet = wb['Profiling']

        # for rowNum in range(2, sheet.max_row):
        #     if sheet.cell(row=rowNum, column=7).value == 'NA':
        #         continue

        #     company = Company()
        #     primary_contact = {}

        #     company.name = sheet.cell(row=rowNum, column=7).value

        #     if sheet.cell(row=rowNum, column=9).value != 'NA':
        #         company.business_sector = sheet.cell(row=rowNum, column=9).value
        #     if sheet.cell(row=rowNum, column=8).value != 'NA':
        #         company.business_industry = sheet.cell(row=rowNum, column=8).value

        #     if sheet.cell(row=rowNum, column=4).value is not None:
        #         if sheet.cell(row=rowNum, column=5).value is None:
        #             primary_contact['name'] = sheet.cell(row=rowNum, column=4).value
        #         else:
        #             primary_contact['name'] = sheet.cell(row=rowNum, column=4).value + " " + sheet.cell(row=rowNum, column=5).value

        #     primary_contact['email'] = sheet.cell(row=rowNum, column=3).value

        #     if sheet.cell(row=rowNum, column=6).value is not None:
        #         primary_contact['contact_number'] = sheet.cell(row=rowNum, column=6).value
        #     company.primary_contact = primary_contact

        #     #import pdb; pdb.set_trace()
        #     company.save()
