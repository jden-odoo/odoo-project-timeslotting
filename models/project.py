from odoo import models, api, fields, _
from datetime import timedelta
import datetime as datetime


class Project(models.Model):

    _inherit = 'project.task'

    no_blocks = fields.Boolean(string='Is Blocked', default=True)

    @api.onchange('planned_date_begin', 'planned_date_end')
    def _foward_schedule_blocked_tasks(self, offsetInit=timedelta(hours=0)):
        '''
        if 'x_studio_expect_time' in self.env['project.task']._fields:
            for task in self:
                if task.x_studio_expect_time:
                    hours = task.x_studio_expect_time % 1
                    minutes = (task.x_studio_expect_time - hours) * 60
                    task.planned_date_begin = task.planned_date_end - timedelta(hours=hours, minutes=minutes)
        '''
        for task in self:
            offset = timedelta(hours=0) + offsetInit

            potential_blocks = task.env['project.task'].search([
                ('id', 'in', task.depend_on_ids.ids)])
            for potential_block in potential_blocks:
                print('Foward Scheduling', potential_block.name)
                if potential_block.stage_id.name != 'Done':
                    potential_block.planned_date_begin = task.planned_date_end + offset + timedelta(hours=1)

                    potential_block.planned_date_end = task.planned_date_end + offset + timedelta(hours=potential_block.x_studio_expect_time) + timedelta(hours=1)
                    offset += timedelta(hours=potential_block.x_studio_expect_time) + timedelta(hours=1)
                    offsetInit += offset
                    potential_block._foward_schedule_blocked_tasks(offsetInit=offsetInit)
    '''
    @api.onchange('depend_on_ids')
    def _onchage_depend_on_ids(self):
        for task in self:
            potential_blocks = task.env['project.task'].search([
                ('id', 'in', task.depend_on_ids.ids)])
            for potential_block in potential_blocks:
                if potential_block.stage_id.name != 'Done':
                    task.no_blocks = False
                    break
                else:
                    task.no_blocks = True
                print(potential_block.stage_id.name)
            if task.no_blocks:
                temp_date = fields.Datetime.to_datetime(potential_blocks[0].date_deadline)
                print('temp date', temp_date)
                task.write({'planned_date_begin': temp_date})
    '''