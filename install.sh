#Peut etre mieux d'installer depuis les repo



# Clone Owamp and I2Util
git clone --recurse-submodules https://github.com/perfsonar/owamp.git
cd owamp/I2util

#Requirement : Install Automake if needed !!!!
libtoolize --force
aclocal
autoheader
automake --force-missing --add-missing
autoconf
./configure
make
make install


