# coding:utf-8 
import requests
from requests.api import request
from libs.conf import load_user_config
config = load_user_config()

from libs.logger import Log
logging = Log(log_flag='proxy_pool')


def get_proxy():
    return requests.get("http://{}/get/".format(config.PROXY_SERVER)).json()


def delete_proxy(proxy):
    requests.get("http://{ser}/delete/?proxy={proxy}".format(proxy=proxy, ser=config.PROXY_SERVER))


def fetch_url(retry=10, method='get', url=None, headers=None, *args, **kwargs):
    # TODO 爬虫核心函数
    retry_count = 5
    proxy = get_proxy().get("proxy")
    while retry_count > 0:
        try:
            response = request(method=method,
                               url=url,
                               proxies={"http": "http://{}".format(proxy)},
                               headers=headers,
                               allow_redirects=True,
                               verify=False,
                               **kwargs
                               )
            # TODO 使用代理访问 ; 如果响应失败或者被防火墙阻截。
            if int(response.status_code >= 400):
                retry_count -= 1
                logging.warn('[count] proxy={proxy} --> try url={url} error.'.format(
                    count=5 - retry_count, proxy=proxy, url=url
                ))
            else:
                return response
        except Exception:
            retry_count -= 1
            logging.warn('[count] proxy={proxy} --> try url={url} error.'.format(
                count=5 - retry_count, proxy=proxy, url=url
            ))
            logging.critical('{url} Request Backend API error.'.format(url=url))

    # TODO 删除代理池中代理
    delete_proxy(proxy)
    logging.info('[PROXY_DELETE] {}'.format(proxy))
    # TODO 永不放弃, 使用新的代理再试一次
    if retry > 0:
        fetch_url(retry=retry-1, method=method, url=url, headers=headers, *args, **kwargs)
        logging.critical('[PROXY UPDATE {} TIMES TO FETCH]'.format(retry-1))
    else:
        # TODO 代理池质量太差、代码有问题[爬虫、服务端后台]等。
        logging.error('Only god could help you, i think ...')
    return ''
