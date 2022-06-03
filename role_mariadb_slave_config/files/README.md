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
dcli mariadb slave_restore_pre

# 数据还原步骤
# 1、确定当前relay file和position，使用mysqlbinlog提取未执行SQL并执行
mysqlbinlog mysqld-bin-relay-log.000002 --start-position=639 | mysql -uroot -p databasename
# 2、确定drop database SQL位置，例如：#at 5589，则提取日志到指定position之前
mysqlbinlog mysqld-bin-relay-log.000020 --stop-position=5589 | mysql -uroot -p databasename

# 导出还原数据后下载restore-export.gz文件
dcli mariadb slave_export

# 还原生产环境数据库
gzip -dkc restore-export.gz | mysql -uroot -p databasename
```
