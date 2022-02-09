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

### 3.安装docker
    1.sudo yum install -y yum-utils device-mapper-persistent-data lvm2
    2.sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
    3.sudo yum install docker-ce docker-ce-cli containerd.io
    如果安装失败，需要进行升级包 yum -y update
    4.开启docker服务 systemctl start docker

### 4.创建docker内网
    1.docker network create --driver bridge --subnet=172.16.12.0/16 --gateway=172.16.12.1 mynetwork

### 安装 mysql 如有Mysql可不装
    1.docker pull mysql:5.7.27
    2. 生成容器
    docker run -p 3306:3306 --restart=always --name mysql --network=mynetwork --ip 172.16.12.2 -v /home/docker/mysql/conf.d:/etc/mysql/conf.d -v /home/docker/mysql/my.cnf:/etc/my.cnf -v /home/docker/mysql/logs:/logs -v /home/docker/mysql/data:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=Hbwj@123 -d mysql:5.7.27
    3.开放端口
    firewall-cmd --zone=public --add-port=3306/tcp --permanent
    firewall-cmd --reload
    4.将环境目录下的sql导入到新增库中
    
    用户密码默认为 root Hbwj@123

### 4.修改配置文件
    1.进入后端根目录
    2.vim文件 BackService/settings.py


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