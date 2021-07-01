INSERT INTO subscriber(username,domain,`password`,ha1,ha1b) VALUES(#{userName},#{domain},#{password},MD5(CONCAT(#{userName},':',#{domain},':',#{password})),MD5(CONCAT(#{userName},'@',#{domain},':',#{domain},':',#{password})))

insert into yyd_gateways(gwproxy,gwport,gwuser,gwpasswd,prefix) values('xxx',5060,'xxxx','xxxx','+')

insert into yyd_route(name,createTime) values('twilio',now());
insert into yyd_route_item(routeId,code,gwid,isDefault,createTime) values(8,'1',2,true,now());
insert into yyd_did(subscriberId,did,gwid,nation_code,route_id) values(1,'13511111111',2,'86',8);