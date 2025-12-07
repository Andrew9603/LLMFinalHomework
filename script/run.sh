#!/bin/bash
# scripts/run.sh - 基于RAG的交通流仿真代码生成系统一键启动脚本
# 使用说明:
#   bash run.sh --dev   # 开发环境（调试模式，日志级别DEBUG）
#   bash run.sh --prod  # 生产环境（稳定模式，日志级别INFO，开启权限控制）
#   bash run.sh --help  # 查看帮助

# ==================== 全局配置 ====================
PROJECT_ROOT=$(cd $(dirname $0)/..; pwd)  # 项目根目录（自动定位）
PYTHON_CMD="python3"                     # Python命令（根据环境调整为python/python3）
SERVICE_PORT=8080                        # 默认服务端口
LOG_DIR="${PROJECT_ROOT}/logs"           # 日志目录
ENV_FILE="${PROJECT_ROOT}/.env"          # 环境变量文件

# ==================== 颜色输出函数 ====================
red() { echo -e "\033[31m$1\033[0m"; }
green() { echo -e "\033[32m$1\033[0m"; }
yellow() { echo -e "\033[33m$1\033[0m"; }
blue() { echo -e "\033[34m$1\033[0m"; }

# ==================== 帮助信息 ====================
show_help() {
    cat << EOF
基于RAG的开放式交通流仿真代码生成系统启动脚本
用法: $0 [选项]
选项:
  --dev    启动开发环境（调试模式，日志级别DEBUG，禁用权限校验）
  --prod   启动生产环境（稳定模式，日志级别INFO，开启RBAC/SSH/Frp安全机制）
  --help   显示本帮助信息
  --check  仅检查环境依赖，不启动服务
EOF
}

# ==================== 环境检查函数 ====================
check_env() {
    blue "===== 开始环境检查 ====="

    # 1. 检查Python版本
    PYTHON_VERSION=$(${PYTHON_CMD} --version 2>&1 | awk '{print $2}' | cut -d. -f1,2)
    VERSION_OK=$(echo "$PYTHON_VERSION >= 3.8 && $PYTHON_VERSION < 3.11" | bc)
    if [ $VERSION_OK -ne 1 ]; then
        red "错误：Python版本需为3.8~3.10，当前版本为${PYTHON_VERSION}"
        exit 1
    fi
    green "✅ Python版本检查通过 (${PYTHON_VERSION})"

    # 2. 检查依赖安装
    if [ ! -f "${PROJECT_ROOT}/requirements.txt" ]; then
        red "错误：未找到requirements.txt（路径：${PROJECT_ROOT}/requirements.txt）"
        exit 1
    fi
    ${PYTHON_CMD} -m pip check > /dev/null 2>&1
    if [ $? -ne 0 ]; then
        yellow "⚠️  依赖未完全安装，开始自动安装..."
        ${PYTHON_CMD} -m pip install -r "${PROJECT_ROOT}/requirements.txt" --upgrade
        if [ $? -ne 0 ]; then
            red "错误：依赖安装失败，请手动执行 pip install -r requirements.txt"
            exit 1
        fi
    fi
    green "✅ 依赖检查/安装通过"

    # 3. 检查配置文件
    CONFIG_FILES=("config/model_config.py" "config/security_config.py")
    for file in "${CONFIG_FILES[@]}"; do
        if [ ! -f "${PROJECT_ROOT}/${file}" ]; then
            red "错误：未找到配置文件 ${file}"
            exit 1
        fi
    done
    green "✅ 配置文件检查通过"

    # 4. 检查日志目录
    if [ ! -d "${LOG_DIR}" ]; then
        mkdir -p "${LOG_DIR}"
        green "✅ 日志目录已创建 (${LOG_DIR})"
    fi

    # 5. 检查Ollama服务（模型部署依赖）
    ollama --version > /dev/null 2>&1
    if [ $? -ne 0 ]; then
        yellow "⚠️  未检测到Ollama，开始自动安装（仅支持Linux/macOS）..."
        curl -fsSL https://ollama.com/install.sh | sh
        # 启动Ollama服务
        ollama serve > "${LOG_DIR}/ollama.log" 2>&1 &
        sleep 5  # 等待服务启动
    fi
    # 拉取CodeGeeX4模型（首次启动自动拉取）
    ollama pull codegeex4:9b > /dev/null 2>&1 &
    green "✅ Ollama/模型检查通过"

    blue "===== 环境检查完成 ====="
}

# ==================== 启动服务函数 ====================
start_service() {
    ENV_MODE=$1
    blue "===== 启动${ENV_MODE}环境服务 ====="

    # 设置环境变量
    export LOG_LEVEL="DEBUG"
    export SERVICE_PORT=${SERVICE_PORT}
    export FRP_ENABLE="False"
    export CODE_VALIDATE_ENABLE="True"

    if [ "${ENV_MODE}" = "prod" ]; then
        export LOG_LEVEL="INFO"
        export FRP_ENABLE="True"          # 生产环境启用Frp内网穿透
        export RBAC_ENABLE="True"         # 生产环境启用RBAC权限控制
        export LOG_DESENSITIZE="True"     # 生产环境日志脱敏
    fi

    # 加载.env文件（优先级高于脚本默认值）
    if [ -f "${ENV_FILE}" ]; then
        yellow "⚠️  加载环境变量文件 ${ENV_FILE}"
        export $(grep -v '^#' ${ENV_FILE} | xargs)
    fi

    # 启动Web服务（基于Flask/Open-WebUI）
    cd "${PROJECT_ROOT}"
    green "🚀 启动服务（端口：${SERVICE_PORT}，日志级别：${LOG_LEVEL}）"
    if [ "${ENV_MODE}" = "dev" ]; then
        # 开发环境：开启自动重载
        ${PYTHON_CMD} -m flask --app src/main run --host 0.0.0.0 --port ${SERVICE_PORT} --debug \
            > "${LOG_DIR}/service.log" 2>&1 &
    else
        # 生产环境：使用Gunicorn高性能服务器
        ${PYTHON_CMD} -m gunicorn -w 4 -b 0.0.0.0:${SERVICE_PORT} src.main:app \
            --access-logfile "${LOG_DIR}/access.log" \
            --error-logfile "${LOG_DIR}/error.log" \
            --daemon
    fi

    sleep 3  # 等待服务启动
    # 检查服务是否启动成功
    netstat -tulpn | grep ":${SERVICE_PORT}" > /dev/null 2>&1
    if [ $? -eq 0 ]; then
        green "✅ 服务启动成功！"
        green "访问地址：http://localhost:${SERVICE_PORT}"
        if [ "${ENV_MODE}" = "prod" ] && [ "${FRP_ENABLE}" = "True" ]; then
            green "公网访问地址：http://${FRP_SERVER_ADDR}:${FRP_REMOTE_PORT}"
        fi
    else
        red "❌ 服务启动失败，请查看日志：${LOG_DIR}/service.log"
        exit 1
    fi
}

# ==================== 主逻辑 ====================
case "$1" in
    --dev)
        check_env
        start_service "dev"
        ;;
    --prod)
        check_env
        start_service "prod"
        ;;
    --check)
        check_env
        green "🎉 所有环境检查通过！"
        ;;
    --help)
        show_help
        ;;
    *)
        red "错误：无效参数"
        show_help
        exit 1
        ;;
esac

# 保持脚本运行（可选）
wait