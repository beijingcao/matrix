#!/bin/bash

cd /root/bosstodo/
LOGFILE="/root/bosstodo/log-boss-todo.txt"
MAX_LINES=100

# 写日志并控制文件行数
log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') $1" >> "$LOGFILE"
    
    # 如果文件行数超过 50 行，裁剪内容
    if [[ $(wc -l < "$LOGFILE") -gt $MAX_LINES ]]; then
        tail -n $MAX_LINES "$LOGFILE" > "$LOGFILE.tmp"  # 保留最后 100 行
        mv "$LOGFILE.tmp" "$LOGFILE"
    fi
}

while true; do
    if pgrep -f "python3 /root/bosstodo/boss-todo.py" >/dev/null; then
        log "boss.py is running."
    else
        log "boss.py is not running. Restarting..."
        nohup python3 /root/bosstodo/boss-todo.py >> "$LOGFILE" 2>&1 &
    fi
    sleep 13  # 每13秒检测一次
done
