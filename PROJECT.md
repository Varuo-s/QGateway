# QGateway

Version: Alpha Development

Author: Varuo-s

Project Type:
Open Source AI Runtime

---

# Vision

QGateway 不是一个简单的 API Gateway。

它应该成为：

> Docker 管容器，
> QGateway 管 AI Runtime。

目标：

统一管理所有本地 AI 推理服务、客户端、MCP、Agent、Workspace。

未来支持：

- llama.cpp
- Ollama
- LM Studio
- vLLM
- TensorRT-LLM
- OpenAI Compatible API

并兼容：

- Codex
- Cline
- Continue
- Roo Code
- Cursor
- Claude Code
- OpenAI SDK

---

# Development Principles

整个项目必须遵守以下原则。

## 1.

代码必须稳定优先。

不要为了快速开发而堆代码。

宁可功能少，也不要 Bug 多。

---

## 2.

所有功能必须模块化。

禁止把大量逻辑写到一个文件。

例如：

backend/

services/

providers/

routers/

utils/

config/

每个模块职责单一。

---

## 3.

任何功能必须能够单独测试。

例如：

Model Scanner

Launcher

Responses API

Router

都必须可以独立运行。

---

## 4.

Windows 与 macOS 必须保持一致。

不得只支持 Windows。

路径必须统一使用 pathlib。

禁止写死：

D:\

C:\

/Users/...

全部自动检测。

---

## 5.

配置必须来自配置文件。

禁止硬编码。

例如：

config.yaml

或者

config.json

---

## 6.

任何 Provider 都必须实现统一接口。

例如：

class BaseProvider

connect()

models()

chat()

responses()

embeddings()

health()

未来：

llama.cpp

Ollama

LM Studio

全部继承。

---

# Technology Stack

Backend

Python

FastAPI

httpx

uvicorn

pydantic

PyYAML

Frontend

Vue3

TypeScript

Vite

Element Plus

Icons

@element-plus/icons-vue

Charts

ECharts

Storage

SQLite

Later:

PostgreSQL

---

# Project Structure

QGateway/

backend/

frontend/

docs/

tests/

scripts/

installer/

.github/

README.md

LICENSE

PROJECT.md

---

# Milestone

## Alpha 0.1

目标：

建立真正可运行项目。

功能：

FastAPI

Health API

Web UI

Dashboard

Settings

Log Viewer

Model Scanner

Launcher

Requirements：

浏览器打开：

http://127.0.0.1:4000

即可使用。

---

## Alpha 0.2

加入：

Models 页面

扫描 Models

支持：

AI/

Models/

models/

自动识别 GGUF

显示：

名称

大小

量化

路径

---

## Alpha 0.3

Launcher

自动寻找：

llama-server

Windows

macOS

Linux

一键启动

停止

实时状态

---

## Alpha 0.4

Responses API

实现：

GET /v1/models

POST /v1/responses

兼容：

Codex

OpenAI SDK

Responses API Streaming

---

## Alpha 0.5

Playground

聊天

Streaming

参数：

Temperature

Top P

Max Tokens

Stop

Reasoning

---

## Alpha 0.6

Clients

生成：

Codex

Cline

Continue

配置。

支持：

复制

下载

自动检测。

---

## Alpha 0.7

Logs

实时日志

自动刷新

过滤：

INFO

WARN

ERROR

搜索

下载

---

## Alpha 0.8

Settings

Gateway

Provider

Model

Context

GPU Layers

Flash Attention

Reasoning

保存配置

---

## Alpha 0.9

Workspace

多个 Workspace

多个配置

多个模型

多个 Provider

---

## Alpha 1.0

Release

发布：

Windows

macOS

Linux

Installer

Portable

Docker

---

# UI Design

整体参考：

Docker Desktop

LM Studio

Ollama App

风格：

Dark

Modern

Clean

左侧导航：

Dashboard

Runtime

Models

Playground

Clients

Logs

Settings

About

右侧：

Card Layout

禁止使用传统后台风格。

---

# Development Workflow

任何代码开发遵守：

Design

↓

Implement

↓

Run

↓

Fix

↓

Commit

↓

Push

↓

Next

每完成一个功能必须：

运行

确认

再继续。

禁止一次生成大量未经测试代码。

---

# Git Commit Style

feat:

fix:

refactor:

docs:

style:

perf:

test:

build:

例如：

feat: add GGUF model scanner

fix: responses streaming bug

refactor: split launcher module

---

# AI Coding Rules

Codex 必须：

不要一次修改几十个文件。

一次完成一个功能。

每完成：

运行测试。

如果失败：

优先修复。

不得继续开发新功能。

任何新增代码：

必须保持可维护。

不要生成重复代码。

优先复用已有模块。

---

# Current Goal

当前只做：

Alpha 0.1

目标：

建立真正可运行项目。

不是 Demo。

不是概念设计。

而是 GitHub 上真正的开源项目。

以后所有开发，都必须遵守 PROJECT.md。