#!/bin/sh -e

[ -r /usr/share/java-utils/java-functions ] || exit 1

. /usr/share/java-utils/java-functions

FOPDIR=/var/lib/fop
FOP_CONF=${FOP_CONF:-"$FOPDIR/fop-font.config"}

jars="xmlgraphics-fop avalon-framework-api avalon-framework-impl commons-io xalan xerces-j2 xmlgraphics-batik xmlgraphics-batik/batik-util commons-logging"
CLASSPATH=$(build-classpath $jars)
MAIN_CLASS=org.apache.fop.cli.Main

# If user specified -c option, and it is not the last option (i.e. it has
# an argument), don't override it.
case " $*" in
  *' -c '*) FOP_CONFIG_OPTION="" ;;
  *) FOP_CONFIG_OPTION="-c $FOP_CONFIG" ;;
esac

run $CONFIG ${1:+"$@"}
