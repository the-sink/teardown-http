local json = dofile("data/json.lua") -- Download from https://github.com/rxi/json.lua and place in Teardown/data folder

local request

local function uuid()
    local template ='xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'
    return string.gsub(template, '[xy]', function (c)
        local v = (c == 'x') and math.random(0, 0xf) or math.random(8, 0xb)
        return string.format('%x', v)
    end)
end

function tick() -- Check for an open request, and close it if a response has been given by the python server
    if request ~= nil then
        pcall(function()
            local response = dofile("data/requests/" .. request.uuid .. ".lua")
            if response ~= nil then
                request.callback(response)
                request = nil
            end
        end)
    end
end

local function make_request(url, callback) -- Request function: sets the savegame keys to communicate with the python server and assigns the request variable
    local uuid = uuid()
    DebugPrint("Sending HTTP GET request to url " .. url .. " ... generated UUID is " .. uuid)
    SetString("savegame.mod.request_url", url)
    SetString("savegame.mod.request_uuid", uuid)
    request = {uuid = uuid, callback = callback}
end

make_request("https://jsonplaceholder.typicode.com/todos/1", function(response) -- Example request
    DebugPrint("Response: " .. response)

    local content = json.decode(response)

    DebugPrint("Content of 'title' key: " .. content.title)
end)