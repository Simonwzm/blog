---
title: Clash-Tracing Deployment
date: 2023-10-19 00:26
tags: [Docker, Clash]
description: Click in for more details
cover: https://api.r10086.com/%E6%A8%B1%E9%81%93%E9%9A%8F%E6%9C%BA%E5%9B%BE%E7%89%87api%E6%8E%A5%E5%8F%A3.php?%E5%9B%BE%E7%89%87%E7%B3%BB%E5%88%97=%E5%8A%A8%E6%BC%AB%E7%BB%BC%E5%90%882
---

# Clash-Tracing Deployment


Recently I deployed a clash server behind my dormitory router, but in the past few days I have noticed an unusual increase in proxy dialing traffic. Hence I wanted to investigate into what have been causing the exceptional high traffic overhead. I leverage the tool called `clash-tracing` and thereby I'm here to record how I deployed it in my dormitory network.

### Demand Analysis

What I want is a tool that can run in windows platform and can monitor the proxy traffic of clash.

`clash-tracing` utilizes clash core's `tracing` feature which send logging info out from the core using `websocket` . Then it uses `loki` to store the data in the database and finally visualizes it using `grafana`.

The whole service is wrapped in a docker environment. A docker compose file is used to regulate all third-party containers used in `clash-tracing` and designate the instructions each container need to performs to connect them together.

![image-20231019002304185](https://s2.loli.net/2023/10/19/IprmdXeYn3ftJMC.png)

However, the whole service is meant to be running on Linux. It remains uncertain whether windows platform will support the environment used in the service. So I begin to explore it deeper.

### Trails and Errors

The good news is that in windows docker offers the docker desktop which is an even more noob-friendly tool to set up a docker environment similar to Linux, as it provides visualization and GUIs replacing commands that are hard to remember.

The first time I try to use docker to set up the whole service, it fails to open port 3000 for the `grafana` container. Thanks to GPT, I quickly addressed the problem by setting the port mapping from `3000->3000` to `3000->13000`

But still, although all the containers are running now, `websocat` containers raises error logs that the `websocket` connection to the clash core is malfunctioning. I used the `wscat` tool to connect to the clash core logging server URL, and it returned with correct response. Thanks again to GPT, it found out that the URL specified in the `docker-compose` file uses `127.0.0.1` to represent the host machine. But that `127.0.0.1` will be interpreted by the container as the container itself. The correct form should be `host.docker.internal`

Finally, just to mention that if you are using clash-for-windows, the clash_host URL should be  in  `/user/.config/clash/.config` , specified by the term `external-handler`.

After all these changes to the `docker-compose` file, if you also have an environment to run docker, all preparation steps are done. 

Just run docker either in GUI interface or in shell `docker-compose up -d` (remember to install docker-compose using scoop, extremely fast!)

The configured `docker-compose.yml` is given below

```yaml
version: '3'
services:
  loki:
    image: grafana/loki:2.8.0
    container_name: loki
    restart: always
    user: "0"
    volumes:
      - ./loki/data:/loki
      - ./loki/config.yaml:/etc/loki/local-config.yaml
  grafana:
    image: grafana/grafana-oss:latest
    container_name: grafana
    restart: always
    user: "0"
    volumes:
      - ./grafana/data:/var/lib/grafana
      - ./grafana/panels:/etc/dashboards
      - ./grafana/provisioning/dashboards:/etc/grafana/provisioning/dashboards
      - ./grafana/provisioning/datasources:/etc/grafana/provisioning/datasources
    ports:
      - "13000:3000"
  vector:
    image: timberio/vector:0.X-alpine
    container_name: vector
    restart: always
    volumes:
      - ./vector/vector.toml:/etc/vector/vector.toml
    depends_on:
      - loki
  traffic_scraper:
    image: vi0oss/websocat:0.10.0
    container_name: traffic_scraper
    restart: always
    command: -v --autoreconnect-delay-millis 15000 autoreconnect:ws://host.docker.internal:1206/traffic?token= autoreconnect:tcp:vector:9000
    depends_on:
      - vector
  tracing_scraper:
    image: vi0oss/websocat:0.10.0
    container_name: tracing_scraper
    restart: always
    command: -v --autoreconnect-delay-millis 15000 autoreconnect:ws://host.docker.internal:1206/profile/tracing?token= autoreconnect:tcp:vector:9000
    depends_on:
      - vector
```

