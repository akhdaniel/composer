#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError

class scene(models.Model):

    _name = "vit.scene"
    _description = "vit.scene"


    def action_generate_image(self, ):
        pass


    def action_generate_video(self, ):
        pass


    def download_image(self, ):
        pass


    @api.depends("song_clip_ids")
    def _get_clip_names(self, ):
        """
        {
        "@api.depends":["song_clip_ids"]
        }
        """
        pass


    def download_video(self, ):
        pass


    def action_reload_view(self):
        pass

    name = fields.Char( required=True, copy=False, string=_("Name"))
    description = fields.Text( string=_("Description"))
    start = fields.Float( string=_("Start"))
    end = fields.Float( string=_("End"))
    duration = fields.Float( string=_("Duration"))
    lip_sync = fields.Boolean( string=_("Lip Sync"))
    image_prompt = fields.Text( string=_("Image Prompt"))
    image_url = fields.Text( string=_("Image Url"))
    image_png = fields.Binary( string=_("Image Png"))
    image_png_filename = fields.Char( string=_("Image Png Filename"))
    video_prompt = fields.Text( string=_("Video Prompt"))
    video_url = fields.Text( string=_("Video Url"))
    video_mp4 = fields.Binary( string=_("Video Mp4"))
    video_mp4_filename = fields.Char( string=_("Video Mp4 Filename"))
    clip_names = fields.Char(compute="_get_clip_names",  string=_("Clip Names"))
    lyrics = fields.Text( string=_("Lyrics"))


    def copy(self, default=None):
        default = dict(default or {})
        default.update({
            'name': self.name + ' (Copy)'
        })
        return super(scene, self).copy(default)

    actor_ids = fields.Many2many(comodel_name="vit.actor",  string=_("Actor"))
    song_id = fields.Many2one(comodel_name="vit.song",  string=_("Song"))
    song_clip_ids = fields.Many2many(comodel_name="vit.song_clip",  string=_("Song Clip"))
