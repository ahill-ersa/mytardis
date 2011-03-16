# -*- coding: utf-8 -*-
#
# Copyright (c) 2010-2011, Monash e-Research Centre
#   (Monash University, Australia)
# Copyright (c) 2010-2011, VeRSI Consortium
#   (Victorian eResearch Strategic Initiative, Australia)
# All rights reserved.
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#    *  Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#    *  Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#    *  Neither the name of the VeRSI, the VeRSI Consortium members, nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE REGENTS AND CONTRIBUTORS ``AS IS'' AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE REGENTS AND CONTRIBUTORS BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
"""
test_views.py
http://docs.djangoproject.com/en/dev/topics/testing/

.. moduleauthor::  Russell Sim <russell.sim@monash.edu>
.. moduleauthor::  Steve Androulakis <steve.androulakis@monash.edu>

"""
from django.test import TestCase
from tardis.tardis_portal import models

class ParameterSetManagerTestCase(TestCase):

    def setUp(self):
        from django.contrib.auth.models import User
        from tempfile import mkdtemp

        user = 'tardis_user1'
        pwd = 'secret'
        email = ''
        self.user = User.objects.create_user(user, email, pwd)

        self.test_dir = mkdtemp()

        self.exp = models.Experiment(title='test exp1',
                                institution_name='monash',
                                created_by=self.user,
                                )
        self.exp.save()

        self.dataset = models.Dataset(description="dataset description...",
                                 experiment=self.exp)
        self.dataset.save()

        self.datafile = models.Dataset_File(dataset=self.dataset,\
            filename="testfile.txt", url="file://1/testfile.txt")

        self.datafile.save()

        self.schema = models.Schema(namespace="http://localhost/psmtest/df/",\
            name="Parameter Set Manager", type=3)

        self.schema.save()

        self.parametername1 = models.ParameterName(\
            schema=self.schema, name="parameter1",\
            full_name="Parameter 1")

        self.parametername1.save()

        self.parametername2 = models.ParameterName(\
            schema=self.schema, name="parameter2",\
            full_name="Parameter 2", is_numeric=True)

        self.parametername2.save()

        self.datafileparameterset = models.DatafileParameterSet(\
            schema=self.schema, dataset_file=self.datafile)

        self.datafileparameterset.save()

        self.datafileparameter1 = models.DatafileParameter(\
            parameterset=self.datafileparameterset,\
            name=self.parametername1, string_value="test1")

        self.datafileparameter1.save()

        self.datafileparameter2 = models.DatafileParameter(\
            parameterset=self.datafileparameterset,\
            name=self.parametername2, numerical_value=2)

        self.datafileparameter2.save()

    def tearDown(self):

        self.exp.delete()
        self.user.delete()
        self.parametername1.delete()
        self.parametername2.delete()
        self.schema.delete()

    def test_get_schema(self):

        self.assertTrue(True)

    def test_get_param(self):

        self.assertTrue(True)

    def get_params(self):

        self.assertTrue(True)

    def set_param(self):

        self.assertTrue(True)

    def new_param(self):

        self.assertTrue(True)

    def set_param_list(self):

        self.assertTrue(True)

    def set_params_from_dict(self):

        self.assertTrue(True)

    def delete_params(self):

        self.assertTrue(True)
