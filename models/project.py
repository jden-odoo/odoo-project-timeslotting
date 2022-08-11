from odoo import models, api, fields, _
from datetime import timedelta
import datetime as datetime


class Project(models.Model):

    _inherit = 'project.task'

    no_blocks = fields.Boolean(string='Is Blocked', default=True)

    @api.onchange('planned_date_end')
    def _compute_planned_date_begin(self):
        if 'x_studio_expect_time' in self.env['project.task']._fields:
            for task in self:
                if task.x_studio_expect_time:
                    hours = task.x_studio_expect_time % 1
                    minutes = (task.x_studio_expect_time - hours) * 60
                    task.planned_date_begin = task.planned_date_end - timedelta(hours=hours, minutes=minutes)

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
                #temp_date = potential_blocks[0].date_deadline.to_datetime()
            if task.no_blocks:
                # print('No Blocking Tasks',potential_blocks[0].date_deadline)
                temp_date = fields.Datetime.to_datetime(potential_blocks[0].date_deadline)
                print('temp date', temp_date)
                task.write({'planned_date_begin': temp_date})
'''
    @api.onchange('stage_id')
    def _onchange_stage_id(self):
        print(self.depend_on_ids)
        print(self.user_ids)
        # for task in self:
        #     print(task)
        #     print(task.stage_id.name)
        # # set is_blocked to true if all task.stage_id.names are 'Done'
        # for task in self:
        #     print(task.stage_id.name)
        #     if task.stage_id.name != 'Done':
        #         task.is_blocked = False
        #         #break
        #     else:
        #         task.is_blocked = True
        # print(task.is_blocked)

            # if task.stage_id.name == 'Done':
            #     task.is_blocked = True
            # else:
            #     task.is_blocked = False
            # print(task.is_blocked)
            # search the depend_on_ids for planned_end_date
            #print(task.depend_on_ids.ids)
            #end_date = self.env['project.task'].search([('id', '=', task.depend_on_ids.id)])
            #print('end date', end_date, '\n \n \n \n')'''