#!/bin/sh

FONTDIR=/usr/share/fonts
TTF_DIR=$FONTDIR/TTF
TTF_TOOL=/usr/bin/ttmkfdir
FOP_CONF=$FONTDIR/fop-font.config

CLASSPATH=/usr/share/java/classes/fop.jar
CLASSPATH=$CLASSPATH:/usr/share/java/classes/jimi-1.0.jar
CLASSPATH=$CLASSPATH:/usr/share/java/classes/w3c.jar
CLASSPATH=$CLASSPATH:/usr/share/java/classes/xalan-2.0.0.jar
CLASSPATH=$CLASSPATH:/usr/share/java/classes/xerces-1.2.3.jar

# create font metric files
for font in  $TTF_DIR/*.ttf; do
    /usr/lib/java-jre/jre/bin/java -classpath $CLASSPATH \
        org.apache.fop.fonts.apps.TTFReader $font /var/lib/fop/$(basename $font .ttf).xml;
done

# create configuration file
$TTF_TOOL -d $TTF_DIR | awk '
    BEGIN { 
        print "<configuration>" 
        print "<fonts>"
    }
    { 
      if (match($1, /.ttf$/) && !FILES[$1]) {
        FILES[$1]=1        # ttmkfdir can create many font entries
                           # for different encodings, this way unwanted
                           # elements will be skipped

        # determine base of file name
        FILE=$1
        sub(/.ttf$/, "", FILE)
        split($2, LIST, "-")

        # get font name
        NAME=LIST[3]

        # get style: normal or italic
        if (match(LIST[5], /i/)) {
            STYLE="italic"
        } else {
            STYLE="normal"
        }

        # get weight: normal or bold
        if (match(LIST[4], /bold/)) {
            WEIGHT="bold"
        } else {
            WEIGHT="normal"
        }

        print "<font metrics-file=\"/var/lib/fop/" FILE ".xml\" kerning=\"yes\" embed-file=\"/usr/share/fonts/TTF/" FILE ".ttf\">"
        print "<font-triplet name=\"" NAME "\" style=\"" STYLE "\" weight=\"" WEIGHT "\"/>"
        print "</font>"
      }
    }
    END { 
        print "</fonts>"
        print "</configuration>" 
    }
' >  $FOP_CONF
