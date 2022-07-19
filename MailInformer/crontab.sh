#!/bin/bash

ps -ef | grep $3 | grep -v grep > /dev/null #查看执行的进程是否存在
if [ $? == 0 ];
then
	tail -n 10 $1 | mail -s "go test -run 2D" $2
fi