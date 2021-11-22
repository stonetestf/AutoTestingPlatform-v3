# 部署说明
## Centos 部署VUE
### 安装 node、npm模块
    # 下载
    wget https://nodejs.org/dist/v10.16.0/node-v10.16.0-linux-x64.tar.xz

    # 解压
    xz -d node-v10.16.0-linux-x64.tar.xz
    tar -xvf node-v10.16.0-linux-x64.tar -C /usr/local

    # 进入目录
    cd node-v10.16.0-linux-x64

    # 创建软连接
    ln -s /usr/local/node-v10.16.0-linux-x64/bin/node /usr/local/bin/node
    ln -s /usr/local/node-v10.16.0-linux-x64/bin/npm /usr/local/bin/npm

    # 测试
    node -v
    npm -v

    # 配置taobao镜像
    npm config set registry https://registry.npm.taobao.org

### 安装pm2
    npm install pm2 -g
    sudo ln -s /usr/local/node-v10.16.0-linux-x64/bin/pm2 /usr/local/bin/pm2

    启动项目：pm2 start app.js
    pm2 show 0（id）//查看某个启动的应用详情
    pm2 show list//查看当前启动的所有应用
    pm2 stop 0(id)//关闭某个应用

### 安装Nginx
    https://www.jianshu.com/p/7a37e03b2107

    重点：一般修改完nginx配制文件都需要对修改后的配制进行check
    [root@cat sbin]$ /usr/local/nginx/sbin/nginx -t -c /usr/local/nginx/conf/nginx.conf

    启动 /usr/local/nginx/sbin/nginx
    重启 /usr/local/nginx/sbin/nginx -s reload

    注意 上面这个安装时第6步，安装后文件会在/usr/local/nginx 

    开启端口
    firewall-cmd --zone=public --add-port=9092/tcp --permanent
    firewall-cmd --reload
