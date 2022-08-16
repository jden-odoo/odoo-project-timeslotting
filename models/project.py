from unicodedata import name
from odoo import models, api, fields, _
from datetime import timedelta


class Project(models.Model):

    _inherit = 'project.task'

    @api.onchange('planned_date_begin')
    def _foward_schedule_blocked_tasks(self, offsetInit=timedelta(hours=0)):
        # print('self._ids', self._ids)

        g1, g2 = False, False

        for task in self._origin:
            if task.planned_date_begin:
                # create a timedelta for the old begin date
                oldDateBegin = timedelta(days=task.planned_date_begin.day, hours=task.planned_date_begin.hour)
                g1 = True

        for task in self.browse(self._ids):
            if task.planned_date_begin and task.x_studio_expect_time:
                task.write({'planned_date_end': task.planned_date_begin + timedelta(hours=task.x_studio_expect_time)})
                # create a timedelta for the new begin date
                newDateBegin = timedelta(days=task.planned_date_begin.day, hours=task.planned_date_begin.hour)
                g2 = True
        
        for task in self.browse(self._ids):
            if task.planned_date_begin and task.x_studio_expect_time and g1 and g2:
                # compute time delta between old and new begin date
                delta = timedelta(hours = (newDateBegin - oldDateBegin).total_seconds() / 3600)
                # check if delta value is positive or negative
                if delta > timedelta(hours=0):
                    for subtask in self.search([('project_id', '=', self.project_id.id)]):
                        # check if subtask begin date is after newDateBegin
                        if timedelta(days=subtask.planned_date_begin.day, hours=subtask.planned_date_begin.hour) >= newDateBegin:
                            # compute new subtask begin date
                            newSubtaskBegin = subtask.planned_date_begin + delta
                            # update subtask begin date
                            subtask.write({'planned_date_begin': newSubtaskBegin})
                            # update subtask end date
                            subtask.write({'planned_date_end': newSubtaskBegin + timedelta(hours=subtask.x_studio_expect_time)})