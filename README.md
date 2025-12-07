# 🚦 基于 RAG 的开放式交通流仿真代码生成系统

## 🌟 项目简介

本项目旨在构建一个基于RAG技术和大语言模型的代码生成系统，用于自动化生成SUMO (Simulation of Urban Mobility)平台的交通流仿真配置文件（如路网文件 `.net.xml`、路由文件 `.rou.xml` 等）。

通过整合 CodeGeeX4-9B 和 BGE-M3 模型，并搭建 Open-WebUI 前端界面，项目实现了用户通过自然语言描述仿真需求，系统即可自动生成可执行的 SUMO 配置代码，大幅降低了交通仿真建模的技术门槛。

### 核心技术栈

* [cite_start]**基座模型 (LLM):** CodeGeeX4-9B (代码生成) [cite: 37]
* [cite_start]**嵌入模型 (Embedding):** BGE-M3 (RAG 检索) [cite: 40]
* [cite_start]**模型服务框架:** Ollama [cite: 5]
* [cite_start]**前端界面:** Open-WebUI [cite: 29]
* [cite_start]**内网穿透与安全:** Frp + Token 认证 + SSH 密钥 [cite: 66, 79, 109, 151]

## 🚀 部署指南

本指南假设您已拥有一个可供部署的内网环境（如阿里云 DSW 实例）和一个公网服务器（如阿里云 ECS 或 VPS），并使用 `root` 或具有 `sudo` 权限的用户进行操作。

### 阶段一：基础框架部署（在内网 DSW 终端执行）

#### 1. Ollama 框架部署

Ollama 用于轻量化部署 CodeGeeX4 和 BGE-M3 模型。

```bash
# 1. 安装 Ollama
[cite_start]curl -fsSL [https://ollama.com/install.sh](https://ollama.com/install.sh) | sh [cite: 5]

# 2. 更新 apt 并安装 systemd/systemctl (用于服务管理)
[cite_start]sudo apt-get update [cite: 7]
[cite_start]sudo apt-get install systemd -y [cite: 9]
[cite_start]sudo apt-get install systemctl -y [cite: 10]

# 3. 设置并启动 Ollama 服务
[cite_start]sudo systemctl enable ollama [cite: 12]
[cite_start]sudo systemctl start ollama [cite: 14]
[cite_start]sudo systemctl status ollama # 检查状态 [cite: 16]