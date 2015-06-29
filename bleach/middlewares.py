#!/usr/bin/env python
# coding=utf-8
"""
File: middlewares.py.py
Author: CHENZY
Date: 2015/06/15
"""
# Importing base64 library because we'll need it ONLY in case if the proxy we are going to use requires authentication
import base64

class ProxyMiddleware(object):
    # overwrite process request
    def process_request(self, request, spider):
        # Set the location of the proxy
        request.meta['proxy'] = "http://127.0.0.1:8118"
        # Use the following lines if your proxy requires authentication
        # proxy_user_pass = "USERNAME:PASSWORD"
        # setup basic authentication for the proxy
        # encoded_user_pass = base64.encodestring(proxy_user_pass)
        # request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass