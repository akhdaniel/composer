#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError

class actor(models.Model):

    _name = "vit.actor"
    _description = "vit.actor"


    def generate_actor(self, ):
        pass


    def action_reload_view(self):
        pass

    name = fields.Char( required=True, copy=False, string=_("Name"))
    image = fields.Binary( string=_("Image"))
    image_prompt = fields.Text( string=_("Image Prompt"))
    image_url = fields.Text( string=_("Image Url"))


    def copy(self, default=None):
        default = dict(default or {})
        default.update({
            'name': self.name + ' (Copy)'
        })
        return super(actor, self).copy(default)

    song_id = fields.Many2one(comodel_name="vit.song",  string=_("Song"))
