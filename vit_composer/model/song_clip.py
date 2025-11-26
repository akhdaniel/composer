#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError

class song_clip(models.Model):

    _name = "vit.song_clip"
    _description = "vit.song_clip"


    @api.depends("clip_mp3")
    def _get_clip_url(self, ):
        """
        {
        "@api.depends":["clip_mp3"]
        }
        """
        pass


    @api.depends("scene_ids")
    def _get_scene_names(self, ):
        """
        {
        "@api.depends":["scene_ids"]
        }
        """
        pass


    def action_reload_view(self):
        pass

    name = fields.Char( required=True, copy=False, string=_("Name"))
    clip_mp3 = fields.Binary( string=_("Clip Mp3"))
    clip_mp3_filename = fields.Char( string=_("Clip Mp3 Filename"))
    clip_mp3_url = fields.Char(compute="_get_clip_url",  string=_("Clip Mp3 Url"))
    scene_names = fields.Char(compute="_get_scene_names",  string=_("Scene Names"))


    def copy(self, default=None):
        default = dict(default or {})
        default.update({
            'name': self.name + ' (Copy)'
        })
        return super(song_clip, self).copy(default)

