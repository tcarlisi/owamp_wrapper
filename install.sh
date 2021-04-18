#Requirement : Install Automake and libotool

cd Implementation
git clone --recurse-submodules https://github.com/perfsonar/owamp.git
mkdir executables
mkdir outputs
mkdir outputs/dir_test
mkdir outputs/dir_pid
cd owamp
autoreconf -f -i
./configure --prefix $PWD/../executables
make
make install
