# simpleui 设置

# 首页配置
SIMPLEUI_HOME_PAGE = '/sta/homepage'
# 首页标题
SIMPLEUI_HOME_TITLE = '首页'
# 首页图标,支持element-ui的图标和fontawesome的图标
SIMPLEUI_HOME_ICON = 'el-icon-date'

# 设置simpleui 点击首页图标跳转的地址
SIMPLEUI_INDEX = '/'

# 首页显示服务器、python、django、simpleui相关信息
SIMPLEUI_HOME_INFO = False

# 首页显示快速操作
SIMPLEUI_HOME_QUICK = False

# 首页显示最近动作
SIMPLEUI_HOME_ACTION = False

# 自定义SIMPLEUI的Logo
SIMPLEUI_LOGO = '/static/common/topsec_icon.png'

# 登录页粒子动画，默认开启，False关闭
SIMPLEUI_LOGIN_PARTICLES = True

# 让simpleui 不要收集相关信息
SIMPLEUI_ANALYSIS = False

# 自定义simpleui 菜单
SIMPLEUI_CONFIG = {
    # 在自定义菜单的基础上保留系统模块, 设为True代表从APP构建
    'system_keep': False,

    'menus': [
        {'name': 'IDPS规则管理',
        'icon': 'fa fa-th-large',
        'models': [
        {
            'name': 'ATT&CK',
            'url': 'xrule/attackphasechain/',
            # 'icon': 'fab fa-chain'
            'icon': 'fa fa-circle'
        },
            {
            'name': '规则类型列表',
            'url': 'xrule/ipsruleclass/',
            'icon': 'fa fa-columns'
        },{
            'name': '规则列表',
            'url': 'xrule/ipsrule/',
            'icon': 'fa fa-surprise'
        },  {
            'name': '规则模板管理',
            'url': 'xrule/ipsruletpl/',
            'icon': 'far fa-bookmark'
        },]
        },

        {'name': 'WAF规则管理',
        'icon': 'fa fa-th-large',
        'models': [
            {
            'name': '规则类型列表',
            'url': 'xrule/rulecate/',
            'icon': 'fa fa-columns'
        },{
            'name': '规则列表',
            'url': 'xrule/ruletxt2/',
            'icon': 'fa fa-surprise'
        },  
        ]
        },

            {'name': 'CIS安全事件',
        'icon': 'fa fa-th-large',
        'models': [
            {
            'name': '事件类型列表',
            'url': 'xrule/ciseventcategory/',
            'icon': 'fa fa-columns'
        },
        ]
        },
       
        {'name': '任务管理',
         'icon': 'fa fa-asterisk',
         'models': [{
             'name': '任务队列',
             'url': 'ops/taskrundhistory/',
             'icon': 'fa fa-circle'
             },{
             'name': '任务监控flower',
             'url': '/flower',
             'icon': 'fa fa-adjust'
             },
            ]
         },

        # {'name': '用户管理',
        #  'icon': 'fa fa-user',
        #  'models': [{
        #      'name': '用户管理',
        #      'url': 'secs/user/',
        #      'icon': 'fa fa-circle'
        #  },{
        #      'name': '组织结构',
        #      'url': 'secs/organization/',
        #      'icon': 'fab fa-wpexplorer'
        #  },]
        #  }
    ]
}

# 是否显示默认图标，默认=True
SIMPLEUI_DEFAULT_ICON = False

# 图标设置，图标参考：
SIMPLEUI_ICON = {
    '系统管理': 'fab fa-apple',
    '用户管理': 'fas fa-user-tie'
}

# 指定simpleui 是否以脱机模式加载静态资源，为True的时候将默认从本地读取所有资源，即使没有联网一样可以。适合内网项目
# 不填该项或者为False的时候，默认从第三方的cdn获取
SIMPLEUI_STATIC_OFFLINE = True