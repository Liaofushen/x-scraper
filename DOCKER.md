# Docker 使用说明

本项目使用 Microsoft Playwright 官方基础镜像，提供了完整的浏览器环境。

## 特性

- ✅ 基于 `mcr.microsoft.com/playwright:v1.56.1-noble-amd64`
- ✅ 预装 Chromium 浏览器和所有依赖
- ✅ 使用 `uv` 快速安装 Python 依赖
- ✅ 挂载源代码实现热更新（除 `.venv` 外）
- ✅ 数据和日志持久化
- ✅ 支持开发和生产模式

## 快速开始

### 1. 构建镜像

首次构建（启用 BuildKit 缓存优化）：

```bash
# 启用 Docker BuildKit（推荐）
export DOCKER_BUILDKIT=1
export COMPOSE_DOCKER_CLI_BUILD=1

# 构建镜像
docker-compose build
```

或者直接使用：

```bash
DOCKER_BUILDKIT=1 docker-compose build
```

**注意**：首次构建需要 5-8 分钟（编译 pandas、numpy 等），但后续构建只需 30 秒-2 分钟（得益于缓存）。

### 2. 运行容器

```bash
# 运行默认命令
docker-compose up

# 后台运行
docker-compose up -d

# 查看日志
docker-compose logs -f
```

### 3. 自定义命令

编辑 `docker-compose.yml` 中的 `command` 字段：

```yaml
services:
  x-scraper:
    command: ["uv", "run", "python", "main.py", "--help"]
```

或直接运行：

```bash
docker-compose run --rm x-scraper uv run python test_sdk.py
```

## 运行模式

### Guest 模式（无需登录）

使用 guest 模式快速抓取公开推文，无需 Twitter 登录：

```bash
# 运行 guest 模式（默认抓取 @stable 的 20 条推文）
docker-compose --profile guest run --rm x-scraper-guest

# 自定义 guest 模式抓取
docker-compose --profile guest run --rm x-scraper-guest \
  uv run python main.py guest elonmusk --max-tweets 50

# 带 AI 分析
docker-compose --profile guest run --rm x-scraper-guest \
  uv run python main.py guest stable --max-tweets 20 --analyze
```

### Interactive 模式（需要登录）

使用交互式 CLI 界面：

```bash
# 启动交互式模式
docker-compose --profile interactive run --rm x-scraper-interactive

# 这将进入交互式界面，可以选择各种操作：
# - 抓取用户推文
# - 搜索推文
# - 历史推文抓取
# - Guest 模式抓取
```

### 开发模式

进入开发容器的 bash shell：

```bash
# 启动开发容器
docker-compose --profile dev run --rm x-scraper-dev

# 在容器内执行命令
uv run python main.py --help
uv run python test_sdk.py
uv run python demo_guest_mode.py
uv run python main.py guest stable --max-tweets 10
```

## 目录结构

挂载的目录和文件：

- `./xscraper` - 主代码目录
- `./cli` - CLI 工具
- `./examples` - 示例代码
- `./main.py` - 主入口文件
- `./data` - 数据目录（持久化）
- `./logs` - 日志目录（持久化）
- `./config.ini` - 配置文件（只读）
- `./playwright_cookies.json` - Cookies 文件

## 配置说明

### 环境变量

在 `docker-compose.yml` 中的 `environment` 部分设置：

```yaml
environment:
  - PYTHONUNBUFFERED=1
  - PLAYWRIGHT_BROWSERS_PATH=/ms-playwright
  - PROXY_URL=socks5://your-proxy:1080
  - OPENAI_API_KEY=your-api-key
```

或创建 `.env` 文件（参考 `.env.example`）。

### 资源限制

取消注释 `docker-compose.yml` 中的 `deploy` 部分：

```yaml
deploy:
  resources:
    limits:
      cpus: '2'
      memory: 4G
    reservations:
      cpus: '1'
      memory: 2G
```

### 共享内存

Chromium 需要足够的共享内存，默认设置为 2GB：

```yaml
shm_size: '2gb'
```

## 常用命令

### 基础命令

```bash
# 构建镜像
docker-compose build

# 启动默认服务（后台运行）
docker-compose up -d

# 停止服务
docker-compose down

# 查看日志
docker-compose logs -f x-scraper

# 进入运行中的容器
docker-compose exec x-scraper /bin/bash

# 重启服务
docker-compose restart

# 删除容器和卷
docker-compose down -v
```

### Profile 模式命令

```bash
# Guest 模式（无需登录抓取）
docker-compose --profile guest run --rm x-scraper-guest

# Interactive 模式（交互式界面）
docker-compose --profile interactive run --rm x-scraper-interactive

# 开发模式（bash shell）
docker-compose --profile dev run --rm x-scraper-dev

# 查看所有可用服务
docker-compose config --services

# 同时启动多个 profile
docker-compose --profile guest --profile dev up
```

### 快速命令示例

```bash
# 快速抓取某个用户的推文（guest 模式）
docker-compose --profile guest run --rm x-scraper-guest \
  uv run python main.py guest elonmusk --max-tweets 30

# 运行测试
docker-compose --profile dev run --rm x-scraper-dev \
  uv run python test_sdk.py

# 运行 demo
docker-compose --profile dev run --rm x-scraper-dev \
  uv run python demo_guest_mode.py
```

## 故障排除

### 问题：浏览器启动失败

**解决方案：** 增加共享内存大小

```yaml
shm_size: '4gb'
```

### 问题：权限错误

**解决方案：** 确保 data 和 logs 目录有写权限

```bash
chmod -R 755 data logs
```

### 问题：依赖安装失败

**解决方案：** 清理缓存重新构建

```bash
docker-compose build --no-cache
```

### 问题：代理配置

如果需要使用代理，在 `docker-compose.yml` 中添加：

```yaml
environment:
  - HTTP_PROXY=http://proxy.example.com:8080
  - HTTPS_PROXY=http://proxy.example.com:8080
  - NO_PROXY=localhost,127.0.0.1
```

## 性能优化

### 已启用的优化

1. **BuildKit 缓存挂载**：uv 下载和编译的包会被缓存，后续构建速度提升 80%+
2. **Python 版本锁定**：限制在 Python 3.11-3.13，避免使用过新版本导致无预编译 wheels
3. **挂载代码**：开发时通过 volume 挂载代码，无需重新构建

### 额外优化建议

1. **避免频繁修改依赖**：尽量不要修改 `pyproject.toml` 和 `uv.lock`
2. **资源限制**：根据实际需求调整 CPU 和内存限制
3. **网络模式**：如需更好的网络性能，使用 `network_mode: "host"`
4. **多阶段构建**：如果镜像过大，可以考虑多阶段构建（生产环境）

## 生产部署建议

1. 不要挂载源代码，而是在构建时 COPY 进镜像
2. 使用环境变量或 secrets 管理敏感信息
3. 配置适当的重启策略和健康检查
4. 使用专用的日志收集系统
5. 定期更新基础镜像和依赖

### 生产环境 Dockerfile 示例

```dockerfile
FROM mcr.microsoft.com/playwright:v1.56.1-noble-amd64

WORKDIR /app

RUN pip install --no-cache-dir uv

COPY pyproject.toml uv.lock README.md ./
RUN uv sync --no-dev

# Copy all source code
COPY xscraper ./xscraper
COPY cli ./cli
COPY main.py ./

RUN mkdir -p data logs

ENTRYPOINT ["uv", "run", "python", "main.py"]
```

