#!/usr/bin/python

import fire

class OpenRestyCli(object):
  def install(self):
   print "Install......."

class HelloCli(object):
  def hello(self):
   print "Hello......"

class Dcli(object):
 def __init__(self):
  self.openresty = OpenRestyCli()
  self.hello = HelloCli()

if __name__ == "__main__":
 fire.Fire(Dcli)
