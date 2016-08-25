# 补充功能

## 安装ansible

```bash
yum -y install ansible
```

## 拷贝配置文件

```bash
cp -r * /etc/ansible
```

## 修改配置文件fuel.ini

1. 修改cluster id

## 使用

1. 使用角色做为目标

	```bash
	ansible controller -m ping
	```

2. 使用主机名称做为目标

	```bash
	ansible node-1 -m ping
	```

