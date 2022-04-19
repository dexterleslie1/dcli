local _M = { _VERSION = '1.0.0' }

-- 获取客户端真实ip地址
function _M.getClientIp()
        local headers=ngx.req.get_headers()
        local clientIp;
        local xForwardedFor = headers["X_Forwarded_For"];
        if not xForwardedFor then
                xForwardedFor = "";
        end
        -- ngx.log(ngx.WARN, "X-Forwarded-For=" .. xForwardedFor);
        if xForwardedFor then
                local count = 0;
                for k, v in string.gmatch(xForwardedFor, "[^,]+") do
                        if count==0 then
                                clientIp = k;
                                -- ngx.log(ngx.WARN, "X-Forwarded-For=" .. xForwardedFor .. "提取到客户端ip地址:" .. clientIp);
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

-- 拦截5秒内超过120个请求情况
function _M.ccDetectionReqLimit(clientIp, requestUrl, dictMyLimitReq)
    -- 默认观察周期5秒
    local valueDefaultObservationPeriodInSeconds = 5;
    -- 请求总次数
    local keySituation1RequestCount = "situation1RequestCount#";
    -- 允许最大请求总次数
    local valueSituation1MaximumAllow = 120;

    -- 设置相关key对应初始化value
    local requestCount = dictMyLimitReq:get(keySituation1RequestCount .. clientIp);
    if not requestCount then
        dictMyLimitReq:set(keySituation1RequestCount .. clientIp, 0, valueDefaultObservationPeriodInSeconds);
    end

    -- 判断5秒内是否超过120次
    local requestCount = dictMyLimitReq:get(keySituation1RequestCount .. clientIp);
    if requestCount >= valueSituation1MaximumAllow then
        ngx.log(ngx.WARN, "Client " .. clientIp .. " committed REQ " .. requestCount ..  " times maximum allow " .. valueSituation1MaximumAllow  .. " within " .. valueDefaultObservationPeriodInSeconds .. " seconds, request url=" .. requestUrl);

        -- 重置requestCount防止高频fail2ban日志尾巴问题
        dictMyLimitReq:set(keySituation1RequestCount, 0);
    end

    dictMyLimitReq:incr(keySituation1RequestCount .. clientIp, 1);
end

-- 拦截5秒内超过50个请求情况
function _M.ccDetectionReqAccLimit(clientIp, requestUrl, dictMyLimitReq)
    -- 默认观察周期5秒
    local valueDefaultObservationPeriodInSeconds = 5;
    -- 默认REQAcc committed观察周期60秒
    local valueDefaultREQAccCommittedObservationPeriodInSeconds = 120;
    -- 请求总次数
    local keySituation2RequestCount = "situation2RequestCount#";
    -- 允许最大请求总次数
    local valueSituation2RequestCountMaximumAllow = 50;
    -- 允许最大违规总次数
    local valueSituation2CommittedCountMaximumAllow = 9;
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
        ngx.log(ngx.WARN, "客户端 " .. clientIp .. " REQAcc犯规+1，reqCnt=" .. requestCount .. ";maximumAllow=" .. valueSituation2RequestCountMaximumAllow);

        dictMyLimitReq:incr(keySituation2CommittedCount .. clientIp, 1);
        dictMyLimitReq:set(keySituation2RequestCount .. clientIp, 0, valueDefaultObservationPeriodInSeconds);

        local committedCount = dictMyLimitReq:get(keySituation2CommittedCount .. clientIp);
        if committedCount >= valueSituation2CommittedCountMaximumAllow then
            ngx.log(ngx.WARN, "Client " .. clientIp .. " committed REQAcc " .. committedCount ..  " times maximum allow " .. valueSituation2CommittedCountMaximumAllow  .. " within " .. valueDefaultREQAccCommittedObservationPeriodInSeconds .. " seconds, request url=" .. requestUrl);
        end
    end

    dictMyLimitReq:incr(keySituation2RequestCount .. clientIp, 1);
end

return _M