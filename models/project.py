from odoo import models, api

class Project(models.Model):

    _inherit = 'project.task'

    @api.depends('planned_date_begin')
    def _compute_planned_date_begin(self):
        for task in self:
            if task.x_studio_expect_time:
                print(task.x_studio_expect_time, '\n \n \n \n')