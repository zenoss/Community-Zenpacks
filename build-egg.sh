#! /bin/sh

# Use Zenoss's python if it exists, otherwise python2.4, otherwise python
PYTHON=`which $ZENHOME/bin/python`
PYTHON=${PYTHON:-`which python2.4`}
PYTHON=${PYTHON:-`which python`}

fail()
{
    echo $*
    exit 1
}

PACK=$1
OS=$2
ZVERSION=$3
if [ "$OS" = "" ]
then
  OS="el5"
fi

echo PACK: $PACK
echo OS: $OS
echo ZVERSION: $ZVERSION

echo
cp -r $PACK $TMPDIR
cp LICENSE.txt $TMPDIR/$PACK
cd $TMPDIR/$PACK
find . | grep .svn | xargs rm -rf
echo In $PACK
$PYTHON setup.py bdist_egg
cd -
mv $TMPDIR/$PACK/dist/*.egg .
rm -rf $TMPDIR/$PACK
true

