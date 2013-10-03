# -*- coding: utf-8 -*-
VERSION = (0, 0, 7)
AUTHOR = "Rob Charlwood, Florian Demmer"
COPYRIGHT = "2010-2013"
PROJECT_NAME = "mothertongue"

def get_version(svn=False, limit=3):
    """Returns the version as a human-format string."""
    v = '.'.join([str(i) for i in VERSION[:limit]])
    return v

def get_author():
    return u'%s' % AUTHOR

def get_copyright():
    return u'%s' % COPYRIGHT

def get_appname():
    return u'%s' % PROJECT_NAME
