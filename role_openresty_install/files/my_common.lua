local cjson=require 'cjson'
-- local geo=require 'resty.maxminddb'
--
-- -- 初始化geo
-- if not geo.initted() then
--     geo.init("/usr/local/openresty/GeoLite2-City.mmdb")
-- end

local ip2region = require 'resty.ip2region'
local ip2regionLocation = ip2region.new({
        file = "/usr/local/openresty/ip2region.db",
        dict = "ip_data",
        mode = "memory" -- maybe memory,binary or btree
});

local _M = { _VERSION = '1.0.0' }

-- 获取客户端真实ip地址
function _M.getClientIp()
        local varHeaders = ngx.req.get_headers()
        local clientIp;
        local varXForwardedFor = varHeaders["x-forwarded-for"];
        if (varXForwardedFor == nil or varXForwardedFor == "") then
                varXForwardedFor = "";

                -- 没有x-forwarded-for表示客户端直接访问openresty
                -- 此时需要设置ngx.var.remote_addr为x-forwarded-for的值
                ngx.req.set_header("x-forwarded-for", ngx.var.remote_addr);
        end
        -- ngx.log(ngx.WARN, "x-forwarded-for=" .. varXForwardedFor);
        if varXForwardedFor then
                local count = 0;
                for k, v in string.gmatch(varXForwardedFor, "[^,]+") do
                        if count==0 then
                                clientIp = k;
                                -- ngx.log(ngx.CRIT, "x-forwarded-for=" .. varXForwardedFor .. "提取到客户端ip地址:" .. clientIp);
                                break;
                        end
                        count = count+1;
                end
        end
        if not clientIp then
                clientIp = ngx.var.remote_addr;
        end
        return clientIp;
end

-- 获取客户端请求url
function _M.getRequestUrl()
        local fullUrl = ngx.var.scheme .. "://" .. ngx.var.http_host .. ngx.var.request_uri;
        return fullUrl;
end

-- 拦截5秒内超过100个请求情况
function _M.ccDetectionReqLimit(clientIp, requestUrl, dictMyLimitReq, dictLogTail)
    local keyLogTail = "logTail"
    if dictLogTail:get(keyLogTail .. clientIp) == nil then
        -- 默认观察周期5秒
        local valueDefaultObservationPeriodInSeconds = 5;
        -- 请求总次数
        local keySituation1RequestCount = "situation1RequestCount#";
        -- 允许最大请求总次数
        local valueSituation1MaximumAllow = 100;

        -- 设置相关key对应初始化value
        local requestCount = dictMyLimitReq:get(keySituation1RequestCount .. clientIp);
        if not requestCount then
            dictMyLimitReq:set(keySituation1RequestCount .. clientIp, 0, valueDefaultObservationPeriodInSeconds);
        end

        -- 判断5秒内是否超过120次
        local requestCount = dictMyLimitReq:get(keySituation1RequestCount .. clientIp);
        if requestCount >= valueSituation1MaximumAllow then
            ngx.log(ngx.CRIT, "Client " .. clientIp .. " committed REQ " .. requestCount ..  " times maximum allow " .. valueSituation1MaximumAllow  .. " within " .. valueDefaultObservationPeriodInSeconds .. " seconds, request url=" .. requestUrl);

            -- 重置requestCount防止高频fail2ban日志尾巴问题
            dictMyLimitReq:set(keySituation1RequestCount .. clientIp, 0);

            -- 防止日志尾巴
            dictLogTail:set(keyLogTail .. clientIp, clientIp, 60);
        end

        dictMyLimitReq:incr(keySituation1RequestCount .. clientIp, 1);
    end
end

