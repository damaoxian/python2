#!/bin/bash

# Fly.io 部署脚本

echo "🚀 开始部署到 Fly.io..."

# 检查是否已安装 flyctl
if ! command -v flyctl &> /dev/null; then
    echo "❌ flyctl 未安装，请先安装 Fly.io CLI"
    echo "安装命令："
    echo "curl -L https://fly.io/install.sh | sh"
    exit 1
fi

# 检查是否已登录
if ! flyctl auth whoami &> /dev/null; then
    echo "🔐 请先登录 Fly.io"
    flyctl auth login
fi

# 创建应用（如果不存在）
if ! flyctl apps list | grep -q "net1"; then
    echo "📱 创建新应用..."
    flyctl apps create net1
fi

# 部署应用
echo "🚀 部署应用..."
flyctl deploy

echo "✅ 部署完成！"
echo "🌐 应用地址：https://net1.fly.dev"
