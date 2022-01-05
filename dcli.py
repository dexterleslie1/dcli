#!/usr/bin/python2
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


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    fire.Fire(Dcli)
