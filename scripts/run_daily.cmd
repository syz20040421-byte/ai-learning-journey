@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul 2>&1

REM ============================================================
REM  每日学习任务生成与推送 - 调度入口
REM  被 Windows 任务计划程序（登录触发）和 Hermes cron 双路调用
REM  daily_gate.py 保证一天只真正执行一次
REM ============================================================

set "BASE=D:\work-coding\Knowledge base\AI_KnowledgeBase"
set "SCRIPTS=%BASE%\scripts"
set "PY=C:\Users\21537\AppData\Local\hermes\hermes-agent\venv\Scripts\python.exe"
set "HERMES=C:\Users\21537\AppData\Local\hermes\hermes-agent\venv\Scripts\hermes.exe"
set "LOG=%BASE%\state\run_daily.log"

echo. >> "%LOG%"
echo ============================================ >> "%LOG%"
echo [%DATE% %TIME%] run_daily 启动 >> "%LOG%"

REM ---- 判重闸门 ----
"%PY%" "%SCRIPTS%\daily_gate.py" >> "%LOG%" 2>&1
set GATE=!ERRORLEVEL!

if !GATE! EQU 10 (
    echo [%TIME%] 今天已推送过，退出 >> "%LOG%"
    exit /b 0
)
if !GATE! EQU 11 (
    echo [%TIME%] 休息日，退出 >> "%LOG%"
    exit /b 0
)
if !GATE! NEQ 0 (
    echo [%TIME%] 闸门异常 exit=!GATE!，退出 >> "%LOG%"
    exit /b 1
)

echo [%TIME%] 已抢到今日锁，开始生成任务 >> "%LOG%"

REM ---- 等网络就绪（开机后网卡可能还没连上）----
set RETRY=0
:waitnet
"%PY%" -c "import urllib.request,sys; urllib.request.urlopen('https://open.feishu.cn',timeout=8); sys.exit(0)" >nul 2>&1
if !ERRORLEVEL! EQU 0 goto netok
set /a RETRY+=1
if !RETRY! GEQ 10 (
    echo [%TIME%] 网络等待超时，仍继续尝试 >> "%LOG%"
    goto netok
)
echo [%TIME%] 网络未就绪，第 !RETRY! 次等待 15s >> "%LOG%"
timeout /t 15 /nobreak >nul 2>&1
goto waitnet
:netok

echo [%TIME%] 网络就绪，调用 Hermes >> "%LOG%"

REM ---- 调用 Hermes 生成并推送今日任务 ----
"%HERMES%" chat -q "执行每日学习教练任务。加载 daily-study-coach 技能并严格按其步骤执行。学习仓库根目录: D:\work-coding\Knowledge base\AI_KnowledgeBase" >> "%LOG%" 2>&1

set RC=!ERRORLEVEL!
echo [%TIME%] Hermes 退出码=!RC! >> "%LOG%"

if !RC! NEQ 0 (
    echo [%TIME%] 生成失败，释放今日锁以便重试 >> "%LOG%"
    "%PY%" "%SCRIPTS%\daily_gate.py" --release >> "%LOG%" 2>&1
    exit /b 1
)

echo [%TIME%] 完成 >> "%LOG%"
exit /b 0
