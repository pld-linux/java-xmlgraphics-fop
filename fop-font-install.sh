#!/bin/sh

FONTDIR=/usr/share/fonts
TTF_DIR=$FONTDIR/TTF
TTF_TOOL=/usr/bin/ttmkfdir
FOP_CONF=$FONTDIR/fop-font.config

jars="fop xml-apis xalan xerces commons-io xmlgraphics-commons"

CLASSPATH=$(build-classpath $jars)
export CLASSPATH

# create font metric files
for font in  $TTF_DIR/*.ttf; do
    java -classpath $CLASSPATH \
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
