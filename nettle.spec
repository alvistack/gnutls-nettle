%global debug_package %{nil}

Name: nettle
Epoch: 100
Version: 3.7.3
Release: 1%{?dist}
Summary: A low-level cryptographic library
License: LGPL-2.1-or-later
URL: https://github.com/gnutls/nettle/tags
Source0: %{name}_%{version}.orig.tar.gz
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: gcc
BuildRequires: gettext-devel
BuildRequires: gmp-devel >= 6.1.0
BuildRequires: libtool
BuildRequires: m4
BuildRequires: make
BuildRequires: pkgconfig
BuildRequires: texinfo
BuildRequires: texlive

%description
Nettle is a cryptographic library that is designed to fit easily in more
or less any context: In crypto toolkits for object-oriented languages
(C++, Python, Pike, ...), in applications like LSH or GNUPG, or even in
kernel space.

%prep
%autosetup -T -c -n %{name}_%{version}-%{release}
tar -zx -f %{S:0} --strip-components=1 -C .

%build
autoreconf -i
%configure \
    --enable-static \
    --enable-shared \
    --enable-fat \
    --disable-documentation
%make_build
make nettle.info

%install
%make_install
install -Dpm755 -d %{buildroot}%{_infodir}
install -Dpm644 -t %{buildroot}%{_infodir} nettle.info

%check

%if 0%{?suse_version} > 1500 || 0%{?sle_version} > 150000
%package -n libnettle8
Summary: Cryptographic Library
License: LGPL-2.1-or-later
Group: System/Libraries

%description -n libnettle8
Nettle is a cryptographic library that is designed to fit easily in more or
less any context: In crypto toolkits for object-oriented languages (C++,
Python, Pike, ...), in applications like LSH or GNUPG, or even in kernel space.

%package -n libhogweed6
Summary: Cryptographic Library for Public Key Algorithms
License: LGPL-2.1-or-later
Group: System/Libraries

%description -n libhogweed6
Nettle is a cryptographic library that is designed to fit easily in more or
less any context: In crypto toolkits for object-oriented languages (C++,
Python, Pike, ...), in applications like LSH or GNUPG, or even in kernel space.

The libhogweed library contains public key algorithms to use with libnettle.

%package -n libnettle-devel
Summary: Cryptographic Library
License: LGPL-2.1-or-later
Group: Development/Libraries/C and C++
Requires: glibc-devel
Requires: gmp-devel
Requires: libhogweed6 = %{epoch}:%{version}-%{release}
Requires: libnettle8 = %{epoch}:%{version}-%{release}

%description -n libnettle-devel
Nettle is a cryptographic library that is designed to fit easily in more or
less any context: In crypto toolkits for object-oriented languages (C++,
Python, Pike, ...), in applications like LSH or GNUPG, or even in kernel space.

%description
Nettle is a cryptographic library that is designed to fit easily in more or
less any context: In crypto toolkits for object-oriented languages (C++,
Python, Pike, ...), in applications like LSH or GNUPG, or even in kernel space.

This package contains a few command-line tools to perform cryptographic
operations using the nettle library.

%post -n libnettle8 -p /sbin/ldconfig
%postun -n libnettle8 -p /sbin/ldconfig
%post -n libhogweed6 -p /sbin/ldconfig
%postun -n libhogweed6 -p /sbin/ldconfig

%files -n libnettle8
%license COPYING*
%{_libdir}/libnettle.so.8
%{_libdir}/libnettle.so.8.*

%files -n libhogweed6
%license COPYING*
%{_libdir}/libhogweed.so.6
%{_libdir}/libhogweed.so.6.*

%files -n libnettle-devel
%license COPYING*
%{_includedir}/nettle
%{_infodir}/nettle.info.gz
%{_libdir}/libhogweed.a
%{_libdir}/libhogweed.so
%{_libdir}/libnettle.a
%{_libdir}/libnettle.so
%{_libdir}/pkgconfig/hogweed.pc
%{_libdir}/pkgconfig/nettle.pc

%files
%license COPYING*
%{_bindir}/nettle-hash
%{_bindir}/nettle-lfib-stream
%{_bindir}/nettle-pbkdf2
%{_bindir}/pkcs1-conv
%{_bindir}/sexp-conv
%endif

%if !(0%{?suse_version} > 1500) && !(0%{?sle_version} > 150000)
%package devel
Summary: Development headers for a low-level cryptographic library
Requires: nettle = %{epoch}:%{version}-%{release}
Requires: gmp-devel

%description devel
Nettle is a cryptographic library that is designed to fit easily in more
or less any context: In crypto toolkits for object-oriented languages
(C++, Python, Pike, ...), in applications like LSH or GNUPG, or even in
kernel space.  This package contains the files needed for developing 
applications with nettle.

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license COPYINGv2 COPYING.LESSERv3
%{_bindir}/nettle-hash
%{_bindir}/nettle-lfib-stream
%{_bindir}/nettle-pbkdf2
%{_bindir}/pkcs1-conv
%{_bindir}/sexp-conv
%{_infodir}/nettle.info.gz
%{_libdir}/libhogweed.so.6
%{_libdir}/libhogweed.so.6.*
%{_libdir}/libnettle.so.8
%{_libdir}/libnettle.so.8.*

%files devel
%{_includedir}/nettle
%{_libdir}/libhogweed.a
%{_libdir}/libhogweed.so
%{_libdir}/libnettle.a
%{_libdir}/libnettle.so
%{_libdir}/pkgconfig/hogweed.pc
%{_libdir}/pkgconfig/nettle.pc
%endif

%changelog
