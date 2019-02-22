awesome.sql是数据库文件，需要手动导入mysql数据库，并在config_override.py中进行数据库的参数设置。

看文档的顺序是:
    config_default.py  config_override.py config.py  apis.py  app.py  结合handlers.py的结构看coroweb.py  models.py(orm.py的接口文件，结合数据库进行改写)  orm.py
apis.py:
    Page类和Error类
app.py:
    网站的入口函数
    init_jinja2：
           对jinja2进行初始化，指定解析块的标识符
           templates目录，以及filters（一系列）的指定
    _factory：
            会在进入post get函数之前进入。主要是对response进行预处理
            auth_factory：
                对/manage/进行权限分析，只能是管理员才能进入
            response_factory：
                关键的一句话：
                resp = web.Response(body=app['__templating__'].get_template(template).render(**r).encode('utf-8'))
                其中r是一个dict,需要绑定到模板上的数据。
config.py:
    自定义了一个Dict,可以对属性进行访问，对初始化的数据，扩展了一种方式：（tuple）,（tuple）
coroweb.py:
    网站框架的核心部分
    主要是把路径和函数进行绑定。
    RequestHandler类：
        对链接请求进行统一的处理映射。 围绕着params = yield from request.json()进行编写。
        获取全部参数后，再根据目标函数的参数表，。。。 生成目标函数需要的参数。这里需要注意，前端post等的key
    add_route:
        类似的这3个函数就是route绑定。
handlers.py:
    主要的API（网址）处理
models.py:
    三个class对应三个表格，表格中的属性一定要填写，可以设置默认值
orm.py:
    1,注意新的sql语句模式的加入(ModelMetaclass)
    2,三个表格类的调用模式全是临时调用，就是不涉及到全局类。

