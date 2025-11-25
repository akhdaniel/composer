#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError

class prompt(models.Model):

    _name = "vit.prompt"
    _description = "vit.prompt"


    def action_reload_view(self):
        pass

    name = fields.Char( required=True, copy=False, string=_("Name"))
    user_prompt = fields.Text( string=_("User Prompt"))
    system_prompt = fields.Text( string=_("System Prompt"))


    def copy(self, default=None):
        default = dict(default or {})
        default.update({
            'name': self.name + ' (Copy)'
        })
        return super(prompt, self).copy(default)

