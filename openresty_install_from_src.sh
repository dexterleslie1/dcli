#!/bin/bash
#
# Install openresty from source code

source ./common.lib

main() {
 if [ -f "/usr/local/openresty/nginx/sbin/nginx" ]; then
  echo "Openresty has been installed"
 else
  echo "Openresty has not been installed, start to install it wait..."
 
  rm -rf /tmp/openresty*
  rm -rf /tmp/naxsi*

  yum -y install make readline-devel pcre-devel openssl-devel gcc perl
  curl https://bucket-public-common.oss-cn-hangzhou.aliyuncs.com/nginx/naxsi-0.56.tar.gz --output /tmp/naxsi-0.56.tar.gz
  curl https://bucket-public-common.oss-cn-hangzhou.aliyuncs.com/nginx/openresty-1.15.8.1.tar.gz --output /tmp/openresty-1.15.8.1.tar.gz
  (cd /tmp && \
   tar -xzf naxsi-0.56.tar.gz && \
   tar -xzf openresty-1.15.8.1.tar.gz && \
   cd openresty-1.15.8.1 && \
   ./configure --add-module=/tmp/naxsi-0.56/naxsi_src && \
   make install)

  cp -nf /tmp/naxsi-0.56/naxsi_config/naxsi_core.rules /usr/local/openresty/nginx/conf/naxsi_core.rules
  cp -nf openresty.service /usr/lib/systemd/system/openresty.service
 fi
}

main
