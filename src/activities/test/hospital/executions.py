# -*- coding: utf-8 -*-
#
# Copyright 2009: Johannes Raggam, BlueDynamics Alliance
#                 http://bluedynamics.com
# GNU Lesser General Public License Version 2 or later

__author__ = """Johannes Raggam <johannes@raggam.co.at>"""
__docformat__ = 'plaintext'

from activities.runtime.interfaces import IExecution
from zope.interface import implements
from zope.component import getGlobalSiteManager
import sys

class Diagnosis(object):
    implements(IExecution)
    name = "diagnosis"

    def __call__(self, action_info, stereotype_info, data):
        if data['patient'].health < 30:
            data['diagnosis'] = "acute"
        else:
            data['diagnosis'] = "normal"
        return data

class DataAcquisition(object):
    implements(IExecution)
    name = "data-acquisition"

    def __call__(self, action_info, stereotype_info, data):
        data['name'] = data['patient'].name
        return data

class DataVerification(object):
    implements(IExecution)
    name = "data-verification"

    def __call__(self, action_info, stereotype_info, data):
        # delete this key, because at the same time a diagnosis is made
        # which leads to different values and a conflict when trying to merge
        del data['diagnosis']
        return data

class Therapy(object):
    implements(IExecution)
    name = "therapy"

    def __call__(self, action_info, tgv_dict, data):
        if 'variation' in tgv_dict.keys() and \
           tgv_dict['variation'] == "acute":
            data['patient'].health += 30
        else:
            data['patient'].health += 40

        return data


gsm = getGlobalSiteManager()
gsm.registerUtility(component=Diagnosis(), name=Diagnosis.name)
gsm.registerUtility(component=DataAcquisition(), name=DataAcquisition.name)
gsm.registerUtility(component=DataVerification(), name=DataVerification.name)
gsm.registerUtility(component=Therapy(), name=Therapy.name)

#