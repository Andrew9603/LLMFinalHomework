# 1、下载Frp程序
# wget https://github.com/fatedier/frp/releases/download/v0.61.0/frp_0.61.0_linux_amd64.tar.gz
# 2、解压Frp
# tar -xzvf frp_0.61.0_linux_amd64.tar.gz
# 3、进入目录
# cp frp_0.61.0_linux_amd64/* ./
# 4、打开 frps.toml
# vim frps.toml
# 5、编辑
# bindPort = 7000
# authentication.method = "token"
# authentication.token = "#@zhangmang119"
# webServer.addr = "0.0.0.0"
# webServer.port = 7500
# webServer.user = "admin"
# webServer.password = "admin"
# 6、启动Frp服务端
# chmod +x frps
# nohup ./frps -c frps.toml > frps.log 2>&1 &
# 7、验证
# tail -f frps.log
# # 正常会显示 "frps started successfully"
# 8.防火墙开放7000 ，18080，11434端口
# firewall-cmd --zone=public --add-port=7000/tcp --permanent
# firewall-cmd --zone=public --add-port=18080/tcp --permanent
# firewall-cmd --zone=public --add-port=11434/tcp --permanent
# firewall-cmd --reload
# firewall-cmd --zone=public --list-ports
# 5.1 Frp客户端配置
# 1、下载Frp程序
# wget https://github.com/fatedier/frp/releases/download/v0.61.0/frp_0.61.0_linux_amd64.tar.gz
# 2、解压Frp
# tar -xzvf frp_0.61.0_linux_amd64.tar.gz
# 3、进入目录
# cp frp_0.61.0_linux_amd64/* ./
# 4、打开 frpc.toml
# vim frpc.toml
# 5、编辑
# serverAddr = "47.95.42.31"
# serverPort = 7000
# authentication.method = "token"  //auth.method = "token"
# authentication.token = "#@zhangmang119" // auth.token = "#@zhangmang119"
# [[proxies]]
# name = "openwebui"
# type = "tcp"
# localIP = "127.0.0.1"
# localPort = 8080            # OpenWebUI本地端口
# remotePort = 18080          # 外网访问端口
#
# [[proxies]]
# name = "ollama"
# type = "tcp"
# localIP = "127.0.0.1"
# localPort = 11434           # Ollama本地端口
# remotePort = 11434          # 外网访问端口
#
# 6、启动
# chmod +x frpc
# nohup ./frpc -c frpc.toml > frpc.log 2>&1 &
# 7、验证
# tail -f frpc.log
# # 正常会显示 "start proxy success" 和端口映射信息
# 8、加入 systemd 服务，方便启动和查看状态
# 更新软件源：
# sudo apt update
# 安装 nano：
# sudo apt install nano -y
# 创建 systemd 服务文件
# sudo nano /etc/systemd/system/frpc.service
#
# 路径：/mnt/workspace/frp_0.61.0_linux_amd64/frpc
# /mnt/workspace/frp_0.61.0_linux_amd64
#
# [Unit]
# Description=Frp Client Service
# After=multi-user.target
#
#
# [Service]
# Type=simple
# User=root
# Restart=on-failure
# RestartSec=5s
# ExecStart=/home/admin/workspace/frp_0.61.0_linux_amd64/frpc -c /home/admin/workspace/frp_0.61.0_linux_amd64/frpc.toml
# WorkingDirectory=/home/admin/workspace/frp_0.61.0_linux_amd64/
#
# [Install]
# WantedBy=multi-user.target
