#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)
from .libs.wavespeed import Wavespeed
import requests
import base64
import time

class scene(models.Model):
    _name = "vit.scene"
    _inherit = "vit.scene"

    # @api.depends("song_clip_ids")
    # def _get_clip_names(self, ):
    #     """
    #     {
    #     "@api.depends":["song_clip_ids"]
    #     }
    #     """
    #     for rec in self:
    #         rec.clip_names = ", ".join(rec.song_clip_ids.mapped('name'))

    @api.depends("clip_mp3")
    def _get_clip_url(self, ):
        """
        {
        "@api.depends":["clip_mp3"]
        }
        """
        base_url =self.env["ir.config_parameter"].sudo().get_param("web.base.url")
        for rec in self:
            rec.clip_mp3_url = f"{base_url}/web/image/vit.scene/{rec.id}/clip_mp3?unique={int(time.time())}"

    def action_generate_image(self, ):
        if not self.image_prompt:
            raise UserError('Scene mage prompt empty!')
        
        api_key = self.env["ir.config_parameter"].sudo().get_param("wavespeed_api_key")
        ws = Wavespeed(api_key=api_key)
        ref_image=[]

        if self.actor_ids:
            actor = self.actor_ids[0]
            base_url =self.env["ir.config_parameter"].sudo().get_param("web.base.url")
            ref_image.append(f"{base_url}/web/image/vit.actor/{actor.id}/image?unique={int(time.time())}")

        image_url = ws.generate_image(
            image_prompt=self.image_prompt,
            model_name='bytedance/seedream-v4/edit',
            reference_image_url=ref_image)
        
        self.image_url = image_url
        self.download_wavespeed_result(self.image_url, 'image_png', 'png')


    def action_generate_video(self, ):
        if not self.image_png:
            raise UserError('Scene reference image empty!')
        if not self.video_prompt:
            raise UserError('Scene video prompt empty!')
        
        api_key = self.env["ir.config_parameter"].sudo().get_param("wavespeed_api_key")
        ws = Wavespeed(api_key=api_key)

        base_url =self.env["ir.config_parameter"].sudo().get_param("web.base.url")
        ref_image = f"{base_url}/web/image/vit.scene/{self.id}/image_png?unique={int(time.time())}"


        if not self.lip_sync:
            additional_payload = {
                'image':ref_image
            }
            video_url = ws.generate_video(
                video_prompt=self.video_prompt,
                model_name='wavespeed-ai/wan-2.2/i2v-5b-720p',
                additional_payload=additional_payload)
        else:
            ref_audio = f"{base_url}/web/image/vit.scene/{self.id}/image_png?unique={int(time.time())}"
            additional_payload = {
                "audio": ref_audio,
                "image": ref_image,
                "seed": -1
            }
            video_url = ws.generate_video(
                video_prompt=self.video_prompt,
                model_name='infinitetalk-fast',
                additional_payload=additional_payload)            
        
        self.video_url = video_url
        self.download_wavespeed_result(self.video_url, 'video_mp4', 'mp4')


    def download_wavespeed_result(self, result_url, field_name, ext):
        for rec in self:
            if not result_url:
                continue

            try:
                filename = f"{self.name}.{ext}"
                response = requests.get(result_url, timeout=10)
                if response.status_code == 200:
                    # response.content sudah berupa bytes
                    rec.write({
                        field_name: base64.b64encode(response.content),
                        f"{field_name}_filename": filename
                    })
                else:
                    # optional: log error / raise warning
                    raise UserError(
                        "Failed to download image from %s, status: %s", result_url, response.status_code
                    )
            except Exception as e:
                # optional: log error
                raise UserError("Error downloading image from %s: %s", result_url, e)

    def download_image(self):
        result_url = self.result_url
        field_name = 'image_png'
        ext = 'png'
        self.download_wavespeed_result(result_url, field_name, ext)
    
    def download_video(self):
        result_url = self.result_url
        field_name = 'video_mp4'
        ext = 'mp4'
        self.download_wavespeed_result(result_url, field_name, ext)