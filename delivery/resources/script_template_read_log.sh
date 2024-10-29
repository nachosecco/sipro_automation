
${READ_LOG_SSH_COMMAND} ${READ_LOG_USER}@${READ_LOG_HOST_TO_CONNECT} "tail -${READ_LOG_LINES_TO_READ} -${READ_LOG_PATH}"

#this is a example... of should look like
#ssh  jenkins@tug15.den1.rowdy.cc "tail -8000 /app/app-web-delivery/logs/app-web-delivery-base.log"
