function setup_gpio_pins()
    gpio.mode(indicator, gpio.OUTPUT)
    for k, v in pairs(my_gpio_pins) do
        gpio.mode(v, gpio.OUTPUT)
    end
end

function split(str,sep)
    local array = {}
    local reg = string.format("([^%s]+)",sep)
    for mem in string.gmatch(str,reg) do
        table.insert(array, mem)
    end
    return array
end

function get_mac_address()
    mac_address = wifi.sta.getmac()
    mac_address = string.gsub(mac_address,":","")
    return mac_address
end

function set_state(data)
    if string.match(data,"-") then
        local arr = split(data,"-")
        
        for k, v in pairs(arr) do
          gpio.write(4+tonumber(k),v)
        end
    else
        gpio.write(5,data)
    end
     
end

function send_login_request(sck)
    print("Build Login Request and Send")
    local login_command = "*SP," .. get_mac_address() .. ",LOGIN,0#"
    print(login_command)
    sck:send(login_command)  
end

function get_pin_state()
    local val =""
    for k, v in pairs(my_gpio_pins) do
        val = val .. gpio.read(v)
    end
    print(val)
    return val
end

function create_data_message()
    return "*SP," .. get_mac_address() .. ",DATA," .. get_pin_state() .. "#"
end

function start_writing_data(sck)
    timer = tmr.create()
    timer:register(30000, tmr.ALARM_AUTO, function()
        local message = create_data_message()
        print(message)
        sck:send(message)
    end)
    timer:start()
end

function process_response_from_socket(sck,data)
    local xVal = string.gsub(data,"*","")
    xVal = string.gsub(xVal,"#","")

    local array = split(xVal,",")

    local command = array[2]

    local state_data = array[3]

    print(command,state_data)

    if command == "LOGIN_SUCCESS" then
        print("Login Success Called")
        set_state(state_data)
        start_writing_data(sck)
    elseif command == "CHANGE_STATE" then
--        execute_gpio_command(sck,array[3])

    elseif command == "STATE_CHANGE" then
         set_state(state_data)    
    end
end


function connect_to_socket_server()
    client = net.createConnection(net.TCP,0)

    client:on("receive", function(sck, c)
         process_response_from_socket(sck,c)
        end)
    client:on("reconnection", function() 
        print("reconnection Called")
--        Low Indicator when Reconnect Called
         gpio.write(indicator,gpio.LOW)
        end)
    client:on("disconnection", function()
        print("disconnection Called") 
--        Low Indicator when Reconnect Called
         gpio.write(indicator,gpio.LOW)
        end)
    client:on("connection", function(sck)
--        start_writing_data(sck)
          send_login_request(sck)
          print("Connected")
          gpio.write(indicator,gpio.HIGH)

--        High Indicator and Low Temp Wifi when Reconnect Called
        
    end)
    client:connect(8547,"167.71.227.221")

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

                setup_gpio_pins()
                connect_to_socket_server()
                
                mytimer:unregister()
            end
        end)
    mytimer:start()
end


my_gpio_pins={5,6,7,8}
indicator = 2


if file.exists("config.lua") then
    wifi.sta.disconnect()
    dofile("config.lua")
    
    connect_actual_wifi(station_cfg)
    print(station_cfg,"HJHJHJHJ")

    for k, v in pairs(station_cfg) do
      print(k, v)
    end
    
else
--    connect_temporary_wifi()
    ssid, password, bssid_set, bssid=wifi.sta.getconfig()

    print("Else Block Called")

    if ssid == "" then
        enduser_setup.start(
          function()
            print("Connected to WiFi as:" .. wifi.sta.getip())  
            
            ssid, password, bssid_set, bssid=wifi.sta.getconfig() 

            fd = file.open("config.lua", "w+")

            if fd then
                fd.writeline('station_cfg={}')
                fd.writeline("station_cfg.ssid = " .. "\"" .. ssid .. "\"")
                fd.writeline("station_cfg.pwd = " .. "\"" .. password .. "\"")
                fd.close()
            end
    
            print(wifi.sta.getconfig())

            local station_cfg = {}
            station_cfg.ssid = ssid
            station_cfg.pwd = password

            connect_actual_wifi(station_cfg)

--            Connect To Server
          end,
          function(err, str)
            print("enduser_setup: Err #" .. err .. ": " .. str)
          end,
          print -- Lua print function can serve as the debug callback
        )
    else
        print("SSID NOT NIL " .. ssid)
--            Connect To Server
        ssid, password, bssid_set, bssid=wifi.sta.getconfig()
        local station_cfg = {}
        station_cfg.ssid = ssid
        station_cfg.pwd = password
        connect_actual_wifi(station_cfg)
    end
end




