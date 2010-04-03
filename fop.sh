#!/bin/sh

FONTDIR=/usr/share/fonts
FOP_CONF=$FONTDIR/fop-font.config

jars="fop avalon-framework xalan xerces-j2 batik"
CLASSPATH=$(build-classpath $jars)

exec java -classpath $CLASSPATH org.apache.fop.apps.Fop -c $FOP_CONF $@
