# bottle.app
a python web app server framework based on bottle.py

## What?
bottle.app is an instantly available web app server written in Python based on [bottle.py](http://www.bottlepy.org), a lightweight web framework. With ready-to-use feature for http protocol, request routing and handling, storage access wrappper, logging, Testing, and more, the web app server has been supporting enormous user access to the [game community site](http://forum.tgp.qq.com/bbs.html).

### Architecture
to be continued

### Http Protocol Parser
Based on `Bottle.request`, it is very convenient to handle incoming http request by parsing and wrapping parameters, and provide parameters abstraction (uri parameters or get/post data) for the request handling modules(main logic part for web project). It is integrated in the framework so that no extra code needs written for http protocol parsing. 

### Request routing and handling
The framework class `Bottle` makes a comprehensive abstraction of request routing. By hooking handler function of the `Bottle` class, it is very extensiable to customize request routing policy. 

The `bottle.app` routes request by uri path deduction: with static file on the intended path, return to web client with the static file; otherwise, regard the uri as an argument collection for app business module request. 

For instance, `http://localhost/index.html` is conceived to be static resource as `/index.html` exist in default directory, and `http://localhost/api/hello/display` is regarded as a dynamic request, with which the module name is `Hello` and handler function is `display`.

### Storage Access Wrapper

### Logging

### Testing


## Why?

## How?
