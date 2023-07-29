---
title: Building a Dormitory Webserver from scratch
date: 2023-07-29 14:05
tags: 
decsription:
cover: https://api.r10086.com/%E6%A8%B1%E9%81%93%E9%9A%8F%E6%9C%BA%E5%9B%BE%E7%89%87api%E6%8E%A5%E5%8F%A3.php?%E5%9B%BE%E7%89%87%E7%B3%BB%E5%88%97=%E5%8A%A8%E6%BC%AB%E7%BB%BC%E5%90%882
---


# Building a Dormitory Web Server from Scratch

A few months ago, I ventured into hosting my personal blog on my first ever cloud server. The affordability was certainly attractive, but the server's limited capabilities couldn't handle too many tasks or support a development environment. However, with a PC and a spare laptop in my dormitory, both equipped with a development environment, the idea of setting up a web server that could be accessed over the school's LAN seemed like a plausible solution. The one obstacle was its lack of accessibility over the public Internet.

This challenge piqued my curiosity, and within four days, I found a solution. In this article, I'll share the architecture of my network and explain how it works.

## Domain Selection and Cloud Server Nginx

I had a cloud server available on the public Internet at `1.xx.xx.xx`. The first step was to set up an Nginx server on this cloud server. Since location `/` had already been assigned to my blog server, the task was to decide the entry point to my dormitory server.

Initially, I considered creating another location section on Nginx to serve as the dormitory server's entry point. This worked well, but there was a hitch. My main domain utilized CDN acceleration, which unfortunately did not support the `WebSocket` service. Consequently, the hot reload module from my `vite` development server was compromised.

The solution was to establish a subdomain, `school.zimeng.work`, from my main domain. After securing an SSL certificate and WSS CDN for it, I had an operational entry point. This subdomain, still directed to the cloud server, also allowed me to practice my Nginx skills while reducing the coupling between my current and previous services.

To upgrade the system, I needed to create another server section that recognized `school.zimeng.work` as the server name. Nginx identifies incoming requests primarily by server_name, which is the address or domain we request in our browser. For this subdomain, I created a new server block.

This server block functions as a reverse proxy server, redirecting incoming requests to an FRP server that operates on the same cloud host. The FRP server's task is to expose my dormitory server hidden behind the school's local LAN.

## FRP Server

The FRP Server is a tool used to expose servers that are either behind a NAT or not available on the Internet. It needs a public host available on the Internet as a FRP server. Once you've configured the client server on the device you wish to expose, the connection between the server and clients becomes operational.

In this setup, the http connection between the cloud server and my dormitory server was crucial. To create a uniform interface, I configured another Nginx server at the dormitory to serve as the outgoing interface for all web apps hosted in the dormitory LAN. As a result, the FRP connection only maintains one communication channel between the cloud server's Nginx and the dormitory's Nginx server.

In essence, any requests to `school.zimeng.work` get dumped by the cloud server's Nginx to the FRP server. The FRP server then forwards these requests to a uniform `http` channel reaching the dormitory Nginx server. The requests for different web apps are recognized here and dispatched to the relevant servers within the dormitory LAN. 

> Note: I encountered difficulties configuring a `https` FRP connection. This represents a security risk as users are unaware of this issue during connection. It remains an area that needs further exploration.

## Dormitory Nginx Server

As previously mentioned, I installed another Nginx server as the outward interface to establish a uniform FRP tunnel and a more flexible, extensible configuration for the dormitory LAN web apps. Before setting up this Nginx server, I had to configure the FRP client to receive messages from the FRP server. I redirected these received requests to ports 80 and 443, where the Nginx server runs on the same host.

> Note: I bypassed NAT penetration on my dormitory router here. FRP doesn't require NAT penetration, eliminating the need for this configuration. However, with Nginx already in place, enabling HTTP services at ports 80 and 443 within the school's LAN could be useful. If you wish to have Nginx listen for requests from the school's LAN, NAT penetration for ports 80 and 443 at the gateway-side becomes necessary.

The next step was to configure the dormitory's Nginx server as a reverse proxy server. I utilized `proxy_pass` extensively in my configuration. It allowed me to build locations such as `/api/` or `/webapp/`, which provided semantic clarity and better coupling between different parts.

That concludes the overview of my dormitory server architecture. I hope you find it insightful and helpful.