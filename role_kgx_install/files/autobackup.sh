#!/bin/sh
suser=root
spassword=123456
database=datanode

bucket=backup-db-all
bucketBaseDir=backup-lhcxxx

basedir=`pwd`

{
LOCK=$basedir/autobackup.lockfile
if [ -f $LOCK ]; then
  echo "Autobackup cronb is running!"
  exit 6
fi
touch $LOCK

prevBaseBackupDir=`date --date '-2 days 3 hour ago' +%Y-%m-%d`
rm -rf $basedir/$prevBaseBackupDir

isMysqlRunning=`docker ps | grep kgx-datanode-db |wc -l`

if [ $isMysqlRunning -le 0 ]; then
 echo "MYSQL is not running.Can't perform backup.Program will exit."
 rm $LOCK
 exit 2
fi

cd $basedir

currentBaseBackupDir=`date --date '7 hours ago 3 minutes ago' +%Y-%m-%d`
echo "Current base backup directory:$currentBaseBackupDir"

if [ ! -d "$currentBaseBackupDir" ]; then
 mkdir $currentBaseBackupDir
fi

cd $basedir/$currentBaseBackupDir

currentBackup=`date +%Y-%m-%d_%H-%M-%S`
echo $currentBackup

currentBackupFile=$currentBackup.sql
echo $currentBackupFile

docker exec -i kgx-datanode-db mysqldump -u$suser -p$spassword --single-transaction --quick --lock-tables=false --master-data=2 $database > $currentBackupFile
tar -czf $basedir/$currentBaseBackupDir/$currentBackupFile.tar.gz $currentBackupFile
rm -f $currentBackupFile
aws s3api put-object --bucket $bucket --key $bucketBaseDir/$currentBaseBackupDir/$currentBackupFile.tar.gz --body $basedir/$currentBaseBackupDir/$currentBackupFile.tar.gz
}||{
pwd
}

rm $LOCK