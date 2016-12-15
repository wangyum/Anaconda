#!/bin/bash

BIN=$PREFIX/bin

if [ `uname` == Darwin ]
then
    mv anaconda_navigator/app/Navigator.app $PREFIX/navigatorapp
    find $PREFIX/navigatorapp -name '__init__.py' | xargs rm

    AE=$PREFIX/navigatorapp/Contents/MacOS/run.sh
    cat <<EOF >$AE
#!/bin/sh
export PATH=$PREFIX/bin:"\$PATH"
$PREFIX/bin/anaconda-navigator \$@
EOF
    chmod +x $AE

    POST_LINK=$BIN/.anaconda-navigator-post-link.sh
    PRE_UNLINK=$BIN/.anaconda-navigator-pre-unlink.sh
    cp $RECIPE_DIR/osx-post.sh $POST_LINK
    cp $RECIPE_DIR/osx-pre.sh $PRE_UNLINK
    chmod +x $POST_LINK $PRE_UNLINK

else # not Darwin
    rm -rf anaconda_navigator/app/Navigator.app
fi

$PYTHON setup.py install --old-and-unmanageable
