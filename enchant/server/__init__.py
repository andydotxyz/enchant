from flask import Flask, abort, render_template
from graphene import Enum, List, NonNull, ObjectType, String, Schema
from flask_graphql import GraphQLView

from enchant import model, data

def get_site_or_abort(sitename):
    site = model.get_site(data.SITES, sitename)
    if site is None:
        abort(404)
    return site

def get_page_or_abort(site, pagename):
    page = site.get_page(pagename)
    if page is None:
        abort(404)
    return page

class Query(ObjectType):
    sites = List(model.Site, description='Enchant Sites')
    def resolve_sites(self, args, context, info):
        return data.SITES

view_func = GraphQLView.as_view('graphql', schema=Schema(query=Query))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html', title='Enchant CMS')

@app.route('/sites')
def sitelist():
    return render_template('sites.html', title='Enchant CMS Sites',
            sitelist = data.SITES)

@app.route('/sites/<sitename>')
def site(sitename):
    site = get_site_or_abort(sitename)

    return render_template('hosted.html', site=site, page=site.pages[0])

@app.route('/sites/<sitename>/<pagename>')
def page(sitename, pagename):
    site = get_site_or_abort(sitename)
    page = get_page_or_abort(site, pagename)

    return render_template('hosted.html', site=site, page=page)

app.add_url_rule('/api', view_func=view_func)

if __name__ == '__main__':
    app.run()

