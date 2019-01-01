# Copyright 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import random

import webapp2
import urllib2

GCF_URL = 'https://us-central1-blinkist-228203.cloudfunctions.net/send_email?sunday=true'

class SundayBlinkistEmail(webapp2.RequestHandler):
    def get(self):
        request = urllib2.Request(GCF_URL, headers={"cronrequest" : "true"})
        contents = urllib2.urlopen(request).read()

app = webapp2.WSGIApplication([
    ('/sunday', SundayBlinkistEmail),
    ], debug=True)
