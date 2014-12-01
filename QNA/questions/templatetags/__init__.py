'''
Created on Oct 13, 2014

@author: ejiahug
'''
import re

splitter = re.compile(r'\s*=\s*')
matcher = re.compile(r'^.+=.+$')

def argument_parser(arguments):
    return dict(splitter.split(s) for s in arguments if matcher.match(s))