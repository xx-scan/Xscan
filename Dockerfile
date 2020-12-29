FROM centos:7

ENV LANG en_US.UTF-8

ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN curl -o /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-7.repo && \
    sed -i -e '/mirrors.cloud.aliyuncs.com/d' -e '/mirrors.aliyuncs.com/d' /etc/yum.repos.d/CentOS-Base.repo
RUN curl -o /etc/yum.repos.d/epel.repo http://mirrors.aliyun.com/repo/epel-7.repo
RUN yum makecache

RUN yum install -y python36 python36-devel python36-pip \
		 libtiff-devel libjpeg-devel libzip-devel freetype-devel \
     lcms2-devel libwebp-devel tcl-devel tk-devel sshpass \
     openldap-devel mariadb-devel mysql-devel libffi-devel \
     openssh-clients telnet openldap-clients gcc nmap masscan

# Install Mysql Client
WORKDIR /usr/src/app
VOLUME /usr/src/app
ADD ./requirements.txt /requirements.txt

RUN pip3 install --upgrade pip --index-url https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip3 install -r /requirements.txt

USER root