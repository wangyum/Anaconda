# Install tensorflow

### Our cluster environment:

CentOS 6.7, JDK 1.8, Cloudera Manager 5.5.1, CDH 5.4.3, Anaconda 4.0.0, Spark 2.1.0([install latest spark](https://github.com/wangyum/cm_csds/tree/master/SPARK)),

### Upgrade gcc to 4.8.2
```bash
wget http://people.centos.org/tru/devtools-2/devtools-2.repo -O /etc/yum.repos.d/devtools-2.repo
yum install devtoolset-2-gcc devtoolset-2-binutils devtoolset-2-gcc-c++
# active devtoolset-2
scl enable devtoolset-2 bash
# verification
gcc -v
```

### Install bazel:
```bash
wget https://github.com/bazelbuild/bazel/releases/download/0.4.2/bazel-0.4.2-dist.zip
unzip bazel-0.4.2-dist.zip -d bazel
sh bazel/compile.sh
```
### Configure the installation
```
export PATH=/opt/cloudera/parcels/Anaconda/bin/:/root/bazel/output/:${PATH}

git clone https://github.com/tensorflow/tensorflow && cd tensorflow
git checkout v1.0.0
# ./configure
Please specify optimization flags to use during compilation [Default is -march=native]: 
Do you wish to use jemalloc as the malloc implementation? (Linux only) [Y/n] n
jemalloc disabled on Linux
Do you wish to build TensorFlow with Google Cloud Platform support? [y/N] N
No Google Cloud Platform support will be enabled for TensorFlow
Do you wish to build TensorFlow with Hadoop File System support? [y/N] y
Hadoop File System support will be enabled for TensorFlow
Do you wish to build TensorFlow with the XLA just-in-time compiler (experimental)? [y/N] 
No XLA support will be enabled for TensorFlow
Found possible Python library paths:
  /opt/cloudera/parcels/Anaconda/lib/python2.7/site-packages
Please input the desired Python library path to use.  Default is [/opt/cloudera/parcels/Anaconda/lib/python2.7/site-packages]

Using python library path: /opt/cloudera/parcels/Anaconda/lib/python2.7/site-packages
Do you wish to build TensorFlow with OpenCL support? [y/N] N
No OpenCL support will be enabled for TensorFlow
Do you wish to build TensorFlow with CUDA support? [y/N] N
No CUDA support will be enabled for TensorFlow
Configuration finished
```

### Package tensorflow
```bash
bazel build  --linkopt='-lrt' -c opt //tensorflow/tools/pip_package:build_pip_package
bazel-bin/tensorflow/tools/pip_package/build_pip_package /tmp/tensorflow_pkg
```

### Install tensorflow
```bash
pip install /tmp/tensorflow_pkg/tensorflow-1.0.0-cp27-cp27mu-linux_x86_64.whl
```
