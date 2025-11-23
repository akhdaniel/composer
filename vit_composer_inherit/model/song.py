#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError
import json
from .libs.openai_lib import *
from .libs.wavespeed import Wavespeed
import requests
import base64
import logging
_logger = logging.getLogger(__name__)

class song(models.Model):
    _name = "vit.song"
    _inherit = "vit.song"

    def action_generate_song(self, ):
        pass


    def action_generate_scenes(self, ):
        context = self.lyrics
        additional_command=""
        system_prompt = "You are a helpfull assistant"
        question = ""
        user_prompt = """Lirik lagu: {context} 
{question}
Buat data scenes untuk music video, dengan image prompt, start end frame dan durasi dalam detik.
Response HANYA dalam Format data JSON plain text, bukan MD, dan harus seperti ini contohnya, tanpa penjelasan di awal dan akhir:
[
    {{
      "scene": "Opening",
      "description": "Close-up penyanyi di kamar temaram, cahaya kuning lembut, ekspresi reflektif.",
      "duration":"10",
      "start":"0",
      "end":"10",
      "image_prompt": "cinematic close-up of a man sitting alone in a dim warm-lit bedroom, emotional eyes, film grain, shallow depth of field"
    }},
    ...
]
"""
        openai_api_key = self.env["ir.config_parameter"].sudo().get_param("openai_api_key")
        openai_base_url = self.env["ir.config_parameter"].sudo().get_param("openai_base_url", None)

        model = self.gpt_model_id.name

        scenes = generate_content(openai_api_key=openai_api_key, 
                                openai_base_url=openai_base_url, model=model, 
                                system_prompt=system_prompt, user_prompt=user_prompt, 
                                context=context, question=question, 
                                additional_command=additional_command)    
        _logger.info('scenes====')
        _logger.info(scenes)
        scenes = scenes.replace('```json','').replace('```','')
        scenes = json.loads(scenes)   

        scene_ids = []
        for scene in scenes:
            scene_ids.append((0,0,{
                "name": scene['scene'],
                "description": scene['description'],
                "duration": scene['duration'],
                "start": scene['start'],
                "end": scene['end'],
                "image_prompt": scene['image_prompt'],
            }))
        self.scene_ids = scene_ids


