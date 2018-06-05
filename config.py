# -*- coding: utf-8 -*-
__author__ = '樱花落舞'
class global_var:
    name = None

def set_name(name):
    global_var.name = name

def get_name():
    return global_var.name