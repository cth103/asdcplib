asdcplib
======

This branch is based on asdcplib 2.5.11 and has the following basic changes needed for [libdcp](https://github.com/cth103/libdcp) and hence [DCP-o-matic](https://github.com/cth103/dcpomatic):

- Tweaks to allow resumption of writes to partial MXFs.
- Additions to allow hashing of MXFs while they are being written.
- Replacement of some code with shorter versions using boost.
- Fixes for various compiler warnings.

asdcplib is ‘an open source implementation of SMPTE and the MXF Interop “Sound & Picture Track File” format. It was originally developed with support from DCI. Development is currently supported by CineCert and other d-cinema manufacturers. See the bundled README file for more information. asdcplib is implemented in C++ and builds on Win32 and most unix platforms that support GCC.’

https://carlh.net/asdcplib

Building
-----------

    ./waf configure
    ./waf build
    sudo ./waf install


### Build options

    --target-windows      set up to do a cross-compile to Windows
    --enable-debug        build with debugging information and without optimisation
    --static              build statically

### Dependencies

- pkg-config (for build system)
- openssl


---
Bug reports and queries to Carl Hetherington <cth@carlh.net>
