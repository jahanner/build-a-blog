
import os
import webapp2
import jinja2
from google.appengine.ext import db


template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),autoescape = True)

# class Art(db.Model):
#     title = db.StringProperty(required = True)
#     art = dc.TextProperty(required = True)
#     created = db.DateTimeProperty(auto_now_add = True)


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
                error_content = "Content is required."
            if blogcontent:
                error_title = "A title is required."
            self.render("new_post.html",title = title, blogcontent = blogcontent, error_content = error_content, error_title = error_title)

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/blog', MainHandler),
    ('/new_post', NewPost),
], debug=True)


# Need to set up database
# Need to make homepage with 5 newest posts
# Still need to add new dynamic webpage based on database
