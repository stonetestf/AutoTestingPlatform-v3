# Centos7部署说明 
## 环境安装
### 环境注意
    一定要使用Django==2.0.7 和 dwebsocket==0.4.2 这个版本 --- 不然会报错

### 1.安装python37环境
    1.将部署文件中的 Python-3.7.0.tar.xz 上传到服务器中
    2.tar -xvJf  Python-3.7.0.tar.xz
    3.编译安装
        mkdir /usr/local/python3
        cd Python-3.7.0
        /configure --prefix=/usr/local/python3
        make && make install
    4.创建软连接
        ln -s /usr/local/python3/bin/python3 /usr/local/bin/python3
        ln -s /usr/local/python3/bin/pip3 /usr/local/bin/pip3
    5.测试
        python3 -V
        pip3 -V

### 2.安装Python依赖
    1.进入后端项目根目录
    2.pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple --no-dependencies
    3.如遇报错请看下面环境安装错误提示

### 3.安装mysql数据库 如果已有可以跳过安装直接把SQL文件导入到库中
    1.wget -i -c http://dev.mysql.com/get/mysql57-community-release-el7-10.noarch.rpm
2.yum -y install mysql57-community-release-el7-10.noarch.rpm
3.yum -y install mysql-community-server


### 4.修改配置文件


## 环境安装错误处理：
### 安装mysqlcen错误处理
    yum install mysql-devel gcc gcc-devel python-devel
    pip3 install mysqlclient

### Could not find a version that satisfies the requirement numpy==1.13.3
    pip3 install --upgrade pip

# 运行说明
    1.运行nginx
        /usr/local/nginx/sbin/nginx
    
    2.进入后端目录 运行
        python3 -u manage.py runserver 0.0.0.0:9090
    



# 平台说明
## 接口维护
    1.接口中的前置操作,会在接口运行前运行
    2.接口中的后置操作,只会在接口运行完成后进行!

## 用例维护
    1.在执行用例时,如有引用{{变量}} 这种操作时,会存在优先级的引用顺序，在用例中优先查找当前用例提取的值,如果没有才会去全局变量中查找！
    2.历史恢复时,如当前用例中有上传类文件时，并不会恢复此文件!