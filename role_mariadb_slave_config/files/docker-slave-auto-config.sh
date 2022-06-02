#!/bin/bash

set -ex

varContainerName=$varSlaveContainerName

varDatabaseExistsCount=`mysql -uroot -p123456 -P3306 -h$varContainerName -e "show databases" | grep "$varMasterDatabaseName" | wc -l`
if ! [[ $varDatabaseExistsCount -eq 0 ]]; then
  echo "数据库同步容器之前已经初始化，不需要重新初始化，你可以忽略此提示信息"
  exit
fi

# 解压/tmp/fullybackup-restore.tar.gz
rm -f /tmp/*.sql
(cd /tmp && tar -xvzf fullybackup-restore.tar.gz)
(cd /tmp && mv *.sql fullybackup-restore.sql || mv .*.sql fullybackup-restore.sql)

mysql -uroot -p123456 -P3306 -h$varContainerName -e "create database $varMasterDatabaseName" && \
echo "成功创建数据库$varMasterDatabaseName，正在使用全量备份还原数据库，可能需要等待一段时间。。。" && \
pv /tmp/fullybackup-restore.sql | mysql -uroot -p123456 -P3306 -h$varContainerName $varMasterDatabaseName && \
echo "成功还原数据库$varMasterDatabaseName"

# 解析全量备份并获取master_log_file和master_log_pos
varMasterLogFile=`head -500 /tmp/fullybackup-restore.sql | grep "CHANGE MASTER TO" | awk -F '[ = , ;]' '{print $5}'`
varMasterLogPos=`head -500 /tmp/fullybackup-restore.sql | grep "CHANGE MASTER TO" | awk -F '[ = , ;]' '{print $8}'`

rm -f /tmp/fullybackup-restore.sql

if [[ "$varReplicationDelayInSeconds" == "" ]]; then
  mysql -uroot -p123456 -P3306 -h$varContainerName -e "change master to master_host='$varMasterIp',master_port=$varMasterPort,master_user='$varMasterReplicationUser',master_password='$varMasterReplicationUserPassword',master_log_file=$varMasterLogFile,master_log_pos=$varMasterLogPos" && echo "成功执行change master命令"
else
  mysql -uroot -p123456 -P3306 -h$varContainerName -e "change master to master_host='$varMasterIp',master_port=$varMasterPort,master_user='$varMasterReplicationUser',master_password='$varMasterReplicationUserPassword',master_log_file=$varMasterLogFile,master_log_pos=$varMasterLogPos,master_delay=$varReplicationDelayInSeconds" && echo "成功执行change master命令"
fi

mysql -uroot -p123456 -P3306 -h$varContainerName -e "start slave" && echo "成功启动slave复制进程"
