#Requirement : Install Automake and libotool

cd Implementation

# get owamp from git 
git clone --recurse-submodules https://github.com/perfsonar/owamp.git

# create needed directories
mkdir executables
mkdir outputs
mkdir outputs/dir_test
mkdir outputs/dir_pid

# install owamp
cd owamp
autoreconf -f -i
./configure --prefix $PWD/../executables
make
make install

# add password
../executables/bin/aespasswd -n -f ../config/owamp-server.pfs admin