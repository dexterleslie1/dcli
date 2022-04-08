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

return _M