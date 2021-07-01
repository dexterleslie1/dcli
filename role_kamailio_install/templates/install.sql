
use kamailio;
SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;


-- ----------------------------
-- Table structure for acc
-- ----------------------------


 alter table  acc add column if not exists `src_ip` varchar(64) NOT NULL DEFAULT '';
 alter table  acc add column if not exists `dst_ouser` varchar(64) NOT NULL DEFAULT '';
 alter table  acc add column if not exists `dst_user` varchar(64) NOT NULL DEFAULT '';
 alter table  acc add column if not exists `dst_domain` varchar(128) NOT NULL DEFAULT '';
 alter table  acc add column if not exists `src_user` varchar(64) NOT NULL DEFAULT '';
 alter table  acc add column if not exists `src_domain` varchar(128) NOT NULL DEFAULT '';
 alter table  acc add column if not exists`cdr_id` int(11) NOT NULL DEFAULT '0';

-- ----------------------------
-- Table structure for missed_calls
-- ----------------------------

 alter table  missed_calls add column if not exists `src_ip` varchar(64) NOT NULL DEFAULT '';
 alter table  missed_calls add column if not exists `dst_ouser` varchar(64) NOT NULL DEFAULT '';
 alter table  missed_calls add column if not exists `dst_user` varchar(64) NOT NULL DEFAULT '';
 alter table  missed_calls add column if not exists `dst_domain` varchar(128) NOT NULL DEFAULT '';
 alter table  missed_calls add column if not exists `src_user` varchar(64) NOT NULL DEFAULT '';
 alter table  missed_calls add column if not exists `src_domain` varchar(128) NOT NULL DEFAULT '';
 alter table  missed_calls add column if not exists`cdr_id` int(11) NOT NULL DEFAULT '0';





-- ----------------------------
-- Table structure for acc_cdrs
-- ----------------------------

alter table acc_cdrs add column if not exists `caller` varchar(60) DEFAULT NULL;
alter table acc_cdrs add column if not exists `callee` varchar(60) DEFAULT NULL;
alter table acc_cdrs add column if not exists `trans_to` varchar(60) DEFAULT NULL;
alter table acc_cdrs add column if not exists `src_user` varchar(24) DEFAULT NULL;
alter table acc_cdrs add column if not exists `dest_user` varchar(24) DEFAULT NULL;
alter table acc_cdrs add column if not exists `scr_domain` varchar(60) DEFAULT NULL;
alter table acc_cdrs add column if not exists `dest_domain` varchar(60) DEFAULT NULL;
alter table acc_cdrs add column if not exists `callid` varchar(128) DEFAULT NULL;
alter table acc_cdrs add column if not exists `ctype` int(11) DEFAULT NULL;
alter table acc_cdrs add column if not exists `provid_in` int(11) DEFAULT NULL;
alter table acc_cdrs add column if not exists `provid_out` int(11) DEFAULT NULL;
alter table acc_cdrs add column if not exists `sipcode` int(11) DEFAULT NULL;
alter table acc_cdrs add column if not exists `reason` varchar(60) DEFAULT NULL;
alter table acc_cdrs add column if not exists `q850` int(11) DEFAULT NULL;

CREATE TABLE IF NOT EXISTS yyd_ip_parse_result(
	id BIGINT NOT NULL PRIMARY KEY AUTO_INCREMENT,
	username VARCHAR(150) NOT NULL,
	ip VARCHAR(150) NOT NULL,
	result VARCHAR(512) NOT NULL COMMENT '解析结果',
	createTime DATETIME NOT NULL COMMENT '创建时间'
) ENGINE=INNODB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for yyd_cdr
-- ----------------------------

