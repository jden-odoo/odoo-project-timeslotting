from odoo import models, api
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

        