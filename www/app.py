#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Michael Liao'

'''
async web application.
这是框架的函数入口，如果想要使用‘程序启动后，当用户修改了代码，让程序重新启动’的功能，可以使用当前目录下的pymonitor.py作为程序的启动文件
'''

import logging; logging.basicConfig(level=logging.INFO)     #使用了logging,此处level设置的log的优先级，其warning error都会输出打印，
                                                            #优先级的排序：error > warning> info> debug
                                                            #此外关于日志的输出位置等信息也在这进行配置，比如默认是输出到控制台，当然还可以输出到文件。
import asyncio, os, json, time
from datetime import datetime

from aiohttp import web
from jinja2 import Environment, FileSystemLoader

from config import configs

import orm
from coroweb import add_routes, add_static

from handlers import cookie2user, COOKIE_NAME

#jianja2是python服务器常用的模板库，关于模板，请参见jsx的写法，其实他就是把html文件的特定的东西进行动态的替换。
#使用这个框架需要注意“{{}}”等符号，与模板中的vue框架中的符号”{{}}“等符号冲突了，这些符号只会被jianja2进行处理（模板就是先被jianja2渲染的）
def init_jinja2(app, **kw):
    logging.info('init jinja2...')
    options = dict(
        autoescape = kw.get('autoescape', True),
        block_start_string = kw.get('block_start_string', '{%'),
        block_end_string = kw.get('block_end_string', '%}'),
        variable_start_string = kw.get('variable_start_string', '{{'),
        variable_end_string = kw.get('variable_end_string', '}}'),
        auto_reload = kw.get('auto_reload', True)
    )  #获取的值都是默认的值（获取不到），可以自定义符号
    path = kw.get('path', None) #L39-L43 配置模板文件路径
    if path is None:
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')  ##默认，会在当前目录下寻找模板文件
    logging.info('set jinja2 template path: %s' % path)
    env = Environment(loader=FileSystemLoader(path), **options)
    # L45-L48 配置处理管道（前端的叫法），一般是对一些数据进行格式化显示
    filters = kw.get('filters', None)
    if filters is not None:
        for name, f in filters.items():
            env.filters[name] = f
    app['__templating__'] = env

#由于aiohttp是基于asyncio（一个异步框架），所有异步操作的函数（以yield from /await返回结果的都是异步函数）
#FAQ ：handlers.py文件中关于具体URl处理的函数未加@asyncio.coroutine？
#      这些函数的修饰在coroweb.py的add_route中动态加了异步修饰
#以下四个函数是web的中间件部分，使用在L170
@asyncio.coroutine
def logger_factory(app, handler):
    @asyncio.coroutine
    def logger(request):
        logging.info('Request: %s %s' % (request.method, request.path))
        # yield from asyncio.sleep(0.3)
        return (yield from handler(request))
    return logger

@asyncio.coroutine
def auth_factory(app, handler):
    '''
    获取请求的cookie,并处理
    :param app:
    :param handler:
    :return:
    '''
    @asyncio.coroutine
    def auth(request):
        logging.info('check user: %s %s' % (request.method, request.path))
        request.__user__ = None
        cookie_str = request.cookies.get(COOKIE_NAME)
        if cookie_str:
            user = yield from cookie2user(cookie_str)
            if user:
                logging.info('set current user: %s' % user.email)
                request.__user__ = user
        if request.path.startswith('/manage/') and (request.__user__ is None or not request.__user__.admin):
            return web.HTTPFound('/signin')
        return (yield from handler(request))
    return auth
#未使用
@asyncio.coroutine
def data_factory(app, handler):
    '''
    查看请求的数据
    :param app:
    :param handler:
    :return:
    '''
    @asyncio.coroutine
    def parse_data(request):
        if request.method == 'POST':
            if request.content_type.startswith('application/json'):
                request.__data__ = yield from request.json()
                logging.info('request json: %s' % str(request.__data__))
            elif request.content_type.startswith('application/x-www-form-urlencoded'):
                request.__data__ = yield from request.post()
                logging.info('request form: %s' % str(request.__data__))
        return (yield from handler(request))
    return parse_data

@asyncio.coroutine
def response_factory(app, handler):
    '''
    主要是对返回数据的数据头进行处理。用yield from handler(request)隔开
    :param app:
    :param handler:
    :return:
    '''
    @asyncio.coroutine
    def response(request):
        logging.info('Response handler...')
        r = yield from handler(request)    #这句话很关键，需要等待handers.py中的url函数的处理结果，下面的一些代码是对返回类型进行判断和组装。这个函数运行完后，一个响应就完整结束。
        if isinstance(r, web.StreamResponse):  #流数据
            return r
        if isinstance(r, bytes):  #bytes
            resp = web.Response(body=r)
            resp.content_type = 'application/octet-stream'
            return resp
        if isinstance(r, str):
            if r.startswith('redirect:'):
                return web.HTTPFound(r[9:])
            resp = web.Response(body=r.encode('utf-8'))
            resp.content_type = 'text/html;charset=utf-8'
            return resp
        if isinstance(r, dict):
            template = r.get('__template__')  #类比getattr
            if template is None: #dict转json
                resp = web.Response(body=json.dumps(r, ensure_ascii=False, default=lambda o: o.__dict__).encode('utf-8'))
                resp.content_type = 'application/json;charset=utf-8'
                return resp
            else:
                r['__user__'] = request.__user__
                resp = web.Response(body=app['__templating__'].get_template(template).render(**r).encode('utf-8'))
                resp.content_type = 'text/html;charset=utf-8'
                return resp
        if isinstance(r, int) and r >= 100 and r < 600:
            return web.Response(r)
        if isinstance(r, tuple) and len(r) == 2:
            t, m = r
            if isinstance(t, int) and t >= 100 and t < 600:
                return web.Response(t, str(m))
        # default:
        resp = web.Response(body=str(r).encode('utf-8'))
        resp.content_type = 'text/plain;charset=utf-8'
        return resp
    return response
#这里配置了一个管道处理的函数
def datetime_filter(t):
    delta = int(time.time() - t)
    if delta < 60:
        return u'1分钟前'
    if delta < 3600:
        return u'%s分钟前' % (delta // 60)
    if delta < 86400:
        return u'%s小时前' % (delta // 3600)
    if delta < 604800:
        return u'%s天前' % (delta // 86400)
    dt = datetime.fromtimestamp(t)
    return u'%s年%s月%s日' % (dt.year, dt.month, dt.day)

@asyncio.coroutine
def init(loop):
    yield from orm.create_pool(loop=loop, **configs.db)
    app = web.Application(loop=loop, middlewares=[
        logger_factory, auth_factory, response_factory
    ])   #绑定的这3个函数，会在进入post get函数之前进入。
    init_jinja2(app, filters=dict(datetime=datetime_filter))   #传入模板的处理函数，使用方式： {{ blog.created_at|datetime }}，可以设置很多这样的函数。
    add_routes(app, 'handlers')  #把handel文件下的路径和函数关联起来
    add_static(app)
    srv = yield from loop.create_server(app.make_handler(), '127.0.0.1', 9000)
    logging.info('server started at http://127.0.0.1:9000...')
    return srv

loop = asyncio.get_event_loop()
loop.run_until_complete(init(loop))
loop.run_forever()
