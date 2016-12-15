#!/bin/bash

# Remove old Navigator.app if it exists
rm -rf $HOME/Desktop/Navigator.app
rm -rf $PREFIX/Navigator.app

cp -r $PREFIX/navigatorapp $PREFIX/Navigator.app
rm -rf $PREFIX/navigatorapp

ln -s -f $PREFIX/Navigator.app $HOME/Desktop/ || exit 0
