#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError

class song(models.Model):

    _name = "vit.song"
    _description = "vit.song"


    def action_generate_song(self, ):
        pass


    def action_generate_scenes(self, ):
        pass


    def action_split_song(self, ):
        pass


    def action_generate_scene_images(self, ):
        pass


    def action_generate_scene_videos(self, ):
        pass


    @api.depends("song_mp3")
    def _get_song_url(self, ):
        """
        {
        "@api.depends":["song_mp3"]
        }
        """
        pass


    def action_download_capcut(self, ):
        pass


    def action_reload_view(self):
        pass

    name = fields.Char( required=True, copy=False, string=_("Name"))
    prompt = fields.Text(string="Song Prompt")
    lyrics = fields.Text( string=_("Lyrics"))
    duration = fields.Float( string=_("Duration"))
    original_url = fields.Char( string=_("Original Url"))
    song_mp3 = fields.Binary( string=_("Song Mp3"))
    song_mp3_filename = fields.Char( string=_("Song Mp3 Filename"))
    song_mp3_url = fields.Char(compute="_get_song_url",  string=_("Song Mp3 Url"))
    song_clips_zip = fields.Binary( string=_("Song Clips Zip"))
    song_clips_zip_filename = fields.Char( string=_("Song Clips Zip Filename"))
    scene_images_zip = fields.Binary( string=_("Scene Images Zip"))
    scene_images_zip_filename = fields.Char( string=_("Scene Images Zip Filename"))
    scene_videos_zip = fields.Binary( string=_("Scene Videos Zip"))
    scene_videos_zip_filename = fields.Char( string=_("Scene Videos Zip Filename"))


    def copy(self, default=None):
        default = dict(default or {})
        default.update({
            'name': self.name + ' (Copy)'
        })
        return super(song, self).copy(default)

    gpt_model_id = fields.Many2one(comodel_name="vit.gpt_model",  string=_("Gpt Model"))
    scene_prompt_id = fields.Many2one(comodel_name="vit.prompt",  string=_("Scene Prompt"))
    scene_ids = fields.One2many(comodel_name="vit.scene",  inverse_name="song_id",  string=_("Scene"))
    actor_ids = fields.One2many(comodel_name="vit.actor",  inverse_name="song_id",  string=_("Actor"))
