#Peut etre mieux d'installer depuis les repo



# Clone Owamp and I2Util
git clone --recurse-submodules https://github.com/perfsonar/owamp.git
cd owamp

#Requirement : Install Automake
#			libotool
#libtoolize --force
#aclaloc
#autoheader
#automake --force-missing --add-missing
#autoconf
autoreconf -f -i
./configure --prefix ~/Documents/TFE/OWAMP_Wrapper/Implementation/executables
make
make install


