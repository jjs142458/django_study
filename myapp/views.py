from difflib import HtmlDiff
from select import select
from turtle import title
from urllib import request
from django.http import HttpResponse
from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt

nextid = 4
topics = [
    {'id': 1, 'title': 'routing', 'body': 'Routing is...'},
    {'id': 2, 'title': 'view', 'body': 'view is...'},
    {'id': 3, 'title': 'model', 'body': 'model is...'}
]
# Create your views here.


def HTMLtem(articleTag, id=None):
    global topics
    ol = ''
    for topic in topics:
        ol += f'<li><a href=/read/{topic["id"]}/>{topic["title"]}</a></li>'
    return f'''
    <html>
    <body>
        <h1><a href='/'>abc</a></h1>
        <ol>
            {ol}
        </ol>

       {articleTag}
        <ul>
            <li><a href ="/create/">create</a></li>
            <li>    
                <form action="/delete/" method="post">
                    <input type="hidden" name="id" value={id}>
                    <input type="submit" value="delete">
                </form>
            </li>
            <li><a href="/update/{id}">update</a></li>
        </ul>
    </body>
    </html>'''


def index(req):
    article = '''
    <h2>welcome</h2>
    Hello, Django
    '''
    return HttpResponse(HTMLtem(article))


@csrf_exempt
def create(req):
    global nextid
    if req.method == 'GET':

        article = '''
        <form action="/create/" method="post">
            <p><input type="text" name="title" placeholder="title"></p>
            <p><textarea name="body" placeholder="body"></textarea></p>
            <p><input type="submit"></p>
        </form>
        '''
        return HttpResponse(HTMLtem(article))
    elif req.method == 'POST':
        title = req.POST["title"]
        body = req.POST["body"]
        newtopic = {'id': nextid, 'title': title, 'body': body}
        topics.append(newtopic)
        url = '/read/'+str(nextid)
        nextid += 1
        return redirect(url)


def read(req, id):
    global topics
    article = ''
    for topic in topics:
        if topic["id"] == int(id):
            article = f'<h2>{topic["title"]}</h2>{topic["body"]}'
    return HttpResponse(HTMLtem(article, id))


@csrf_exempt
def delete(req):
    global topics
    if req.method == 'POST':
        id = req.POST["id"]
        newtopics = []
        for topic in topics:
            if topic["id"] != int(id):
                newtopics.append(topic)
        topics = newtopics
        return redirect('/')


@csrf_exempt
def update(req, id):
    global topics
    if req.method == 'GET':
        for topic in topics:
            if topic["id"] == int(id):
                selectedTopic = {
                    "title": topic["title"],
                    "body": topic["body"]
                }
        article = f'''
        <form action="/update/{id}/" method="post">
            <p><input type="text" name="title" placeholder="title" value={selectedTopic["title"]}></p>
            <p><textarea name="body" placeholder="body">{selectedTopic["body"]}</textarea></p>
            <p><input type="submit"></p>
        </form>
        '''
        return HttpResponse(HTMLtem(article, id))
    elif req.method == 'POST':
        title = req.POST["title"]
        body = req.POST["body"]

        for topic in topics:
            if topic["id"] == int(id):
                topic["title"] = title
                topic["body"] = body

        return redirect(f'/read/{id}')
