# mariadb slave操作文档

```shell
# 切换到项目所在的工作目录，配置slave
dcli mariadb slave_config

# 切换到项目所在的工作目录，启动slave
dcli mariadb slave_start

# 查看同步状态
dcli mariadb slave_status

# 清除无用的容器
dcli mariadb slave_cleanup

# 准备数据恢复容器
dcli mariadb slave_restore_prepare
```