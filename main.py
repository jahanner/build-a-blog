#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
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
#
import os
import webapp2
import jinja2

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),autoescape = True)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class MainHandler(Handler):
    def get(self):
        self.render("new_post_views.html")

class NewPost(Handler):
    def get(self):
        self.render("new_post.html")

    def post(self):
        title = self.request.get("title")
        blogcontent = self.request.get("blogcontent")
        error_title = ""
        error_content = ""


        if title and blogcontent:
            self.write("hey")
        else:
            if title:
                error_content = "We need Content"
            if blogcontent:
                error_title = "We need title"
            self.render("new_post.html",title = title, blogcontent = blogcontent, error_content = error_content, error_title = error_title)

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/blog', MainHandler),
    ('/newpost', NewPost),
], debug=True)
