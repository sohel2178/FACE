function setup_gpio_pins()
    gpio.mode(indicator, gpio.OUTPUT)
    gpio.mode(lock_pin, gpio.OUTPUT)
    gpio.mode(buzzer_pin, gpio.OUTPUT)

    gpio.write(lock_pin,gpio.LOW)
    gpio.write(buzzer_pin,gpio.LOW)
    gpio.write(indicator,gpio.LOW)
end

function set_low_state()
    local mytimer = tmr.create()
    mytimer:register(5000, tmr.ALARM_AUTO, function() 
             gpio.write(lock_pin,gpio.LOW)
             gpio.write(buzzer_pin,gpio.LOW)

            mytimer:unregister()
        end)
    mytimer:start()

end

function unlock_pin()
    if gpio.read(lock_pin)== gpio.LOW then
        gpio.write(lock_pin,gpio.HIGH)
        gpio.write(buzzer_pin,gpio.HIGH)
        set_low_state()
    end
end

function create_server()
    print("Server Connected")
    gpio.write(indicator,gpio.HIGH)
    srv=net.createServer(net.TCP)
    srv:listen(8888,function(conn)
      conn:on("receive",function(conn,payload)
        payload = string.gsub(payload, "%s+", "")

        print(payload)

        if payload == "UNLOCK" then
            unlock_pin()
        end

        
        
      end)
      conn:on("sent",function(conn) 
        print("Sent")
      end)
    end)
end

function write_config_file(ssid,password)
    
    fd = file.open("config.lua", "w+")
    
    if fd then
        fd.writeline('station_cfg={}')
        fd.writeline("station_cfg.ssid = " .. "\"" .. ssid .. "\"")
        fd.writeline("station_cfg.pwd = " .. "\"" .. password .. "\"")
        fd.close()
    end
end

function get_station_config(ssid,password)
    local station_cfg = {}
    station_cfg.ssid = ssid
    station_cfg.pwd = password

    return station_cfg
end

function get_mac_address()
    mac_address = wifi.sta.getmac()
    mac_address = string.gsub(mac_address,":","")
    return mac_address
end

function quote(str)
    return "\""..str.."\""
end




function post_ip_and_port(ip,port)
    print(ip,port)
    print(get_mac_address())

    local body = "{" .. quote("mac_address") .. ":" .. quote(get_mac_address()) .. "," .. quote("ip") .. ":" .. quote(ip) .. "," .. quote("port") ..":" .. quote(port) .. "}"
    print(body)
    http.post('http://167.71.227.221:2255/api/cameradevices',
      'Content-Type: application/json\r\n',
      body,
      function(code, data)
        if (code < 0) then
          print("HTTP request failed")
        else
          if code ==201 then
            setup_gpio_pins()
            create_server()
            
          end
        end
    end)
end

function connect_actual_wifi(station_cfg)

    wifi.sta.disconnect()
    wifi.setmode(wifi.STATION)
    
    wifi.sta.config(station_cfg)
    wifi.sta.connect()
    
    local mytimer = tmr.create()
    mytimer:register(10000, tmr.ALARM_AUTO, function() 
            if(wifi.sta.getip()~=nil) then
                print("Actual Wifi is Connected ")

                post_ip_and_port(wifi.sta.getip(),port)

--                setup_gpio_pins()
--                connect_to_socket_server()
                
                mytimer:unregister()
            end
        end)
    mytimer:start()
end


function end_user_setup()
    ssid, password, bssid_set, bssid=wifi.sta.getconfig()

    if ssid == "" then
        enduser_setup.start(
          function()
            print("Connected to WiFi as:" .. wifi.sta.getip())

            ssid, password, bssid_set, bssid=wifi.sta.getconfig()

--            Write Config File
            write_config_file(ssid,password)
            
    
            print(wifi.sta.getconfig())

--            local station_cfg = {}
--            station_cfg.ssid = ssid
--            station_cfg.pwd = password

            connect_actual_wifi(get_station_config(ssid,password))

--            Connect To Server
          end,
          function(err, str)
            print("enduser_setup: Err #" .. err .. ": " .. str)
          end,
          print -- Lua print function can serve as the debug callback
        )
    else
        print("SSID NOT NIL " .. ssid)
--        local station_cfg = {}
--        station_cfg.ssid = ssid
--        station_cfg.pwd = password
        connect_actual_wifi(get_station_config(ssid,password))
    end

end


indicator = 8
lock_pin = 1
buzzer_pin = 2
port = 8888

if file.exists("config.lua") then
    wifi.sta.disconnect()
    dofile("config.lua")
    connect_actual_wifi(station_cfg)
    print(station_cfg,"HJHJHJHJ")
    
else
    end_user_setup()
end
