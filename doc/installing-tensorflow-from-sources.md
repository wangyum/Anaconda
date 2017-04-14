# Install tensorflow

### Our cluster environment:

CentOS 6.7, JDK 1.8, Cloudera Manager 5.5.1, CDH 5.4.3, Anaconda 4.0.0, Spark 2.1.0([install latest spark](https://github.com/wangyum/cm_csds/tree/master/SPARK)),

### Upgrade gcc to 4.8.2
```bash
wget http://people.centos.org/tru/devtools-2/devtools-2.repo -O /etc/yum.repos.d/devtools-2.repo
yum install -y zip unzip patch libcurl-devel git devtoolset-2-gcc devtoolset-2-binutils devtoolset-2-gcc-c++
# active devtoolset-2
scl enable devtoolset-2 bash
# verification
gcc -v
```

### Install JDK(optional):
```
wget --header "Cookie: oraclelicense=accept-securebackup-cookie" http://download.oracle.com/otn-pub/java/jdk/8u102-b14/jdk-8u102-linux-x64.rpm
sudo yum localinstall -y jdk-8u102-linux-x64.rpm
export JAVA_HOME=/usr/java/jdk1.8.0_102
```

### Install Anaconda(optional):
```
git clone https://github.com/wangyum/Anaconda.git "/opt/cloudera/parcels/Anaconda"
```

### Install bazel:
```bash
wget https://github.com/bazelbuild/bazel/releases/download/0.4.5/bazel-0.4.5-dist.zip
unzip bazel-0.4.5-dist.zip -d bazel
sh bazel/compile.sh
```
### Configure the installation
```
export PATH=/opt/cloudera/parcels/Anaconda/bin/:/root/bazel/output/:${PATH}

git clone https://github.com/tensorflow/tensorflow && cd tensorflow
git checkout v1.1.0-rc1
# ./configure 
Please specify the location of python. [Default is /opt/cloudera/parcels/Anaconda/bin/python]: 
Please specify optimization flags to use during compilation when bazel option "--config=opt" is specified [Default is -march=native]: 
Do you wish to use jemalloc as the malloc implementation? [Y/n] n
jemalloc disabled
Do you wish to build TensorFlow with Google Cloud Platform support? [y/N] 
No Google Cloud Platform support will be enabled for TensorFlow
Do you wish to build TensorFlow with Hadoop File System support? [y/N] y
Hadoop File System support will be enabled for TensorFlow
Do you wish to build TensorFlow with the XLA just-in-time compiler (experimental)? [y/N] 
No XLA support will be enabled for TensorFlow
Found possible Python library paths:
  /opt/cloudera/parcels/Anaconda/lib/python2.7/site-packages
Please input the desired Python library path to use.  Default is [/opt/cloudera/parcels/Anaconda/lib/python2.7/site-packages]

Using python library path: /opt/cloudera/parcels/Anaconda/lib/python2.7/site-packages
Do you wish to build TensorFlow with OpenCL support? [y/N] 
No OpenCL support will be enabled for TensorFlow
Do you wish to build TensorFlow with CUDA support? [y/N] 
No CUDA support will be enabled for TensorFlow
INFO: Starting clean (this may take a while). Consider using --async if the clean takes more than several minutes.
Configuration finished
```

### Package tensorflow
```bash
bazel build  --linkopt='-lrt' -c opt //tensorflow/tools/pip_package:build_pip_package
bazel-bin/tensorflow/tools/pip_package/build_pip_package /tmp/tensorflow_pkg
```

### Install tensorflow
```bash
pip install --upgrade /tmp/tensorflow_pkg/tensorflow-1.0.1-cp27-cp27mu-linux_x86_64.whl
```
