#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError
from .libs.wavespeed import Wavespeed
import requests
import base64

class actor(models.Model):

    _name = "vit.actor"
    _inherit = "vit.actor"

    def action_generate_actor(self, ):
        api_key = self.env["ir.config_parameter"].sudo().get_param("wavespeed_api_key")
        ws = Wavespeed(api_key=api_key)
        image_url = ws.generate_image(image_prompt=self.image_prompt, model_name='bytedance/seedream-v3')
        self.image_url = image_url
        self.download_image()

    def download_image(self):
        for rec in self:
            image_url = rec.image_url
            if not image_url :
                continue

            try:
                response = requests.get(image_url, timeout=10)
                if response.status_code == 200:
                    # response.content sudah berupa bytes
                    rec.image = base64.b64encode(response.content)
                else:
                    # optional: log error / raise warning
                    raise UserError(
                        "Failed to download image from %s, status: %s", image_url, response.status_code
                    )
            except Exception as e:
                # optional: log error
                raise UserError("Error downloading image from %s: %s", image_url, e)