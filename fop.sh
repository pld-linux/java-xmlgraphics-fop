#!/bin/sh

FONTDIR=/usr/share/fonts
FOP_CONF=$FONTDIR/fop-font.config

CLASSPATH=/usr/share/java/classes/fop.jar
CLASSPATH=$CLASSPATH:/usr/share/java/classes/jimi-1.0.jar
CLASSPATH=$CLASSPATH:/usr/share/java/classes/w3c.jar
CLASSPATH=$CLASSPATH:/usr/share/java/classes/xalan-2.0.0.jar
CLASSPATH=$CLASSPATH:/usr/share/java/classes/xerces-1.2.3.jar

/usr/lib/java-jre/jre/bin/java -classpath $CLASSPATH \
    org.apache.fop.apps.Fop -c $FOP_CONF $@
