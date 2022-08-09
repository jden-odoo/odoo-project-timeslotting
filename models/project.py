from odoo import models, api, fields, _
from datetime import timedelta

class Project(models.Model):

    _inherit = 'project.task'

    @api.onchange('planned_date_end')
    def _compute_planned_date_begin(self):
        for task in self:
            if task.x_studio_expect_time:
                hours = task.x_studio_expect_time % 1
                minutes = (task.x_studio_expect_time - hours) * 60
                task.planned_date_begin = task.planned_date_end - timedelta(hours=hours, minutes=minutes)

    is_blocking = fields.Boolean(string='Is Blocking', default=True)

    @api.onchange('stage_id')
    def _onchange_stage_id(self):
        for task in self:
            if task.stage_id.name == 'Blocking':
                task.is_blocking = True

    @api.onchange('stage_id')
    def _onchange_stage_id(self):
        print('_onchange_stage_id')
        for task in self:
            if task.stage_id.name == 'Done' and task.is_blocking:
                # search the depend_on_ids for planned_end_date
                print(task.depend_on_ids.ids[0])
                #end_date = self.env['project.task'].search([('id', '=', task.depend_on_ids.id)])
                #print('end date', end_date, '\n \n \n \n')