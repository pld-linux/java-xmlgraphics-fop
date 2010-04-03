#!/bin/sh -e

FONTDIR=/usr/share/fonts
FOP_CONF=$FONTDIR/fop-font.config

jars="xmlgraphics-fop avalon-framework-api avalon-framework-impl commons-io xalan xerces-j2 xmlgraphics-batik xmlgraphics-batik/batik-util"
CLASSPATH=$(build-classpath $jars)

exec java -classpath $CLASSPATH org.apache.fop.cli.Main -c $FOP_CONF $@
