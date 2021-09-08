

from odoo import models, fields, api


class test_absensi(models.Model):
	_name = 'test_absensi.test_absensi'
	_rec_name = 'number'
	_description = 'test_absensi'

	number = fields.Char('Number',readonly=True, required=True, copy=False, default='New')
	date = fields.Date('Tanggal')
	in_date = fields.Float('In Date')
	out_date = fields.Float('Out Date')
	name = fields.Char('Keterangan')


	line_ids = fields.One2many('test_absensi.test_absensi_line','absensi_id','Data Absensi')

	@api.model
	def create(self, vals):
		if vals.get('number', 'New') == 'New':
			vals['number'] = self.env['ir.sequence'].next_by_code('self.absensi') or 'New'
		result = super(test_absensi, self).create(vals)
		return result




class test_absensi_line(models.Model):
	_name = 'test_absensi.test_absensi_line'
	_description = 'test_absensi_line'

	absensi_id = fields.Many2one('test_absensi.test_absensi')
	time = fields.Float(string='Jam')
	partner_id = fields.Many2one('res.partner','Nama Karyawan')
	state = fields.Selection([
		('terlambat', 'Terlambat'),
		('ontime', 'Ontime'),
	], string="Status", compute='get_state', readonly='True')


	@api.depends('time')
	def get_state(self):
		for line in self:
			in_date = line.absensi_id.in_date
			if line.time > in_date:
				line.state = 'terlambat'
			else:
				line.state = 'ontime'









