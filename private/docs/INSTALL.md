## 安装基础环境


## Redis
```bash

docker run --name redis -d --restart=always \
  -p 6379:6379 \
  -e 'REDIS_PASSWORD=sqsjywl123' \
  -v /srv/docker/redis:/var/lib/redis \
   registry.cn-hangzhou.aliyuncs.com/xxzhang/redis:4.0.9
 

docker run -itd --name=mysql -p 3306:3306 --restart=always \
-v /srv/docker/data/mysqldata:/var/lib/mysql \
-e MYSQL_USER=admin007 \
-e MYSQL_PASSWORD=myadmin@816 \
-e MYSQL_DATABASE=xxscan \
-e MYSQL_ROOT_PASSWORD=test@1q2w2e4R \
-e character-set-server=utf8 \
-e collation-server=utf8_general_ci \
registry.cn-hangzhou.aliyuncs.com/xxzhang/mysql:5.7


docker exec -t mysql mysql -uroot -ptest@1q2w2e4R -e 'drop database xscan;'
docker exec -t mysql mysql -uroot -ptest@1q2w2e4R -e 'CREATE DATABASE `xscan` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;'
```