#!/bin/sh

FONTDIR=/usr/share/fonts
FOP_CONF=$FONTDIR/fop-font.config

JCL=/usr/lib/java

CLASSPATH=$JCL/fop.jar
CLASSPATH=$CLASSPATH:$JCL/jimi-1.0.jar
CLASSPATH=$CLASSPATH:$JCL/logkit-1.0b4.jar
CLASSPATH=$CLASSPATH:$JCL/batik.jar
CLASSPATH=$CLASSPATH:$JCL/xalan.jar
CLASSPATH=$CLASSPATH:$JCL/xerces.jar

java -classpath $CLASSPATH org.apache.fop.apps.Fop -c $FOP_CONF $@
