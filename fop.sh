#!/bin/sh

FONTDIR=/usr/share/fonts
FOP_CONF=$FONTDIR/fop-font.config

CLASSPATH=/usr/lib/java/fop.jar
CLASSPATH=$CLASSPATH:/usr/lib/java/jimi-1.0.jar
CLASSPATH=$CLASSPATH:/usr/lib/java/batik.jar
CLASSPATH=$CLASSPATH:/usr/lib/java/xalan.jar
CLASSPATH=$CLASSPATH:/usr/lib/java/xerces.jar

java -classpath $CLASSPATH org.apache.fop.apps.Fop -c $FOP_CONF $@
