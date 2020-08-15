#!/usr/bin/python
# -*- coding: UTF-8 -*-

import fire
import cli_freeswitch
import cli_openresty


class Dcli(object):
    def __init__(self):
        self.openresty = cli_openresty.OpenrestyCli()
        self.freeswitch = cli_freeswitch.FreeswitchCli()


if __name__ == "__main__":
    fire.Fire(Dcli)
