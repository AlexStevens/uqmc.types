from five import grok
from plone import api
from zope.interface import Interface
from Products.CMFCore.utils import getToolByName


grok.templatedir('templates')


class ExecutivesView(grok.View):
    grok.name('executives')
    grok.context(Interface)

    def get_executives(self):
        return self
