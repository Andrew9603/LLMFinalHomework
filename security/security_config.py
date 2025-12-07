import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class SecurityConfig:
    """安全相关配置（权限、加密、网络防护）"""
    # ========== RBAC权限控制 ==========
    # 超级管理员账号（默认初始化用，可在WebUI修改）
    ADMIN_USERNAME = os.getenv("ADMIN_USER", "admin")
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "Traffic@2025")  # 初始密码，建议部署后修改
    # 权限角色定义（与Web端角色对应）
    ROLES = {
        "admin": ["chat", "view_session", "edit_session", "rag_access", "user_manage", "system_setting"],
        "user": ["chat", "view_session", "edit_session"],
        "pending": []  # 待激活用户无权限
    }
    # Session有效期（单位：小时）
    SESSION_EXPIRE_HOURS = int(os.getenv("SESSION_EXPIRE", 24))
    # JWT密钥（用于会话加密，生产环境请替换为随机字符串）
    JWT_SECRET_KEY = os.getenv("JWT_SECRET", "traffic-simulation-rag-2025-key")
    JWT_ALGORITHM = "HS256"

    # ========== SSH密钥认证 ==========
    # 私钥路径（用于连接阿里云ECS/DSW）
    SSH_PRIVATE_KEY_PATH = os.getenv("SSH_PRIVATE_KEY_PATH", "./ssh/id_rsa")
    # 私钥密码（若未设置则为空）
    SSH_KEY_PASSWORD = os.getenv("SSH_KEY_PASSWORD", "")
    # 禁止密码登录（强制SSH密钥认证）
    SSH_DISABLE_PASSWORD_LOGIN = os.getenv("SSH_DISABLE_PWD", "True").lower() == "true"

    # ========== Frp内网穿透 ==========
    FRP_ENABLE = os.getenv("FRP_ENABLE", "False").lower() == "true"  # 是否启用Frp
    FRP_SERVER_ADDR = os.getenv("FRP_SERVER_ADDR", "frp.example.com")  # Frp服务端地址
    FRP_SERVER_PORT = int(os.getenv("FRP_SERVER_PORT", 7000))  # Frp服务端端口
    FRP_TOKEN = os.getenv("FRP_TOKEN", "")  # Frp预共享密钥（与服务端一致）
    # 本地服务映射配置（WebUI端口映射）
    FRP_LOCAL_PORT = int(os.getenv("FRP_LOCAL_PORT", 8080))  # 本地Web服务端口
    FRP_REMOTE_PORT = int(os.getenv("FRP_REMOTE_PORT", 8081))  # 公网访问端口
    # TLS加密开关（Frp传输加密）
    FRP_TLS_ENABLE = os.getenv("FRP_TLS", "True").lower() == "true"

    # ========== 网络安全 ==========
    # 允许访问的IP白名单（生产环境建议配置，格式：["192.168.1.0/24", "10.0.0.0/8"]）
    IP_WHITELIST = os.getenv("IP_WHITELIST", "").split(",") if os.getenv("IP_WHITELIST") else []
    # 禁止频繁请求（防暴力攻击）
    RATE_LIMIT = int(os.getenv("RATE_LIMIT", 10))  # 每分钟最大请求数
    RATE_LIMIT_KEY = "ip"  # 按IP限流

    # ========== 数据安全 ==========
    # 敏感信息加密盐值（用于密码加密存储）
    ENCRYPT_SALT = os.getenv("ENCRYPT_SALT", "traffic_simulation_salt_2025")
    # 日志脱敏开关（是否隐藏敏感信息）
    LOG_DESENSITIZE = os.getenv("LOG_DESENSITIZE", "True").lower() == "true"

# 实例化配置对象
security_config = SecurityConfig()

if __name__ == "__main__":
    # 验证安全配置
    print("=== 安全配置验证 ===")
    print(f"管理员账号: {security_config.ADMIN_USERNAME}")
    print(f"RBAC角色数: {len(security_config.ROLES)}")
    print(f"Frp启用状态: {security_config.FRP_ENABLE}")
    print(f"SSH密钥认证: {'启用' if security_config.SSH_DISABLE_PASSWORD_LOGIN else '禁用'}")
    print(f"限流配置: {security_config.RATE_LIMIT}次/分钟")