-- 拦截5秒内超过50个请求情况
function _M.ccDetectionReqAccLimit(clientIp, requestUrl, dictMyLimitReq, dictLogTail)
    local keyLogTail = "logTail"
    if dictLogTail:get(keyLogTail .. clientIp) == nil then
        -- 默认观察周期5秒
        local valueDefaultObservationPeriodInSeconds = 5;
        -- 默认REQAcc committed观察周期60秒
        local valueDefaultREQAccCommittedObservationPeriodInSeconds = 60;
        -- 请求总次数
        local keySituation2RequestCount = "situation2RequestCount#";
        -- 允许最大请求总次数
        local valueSituation2RequestCountMaximumAllow = 50;
        -- 允许最大违规总次数
        local valueSituation2CommittedCountMaximumAllow = 4;
        -- 违规总次数
        local keySituation2CommittedCount = "situation2CommittedCount#";

        -- 设置相关key对应初始化value
        local requestCount = dictMyLimitReq:get(keySituation2RequestCount .. clientIp);
        if not requestCount then
            dictMyLimitReq:set(keySituation2RequestCount .. clientIp, 0, valueDefaultObservationPeriodInSeconds);
        end
        local committedCount = dictMyLimitReq:get(keySituation2CommittedCount .. clientIp);
        if not committedCount then
            dictMyLimitReq:set(keySituation2CommittedCount .. clientIp, 0, valueDefaultREQAccCommittedObservationPeriodInSeconds);
        end

        -- 判断5秒内是否超过50次
        local requestCount = dictMyLimitReq:get(keySituation2RequestCount .. clientIp);
        if requestCount >= valueSituation2RequestCountMaximumAllow then
            ngx.log(ngx.ERR, "客户端 " .. clientIp .. " REQAcc犯规+1，reqCnt=" .. requestCount .. ";maximumAllow=" .. valueSituation2RequestCountMaximumAllow);

            dictMyLimitReq:incr(keySituation2CommittedCount .. clientIp, 1);
            dictMyLimitReq:set(keySituation2RequestCount .. clientIp, 0, valueDefaultObservationPeriodInSeconds);

            local committedCount = dictMyLimitReq:get(keySituation2CommittedCount .. clientIp);
            if committedCount >= valueSituation2CommittedCountMaximumAllow then
                ngx.log(ngx.CRIT, "Client " .. clientIp .. " committed REQAcc " .. committedCount ..  " times maximum allow " .. valueSituation2CommittedCountMaximumAllow  .. " within " .. valueDefaultREQAccCommittedObservationPeriodInSeconds .. " seconds, request url=" .. requestUrl);
                dictMyLimitReq:set(keySituation2CommittedCount .. clientIp, 0, valueDefaultREQAccCommittedObservationPeriodInSeconds);

                -- 防止日志尾巴
                dictLogTail:set(keyLogTail .. clientIp, clientIp, 60);
            end
        end

        dictMyLimitReq:incr(keySituation2RequestCount .. clientIp, 1);
    end
end

-- https://blog.csdn.net/yinjinshui/article/details/118702545
function _M.ccGeoIpLimitation(clientIp, dictMyLimitReq, dictLogTail,
                enableGeoGlobal, enableGeoChinaMainland, enableGeoHongkong, enableGeoTaiwan, enableGeoBeijing, enableGeoFujian,
                enableGeoJiangxi, enableGeoHunan, enableGeoZhejiang, enableGeoChongqing)
    local keyLogTail = "logTail";
    if dictLogTail:get(keyLogTail .. clientIp) == nil then
        if enableGeoGlobal == nil then
            enableGeoGlobal = true
        end
        if enableGeoChinaMainland == nil then
            enableGeoChinaMainland = true
        end
        if enableGeoHongkong == nil then
            enableGeoHongkong = true
        end
        if enableGeoTaiwan == nil then
            enableGeoTaiwan = true
        end
        if enableGeoBeijing == nil then
            enableGeoBeijing = true
        end
        if enableGeoFujian == nil then
            enableGeoFujian = true
        end
        if enableGeoJiangxi == nil then
            enableGeoJiangxi = true
        end
        if enableGeoHunan == nil then
            enableGeoHunan = true
        end
        if enableGeoZhejiang == nil then
            enableGeoZhejiang = true
        end
        if enableGeoChongqing == nil then
            enableGeoChongqing = true
        end

        if not (enableGeoGlobal and enableGeoHongkong and
            enableGeoTaiwan and enableGeoBeijing and
            enableGeoFujian and enableGeoJiangxi and
            enableGeoHunan and enableGeoZhejiang and
            enableGeoChongqing and enableGeoChinaMainland)
        then
            local ban = false;
            --local res,err = geo.lookup(clientIp);
            local res, err = ip2regionLocation:search(clientIp)
            if res then
                local province = nil;
                local country = nil;
                --[[if not (res["subdivisions"] == nil) then
                    province = res["subdivisions"][1]["iso_code"];
                end
                if not (res["country"] == nil) then
                    country = res["country"]["iso_code"];
                end]]

                country = res["country"]
                province = res["province"]
                if country == "中国" and province == "香港" then
                        country = "HK"
                elseif country == "中国" and province == "台湾" then
                        country = "TW"
                elseif country == "中国" then
                        country = "CN"
                else
                        -- 非中国
                        country = "NCN"
                end
                if province == "广东" then
                        province = "GD"
                elseif province == "北京" then
                        province = "BJ"
                elseif province == "福建" then
                        province = "FJ"
                elseif province == "江西" then
                        province = "JX"
                elseif province == "湖南" then
                        province = "HN"
                elseif province == "浙江" then
                        province = "ZJ"
                elseif province == "重庆" then
                        province = "CQ"
                else
                        -- 其他省份
                        province = "OP"
                end

                if country == "CN" and not (province == nil) and province == "GD" then
                    ban = false;
                else
                    if not (country == "CN" or country == "HK" or country == "TW") and not enableGeoGlobal then
                        -- 全球关闭
                        ban = true;
                    elseif country == "HK" then
                        -- 香港
                        if not enableGeoHongkong then
                            ban = true;
                        end
                    elseif country == "TW" then
                        -- 台湾
                        if not enableGeoTaiwan then
                            ban = true;
                        end
                    elseif country == "CN" and not (province == nil) and province == "BJ" then
                        -- 北京
                        if not enableGeoBeijing then
                            ban = true;
                        end
                    elseif country == "CN" and not (province == nil) and province == "FJ" then
                                    -- 福建
                        if not enableGeoFujian then
                            ban = true;
                        end
                    elseif country == "CN" and not (province == nil) and province == "JX" then
                                    -- 江西
                        if not enableGeoJiangxi then
                            ban = true;
                        end
                    elseif country == "CN" and not (province == nil) and province == "HN" then
                                    -- 湖南
                        if not enableGeoHunan then
                            ban = true;
                        end
                    elseif country == "CN" and not (province == nil) and province == "ZJ" then
                                    -- 浙江
                        if not enableGeoZhejiang then
                            ban = true;
                        end
                    elseif country == "CN" and not (province == nil) and province == "CQ" then
                                    -- 重庆
                        if not enableGeoChongqing then
                            ban = true;
                        end
                    else
                        -- 其他省份
                        if country == "CN" and not enableGeoChinaMainland then
                            ban = true;
                        end
                    end
                end
            else
                -- 全球关闭
                if not enableGeoGlobal then
                    ban = true;
                end
            end

            if ban then
                ngx.log(ngx.CRIT, "Client " .. clientIp .. " committed RegionForbidden");

                -- 防止日志尾巴
                dictLogTail:set(keyLogTail .. clientIp, clientIp, 60);

                -- 打印geoip2解析结果到日志
                --[[local resString = "";
                if not (res == nil) then
                    resString = cjson.encode(res);
                end
                ngx.log(ngx.ERR, "客户端ip地址: " .. clientIp .. " 解析结果: " .. resString);]]
            end
        end
	end
