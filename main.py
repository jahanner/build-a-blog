                                                                                       
import webapp2
import jinja2
import os
from google.appengine.ext import db


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

class Post(db.Model):
    title = db.StringProperty(required = True)
    blogcontent = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)


class ViewPostHandler(Handler):
    def get(self, id):
        content = Post.get_by_id(int(id))
        self.render('permalink.html', content = content)


class FrontPage(Handler):
    def get(self):
        content = db.GqlQuery("SELECT * FROM Post ORDER BY created DESC LIMIT 5")
        self.render("front_page.html", content = content)

class NewPost(Handler):
    def get(self):
        self.render("new_post.html")

    def post(self):
        title = self.request.get("title")
        blogcontent = self.request.get("blogcontent")
        error_title = ""
        error_content = ""

        if title and blogcontent:
            blog = Post(title = title, blogcontent = blogcontent)
            blog.put()
            self.redirect('/blog/' + str(blog.key().id()))
        else:
            if title:
                error_content = "Content is required."
            if blogcontent:
                error_title = "A title is required."
            self.render("new_post.html", title = title, blogcontent = blogcontent, error_content = error_content, error_title = error_title)

app = webapp2.WSGIApplication([
  ('/', FrontPage),
  ('/blog', FrontPage),
  (webapp2.Route('/blog/<id:\d+>', ViewPostHandler)),
  ('/new_post', NewPost),
], debug=True)
