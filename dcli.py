#!/usr/bin/python
# -*- coding: UTF-8 -*-

import fire
import platform
import cli_common
import cli_freeswitch


class OpenRestyCli(object):
    def install(self, from_source=False):
        # Support centOS7, centOS8 only
        var_platform = platform.platform()
        if not "el7" in var_platform and not "el8" in var_platform:
            raise Exception, "Support centOS7, centOS8 platform only to compile and install openresty."

        if from_source:
            # TODO: Check if openresty has been installed or tell user to uninstall it firstly.

            # Install necessary compile component
            var_command = "yum install make readline-devel pcre-devel openssl-devel gcc perl"
            cli_common.execute_command(var_command)

            # Download and prepare openresty, naxsi source code
            var_openresty_package = "openresty-1.15.8.1.tar.gz"
            var_openresty_decompress_directory = "openresty-1.15.8.1"
            var_naxsi_package = "naxsi-0.56.tar.gz"
            var_naxsi_decompress_directory = "naxsi-0.56"

            var_command = "curl https://bucket-public-common.oss-cn-hangzhou.aliyuncs.com/nginx/" + \
                          var_openresty_package + " --output /tmp/" + var_openresty_package
            cli_common.execute_command(var_command)

            var_command = "curl https://bucket-public-common.oss-cn-hangzhou.aliyuncs.com/nginx/" + \
                          var_naxsi_package + " --output /tmp/" + var_naxsi_package
            cli_common.execute_command(var_command)

            var_command = "rm -rf /tmp/" + var_naxsi_decompress_directory
            cli_common.execute_command(var_command)
            var_command = "rm -rf /tmp/" + var_openresty_decompress_directory
            cli_common.execute_command(var_command)

            var_command = "cd /tmp && tar -xzf " + var_openresty_package;
            cli_common.execute_command(var_command)
            var_command = "cd /tmp && tar -xzf " + var_naxsi_package
            cli_common.execute_command(var_command)

            # var_command = "cd /tmp/" + var_openresty_decompress_directory + " && ./configure --add-module=/tmp/" + var_naxsi_decompress_directory + "/naxsi_src"
            # self.execute_command(var_command)
            # var_command = "cd /tmp/" + var_openresty_decompress_directory + " && make install"
            # self.execute_command(var_command)

            var_command = "cp -nf /tmp/naxsi-0.56/naxsi_config/naxsi_core.rules " \
                          "/usr/local/openresty/nginx/conf/naxsi_core.rules"
            cli_common.execute_command(var_command)

            var_openresty_service_file_content = """[Unit]
Description=The OpenResty Application Platform
After=syslog.target network-online.target remote-fs.target nss-lookup.target
Wants=network-online.target

[Service]
Type=forking
PIDFile=/usr/local/openresty/nginx/logs/nginx.pid
ExecStartPre=/usr/local/openresty/nginx/sbin/nginx -t
ExecStart=/usr/local/openresty/nginx/sbin/nginx
ExecReload=/bin/kill -s HUP $MAINPID
ExecStop=/bin/kill -s QUIT $MAINPID
PrivateTmp=true

[Install]
WantedBy=multi-user.target"""
            self.write_file("/usr/lib/systemd/system/openresty.service", var_openresty_service_file_content)

            var_naxsi_file_content = """#LearningMode;
SecRulesEnabled;
#SecRulesDisabled;
DeniedUrl "/RequestDenied";

## Check & Blocking Rules
CheckRule "$SQL >= 8" BLOCK;
CheckRule "$RFI >= 8" BLOCK;
CheckRule "$TRAVERSAL >= 4" BLOCK;
CheckRule "$EVADE >= 4" BLOCK;
CheckRule "$XSS >= 8" BLOCK;"""
            self.write_file("/usr/local/openresty/nginx/conf/naxsi.rules", var_naxsi_file_content)

            var_command = "cp nginx.conf /usr/local/openresty/nginx/conf/nginx.conf"
            cli_common.execute_command(var_command)
        else:
            # TODO: Install openresty from yum repository
            raise Exception, "Install openresty from yum repository not implement yet."

    def write_file(self, target_file, content):
        try:
            var_file = open(target_file, "w")
            var_file.write(content)
        except IOError:
            print("IO exception no such file")
        finally:
            if var_file:
                var_file.close()


class Dcli(object):
    def __init__(self):
        self.openresty = OpenRestyCli()
        self.freeswitch = cli_freeswitch.FreeswitchCli()


if __name__ == "__main__":
    fire.Fire(Dcli)
