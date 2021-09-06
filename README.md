# teardown-http
A rough experiment to allow for HTTP GET requests to be made from a Teardown mod in-game. It uses a python server to monitor changes to your `savegame.xml` (but does not write to it) to look for the local content mod's `request_uuid` and `request_url` keys, and sends the request. The response is written to a lua file, with the name being the uuid that was sent along with the initial request, and the mod reads this lua file with `dofile()`.

![](https://i.imgur.com/INtX0dw.png)

There are a few technical challenges that made me do it in this specific way:
- `dofile()` will not read from the file each call, it caches it when it's first read. This means I can't simply create one `request.lua` file and update it each time, so I went with the uuid name method.
- Updating the `savegame.xml` with new data was unfavorable for many reasons: it's not safe, Teardown won't even detect the change because it wasn't made with one of it's Set() functions, and it would be a mess to properly parse json out of an xml key due to the formatting restrictions (of which lua's multiline strings do not have)
- There is no I/O functionality exposed to Teardown modders (as far as I'm aware) outside of the registry, meaning the python server would need to monitor this file for changes and parse out the needed keys

The fact that it uses the registry to communicate with the python server, and the very fact that a python server needs to run in the background in the first place, makes this impractical for any real uses, hence why it's referred to as an experiment and not a tool. Although, feel free to mess around with it! I had fun working around the limitations to get any sort of http request capabilities possible. There's probably ways of doing this better, so feel free to submit a pr if you've found a better method.

# How to use

The `net` folder needs to be dragged into your `Documents/Teardown/mods` folder. You will need to download [json.lua](https://github.com/rxi/json.lua) and place it in your game's `Teardown/data` folder, as well as create a `requests` folder in the same location. After that, edit the variables at the top of `server.py` accordingly and run the python server. In teardown, open the "net" map and you'll probably (but maybe not - this is not very well tested) see the request and its response pop up as debug prints.
