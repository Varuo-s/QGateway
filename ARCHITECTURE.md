# QGateway Architecture

Version

Alpha

Author

Varuo-s

Architecture

Modular

Plugin-based

Cross-platform

---

# Philosophy

QGateway 的定位：

Open Source AI Runtime

而不是：

Local AI Gateway

它负责：

Provider

↓

Router

↓

Runtime

↓

Workspace

↓

Tools

↓

Clients

↓

Agent

统一管理。

整个系统必须保持：

高内聚

低耦合

模块独立。

---

# High Level Architecture

                UI

                 │

                 ▼

          REST API Layer

                 │

      ┌──────────┴──────────┐

      ▼                     ▼

 Runtime Manager      Workspace Manager

      │                     │

      ▼                     ▼

 Provider Router      Config Manager

      │

 ┌────┼─────────────┐

 ▼    ▼             ▼

llama.cpp

Ollama

LM Studio

vLLM

      │

      ▼

 OpenAI Compatible API

---

# Backend Structure

backend/

api/

providers/

runtime/

launcher/

workspace/

router/

mcp/

clients/

config/

database/

models/

utils/

logging/

services/

---

# Frontend Structure

frontend/

views/

components/

layouts/

router/

stores/

assets/

api/

types/

plugins/

---

# Provider Layer

所有 Provider 必须继承：

BaseProvider

接口：

connect()

disconnect()

health()

list_models()

chat()

responses()

embeddings()

tokenize()

detokenize()

每个 Provider 不允许直接操作 UI。

---

# Runtime

Runtime Manager

负责：

启动

停止

重启

检测状态

自动恢复

日志

PID

端口检测

以后支持多个 Runtime。

---

# Launcher

Launcher 负责：

自动检测：

llama.cpp

ollama

lmstudio

自动构建启动参数。

不得包含业务逻辑。

---

# Workspace

Workspace 保存：

Provider

Model

Temperature

TopP

Context

System Prompt

Clients

每个 Workspace 独立。

---

# Router

Router 不负责推理。

Router 只负责：

收到请求

↓

找到 Provider

↓

转发

↓

返回

不得加入模型逻辑。

---

# Config

所有配置统一：

config.yaml

包括：

Gateway

Providers

Launcher

Workspace

Clients

Logs

MCP

---

# Database

SQLite

保存：

Workspace

History

Logs

Preferences

Providers

Later：

PostgreSQL

---

# Logs

统一：

logging service

所有模块：

只能：

logger.info()

logger.error()

不得 print()

---

# API

所有 API：

RESTful

版本：

/api/v1/

OpenAI：

/v1/models

/v1/chat/completions

/v1/responses

---

# Responses

Responses API

必须完全兼容 OpenAI。

Streaming：

SSE

不得使用 websocket。

---

# Model Scanner

自动扫描：

Models/

models/

AI/Models/

支持：

GGUF

未来：

Safetensors

ONNX

MLX

---

# Plugin

Plugin Interface

未来：

Python Plugin

JavaScript Plugin

MCP Plugin

统一：

plugins/

---

# MCP

MCP Manager

负责：

启动

关闭

注册

发现

Tool List

Provider 无权管理 MCP。

---

# Clients

支持：

Codex

Cline

Continue

Cursor

Claude Code

Roo

OpenAI SDK

生成：

config

JSON

TOML

YAML

---

# UI

左侧导航：

Dashboard

Runtime

Providers

Models

Playground

Clients

Workspace

Logs

Settings

About

---

# Design Rules

禁止：

God Object

God Class

单文件超过：

800 行

超过必须拆分。

---

# Coding Rules

禁止：

复制代码

硬编码

平台判断散落

所有：

Windows

Linux

macOS

统一：

platform.py

---

# Future

Alpha

↓

Beta

↓

RC

↓

1.0

以后：

Provider

Plugin

MCP

Agent

全部热插拔。