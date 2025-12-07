# 🚦 基于 RAG 的开放式交通流仿真代码生成系统

## 🌟 项目简介

基于 RAG 的开放式交通流仿真代码生成系统 是一款融合大语言模型与检索增强生成（RAG）技术的智能工具，旨在解决传统交通仿真工具技术门槛高、建模周期长的痛点。通过自然语言描述，非专业用户可快速获取可直接运行的 SUMO（Simulation of Urban Mobility）仿真代码，将交通建模周期从数天缩短至小时级，为交通规划、科研实验、方案验证等场景提供高效支撑。
核心价值：

- 🚀 低门槛易用：自然语言驱动，无需专业编程与仿真知识

- 📚 精准生成：依托专业化交通仿真知识库，代码可执行率达 84%

- 🔌 开放扩展：支持多源数据接入与 AI 模型对接，适配复杂场景

- 🔒 安全稳定：多层安全防护体系，保障多用户并发访问

## 🏗️ 整体架构
```bash
自然语言输入 → RAG增强模块 → 代码生成引擎 → SUMO仿真代码 → 仿真验证
                  ↑                ↑
                  │                │
            交通知识库          安全部署层
```
```bash
traffic-simulation-code-generator/
│
├── src/                  
│   ├── bge_m3_embedding.py  
│   ├── call_ollama_models.py   
│   └── clean_database.py         
│

│
├── data/                     
│   ├── knowledge/            
│   └── test_cases/          
│
├── security/                   
│   ├── model_config.py      
│   └── security_config.py   
│                    
├── requirements.txt        
└── README.md               

```

## 技术选型与系统组成🤖

| 模块       | 技术选型                                   | 核心作用                                         |
|------------|---------------------------------------------|--------------------------------------------------|
| 基座模型   | CodeGeeX4-9B                                | 提供基础代码生成能力，适配交通仿真场景           |
| 检索增强   | BGE-M3 嵌入模型 + Chroma 向量数据库         | 精准检索领域知识，提升代码生成准确性             |
| 知识库     | 交通仿真领域知识（682 条核心条目）          | 覆盖路网、信号控制、交通流配置等核心任务         |
| 部署环境   | 阿里云 DSW + Ollama 框架 + Open-WebUI       | 轻量化部署，支持多用户并发访问                   |
| 安全机制   | Frp 内网穿透 + SSH 密钥认证 + RBAC 权限控制 | 保障系统访问安全与数据隔离                       |
| 仿真工具   | SUMO 1.18.0                                 | 交通流仿真运行与代码校验                         |


## 使用指南📖
1. 自然语言输入：在 WebUI 输入框中描述交通仿真需求，示例：
 
  - "生成一个十字交叉口路网，双向 4 车道，设置定时信号控制"

  - "创建包含 3 条公交线路的城市路网，交通流量为 1500pcu/h"

2. 代码生成与导出：点击 "生成代码" 按钮，系统将返回完整的 SUMO 仿真代码（.xml 格式），支持直接下载。

3. 仿真运行：

  - 打开 SUMO GUI，导入生成的路网文件（net.xml）和路线文件（routes.xml）

  - 点击 "运行" 按钮，观察交通流仿真效果

  - 支持通过 SUMO 自带工具分析仿真结果（如车辆平均速度、拥堵时长等）



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


```
#### 2. 配置环境变量

```bash
# 阿里云DSW配置
DSW_HOST=your-dsw-host
DSW_PORT=your-dsw-port
# SSH密钥认证
SSH_PRIVATE_KEY_PATH=./ssh/id_rsa
# RBAC权限控制
ADMIN_USER=admin
ADMIN_PASSWORD=your-secure-password
# Ollama配置
OLLAMA_MODEL=codegeex4:9b
OLLAMA_HOST=http://localhost:11434
```
#### 3. 启动服务
```bash
# 启动RAG知识库服务
python service/knowledge_base.py
# 启动代码生成服务
python service/code_generator.py
# 启动WebUI（默认端口：8080）
python webui/app.py
```


## 核心功能演示 🎬
前端UI
<img width="1611" height="813" alt="style" src="https://github.com/user-attachments/assets/a5084701-aa19-41c1-957b-4577f5428909" />


示例 ：十字交叉口仿真代码生成

输入："生成十字交叉口路网，东西向 3 车道，南北向 2 车道，信号周期 60 秒，交通流量 800pcu/h"

输出：

- 路网文件（net.xml）：定义道路拓扑、车道属性、交叉口连接

- 路线文件（routes.xml）：定义车辆类型、行驶路线、发车频率

- 信号控制文件（tls.xml）：定义信号相位、绿灯时长、周期参数
<img width="1839" height="919" alt="sumo_simulation png" src="https://github.com/user-attachments/assets/f37398ef-7aed-4f80-9a52-f98d93b2d5c2" />



## 开发与贡献 🤝

### 开发指南

1. 请基于 dev 分支创建 feature 分支进行开发

2. 代码提交需遵循Conventional Commits规范

3. 新增功能需配套编写测试用例（放置于 tests/ 目录）

4. 提交 PR 前请运行 pytest 确保测试通过

### 知识库扩展

如需扩展知识库覆盖范围，可参考 docs/knowledge_base_guide.md，按照以下流程操作：

1. 采集交通仿真领域相关知识（文献、技术文档、SUMO 官方规范）

2. 按照指定格式（JSONL）进行结构化处理

3. 运行 python tools/knowledge_process.py 导入 Chroma 数据库

4. 执行 python tests/test_retrieval.py 验证检索精度

### 贡献流程

1. Fork 本仓库

2. 创建特性分支：git checkout -b feature/your-feature

3. 提交修改：git commit -m "feat: add your feature"

4. 推送分支：git push origin feature/your-feature

5. 提交 Pull Request

## 未来规划 🛣️

- 扩展知识库覆盖范围（新增智能交通、车路协同等场景知识）

- 优化复杂场景代码生成逻辑（支持多交叉口协同控制、动态交通流）

- 强化仿真结果可视化（新增数据统计图表、拥堵热点分析）

- 支持多语言代码生成（适配 VISSIM、TransModeler 等其他仿真工具）

- 提供 Docker 容器化部署方案，简化环境配置

## 许可证 📜

本项目基于 [MIT 许可证](LICENSE) 开源，允许商业使用、修改、分发，需保留原作者版权声明。

联系方式 📧

- 项目维护者：张勇强 、宋金源、闫本旭

- 技术咨询：3390847466@qq.com








