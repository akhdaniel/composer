from odoo.tests.common import TransactionCase
from odoo.addons.vit_composer.tests.common import VitComposerCommon

from odoo.exceptions import UserError
from odoo.tests import tagged

import logging
_logger = logging.getLogger(__name__)

@tagged('post_install', '-at_install')
class SongTestCase(VitComposerCommon):

	def test_vit_song_count(cls):
		_logger.info(' -------------------- test record count -----------------------------------------')
		cls.assertEqual(
		    4,
		    len(cls.songs)
		)