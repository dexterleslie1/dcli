#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import fire
import cli_freeswitch
import cli_openresty
import cli_kamailio
import cli_develop_env
import cli_prometheus
import cli_grafana
import cli_elk
import cli_mongodb
import cli_mariadb
import cli_rabbitmq
import cli_shadowsocks
import cli_docker
import cli_smartgit
import cli_frp
import cli_xrdp
import cli_maven
import cli_nodejs
import cli_xmind
import cli_pycharm
import cli_jdk
import cli_vscode
import cli_centos_eol
import cli_tomcat
import cli_redis
import cli_zookeeper
import cli_kgx
import cli_fail2ban
import cli_jmeter
import cli_os
import cli_k8s
import cli_selenium
import cli_awscli
import logging


class Dcli(object):
    def __init__(self):
        self.openresty = cli_openresty.OpenrestyCli()
        self.freeswitch = cli_freeswitch.FreeswitchCli()
        self.kamailio = cli_kamailio.KamailioCli()
        self.develop_env = cli_develop_env.DevelopEnvCli()
        self.prometheus = cli_prometheus.PrometheusCli()
        self.grafana = cli_grafana.GrafanaCli()
        self.elk = cli_elk.ElkCli()
        self.mongodb = cli_mongodb.MongodbCli()
        self.mariadb = cli_mariadb.MariadbCli()
        self.rabbitmq = cli_rabbitmq.RabbitmqCli()
        self.shadowsocks = cli_shadowsocks.ShadowsocksCli()
        self.docker = cli_docker.DockerCli()
        self.smartgit = cli_smartgit.SmartgitCli()
        self.frp = cli_frp.FrpCli()
        self.xrdp = cli_xrdp.XrdpCli()
        self.maven = cli_maven.MavenCli()
        self.nodejs = cli_nodejs.NodejsCli()
        self.xmind = cli_xmind.XmindCli()
        self.pycharm = cli_pycharm.PycharmCli()
        self.jdk = cli_jdk.JdkCli()
        self.vscode = cli_vscode.VscodeCli()
        self.centoseol = cli_centos_eol.CentOSEolCli()
        self.tomcat = cli_tomcat.TomcatCli()
        self.redis = cli_redis.RedisCli()
        self.zookeeper = cli_zookeeper.ZookeeperCli()
        self.kgx = cli_kgx.KgxCli()
        self.fail2ban = cli_fail2ban.Fail2banCli()
        self.jmeter = cli_jmeter.JmeterCli()
        self.os = cli_os.OsCli()
        self.k8s = cli_k8s.K8sCli()
        self.selenium = cli_selenium.SeleniumCli()
        self.awscli = cli_awscli.AwsCli()


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    fire.Fire(Dcli)
