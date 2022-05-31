#!/bin/bash

set -ex

# 解压/tmp/fullybackup-restore.tar.gz
rm -f /tmp/*.sql
(cd /tmp && tar -xvzf fullybackup-restore.tar.gz)
(cd /tmp && mv *.sql fullybackup-restore.sql || mv .*.sql fullybackup-restore.sql)

varContainerName=$varSlaveContainerName

mysql -uroot -P3306 -h$varContainerName -e "create database $varMasterDatabaseName" && \
echo "成功创建数据库$varMasterDatabaseName，正在使用全量备份还原数据库，可能需要等待一段时间。。。" && \
mysql -uroot -P3306 -h$varContainerName $varMasterDatabaseName < /tmp/fullybackup-restore.sql && \
echo "成功还原数据库$varMasterDatabaseName"

# 解析全量备份并获取master_log_file和master_log_pos
varMasterLogFile=`grep -r "CHANGE MASTER TO" /tmp/fullybackup-restore.sql | awk -F '[ = , ;]' '{print $5}'`
varMasterLogPos=`grep -r "CHANGE MASTER TO" /tmp/fullybackup-restore.sql | awk -F '[ = , ;]' '{print $8}'`

if [[ "$varReplicationDelayInSeconds" == "" ]]; then
  mysql -uroot -P3306 -h$varContainerName -e "change master to master_host='$varMasterIp',master_port=$varMasterPort,master_user='$varMasterReplicationUser',master_password='$varMasterReplicationUserPassword',master_log_file=$varMasterLogFile,master_log_pos=$varMasterLogPos" && echo "成功执行change master命令"
else
  mysql -uroot -P3306 -h$varContainerName -e "change master to master_host='$varMasterIp',master_port=$varMasterPort,master_user='$varMasterReplicationUser',master_password='$varMasterReplicationUserPassword',master_log_file=$varMasterLogFile,master_log_pos=$varMasterLogPos,master_delay=$varReplicationDelayInSeconds" && echo "成功执行change master命令"
fi

mysql -uroot -P3306 -h$varContainerName -e "start slave" && echo "成功启动slave复制进程"

rm -f /tmp/fullybackup-restore.sql