end

-- 延迟客户端请求，控制频率
function _M.delay(clientIp)
        local dictMyLimitReq = ngx.shared.my_limit_req_store
        local keyDelayReqAccCount = "delayReqAccCount#"
        local valueDefaultObservationPeriodInSeconds = 2
        local valueDelayReqAccCountMaximumAllow = 15
        local requestCount = dictMyLimitReq:get(keyDelayReqAccCount .. clientIp);
        if not requestCount then
                dictMyLimitReq:set(keyDelayReqAccCount .. clientIp, 1, valueDefaultObservationPeriodInSeconds)
        end
        local requestCount = dictMyLimitReq:get(keyDelayReqAccCount .. clientIp)
        if requestCount > valueDelayReqAccCountMaximumAllow then
		        local randomSeconds = math.random(2, 5)
                ngx.log(ngx.ERR, "客户端 " .. clientIp .. " " .. valueDefaultObservationPeriodInSeconds .. "秒内请求" .. requestCount .. "次超过最大允许值" .. valueDelayReqAccCountMaximumAllow .. "次，请求被延迟" .. randomSeconds .. "秒")
                ngx.sleep(randomSeconds)
        end
        dictMyLimitReq:incr(keyDelayReqAccCount .. clientIp, 1);
end

function _M.intercept(clientIp,
                switchGlobal, switchChinaMainland, switchHongkong, switchTaiwan, switchBeijing, switchFujian,
                switchJiangxi, switchHunan, switchZhejiang, switchChongqing)
	-- 判断是否为aws health checker
    local userAgent = ngx.req.get_headers()["user-agent"]
    if not (userAgent == nil) and not (string.find(userAgent, "HealthChecker") == nil and string.find(userAgent, "Edge Health") == nil) then
        --ngx.log(ngx.ERR, "是health checker, user-agent：", userAgent)
        return
    --else
        --ngx.log(ngx.ERR, "不是health checker")
    end

	_M.delay(clientIp)

    local varDictLogTail = ngx.shared.dict_log_tail
    local requestUrl = _M.getRequestUrl();
    local dictMyLimitReq = ngx.shared.my_limit_req_store;

    _M.ccDetectionReqLimit(clientIp, requestUrl, dictMyLimitReq, varDictLogTail);
    _M.ccDetectionReqAccLimit(clientIp, requestUrl, dictMyLimitReq, varDictLogTail);

    _M.ccGeoIpLimitation(clientIp, dictMyLimitReq, varDictLogTail, switchGlobal, switchChinaMainland, switchHongkong, switchTaiwan, switchBeijing, switchFujian, switchJiangxi, switchHunan, switchZhejiang, switchChongqing);
end

return _M