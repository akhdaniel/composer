#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError
import json
from .libs.openai_lib import *
from .libs.wavespeed import Wavespeed
from .libs.audio_splitter import AudioSplitterBase64
import requests
import base64
import io
import zipfile
from pydub import AudioSegment

import logging
_logger = logging.getLogger(__name__)

class song(models.Model):
    _name = "vit.song"
    _inherit = "vit.song"

    @api.depends("song_mp3")
    def _get_song_url(self, ):
        """
        {
        "@api.depends":["song_mp3"]
        }
        """
        base_url =self.env["ir.config_parameter"].sudo().get_param("web.base.url")
        for rec in self:
            rec.song_mp3_url = f"{base_url}/web/image/vit.song/{rec.id}/song_mp3?unique=1763886100000"



    def action_generate_song(self, ):
        pass

    def action_split_song(self, ):
        splitter = AudioSplitterBase64(self.song_mp3,)
        for i, scene in enumerate(self.scene_ids):
            scene.clip_mp3_filename = f'Audio Clip {i}'
            scene.clip_mp3 = splitter.split_range( scene.start, scene.end)

    def get_song_duration(self):
        """
        Returns duration of MP3 (base64) in seconds (float)
        """
        if not self.song_mp3:
            return 0.0

        # Decode base64 → bytes
        audio_bytes = base64.b64decode(self.song_mp3)

        # Load audio into memory using pydub
        audio_segment = AudioSegment.from_file(io.BytesIO(audio_bytes), format="mp3")

        # Duration in milliseconds → convert to seconds
        duration_seconds = len(audio_segment) / 1000.0

        return duration_seconds
    
    def action_generate_scenes(self, ):
        context = self.lyrics
        additional_command=""
        system_prompt = self.prompt_id.system_prompt 
        question = self.get_song_duration()
        user_prompt = self.prompt_id.user_prompt
        openai_api_key = self.env["ir.config_parameter"].sudo().get_param("openai_api_key")
        openai_base_url = self.env["ir.config_parameter"].sudo().get_param("openai_base_url", None)

        model = self.gpt_model_id.name

        scenes = generate_content(openai_api_key=openai_api_key, 
                                openai_base_url=openai_base_url, model=model, 
                                system_prompt=system_prompt, 
                                user_prompt=user_prompt, 
                                context=context, question=question, 
                                additional_command=additional_command)    
        _logger.info('scenes====')
        _logger.info(scenes)
        scenes = scenes.replace('```json','').replace('```','')
        scenes = json.loads(scenes)   

        scene_ids = []
        self.scene_ids = scene_ids
        for scene in scenes:
            scene_ids.append((0,0,{
                "name": scene['scene'],
                "description": scene['description'],
                "duration": scene['duration'],
                "start": scene['start'],
                "end": scene['end'],
                "image_prompt": scene['image_prompt'],
                "video_prompt": scene['video_prompt'],
                "lyrics": scene['lyrics'],
            }))
        self.scene_ids = scene_ids


    def action_download_scene_images(self, ):
        return self.zip_scenes('image_png')
    
    def action_download_scene_videos(self, ):
        return self.zip_scenes('video_mp4')

    def action_download_song_clips(self, ):
        return self.zip_scenes('clip_mp3')   

    def action_download_capcut(self, ):
        pass

    # def zip_song_clips(self, ):
    #     # collect all clips
    #     records = self.song_clip_ids

    #     # create in-memory zip
    #     zip_buffer = io.BytesIO()

    #     with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
    #         for rec in records:
    #             if rec.clip_mp3:
    #                 # get binary data
    #                 mp3_data = base64.b64decode(rec.clip_mp3)

    #                 # define a file name inside zip
    #                 filename = f"{rec.name}.mp3"

    #                 # write inside ZIP
    #                 zipf.writestr(filename, mp3_data)

        
    #     # ----- versi write ke var www
    #     # # Prepare filename
    #     # zip_filename = f"{self.name.replace(' ', '_')}-song_clips.zip"
    #     # server_path = f"/var/www/html/songs/{zip_filename}"

    #     # # Write to physical file
    #     # with open(server_path, "wb") as f:
    #     #     f.write(zip_buffer.getvalue())

    #     # # Generate public URL
    #     # # base_url = self.env["ir.config_parameter"].sudo().get_param("web.base.url")
    #     # ip_addrs = '147.139.134.170'
    #     # download_url = f"http://{ip_addrs}/songs/{zip_filename}"

    #     # # Store the URL in the record
    #     # # self.song_clips_zip_url = download_url

    #     # # Redirect browser to download
    #     # _logger.info(download_url)
    #     # return {
    #     #     "type": "ir.actions.act_url",
    #     #     "url": download_url,
    #     #     "target": "self",
    #     # }
        
    #     # # ----- versi download binary
    #     # prepare zip for download
    #     zip_filename = f"{self.name}-song_clips.zip"
    #     zip_data = zip_buffer.getvalue()
    #     zip_b64 = base64.b64encode(zip_data)
    #     self.song_clips_zip = zip_b64
    #     self.song_clips_zip_filename = zip_filename

    #     # force download using ir.actions.act_url
    #     return {
    #         "type": "ir.actions.act_url",
    #         "url": f"/web/content/vit.song/{self.id}/song_clips_zip/{zip_filename}",
    #         "target": "self",
    #     }

    def zip_scenes(self, fieldname):

        # define a file name inside zip
        if '_png' in fieldname:
            zip_filename = f"{self.name}-scene-images.zip"
            binary_fieldname= 'scene_images_zip'
        elif '_mp3' in fieldname:
            zip_filename = f"{self.name}-scene-song-clips.zip"
            binary_fieldname= 'song_clips_zip'
        elif '_mp4' in fieldname:
            zip_filename = f"{self.name}-scene-videos.zip"
            binary_fieldname= 'scene_videos_zip'

        # create in-memory zip
        zip_buffer = io.BytesIO()

        # collect all clips
        records = self.scene_ids

        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for rec in records:
                if rec[fieldname]:
                    # get binary data
                    data = base64.b64decode(rec[fieldname])
                    # write inside ZIP
                    if '_png' in fieldname:
                        filename = f"{rec.name}.png"
                    elif '_mp3' in fieldname:
                        filename = f"{rec.name}.mp3"
                    elif '_mp4' in fieldname:
                        filename = f"{rec.name}.mp4"
                    zipf.writestr(filename, data)

        # prepare zip for download
        zip_data = zip_buffer.getvalue()
        zip_b64 = base64.b64encode(zip_data)
        self.write({
            binary_fieldname: zip_b64,
            f"{binary_fieldname}_filename" : zip_filename
        })

        # force download using ir.actions.act_url
        return {
            "type": "ir.actions.act_url",
            "url": f"/web/content/vit.song/{self.id}/{binary_fieldname}/{zip_filename}",
            "target": "self",
        }


    def action_generate_scene_videos(self, ):
        pass

    def action_download_song(self):
        return {
            "type": "ir.actions.act_url",
            "url": f"/web/content/vit.song/{self.id}/song_mp3/{self.song_mp3_filename}",
            "target": "self",
        }        