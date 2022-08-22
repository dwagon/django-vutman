#!/bin/bash -x
if [ ${LOGNAME} != "vutman" ];then
    sudo su - vutman -c "/opt/vutman/start.sh" -s /bin/bash
    exit $?
fi

export APPHOME="/opt/vutman"
export GUNICORN="$APPHOME/bin/gunicorn"
export NAME="vutman"
export USER="${NAME}"
export GROUP="${NAME}"

export PIDFILE="$APPHOME/run/$NAME.pid"
export LOGFILE="$APPHOME/log/$NAME.log"
export LOGLEVEL="debug"
export DEBUG=True
export PORT=8000
export WORKERS=2

mkdir -p `dirname ${PIDFILE}`
mkdir -p `dirname ${LOGFILE}`

source /opt/vutman/bin/activate

$GUNICORN --pid="$PIDFILE" --name="$NAME" --workers=$WORKERS --user="$USER" --group="$GROUP" --log-file="$LOGFILE" --log-level="$LOGLEVEL" --bind="127.0.0.1:$PORT" --chdir $APPHOME/django-vutman --preload emailwizard.wsgi
exit $?

# EOF
