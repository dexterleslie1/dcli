local cjson=require 'cjson'
local geo=require 'resty.maxminddb'

-- 初始化geo
if not geo.initted() then
    geo.init("/usr/local/openresty/GeoLite2-City.mmdb")
end

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
function _M.ccDetectionReqLimit(clientIp, requestUrl, dictMyLimitReq)
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
    end

    dictMyLimitReq:incr(keySituation1RequestCount .. clientIp, 1);
end

-- 拦截5秒内超过50个请求情况
function _M.ccDetectionReqAccLimit(clientIp, requestUrl, dictMyLimitReq)
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
        end
    end

    dictMyLimitReq:incr(keySituation2RequestCount .. clientIp, 1);
end

-- https://blog.csdn.net/yinjinshui/article/details/118702545
function _M.ccGeoIpLimitation(clientIp, dictMyLimitReq,
                switchGlobal, switchChinaMainland, switchHongkong, switchTaiwan, switchBeijing, switchFujian,
                switchJiangxi, switchHunan, switchZhejiang, switchChongqing)
	if not (switchGlobal == 1 and switchHongkong == 1 and
		switchTaiwan == 1 and switchBeijing == 1 and
		switchFujian == 1 and switchJiangxi == 1 and
		switchHunan == 1 and switchZhejiang == 1 and
		switchChongqing == 1)
	then
		local ban = 0;
		local res,err = geo.lookup(clientIp);
		-- ngx.log(ngx.CRIT, cjson.encode(res));
		if res then
			local province = nil;
			local country = nil;
			if not (res["subdivisions"] == nil) then
				province = res["subdivisions"][1]["iso_code"];
			end
			if not (res["country"] == nil) then
				country = res["country"]["iso_code"];
			end

			if country == "CN" and not (province == nil) and province == "GD" then
				ban = 0;
			else
				if not (country == "CN" or country == "HK" or country == "TW") and switchGlobal == 0 then
					-- 全球关闭
					ban = 1;
				elseif country == "HK" then
					-- 香港
					if switchHongkong == 0 then
						ban = 1;
					end
				elseif country == "TW" then
					-- 台湾
					if switchTaiwan == 0 then
						ban = 1;
					end
				elseif country == "CN" and not (province == nil) and province == "BJ" then
					-- 北京
					if switchBeijing == 0 then
						ban = 1;
					end
				elseif country == "CN" and not (province == nil) and province == "FJ" then
                    -- 福建
					if switchFujian == 0 then
						ban = 1;
					end
				elseif country == "CN" and not (province == nil) and province == "JX" then
                    -- 江西
					if switchJiangxi == 0 then
						ban = 1;
					end
				elseif country == "CN" and not (province == nil) and province == "HN" then
                    -- 湖南
					if switchHunan == 0 then
						ban = 1;
					end
				elseif country == "CN" and not (province == nil) and province == "ZJ" then
                    -- 浙江
					if switchZhejiang == 0 then
						ban = 1;
					end
				elseif country == "CN" and not (province == nil) and province == "CQ" then
                    -- 重庆
					if switchChongqing == 0 then
						ban = 1;
					end
				else
					-- 其他省份
					if country == "CN" and switchChinaMainland == 0 then
						ban = 1;
					end
				end
			end
		else
			-- 全球关闭
			if switchGlobal == 0 then
				ban = 1;
			end
		end

		local keyLogTail = "geoIpLimitLogTail";
		if ban == 1 and dictMyLimitReq:get(keyLogTail .. clientIp) == nil then
			ngx.log(ngx.CRIT, "Client " .. clientIp .. " committed RegionForbidden");

			-- 防止日志尾巴
			dictMyLimitReq:set(keyLogTail .. clientIp, clientIp, 5);

			-- 打印geoip2解析结果到日志
            local resString = "";
            if not (res == nil) then
                resString = cjson.encode(res);
            end
            ngx.log(ngx.ERR, "客户端ip地址: " .. clientIp .. " 解析结果: " .. resString);
		end
	end
end

return _M