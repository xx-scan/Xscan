## 安装基础环境


## Redis
```bash

docker run --name redis -d --restart=always \
  -p 6379:6379 \
  -e 'REDIS_PASSWORD=sqsjywl123' \
  -v /srv/docker/redis:/var/lib/redis \
   registry.cn-hangzhou.aliyuncs.com/xxzhang/redis:4.0.9
 
```