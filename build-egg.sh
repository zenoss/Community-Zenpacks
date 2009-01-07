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
rm -rf $PACK/dist
cp COPYRIGHT.txt LICENSE.txt $PACK
cd $PACK
echo In $PACK
$PYTHON setup.py bdist_egg
rm COPYRIGHT.txt LICENSE.txt
cd dist
for f in `ls -1 | grep py2.3.egg` ; do
    mv $f `echo $f | sed 's/2.3/2.4/'`
done ;
cd ..
cp dist/*.egg ..
true

