#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError

class song_clip(models.Model):

    _name = "vit.song_clip"
    _inherit = "vit.song_clip"


    @api.depends("clip_mp3")
    def _get_clip_url(self, ):
        """
        {
        "@api.depends":["clip_mp3"]
        }
        """
        base_url =self.env["ir.config_parameter"].sudo().get_param("web.base.url")
        for rec in self:
            rec.clip_mp3_url = f"{base_url}/web/image/vit.song_clip/{rec.id}/clip_mp3?unique=1763886100000"

    @api.depends("scene_ids")
    def _get_scene_names(self, ):
        """
        {
        "@api.depends":["scene_ids"]
        }
        """
        for rec in self:
            rec.scene_names = ",".join(rec.scene_ids.mapped('name'))