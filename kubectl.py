#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# (c) 2016, Nandaja Varma <nandaja.varma@gmail.com>
#
#
#
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this software.  If not, see <http://www.gnu.org/licenses/>.

class Kubectl:

    def __init__(self, module):
        self.module = module
        self.action = self._validated_params('action')


    def run(self):
        action_func = {
                        'create': self.kubectl_create
                      }.get(self.action)

        try:
            return action_func()
        except:
            msg = "No method found for given action"
            self.get_output(rc=3, out=msg, err=msg)


    def kubectl_create(self):
        filename = self.module.params['filename']
        if filename:
            return "%s -f ./%s" % (self.action, filenae)

    def _validated_params(self, opt):
        value = self.module.params[opt]
        if value is None:
            msg = "Please provide %s option in the playbook!" % opt
            self.module.fail_json(msg=msg)
        return value

    def get_command(self, options):
        cmd = self.module.get_bin_path('kubectl', True) + options
        return cmd

    def get_output(self, rc=0, out=None, err=None):
        if rc:
            self.module.fail_json(msg=err, rc=rc, err=err, out=out)
        else:
            self.module.exit_json(changed=1, msg=out)

def main():
    module = AnsibleModule(
            argument_spec = dict(
                action          = dict(required=True, choices=["create",
                                    "stop", "run", "exec", "get"]),
                name            = dict(required=False),
                filename        = dict()
                ),
            supports_check_mode = True
            )


    kube = Kubectl(module)
    options = kube.run()
    cmd = kube.get_command(options)
    rc, out, err = module.run_command(cmd)
    kube.get_output(rc, out, err)



from ansible.module_utils.basic import *

if __name__ == '__main__':
    main()