CREATE TABLE IF NOT EXISTS `yyd_cdr` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT 'ID,自动维护',
  `start_time` datetime NOT NULL DEFAULT '2000-01-01 00:00:00' COMMENT '开始时间，从呼叫开始计算',
  `answer_time` datetime DEFAULT NULL,
  `end_time` datetime NOT NULL DEFAULT '2000-01-01 00:00:00' COMMENT '挂断时间',
  `duration` int(11) NOT NULL DEFAULT '0' COMMENT '通话时长，从应答后计算',
  `caller` varchar(60) DEFAULT NULL COMMENT '主叫号码',
  `callee` varchar(60) DEFAULT NULL COMMENT '被叫号码',
  `trans_to` varchar(60) DEFAULT NULL COMMENT '呼叫转移号码',
  `src_user` varchar(24) DEFAULT NULL COMMENT '主叫账号',
  `dest_user` varchar(24) DEFAULT NULL COMMENT '被叫账号',
  `scr_domain` varchar(60) DEFAULT NULL COMMENT '主叫域',
  `dest_domain` varchar(60) DEFAULT NULL COMMENT '被叫域',
  `callid` varchar(128) DEFAULT NULL COMMENT '通话标识，全局唯一',
  `ctype` int(11) DEFAULT NULL COMMENT '通话类型：1，外网呼入，2呼叫到外网，3，网内呼叫，4，呼叫转移',
  `provid_in` int(11) DEFAULT NULL COMMENT '从外网呼入 提供商id',
  `provid_out` int(11) DEFAULT NULL COMMENT '从内网呼出 提供商id',
  `sipcode` int(11) DEFAULT NULL COMMENT '挂机代码',
  `reason` varchar(60) DEFAULT NULL COMMENT '挂机原因',
  `q850` int(11) DEFAULT NULL COMMENT '保留',
  PRIMARY KEY (`id`),
  KEY `start_time_idx` (`start_time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='此表为和kamailio中的acc_cdrs相同。';

CREATE TABLE IF NOT EXISTS `yyd_clients` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `subscriberId` int(11) NOT NULL,
  `can_wakeup` tinyint(3) NOT NULL DEFAULT 1,
  `agent` varchar(64) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `info_idx` (`subscriberId`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='此表添加新字段时，必须是允许空或者指定缺省值。';

-- ----------------------------
-- Table structure for yyd_did
-- ----------------------------
CREATE TABLE IF NOT EXISTS `yyd_did` (
  `subscriberId` int(10) unsigned NOT NULL,
  `did` varchar(20) DEFAULT '' COMMENT 'Did,虚拟号码，除国际字冠',
  `gwid` int(11) DEFAULT 0 COMMENT '呼入提供商ID',
  `pstn` varchar(48) DEFAULT NULL COMMENT '呼叫转移号码',
  `nation_code` varchar(8) DEFAULT '' COMMENT 'DID的字冠，美国是1，香港是852等',
  `area_code` varchar(8) DEFAULT '' COMMENT '区域代码，保留',
  `refer` tinyint(3) unsigned DEFAULT 0 COMMENT '保留',
  `route_id` int(11) DEFAULT 0 COMMENT '用户路由ID参照yyd_route',
  `refId` int(10) unsigned DEFAULT NULL COMMENT '由AZP系统维护',
  UNIQUE KEY `refId` (`refId`),
  CONSTRAINT `fkYydDidSubscriberId` FOREIGN KEY (`subscriberId`) REFERENCES `subscriber` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='保存用户需你号码信息';


-- ----------------------------
-- Table structure for yyd_gateways
-- ----------------------------

CREATE TABLE IF NOT EXISTS `yyd_gateways` (
  `gwid` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT '提供商ID,自动维护',
  `gwproxy` varchar(120) NOT NULL COMMENT '提供商SIP服务器，SIP网关',
  `gwport` int(11) NOT NULL DEFAULT '5060' COMMENT 'SIP网关端口。缺省5060',
  `gwuser` varchar(120) DEFAULT NULL COMMENT '提供商SIP账号',
  `gwpasswd` varchar(128) DEFAULT NULL COMMENT '网关密码',
  `prefix` varchar(8) DEFAULT '+' COMMENT '国际前缀，缺省+',
  `grp_id` int(11) NOT NULL COMMENT '保留',
  PRIMARY KEY (`gwid`,`grp_id`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COMMENT='当添加提供商网关信息后，自动在Address加入相应信息';

-- ----------------------------
-- Table structure for yyd_route
-- ----------------------------

CREATE TABLE IF NOT EXISTS `yyd_route` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL COMMENT '路由名称',
  `createTime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8 COMMENT='路由表';

-- ----------------------------
-- Table structure for yyd_route_item
-- ----------------------------
CREATE TABLE IF NOT EXISTS `yyd_route_item` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `routeId` int(11) NOT NULL DEFAULT '0' COMMENT '路由id',
  `code` varchar(18) NOT NULL COMMENT '路由匹配模式，当设置为默认时，此值一定是.*',
  `gwid` int(11) NOT NULL DEFAULT '0' COMMENT '提供商id',
  `isDefault` bit(1) NOT NULL DEFAULT b'0' COMMENT '是否默认  0.不是默认  1.默认',
  `createTime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uqcode` (`routeId`,`code`,`gwid`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8 COMMENT='路由项表';

-- ----------------------------
-- Table structure for yyd_media_attr
-- ----------------------------

CREATE TABLE IF NOT EXISTS `yyd_media_attr` (
  `username` varchar(64) NOT NULL,
  `setid` int(11) NOT NULL DEFAULT 1,
  `manual` bit(1) NOT NULL DEFAULT b'0' COMMENT '值为true时，不能自动选择线路，否则程序会自动选择线路',
  PRIMARY KEY (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;



-- ----------------------------
-- Table structure for yyd_rtpengine
-- ----------------------------
CREATE TABLE IF NOT EXISTS `yyd_rtpengine` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `setid` int(11) DEFAULT NULL,
  `flags` varchar(128) DEFAULT NULL,
  `isDefault` tinyint(1) DEFAULT 0,
  `remark` varchar(48),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4;


-- ---------------------------------------修正数据库-------------------------------------------------------
ALTER TABLE `yyd_did` ADD COLUMN if not exists  `refId` int UNSIGNED unique COMMENT  '由AZP系统维护';
ALTER TABLE `yyd_gateways` ADD COLUMN if not exists  `refId` int UNSIGNED unique  COMMENT  '由AZP系统维护';
ALTER TABLE `yyd_route` ADD COLUMN if not exists  `refId` int UNSIGNED unique  COMMENT  '由AZP系统维护';
ALTER TABLE `yyd_route_item` ADD COLUMN if not exists  `refId` int UNSIGNED unique  COMMENT  '由AZP系统维护';
ALTER TABLE `yyd_did` MODIFY COLUMN `gwid` int NULL DEFAULT 0 COMMENT '呼入提供商ID';
ALTER TABLE `yyd_route_item` CHANGE IF EXISTS providerId gwid INT NOT NULL DEFAULT 0;
ALTER TABLE `yyd_gateways` MODIFY COLUMN if  exists `grp_id` int NULL DEFAULT 0 COMMENT '保留';
ALTER TABLE `dispatcher` MODIFY COLUMN if  exists `setid` int NOT NULL DEFAULT 1;
ALTER TABLE `yyd_cdr` add column if not exists `sync` BIT NOT NULL DEFAULT 0;
ALTER TABLE `yyd_media_attr` add column if not exists  `manual` bit(1) NOT NULL DEFAULT b'0' COMMENT '值为true时，不能自动选择线路，否则程序会自动选择线路';
insert into yyd_clients(subscriberId) SELECT A.id from subscriber A LEFT JOIN yyd_clients B ON A.id = B.subscriberId WHERE B.subscriberId is null;
ALTER TABLE `yyd_did` ADD UNIQUE INDEX if not exists `sub_idx`(`subscriberId`) USING BTREE;
DROP TRIGGER IF EXISTS `InsertDefault`;
DROP TRIGGER IF EXISTS `EditDefault`;
DROP PROCEDURE IF EXISTS `MakeTestData`;

DELIMITER $$
CREATE PROCEDURE proc1()
BEGIN
   IF EXISTS(
            SELECT DISTINCT column_name
            FROM information_schema.columns
            WHERE table_schema=DATABASE() AND table_name='yyd_did' AND column_name='username') THEN
          delete from yyd_did;
          alter table yyd_did drop column if exists username;


          alter table yyd_did add column if not exists subscriberId int(10) unsigned not null AFTER `id`;
          alter table yyd_did add constraint fkYydDidSubscriberId foreign key if not exists(subscriberId) references subscriber(id);

   END IF;
END $$
CALL proc1() $$
DROP PROCEDURE IF EXISTS proc1 $$
DELIMITER ;
ALTER TABLE `yyd_did` ADD COLUMN if not exists  `id` int NOT NULL PRIMARY KEY AUTO_INCREMENT;
DROP VIEW IF EXISTS `yyd_vdid`;
DROP VIEW IF EXISTS `yyd_dispatcher`;
DROP PROCEDURE IF EXISTS `CdrFromAcc`;
INSERT INTO address(ip_addr, mask) select '54.172.60.0',30 FROM dual where  NOT EXISTS (SELECT ip_addr FROM address WHERE ip_addr = '54.172.60.0' and  mask=30);
INSERT INTO address(ip_addr, mask) select '54.172.60.0',23 FROM dual where  NOT EXISTS (SELECT ip_addr FROM address WHERE ip_addr = '54.172.60.0' and  mask=23);
INSERT INTO address(ip_addr, mask) select '34.203.250.0',23 FROM dual where  NOT EXISTS (SELECT ip_addr FROM address WHERE ip_addr = '34.203.250.0' and  mask=23);
INSERT INTO address(ip_addr, mask) select '54.244.51.0',30 FROM dual where  NOT EXISTS (SELECT ip_addr FROM address WHERE ip_addr = '54.244.51.0' and  mask=30);
INSERT INTO address(ip_addr, mask) select '54.244.51.0',24 FROM dual where  NOT EXISTS (SELECT ip_addr FROM address WHERE ip_addr = '54.244.51.0' and  mask=24);
INSERT INTO address(ip_addr, mask) select '54.171.127.192',30 FROM dual where  NOT EXISTS (SELECT ip_addr FROM address WHERE ip_addr = '54.171.127.192' and  mask=30);
INSERT INTO address(ip_addr, mask) select '54.171.127.192',26 FROM dual where  NOT EXISTS (SELECT ip_addr FROM address WHERE ip_addr = '54.171.127.192' and  mask=26);
INSERT INTO address(ip_addr, mask) select '52.215.127.0',24 FROM dual where  NOT EXISTS (SELECT ip_addr FROM address WHERE ip_addr = '52.215.127.0' and  mask=24);
INSERT INTO address(ip_addr, mask) select '35.156.191.128',30 FROM dual where  NOT EXISTS (SELECT ip_addr FROM address WHERE ip_addr = '35.156.191.128' and  mask=30);
INSERT INTO address(ip_addr, mask) select '3.122.181.0',24 FROM dual where  NOT EXISTS (SELECT ip_addr FROM address WHERE ip_addr = '3.122.181.0' and  mask=24);
INSERT INTO address(ip_addr, mask) select '54.65.63.192',30 FROM dual where  NOT EXISTS (SELECT ip_addr FROM address WHERE ip_addr = '54.65.63.192' and  mask=30);
INSERT INTO address(ip_addr, mask) select '54.65.63.192',26 FROM dual where  NOT EXISTS (SELECT ip_addr FROM address WHERE ip_addr = '54.65.63.192' and  mask=26);
INSERT INTO address(ip_addr, mask) select '3.112.80.0',24 FROM dual where  NOT EXISTS (SELECT ip_addr FROM address WHERE ip_addr = '3.112.80.0' and  mask=24);
INSERT INTO address(ip_addr, mask) select '54.169.127.128',30 FROM dual where  NOT EXISTS (SELECT ip_addr FROM address WHERE ip_addr = '54.169.127.128' and  mask=30);
INSERT INTO address(ip_addr, mask) select '54.169.127.128',26 FROM dual where  NOT EXISTS (SELECT ip_addr FROM address WHERE ip_addr = '54.169.127.128' and  mask=26);
INSERT INTO address(ip_addr, mask) select '3.1.77.0',24 FROM dual where  NOT EXISTS (SELECT ip_addr FROM address WHERE ip_addr = '3.1.77.0' and  mask=24);
INSERT INTO address(ip_addr, mask) select '54.252.254.64',30 FROM dual where  NOT EXISTS (SELECT ip_addr FROM address WHERE ip_addr = '54.252.254.64' and  mask=30);
INSERT INTO address(ip_addr, mask) select '54.252.254.64',26 FROM dual where  NOT EXISTS (SELECT ip_addr FROM address WHERE ip_addr = '54.252.254.64' and  mask=26);
INSERT INTO address(ip_addr, mask) select '3.104.90.0',24 FROM dual where  NOT EXISTS (SELECT ip_addr FROM address WHERE ip_addr = '3.104.90.0' and  mask=24);
INSERT INTO address(ip_addr, mask) select '177.71.206.192',30 FROM dual where  NOT EXISTS (SELECT ip_addr FROM address WHERE ip_addr = '177.71.206.192' and  mask=30);
INSERT INTO address(ip_addr, mask) select '177.71.206.192',26 FROM dual where  NOT EXISTS (SELECT ip_addr FROM address WHERE ip_addr = '177.71.206.192' and  mask=26);
INSERT INTO address(ip_addr, mask) select '18.228.249.0',24 FROM dual where  NOT EXISTS (SELECT ip_addr FROM address WHERE ip_addr = '18.228.249.0' and  mask=24);
INSERT INTO address(ip_addr, mask) select '81.201.82.45',32 FROM dual where  NOT EXISTS (SELECT ip_addr FROM address WHERE ip_addr = '81.201.82.45' and  mask=32);
INSERT INTO address(ip_addr, mask) select '81.201.82.0',24 FROM dual where  NOT EXISTS (SELECT ip_addr FROM address WHERE ip_addr = '81.201.82.0' and  mask=24);
INSERT INTO address(ip_addr, mask) select '81.201.83.45',32 FROM dual where  NOT EXISTS (SELECT ip_addr FROM address WHERE ip_addr = '81.201.83.45' and  mask=32);
INSERT INTO address(ip_addr, mask) select '81.201.83.0',24 FROM dual where  NOT EXISTS (SELECT ip_addr FROM address WHERE ip_addr = '81.201.83.0' and  mask=24);
INSERT INTO address(ip_addr, mask) select '81.201.85.45',32 FROM dual where  NOT EXISTS (SELECT ip_addr FROM address WHERE ip_addr = '81.201.85.45' and  mask=32);
INSERT INTO address(ip_addr, mask) select '81.201.85.0',24 FROM dual where  NOT EXISTS (SELECT ip_addr FROM address WHERE ip_addr = '81.201.85.0' and  mask=24);
INSERT INTO address(ip_addr, mask) select '81.201.84.195',32 FROM dual where  NOT EXISTS (SELECT ip_addr FROM address WHERE ip_addr = '81.201.84.195' and  mask=32);
INSERT INTO address(ip_addr, mask) select '81.201.84.0',24 FROM dual where  NOT EXISTS (SELECT ip_addr FROM address WHERE ip_addr = '81.201.84.0' and  mask=24);
INSERT INTO address(ip_addr, mask) select '81.201.86.45',32 FROM dual where  NOT EXISTS (SELECT ip_addr FROM address WHERE ip_addr = '81.201.86.45' and  mask=32);
INSERT INTO address(ip_addr, mask) select '81.201.86.0',24 FROM dual where  NOT EXISTS (SELECT ip_addr FROM address WHERE ip_addr = '81.201.86.0' and  mask=24);
INSERT INTO address(ip_addr, mask) select '81.201.89.110',32 FROM dual where  NOT EXISTS (SELECT ip_addr FROM address WHERE ip_addr = '81.201.89.110' and  mask=32);
INSERT INTO address(ip_addr, mask) select '31.169.58.10',32 FROM dual where  NOT EXISTS (SELECT ip_addr FROM address WHERE ip_addr = '31.169.58.10' and  mask=32);
INSERT INTO address(ip_addr, mask) select '31.169.58.11',32 FROM dual where  NOT EXISTS (SELECT ip_addr FROM address WHERE ip_addr = '31.169.58.11' and  mask=32);
INSERT INTO address(ip_addr, mask) select '188.94.185.98',32 FROM dual where  NOT EXISTS (SELECT ip_addr FROM address WHERE ip_addr = '188.94.185.98' and  mask=32);
INSERT INTO address(ip_addr, mask) select '188.94.185.99',32 FROM dual where  NOT EXISTS (SELECT ip_addr FROM address WHERE ip_addr = '188.94.185.99' and  mask=32);
INSERT INTO address(ip_addr, mask) select '188.94.185.110',32 FROM dual where  NOT EXISTS (SELECT ip_addr FROM address WHERE ip_addr = '188.94.185.110' and  mask=32);
INSERT INTO address(ip_addr, mask) select '31.169.63.1',32 FROM dual where  NOT EXISTS (SELECT ip_addr FROM address WHERE ip_addr = '31.169.63.1' and  mask=32);
INSERT INTO address(ip_addr, mask) select '31.169.63.2',32 FROM dual where  NOT EXISTS (SELECT ip_addr FROM address WHERE ip_addr = '31.169.63.2' and  mask=32);
INSERT INTO address(ip_addr, mask) select '85.119.53.51',32 FROM dual where  NOT EXISTS (SELECT ip_addr FROM address WHERE ip_addr = '85.119.53.51' and  mask=32);
INSERT INTO address(ip_addr, mask) select '85.119.53.52',32 FROM dual where  NOT EXISTS (SELECT ip_addr FROM address WHERE ip_addr = '85.119.53.52' and  mask=32);
INSERT INTO `rtpengine`(`setid`, `url`, `weight`, `disabled`, `stamp`)  select 1, 'udp:0.0.0.0:7722', 1, 0, now() from dual  where NOT EXISTS (select * from rtpengine WHERE setid=1 and url='udp:0.0.0.0:7722');

--  ---------------------------------------------以下为工具生成-----------------------------------------------


-- ----------------------------
-- Table structure for yyd_calls
-- ----------------------------
DROP TABLE IF EXISTS `yyd_calls`;
CREATE TABLE `yyd_calls` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `fu` varchar(48) CHARACTER SET utf8 NOT NULL,
  `ru` varchar(48) CHARACTER SET utf8 NOT NULL,
  `state` int(11) DEFAULT NULL,
  `username` varchar(48) CHARACTER SET utf8 DEFAULT NULL,
  `did` varchar(48) CHARACTER SET utf8 DEFAULT NULL,
  `dest` varchar(48) CHARACTER SET utf8 DEFAULT NULL,
  `gwid` int(11) DEFAULT NULL,
  `auser` varchar(48) CHARACTER SET utf8 DEFAULT NULL,
  `apass` varchar(48) CHARACTER SET utf8 DEFAULT NULL,
  `cdr_caller` varchar(48) CHARACTER SET utf8 DEFAULT NULL,
  `cdr_callee` varchar(48) CHARACTER SET utf8 DEFAULT NULL,
  `cdr_trans_to` varchar(48) CHARACTER SET utf8 DEFAULT NULL,
  `cdr_src_user` varchar(48) CHARACTER SET utf8 DEFAULT NULL,
  `cdr_dest_user` varchar(48) CHARACTER SET utf8 DEFAULT NULL,
  `cdr_ctype` int(11) DEFAULT NULL,
  `cdr_provid_in` int(11) DEFAULT NULL,
  `cdr_provid_out` int(11) DEFAULT NULL,
  `cdr_dest_domain` varchar(48) CHARACTER SET utf8 DEFAULT NULL,
  `reason` varchar(48) CHARACTER SET utf8 DEFAULT NULL,
  `callid` varchar(64) CHARACTER SET utf8 DEFAULT NULL,
  `createtime` datetime DEFAULT NULL,
  `failure_code` int(10) unsigned DEFAULT 487,
  PRIMARY KEY (`id`),
  UNIQUE KEY `callid_idx` (`callid`) USING BTREE
) ENGINE=MEMORY AUTO_INCREMENT=389 DEFAULT CHARSET=utf8mb4;



-- ----------------------------
-- Table structure for yyd_wakeup
-- ----------------------------
DROP TABLE IF EXISTS `yyd_wakeup`;
CREATE TABLE `yyd_wakeup` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `callid` varchar(128) NOT NULL,
  `username` varchar(48) DEFAULT NULL,
  `id_index` int(11) NOT NULL,
  `id_label` int(11) NOT NULL,
  `createtime` datetime NOT NULL,
  `expired` int(11) NOT NULL DEFAULT 120,
  PRIMARY KEY (`id`),
  UNIQUE KEY `callid_idx` (`callid`) USING BTREE
) ENGINE=MEMORY AUTO_INCREMENT=90 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- View structure for yyd_dispatcher
-- ----------------------------
DROP VIEW IF EXISTS `yyd_dispatcher`;
CREATE ALGORITHM = UNDEFINED SQL SECURITY DEFINER VIEW `yyd_dispatcher` AS select `dispatcher`.`destination` AS `destination` from `dispatcher`;

-- ----------------------------
-- View structure for yyd_location
-- ----------------------------
DROP VIEW IF EXISTS `yyd_location`;
CREATE ALGORITHM = UNDEFINED SQL SECURITY DEFINER VIEW `yyd_location` AS select `A`.`username` AS `username`,`A`.`domain` AS `domain`,`A`.`contact` AS `contact`,`A`.`instance` AS `instance`,`A`.`expires` AS `expires`,unix_timestamp(`A`.`expires`) - unix_timestamp(current_timestamp()) AS `expires_second` from `location` `A`;

-- ----------------------------
-- View structure for yyd_users
-- ----------------------------
DROP VIEW IF EXISTS `yyd_users`;
CREATE ALGORITHM = UNDEFINED SQL SECURITY DEFINER VIEW `yyd_users` AS select `subscriber`.`username` AS `username`,`subscriber`.`domain` AS `domain`,`subscriber`.`password` AS `password` from `subscriber`;

DROP PROCEDURE IF EXISTS `AddNoCreditCdr`;
delimiter ;;
CREATE PROCEDURE `AddNoCreditCdr`(IN vcallid VARCHAR ( 128 ),
	IN vduration FLOAT(10, 3),
	IN vcaller VARCHAR ( 60 ),
	IN vcallee VARCHAR ( 60 ),
	IN vtrans_to VARCHAR ( 60 ),
	IN vctype INT,
	IN vprovid_in INT,
	IN vprovid_out INT)
BEGIN
	DECLARE
		vscr_domain VARCHAR ( 60 );
	DECLARE
		vdest_domain VARCHAR ( 60 );
	DECLARE
		vsrc_user VARCHAR ( 24 );
	DECLARE
		vdest_user VARCHAR ( 24 );
	DECLARE
		beginTime datetime DEFAULT ( NULL );
	SELECT
		time,
		dst_domain,
		src_domain,
		dst_user,
		src_user INTO beginTime,
		vdest_domain,
		vscr_domain,
		vdest_user,
		vsrc_user
	FROM
		acc
	WHERE
		callid = vcallid
		AND method = 'INVITE';
	IF
		( beginTime IS NOT NULL ) THEN
			INSERT INTO `acc_cdrs` (
				`start_time`,
				`end_time`,
				`duration`,
				`caller`,
				`callee`,
				`trans_to`,
				`src_user`,
				`dest_user`,
				`scr_domain`,
				`dest_domain`,
				`callid`,
				`ctype`,
				`provid_in`,
				`provid_out`,
				`sipcode`,
				`reason`
			)
		VALUES
			(
				beginTime,
				now(),
				vduration,
				vcaller,
				vcallee,
				vtrans_to,
				vsrc_user,
				vdest_user,
				vscr_domain,
				vdest_domain,
				vcallid,
				vctype,
				vprovid_in,
				vprovid_out,
				200,
				'COMPLETED'
			);
	END IF;

END
;;
delimiter ;

-- ----------------------------
-- Function structure for AddPrefix
-- ----------------------------
DROP FUNCTION IF EXISTS `AddPrefix`;
delimiter ;;
CREATE FUNCTION `AddPrefix`(prefix varchar(8),  num varchar(48))
 RETURNS varchar(48) CHARSET utf8
BEGIN
  DECLARE dest varchar(48);
	DECLARE pf VARCHAR(8);
	set dest = TrimNumber(num);
	set pf = Trim(prefix);
	if pf is null then set pf =''; end if;
	if dest<>'' then
		if pf = '0' or pf = '00' then
	   set dest = CONCAT('00',dest);
	  else
	   set dest = CONCAT(pf,dest);
    end if;
	end if;

RETURN dest;
END
;;
delimiter ;

-- ----------------------------
-- Procedure structure for CallerRoute
-- ----------------------------
DROP PROCEDURE IF EXISTS `CallerRoute`;
delimiter ;;
CREATE PROCEDURE `CallerRoute`(IN `user` VARCHAR ( 48 ),
	IN callee_num VARCHAR ( 48 ),
	OUT `rs` INT)
BEGIN
	DECLARE
		v_gwid INT DEFAULT 0;
	DECLARE
		v_len INT DEFAULT 0;
	SELECT
		B.gwid INTO v_gwid
	FROM
		yyd_route AS A
	INNER JOIN
	yyd_route_item AS B
	ON
		A.id = B.routeId
	INNER JOIN
	subscriber AS C
	INNER JOIN
	yyd_did AS Y
	ON
		C.id = Y.subscriberId AND
		A.id = Y.route_id
	where
		C.username = USER
		AND callee_num REGEXP CONCAT(
			'^',
		IF
		( B.isDefault, '.*', B.`code` ))
	ORDER BY
	IF
		(
			B.isDefault,- 1,
		length( B.`code` )) DESC
		LIMIT 1;
	IF
		v_gwid IS NULL THEN

			SET rs = 0;
		ELSE
			SET rs = v_gwid;

	END IF;

END
;;
delimiter ;

-- ----------------------------
-- Procedure structure for CheckValid
-- ----------------------------
DROP PROCEDURE IF EXISTS `CheckValid`;
delimiter ;;
CREATE PROCEDURE `CheckValid`(IN Caller VARCHAR ( 60 ),
	IN Callee VARCHAR ( 60 ))
BEGIN
	DECLARE
		v_caller VARCHAR ( 60 ) DEFAULT ( NULL );
	DECLARE
		v_callee VARCHAR ( 60 ) DEFAULT ( NULL );
	DECLARE
		rs INT DEFAULT ( 0 );

	SET v_caller = TrimNumber ( Caller );

	SET v_callee = TrimNumber ( Callee );
	IF
		v_callee = '' THEN
		SELECT
			count( username ) INTO rs
		FROM
			subscriber
		WHERE
			username = v_caller;
		ELSE SELECT
			count( S.username ) INTO rs
		FROM
			subscriber AS S
	RIGHT JOIN
	yyd_did AS Y
	ON
		S.id = Y.subscriberId
		WHERE
			S.username = v_caller
			OR S.username = v_callee
			OR CONCAT(
				Y.nation_code,
				Y.area_code,
				Y.did
			)= v_callee;

	END IF;
	SELECT
		rs;

END
;;
delimiter ;

-- ----------------------------
-- Function structure for ConcatDid
-- ----------------------------
DROP FUNCTION IF EXISTS `ConcatDid`;
delimiter ;;
CREATE FUNCTION `ConcatDid`(C1 varchar(12),  C2 varchar(12),  num varchar(18))
 RETURNS varchar(48) CHARSET utf8
BEGIN
DECLARE s VARCHAR(48);
set s= num;
if s='' or null then
 return '';
end if;
RETURN CONCAT(ifnull(C1,''),ifnull(C2,''),s);
END
;;
delimiter ;

-- ----------------------------
-- Procedure structure for ExCallInfo
-- ----------------------------
DROP PROCEDURE IF EXISTS `ExCallInfo`;
delimiter ;;
CREATE PROCEDURE `ExCallInfo`(IN call_id VARCHAR ( 48 ))
BEGIN

  DECLARE rtp1 INT DEFAULT(1);
	DECLARE rtp2 int DEFAULT(1);
	call getRtp(call_id,rtp1,rtp2);
	SELECT
		state,
		if(state=1,cdr_src_user,username),
		if(state=1,cdr_src_user,did),
		dest,
		gwid,
		auser,
		apass,
		cdr_caller,
		cdr_callee,
		cdr_trans_to,
		cdr_src_user,
		cdr_dest_user,
		cdr_ctype,
		cdr_provid_in,
		cdr_provid_out,
		cdr_dest_domain,
		reason,
		rtp1,
		rtp2
	FROM
		yyd_calls
	WHERE
		callid=call_id ;
 	DELETE
 	FROM
 		yyd_calls
 	WHERE
 	callid=call_id ;

END
;;
delimiter ;

-- ----------------------------
-- Function structure for FindUser
-- ----------------------------
DROP FUNCTION IF EXISTS `FindUser`;
delimiter ;;
CREATE FUNCTION `FindUser`(UserName VARCHAR ( 60 ))
 RETURNS tinyint(4)
BEGIN
	DECLARE
		ret INT DEFAULT ( 0 );
	DECLARE
		uri VARCHAR ( 60 ) DEFAULT ( NULL );

	SET uri = CONCAT( 'sip:', UserName, '@%' );
	SELECT
		count( id ) INTO ret
	FROM
		dialog
	WHERE
		caller_contact LIKE uri
		OR callee_contact LIKE uri;

	RETURN ret;

END
;;
delimiter ;

-- ----------------------------
-- Procedure structure for GetCallStatus
-- ----------------------------
DROP PROCEDURE IF EXISTS `GetCallStatus`;
delimiter ;;
CREATE PROCEDURE `GetCallStatus`(IN Caller VARCHAR ( 48 ),
	IN Callee VARCHAR ( 48 ),
	IN Call_id VARCHAR ( 48 ))
BEGIN
	DECLARE
		st,
		iswakeup,
		vgwid INT DEFAULT (- 1 );
	DECLARE
		vcallee,
		res VARCHAR ( 48 ) DEFAULT ( NULL );
	DECLARE
		duration INT;

	SET duration = UNIX_TIMESTAMP(
	now());
	SELECT
		state,
		dest,
		gwid,
		reason INTO st,
		vcallee,
		vgwid,
		res
	FROM
		yyd_calls
	WHERE
		fu = Caller
		AND ru = Callee
		LIMIT 1;
	IF
		st =- 1 THEN
			CALL MakeCallInfo ( Caller, Callee, call_id);
		SELECT
			state,
			dest,
			gwid,
			reason INTO st,
			vcallee,
			vgwid,
			res
		FROM
			yyd_calls
		WHERE
			callid = call_id;
		IF
			st >= 400 THEN
				CALL NoDlgCdr ( call_id, NULL, NULL, st );
			DELETE
			FROM
				yyd_calls
			WHERE
				callid = call_id;

		END IF;
		ELSE UPDATE yyd_calls
		SET callid = call_id
		WHERE
			fu = Caller
			AND ru = Callee;

	END IF;

	if vgwid=0 THEN
	 SELECT B.can_wakeup into iswakeup from subscriber A INNER JOIN yyd_clients B ON A.id=B.subscriberId
	 WHERE A.username=vcallee;
	end if;

	SET duration = UNIX_TIMESTAMP(
	now())- duration;
	SELECT
		st AS State,
		vcallee AS Dest,
		vgwid AS Gateway_ID,
		res AS reson,
		iswakeup,
		duration;
	END
;;
delimiter ;

-- ----------------------------
-- Function structure for GetProxy
-- ----------------------------
DROP FUNCTION IF EXISTS `GetProxy`;
delimiter ;;
CREATE FUNCTION `GetProxy`(servername varchar(48),  `port` int)
 RETURNS varchar(60) CHARSET utf8mb4
BEGIN
 DECLARE srv varchar(48) default NULL;
 declare p int default 0;
 set srv = Trim(servername);
 set p = port;
 if p is null then set p=0; end if;
 if p>0 and p<>5060 THEN
  set  srv = CONCAT(srv,':',cast(p AS CHAR (5)));
 end if;
 return srv;



RETURN NULL;
END
;;
delimiter ;

-- ----------------------------
-- Procedure structure for getRtp
-- ----------------------------
DROP PROCEDURE IF EXISTS `getRtp`;
delimiter ;;
CREATE PROCEDURE `getRtp`(IN call_id VARCHAR ( 48 ),
	INOUT rtp1 INT,
	INOUT rtp2 INT)
BEGIN
	DECLARE
		src,
		dest VARCHAR ( 48 );
	DECLARE
	ctype INT DEFAULT ( 1 );

	SET rtp1 = 1;
	SET rtp2 = 1;
	SELECT
		setid,
		setid INTO rtp1,
		rtp2
	FROM
		yyd_rtpengine
	WHERE
		yyd_rtpengine.isDefault = 1;

	SELECT
		cdr_src_user,
		cdr_dest_user,
		cdr_ctype INTO src,
		dest,
		ctype
	FROM
		yyd_calls
	WHERE
		callid = call_id;
	CASE
			ctype
			WHEN 1 THEN
		SELECT
			setid INTO rtp2
		FROM
			yyd_media_attr
		WHERE
			username = dest;

		WHEN 2 THEN
		SELECT
			setid INTO rtp1
		FROM
			yyd_media_attr
		WHERE
			username = src;

		WHEN 3 THEN
		SELECT
			setid INTO rtp2
		FROM
			yyd_media_attr
		WHERE
			username = dest;
		SELECT
			setid INTO rtp1
		FROM
			yyd_media_attr
		WHERE
			username = src;
		ELSE
		set rtp1 = rtp2;


	END CASE;


END
;;
delimiter ;

-- ----------------------------
-- Procedure structure for LocateInvite
-- ----------------------------
DROP PROCEDURE IF EXISTS `LocateInvite`;
delimiter ;;
CREATE PROCEDURE `LocateInvite`(IN user_name varchar(48))
BEGIN

 DECLARE id_idx int default(0);
 DECLARE id_lab int default(0);

 SELECT
	A.id_index,
	A.id_label
	into id_idx,id_lab

FROM
	yyd_wakeup AS A
	INNER JOIN
	yyd_calls AS B
	ON
		A.callid = B.callid
	where A.username=user_name
	ORDER BY 	B.createtime DESC LIMIT 1;


  delete from yyd_wakeup where username=user_name;

select id_idx as R1,id_lab as R2;
END
;;
delimiter ;

-- ----------------------------
-- Procedure structure for MakeCallInfo
-- ----------------------------
DROP PROCEDURE IF EXISTS `MakeCallInfo`;
delimiter ;;
CREATE PROCEDURE `MakeCallInfo`(IN Caller VARCHAR ( 48 ),
	IN Callee VARCHAR ( 48 ),
	IN Call_Id VARCHAR ( 64 ))
BEGIN
	DECLARE
		v_callee VARCHAR ( 48 );
	DECLARE
		out_gwid INT DEFAULT 0;
	DECLARE
		src_user VARCHAR ( 48 ) DEFAULT NULL;
	DECLARE
		from_user VARCHAR ( 48 ) DEFAULT NULL;
	DECLARE
		dest VARCHAR ( 48 );
	DECLARE
		user1 VARCHAR ( 48 );
	DECLARE
		did1 VARCHAR ( 48 );
	DECLARE
		gwid1 INT;
	DECLARE
		user2 VARCHAR ( 48 );
	DECLARE
		did2 VARCHAR ( 48 );
	DECLARE
		v_pstn VARCHAR ( 48 );
	DECLARE
		gwid2 INT;
	DECLARE
		auser VARCHAR ( 64 ) DEFAULT 'none';
	DECLARE
		apass VARCHAR ( 128 ) DEFAULT '0000';
	DECLARE
		pf VARCHAR ( 8 ) DEFAULT '+';
	DECLARE
		vstate INT DEFAULT 0;
	DECLARE
		stname VARCHAR ( 48 );-- -----------------------CDR变量-----------------------------------------------------------------------------------------
	DECLARE
		cdr_caller VARCHAR ( 60 ) DEFAULT NULL;
	DECLARE
		cdr_callee VARCHAR ( 60 ) DEFAULT NULL;
	DECLARE
		cdr_trans_to VARCHAR ( 60 ) DEFAULT NULL;
	DECLARE
		cdr_src_user VARCHAR ( 24 ) DEFAULT NULL;
	DECLARE
		cdr_dest_user VARCHAR ( 24 ) DEFAULT NULL;
	DECLARE
		cdr_ctype INT DEFAULT 0;
	DECLARE
		cdr_provid_in INT DEFAULT 0;
	DECLARE
		cdr_provid_out INT DEFAULT 0;
	DECLARE
		cdr_dest_domain VARCHAR ( 60 ) DEFAULT NULL;-- -----------------呼出-----------------------------
	DECLARE
		ohost VARCHAR ( 200 ) DEFAULT NULL;
	DECLARE
		ouser VARCHAR ( 128 ) DEFAULT NULL;
	DECLARE
		opass VARCHAR ( 128 ) DEFAULT NULL;


	SET v_callee = TrimNumber ( Callee );

	SET cdr_src_user = caller;
	SELECT
		S.username,
		CONCAT(
			Y.nation_code,
			Y.area_code,
			Y.did
		),
		TrimNumber ( Y.pstn ) AS pstn,
		gwid
		INTO user2,
		did2,
		v_pstn,
		gwid2
	FROM
		subscriber AS S
		LEFT JOIN yyd_did AS Y ON S.id = Y.subscriberId
	WHERE
		(
			S.username = v_callee
			OR CONCAT(
				Y.nation_code,
				Y.area_code,
				Y.did
			)= v_callee
		);
	SELECT
		S.username,
		CONCAT(
			Y.nation_code,
			Y.area_code,
			Y.did
		),
		gwid INTO user1,
		did1,
		gwid1
	FROM
		subscriber AS S
		LEFT JOIN yyd_did AS Y ON S.id = Y.subscriberId
	WHERE
		S.username = Caller;
	IF
		v_pstn <> ''
		AND user1 IS NULL THEN
		IF
			did2 <> '' THEN

				SET v_callee = v_pstn;

			SET vstate = 4;

			SET cdr_caller = Caller;

			SET cdr_provid_in = gwid2;
			IF
				out_gwid = 0 THEN
					CALL CallerRoute ( user2, v_callee, out_gwid );

			END IF;
			IF
				out_gwid = 0 THEN

					SET out_gwid = gwid2;

			END IF;
			IF
				out_gwid = 0 THEN

					SET vstate = 566;
				ELSE SELECT
					Trim( prefix ),
					gwuser,
					gwpasswd,
					GetProxy ( gwproxy, gwport ) INTO pf,
					auser,
					apass,
					cdr_dest_domain
				FROM
					yyd_gateways
				WHERE
					gwid = out_gwid;

				SET src_user = user2;

				SET from_user = AddPrefix ( pf, did2 );

				SET dest = AddPrefix ( pf, v_callee );

				SET cdr_trans_to = dest;

				SET cdr_dest_user = user2;

				SET cdr_callee = from_user;

			END IF;
			ELSE
				SET vstate = 565;

		END IF;

	END IF;
	IF
		user1 IS NULL
		AND user2 IS NULL THEN

			SET vstate = 567;



	END IF;
	IF
		vstate = 0 THEN
		IF
			v_callee = did1 THEN

				SET vstate = 564;
			ELSE
			IF
				user2 IS NULL
				AND did1 = '' THEN

					SET vstate = 565;

			END IF;

		END IF;

	END IF;
	IF
		vstate = 0 THEN
		CASE

				WHEN user2 IS NULL THEN
			IF
				out_gwid = 0 THEN
					CALL CallerRoute ( caller, v_callee, out_gwid );

			END IF;
			IF
				out_gwid = 0 THEN

					SET out_gwid = gwid1;

			END IF;
			IF
				out_gwid = 0 THEN

					SET vstate = 566;
				ELSE
				IF
					did1 = '' THEN

						SET vstate = 565;
					ELSE
						SET vstate = 2;
					SELECT
						Trim( prefix ),
						gwuser,
						gwpasswd,
						GetProxy ( gwproxy, gwport ) INTO pf,
						auser,
						apass,
						cdr_dest_domain
					FROM
						yyd_gateways
					WHERE
						gwid = out_gwid;

					SET src_user = user1;

					SET from_user = AddPrefix ( pf, did1 );

					SET dest = AddPrefix ( pf, v_callee );

					SET cdr_dest_user = dest;

					SET cdr_callee = dest;

				END IF;

			END IF;

			WHEN user1 IS NULL THEN

			SET vstate = 1;

			SET src_user = NULL;

			SET from_user = NULL;

			SET dest = user2;
			SELECT
				ifNULL( A.gwid, '' ),
				B.prefix INTO cdr_provid_in,
				pf
			FROM
				yyd_gateways AS B
				INNER JOIN yyd_did AS A ON B.gwid = A.gwid
				INNER JOIN subscriber AS S ON A.subscriberId = S.id
			WHERE
				S.username = dest;

			SET out_gwid = 0;

			SET cdr_callee = AddPrefix ( pf, did2 );
			ELSE
				SET vstate = 3;

			SET src_user = user1;
			SELECT
				Trim( prefix ) INTO pf
			FROM
				yyd_gateways
			WHERE
				gwid = gwid1;

			SET did1 = AddPrefix ( pf, did1 );

			SET from_user =
			IF
				( did1 = '', user1, did1 );

			SET cdr_callee = AddPrefix ( pf, did2 );

			SET dest = user2;

		END CASE;

	END IF;


	CASE
			vstate
			WHEN 567 THEN

			SET stname = '外部攻击';

		WHEN 564 THEN

		SET stname = '不能呼叫自己';

		WHEN 565 THEN

		SET stname = '您未申请号码，不能拨打：$rU';

		WHEN 566 THEN

		SET stname = '没有设置网关';

		WHEN 486 THEN

		SET stname = '用户忙';

		WHEN 1 THEN

		SET stname = '外网呼入';

		WHEN 2 THEN

		SET stname = '内网外呼';

		WHEN 3 THEN

		SET stname = '内网呼叫';

		WHEN 4 THEN

		SET stname = '呼叫转移';
		ELSE
			SET stname = '';

	END CASE;


	SET cdr_provid_out = out_gwid;

	SET cdr_caller = ifnull( from_user, caller );

	SET cdr_dest_user = IFNULL( cdr_dest_user, dest );

	SET cdr_ctype = vstate;
	IF
		vstate = 4 THEN

			SET cdr_caller = Caller;

	END IF;

	SET cdr_caller = ToMsISDNAddPrefix ( cdr_caller, pf, '+' );

	SET cdr_callee = ToMsISDNAddPrefix ( cdr_callee, pf, '+' );

	if (vstate =2 or vstate =4) and FindUser(cdr_src_user) THEN
	set vstate=486;
	SET stname = 'Busy Here';
	end if;

	if (vstate =1) and FindUser(cdr_dest_user) THEN
	set vstate=486;
	SET stname = 'Busy Here';
	end if;

	if (vstate =3) and (FindUser(cdr_dest_user) or FindUser(cdr_src_user)) THEN
	set vstate=486;
	SET stname = 'Busy Here';
	end if;






	INSERT INTO `yyd_calls` (
		`fu`,
		`ru`,
		`state`,
		`username`,
		`did`,
		`dest`,
		`gwid`,
		`auser`,
		`apass`,
		`cdr_caller`,
		`cdr_callee`,
		`cdr_trans_to`,
		`cdr_src_user`,
		`cdr_dest_user`,
		`cdr_ctype`,
		`cdr_provid_in`,
		`cdr_provid_out`,
		`cdr_dest_domain`,
		`reason`,
		`callid`,
		`createtime`
	) SELECT
	Caller,
	Callee,
	vstate,
	src_user,
	from_user,
	dest,
	out_gwid,
	auser,
	apass,
	cdr_caller,
	cdr_callee,
	cdr_trans_to,
	cdr_src_user,
	cdr_dest_user,
	cdr_ctype,
	cdr_provid_in,
	cdr_provid_out,
	cdr_dest_domain,
	stname,
	Call_Id,
	NOW()
	FROM
	DUAL
	WHERE
		NOT EXISTS (
		SELECT
			*
		FROM
			yyd_calls
		WHERE
			fu = caller
			AND ru = callee
		);

END
;;
delimiter ;

-- ----------------------------
-- Procedure structure for NoDlgCdr
-- ----------------------------
DROP PROCEDURE IF EXISTS `NoDlgCdr`;
delimiter ;;
CREATE PROCEDURE `NoDlgCdr`(IN call_id varchar(128),
  IN Ascr_domain varchar(48),
  IN Adest_domain varchar(48),
	in Asip_code int)
BEGIN

	insert into yyd_cdr(
start_time,
end_time,
duration,
caller,
callee,
trans_to,
src_user,
dest_user,
scr_domain,
dest_domain,
callid,
ctype,
provid_in,
provid_out,
sipcode,
reason)




SELECT
	createtime,
	Now(),
  0,
	if(B.cdr_ctype=3,NULL,B.cdr_caller),
	if(B.cdr_ctype=3,NULL,B.cdr_callee),
	B.cdr_trans_to,
	if(B.cdr_ctype=1 or B.cdr_ctype=4,NULL,B.cdr_src_user),
	if(B.cdr_ctype=2,NULL,B.cdr_dest_user),
  Ascr_domain,
  Adest_domain,
  B.callid,
	B.cdr_ctype,
	B.cdr_provid_in,
	B.cdr_provid_out,
	-- B.failure_code as sipcode,
  Asip_code as sipcode,
	case Asip_code when 487 then 'CANCELED' when 486 then 'BUSY' else 'NO_ANSWER' end as reason

FROM
	yyd_calls AS B
where B.callid=call_id;
delete from yyd_calls where callid=call_id;



END
;;
delimiter ;

-- ----------------------------
-- Procedure structure for ProviderInfo
-- ----------------------------
DROP PROCEDURE IF EXISTS `ProviderInfo`;
delimiter ;;
CREATE PROCEDURE `ProviderInfo`(IN v_gwid INT)
BEGIN
	SELECT
	GetProxy(gwproxy,gwport) AS HOST,
		B.gwuser,B.gwpasswd
	FROM
		yyd_gateways AS B
	WHERE
		B.gwid = v_gwid;

END
;;
delimiter ;

-- ----------------------------
-- Procedure structure for RegCheck
-- ----------------------------
DROP PROCEDURE IF EXISTS `RegCheck`;
delimiter ;;
CREATE PROCEDURE `RegCheck`(IN Caller varchar(48))
BEGIN
  DECLARE cnt INT DEFAULT(0);
  select count(username) into cnt from subscriber where username=Caller;
	select cnt as useraccount;
END
;;
delimiter ;

-- ----------------------------
-- Procedure structure for SaveTrascation
-- ----------------------------
DROP PROCEDURE IF EXISTS `SaveTrascation`;
delimiter ;;
CREATE PROCEDURE `SaveTrascation`(IN call_id varchar(128), IN index_n int, IN lable_n int)
BEGIN
declare rs int default(0);

select count(*) into rs from yyd_wakeup where callid=call_id;
 if rs=0 then
  INSERT INTO `yyd_wakeup`(`username`,`callid`, `id_index`, `id_label`, `createtime`,`expired`)
	SELECT 	dest, callid,index_n, lable_n, NOW(),120 FROM yyd_calls where callid=call_id;
 end if;

END
;;
delimiter ;

-- ----------------------------
-- Function structure for ToMsISDNAddPrefix
-- ----------------------------
DROP FUNCTION IF EXISTS `ToMsISDNAddPrefix`;
delimiter ;;
CREATE FUNCTION `ToMsISDNAddPrefix`(phone_num varchar(48),oldpf varchar(8),  newpf varchar(8))
 RETURNS varchar(48) CHARSET utf8
BEGIN
  DECLARE str VARCHAR(48);
	if oldpf=newpf  then RETURN phone_num; end if;
	set str = Trim(phone_num);
	if str is Null or str ='' then RETURN str; end if;
	if oldpf='' then RETURN concat(newpf,str); end if;
	if substring(str, 1,length(oldpf)) = oldpf then
	 return concat(newpf,substr(str,length(oldpf)+1));
  else RETURN str;
	end if;

END
;;
delimiter ;

-- ----------------------------
-- Function structure for TrimNumber
-- ----------------------------
DROP FUNCTION IF EXISTS `TrimNumber`;
delimiter ;;
CREATE FUNCTION `TrimNumber`(call_num varchar(48))
 RETURNS varchar(48) CHARSET utf8
BEGIN

DECLARE i int;
declare r int;
DECLARE v_callee VARCHAR(48);
declare c char(1);
if Call_num is null or trim(Call_num)='' then
set v_callee='';
else



set v_callee = '';

set i = 1;

WHILE i<LENGTH(call_num)+1 DO
 set c = SUBSTR(Call_num,i,1);
 set r = ascii(c);
 set i=i+1;
if r>47 and r <58 THEN
 set v_callee=CONCAT(v_callee,c);
end if;
END WHILE;
set v_callee = TRIM(LEADING '0' FROM v_callee);

end if;


RETURN v_callee;
END
;;
delimiter ;

-- ----------------------------
-- Procedure structure for update_failure_code
-- ----------------------------
DROP PROCEDURE IF EXISTS `update_failure_code`;
delimiter ;;
CREATE PROCEDURE `update_failure_code`(IN fcallid varchar(128), IN fcode int)
BEGIN
 update yyd_calls set failure_code = fcode where callid=fcallid;
 select 1;
END
;;
delimiter ;

-- ----------------------------
-- Event structure for CleanCDRS
-- ----------------------------
DROP EVENT IF EXISTS `CleanCDRS`;
delimiter ;;
CREATE EVENT `CleanCDRS`
ON SCHEDULE
EVERY '1' WEEK STARTS '2020-10-22 14:59:46'
DISABLE
DO BEGIN

 start transaction;
 delete from acc_cdrs;
 COMMIT;

end
;;
delimiter ;

-- ----------------------------
-- Triggers structure for table acc_cdrs
-- ----------------------------
DROP TRIGGER IF EXISTS `newcdr`;
delimiter ;;
CREATE TRIGGER `newcdr` BEFORE INSERT ON `acc_cdrs` FOR EACH ROW BEGIN
	DECLARE
		n_end_time datetime;
	DECLARE
		n_sipcode INT;
	DECLARE
		n_reason VARCHAR ( 60 );
	IF
		EXISTS (
		SELECT
			id
		FROM
			acc
		WHERE
			callid = NEW.callid
			LIMIT 1
			) THEN

			SET new.sipcode = 200;

	END IF;
	IF
		new.caller IS NULL THEN
		if new.end_time is null then set new.end_time=now(); end if;
		if new.sipcode is null then set new.sipcode = 487; end if;
			CALL NoDlgCdr (
				new.callid,
				NEW.scr_domain,
				NEW.dest_domain,
				new.sipcode
			);
		ELSE

		CASE
				new.sipcode
				WHEN 200 THEN

				SET NEW.reason = 'COMPLETED';

			WHEN 603 THEN

			SET NEW.reason = 'BUSY';

			WHEN 486 THEN

			SET NEW.reason = 'BUSY';

			WHEN 487 THEN

			SET NEW.reason = 'CANCELED';

			WHEN 408 THEN

			SET NEW.reason = 'NO_ANSWER';

			WHEN 480 THEN

			SET NEW.reason = 'NO_ANSWER';
			ELSE
				SET NEW.reason = NEW.reason;

		END CASE;
		INSERT INTO yyd_cdr (
			start_time,
			answer_time,
			end_time,
			duration,
			caller,
			callee,
			trans_to,
			src_user,
			dest_user,
			scr_domain,
			dest_domain,
			callid,
			ctype,
			provid_in,
			provid_out,
			sipcode,
			reason,
			q850
		)
		VALUES
			(
				NEW.start_time,
				if(new.sipcode=200,FROM_UNIXTIME( UNIX_TIMESTAMP( NEW.end_time ) - New.duration ),null),
				NEW.end_time,
				Floor( New.duration),
			IF
				(
					NEW.ctype = 3,
					NULL,
					NEW.caller
				),
			IF
				(
					NEW.ctype = 3,
					NULL,
					NEW.callee
				),
				NEW.trans_to,
			IF
				(
					NEW.ctype = 1
					OR NEW.ctype = 4,
					NULL,
					NEW.src_user
				),
			IF
				(
					NEW.ctype = 2,
					NULL,
					NEW.dest_user
				),
				NEW.scr_domain,
				NEW.dest_domain,
				NEW.callid,
				NEW.ctype,
				NEW.provid_in,
				NEW.provid_out,
				NEW.sipcode,
				NEW.reason,
				NEW.q850
			);

	END IF;

END
;;
delimiter ;

-- ----------------------------
-- Triggers structure for table acc_cdrs
-- ----------------------------
DROP TRIGGER IF EXISTS `removecdr`;
delimiter ;;
CREATE TRIGGER `removecdr` AFTER DELETE ON `acc_cdrs` FOR EACH ROW delete from acc where callid=OLD.callid
;;
delimiter ;

-- ----------------------------
-- Triggers structure for table dispatcher
-- ----------------------------
DROP TRIGGER IF EXISTS `newdisp`;
delimiter ;;
CREATE TRIGGER `newdisp` AFTER INSERT ON `dispatcher` FOR EACH ROW begin
INSERT INTO `address`(ip_addr,mask,port) values(new.destination,32,5060);
insert into domain(domain) values(new.destination);
end
;;
delimiter ;

-- ----------------------------
-- Triggers structure for table dispatcher
-- ----------------------------
DROP TRIGGER IF EXISTS `updatedisp`;
delimiter ;;
CREATE TRIGGER `updatedisp` AFTER UPDATE ON `dispatcher` FOR EACH ROW begin
update address set ip_addr = new.destination where ip_addr = old.destination;
update domain set domain = new.destination WHERE domain = old.destination;
END
;;
delimiter ;

-- ----------------------------
-- Triggers structure for table dispatcher
-- ----------------------------
DROP TRIGGER IF EXISTS `rmdisp`;
delimiter ;;
CREATE TRIGGER `rmdisp` AFTER DELETE ON `dispatcher` FOR EACH ROW BEGIN
 delete from address where ip_addr = old.destination;
 delete from domain where domain = old.destination;
end
;;
delimiter ;

-- ----------------------------
-- Triggers structure for table location
-- ----------------------------
DROP TRIGGER IF EXISTS `userlogin`;
delimiter ;;
CREATE TRIGGER `userlogin` AFTER INSERT ON `location` FOR EACH ROW BEGIN
	DECLARE
		st TINYINT Default ( 0 );
	IF
		new.user_agent LIKE '%Azp agent iOS%'
		OR new.user_agent LIKE '%NewRock%' THEN

			SET st = 1;

	END IF;
	UPDATE subscriber A
	INNER JOIN yyd_clients B ON A.id = B.subscriberId
	SET B.can_wakeup = st,B.agent = new.user_agent
	WHERE
		A.username = new.username
		AND B.can_wakeup <> st;

END
;;
delimiter ;
-- ----------------------------
-- Triggers structure for table subscriber
-- ----------------------------
DROP TRIGGER IF EXISTS `onAdd`;
delimiter ;;
CREATE TRIGGER `onAdd` After INSERT ON `subscriber` FOR EACH ROW begin
-- set New.ha1 = MD5(CONCAT(NEW.username, ':',New.domain, ':', NEW.password));
-- set New.ha1b = MD5(CONCAT(NEW.username, '@',New.domain, ':', New.domain,':', NEW.password));
insert into yyd_clients(subscriberId) values(New.id);
end
;;
delimiter ;

-- ----------------------------
-- Triggers structure for table subscriber
-- ----------------------------
DROP TRIGGER IF EXISTS `onUpdate`;
delimiter ;;
CREATE TRIGGER `onUpdate` BEFORE UPDATE ON `subscriber` FOR EACH ROW begin
set New.ha1 = MD5(CONCAT(NEW.username, ':',New.domain, ':', NEW.password));
set New.ha1b = MD5(CONCAT(NEW.username, '@',New.domain, ':', New.domain,':', NEW.password));
end
;;
delimiter ;

-- ----------------------------
-- Triggers structure for table yyd_cdr
-- ----------------------------
DROP TRIGGER IF EXISTS `fillcdr`;
delimiter ;;
CREATE TRIGGER `fillcdr` BEFORE INSERT ON `yyd_cdr` FOR EACH ROW BEGIN
	DECLARE
		n_code INT DEFAULT ( 999 );
	DECLARE
		n_end_time datetime;
	DECLARE
		n_reason VARCHAR ( 60 );
	IF
		new.sipcode IS NULL THEN
		SELECT
			cast( sip_code AS INT ),
			time INTO n_code,
			n_end_time
		FROM
			missed_calls
		WHERE
			callid = new.callid;

		SET new.sipcode = n_code;

		SET new.end_time = n_end_time;

		SET new.answer_time = NULL;
		CASE
				new.sipcode
				WHEN 200 THEN

				SET NEW.reason = 'COMPLETED';

			WHEN 603 THEN

			SET NEW.reason = 'BUSY';

			WHEN 486 THEN

			SET NEW.reason = 'BUSY';

			WHEN 487 THEN

			SET NEW.reason = 'CANCELED';

			WHEN 408 THEN

			SET NEW.reason = 'NO_ANSWER';

			WHEN 480 THEN

			SET NEW.reason = 'NO_ANSWER';
			ELSE
				SET NEW.reason = NEW.reason;

		END CASE;
		DELETE
		FROM
			missed_calls
		WHERE
			callid = new.callid;
	END IF;

END
;;
delimiter ;

-- ----------------------------
-- Triggers structure for table yyd_gateways
-- ----------------------------
DROP TRIGGER IF EXISTS `newgw`;
delimiter ;;
CREATE TRIGGER `newgw` AFTER INSERT ON `yyd_gateways` FOR EACH ROW begin
if  new.gwproxy is not null and TRIM(new.gwproxy)<>'' then

 INSERT INTO domain(domain) select new.gwproxy FROM dual where
 NOT EXISTS (SELECT domain FROM `domain` WHERE domain = new.gwproxy);

end if;

end
;;
delimiter ;

-- ----------------------------
-- Triggers structure for table yyd_gateways
-- ----------------------------
DROP TRIGGER IF EXISTS `updategw`;
delimiter ;;
CREATE TRIGGER `updategw` AFTER UPDATE ON `yyd_gateways` FOR EACH ROW begin
if  new.gwproxy is not null and TRIM(new.gwproxy)<>'' then
 update domain set domain = new.gwproxy WHERE domain = old.gwproxy;
end if;
END
;;
delimiter ;

-- ----------------------------
-- Triggers structure for table yyd_gateways
-- ----------------------------
DROP TRIGGER IF EXISTS `rmgw`;
delimiter ;;
CREATE TRIGGER `rmgw` AFTER DELETE ON `yyd_gateways` FOR EACH ROW BEGIN

 delete from domain where domain = old.gwproxy;
end
;;
delimiter ;

SET FOREIGN_KEY_CHECKS = 1;