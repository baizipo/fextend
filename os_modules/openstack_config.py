#!/usr/bin/env python
import json
import shutil
import sys
import ConfigParser
import shlex
import time

class Config(object):

    def __init__(self):
        self.action = None
        self.filename = None
        self.section = None
        self.key = None
        self.value = None
        # get args form ansible's task
        self.get_args()

        # check args
        for i in [self.filename, self.section, self.key]:
            self.check_arg(i)

        # read config-file
        self.config = ConfigParser.ConfigParser()
        self.config.read(self.filename)

        # handler
        if self.action == 'r':
            self.value = self.get_conf()
            print json.dumps({
                "changed" : True,
                "value"   : self.value
            })
            sys.exit(0)
        elif self.action == 'w':
            self.check_arg(self.value)
            self.backup_conf()
            self.set_conf()
            print json.dumps({
                "changed" : True,
                "msg"   : 'sussced',
            })
            sys.exit(0)
        elif self.action == 'd':
            self.backup_conf()
            self.del_conf()
            print json.dumps({
                "changed" : True,
                "msg"   : 'sussced',
            })
            sys.exit(0)
        else:
            print json.dumps({
                "failed" : True,
                "msg"    : "action must be r or w or d"
            })
            sys.exit(1)

    def del_conf(self):
        self.config.remove_option(self.section, self.key)
        self.config.write(open(self.filename, "w"))

    def backup_conf(self):
        shutil.copy(self.filename, self.filename + '-' + str(time.time()))

    def get_conf(self):
        try:
            value = self.config.get(self.section, self.key)
        except:
            print json.dumps({
                "changed" : False,
                "value"   : self.value
            })
            sys.exit(0)
        return value

    def check_arg(self, k):
        if not k:
            print json.dumps({
                "failed" : True,
                "msg"    : "please check args"
            })
            sys.exit(1)

    def set_conf(self):
        self.config.set(self.section, self.key, self.value)
        self.config.write(open(self.filename, "w"))

    def get_args(self):
        '''
        get args from ansible's task.
        support args:
            action: r or w or d
            filename: file path
            section
            key
            value: if action is w, value must set
        '''

        args_file = sys.argv[1]
        args_data = file(args_file).read()
        arguments = shlex.split(args_data)
        for arg in arguments:
            k, v =arg.split('=')
            setattr(self, k, v)


Config()
