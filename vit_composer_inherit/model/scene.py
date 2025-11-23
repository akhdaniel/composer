#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)
from .libs.wavespeed import Wavespeed
import requests
import base64

class scene(models.Model):
    _name = "vit.scene"
    _inherit = "vit.scene"

    def action_generate_image(self, ):
        api_key = self.env["ir.config_parameter"].sudo().get_param("wavespeed_api_key")
        ws = Wavespeed(api_key=api_key)
        ref_image=None

        if self.actor_ids:
            actor = self.actor_ids[0]
            base_url =self.env["ir.config_parameter"].sudo().get_param("web.base_url")
            ref_image = f"{base_url}/web/image/vit.actor/{actor.id}/image?unique=1763886100000"

        image_url = ws.generate_image(
            image_prompt=self.image_prompt,
            model_name='wavespeed-ai/flux-krea-dev-lora',
            reference_image_url=ref_image)
        
        self.image_url = image_url
        self.download_image()

    def download_image(self, ):
        for rec in self:
            if not rec.image_url:
                continue

            try:
                response = requests.get(rec.image_url, timeout=10)
                if response.status_code == 200:
                    # response.content sudah berupa bytes
                    rec.image_png = base64.b64encode(response.content)
                else:
                    # optional: log error / raise warning
                    raise UserError(
                        "Failed to download image from %s, status: %s", rec.image_url, response.status_code
                    )
            except Exception as e:
                # optional: log error
                raise UserError("Error downloading image from %s: %s", rec.image_url, e)
            

    def action_generate_video(self, ):
        pass

