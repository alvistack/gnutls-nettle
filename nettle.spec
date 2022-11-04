# Copyright 2022 Wong Hoi Sing Edison <hswong3i@pantarei-design.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

%global debug_package %{nil}

%global _lto_cflags %{?_lto_cflags} -ffat-lto-objects

Name: nettle
Epoch: 100
Version: 3.4.1
Release: 1%{?dist}
Summary: A low-level cryptographic library
License: LGPL-2.1-or-later
URL: https://github.com/gnutls/nettle/tags
Source0: %{name}_%{version}.orig.tar.gz
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: gcc
BuildRequires: gmp-devel
BuildRequires: libtool
BuildRequires: m4
BuildRequires: make
BuildRequires: pkgconfig
%if 0%{?suse_version} > 1500 || 0%{?sle_version} > 150000
Requires: libhogweed4 = %{epoch}:%{version}-%{release}
Requires: libnettle6 = %{epoch}:%{version}-%{release}
%endif

%description
Nettle is a cryptographic library that is designed to fit easily in more
or less any context: In crypto toolkits for object-oriented languages
(C++, Python, Pike, ...), in applications like LSH or GNUPG, or even in
kernel space.

%prep
%autosetup -T -c -n %{name}_%{version}-%{release}
tar -zx -f %{S:0} --strip-components=1 -C .

%build
%configure \
%if 0%{?centos_version} == 700
    --enable-mini-gmp \
%endif
    --disable-documentation \
    --disable-static \
    --enable-fat \
    --enable-shared
%make_build

%install
%make_build install DESTDIR=%{buildroot}
chmod 0755 %{buildroot}%{_libdir}/libnettle.so.*
chmod 0755 %{buildroot}%{_libdir}/libhogweed.so.*
find %{buildroot} -type f -name '*.la' -exec rm -rf {} \;

%check

%if 0%{?suse_version} > 1500 || 0%{?sle_version} > 150000
%package -n libnettle6
Summary: Low level cryptographic library (symmetric and one-way cryptos)

%description -n libnettle6
This package contains the symmetric and one-way cryptographic
algorithms. To avoid having this package depend on libgmp, the
asymmetric cryptos reside in a separate library, libhogweed.

%package -n libhogweed4
Summary: Low level cryptographic library (public-key cryptos)

%description -n libhogweed4
This package contains the asymmetric cryptographic algorithms, which,
require the GNU multiple precision arithmetic library (libgmp) for their
large integer computations.

%package -n libnettle-devel
Summary: Low level cryptographic library (development files)
Requires: libhogweed4 = %{epoch}:%{version}-%{release}
Requires: libnettle6 = %{epoch}:%{version}-%{release}
Requires: pkgconfig

%description -n libnettle-devel
This package contains the development files (C headers and static
libraries).

%post -n libnettle6 -p /sbin/ldconfig
%postun -n libnettle6 -p /sbin/ldconfig

%post -n libhogweed4 -p /sbin/ldconfig
%postun -n libhogweed4 -p /sbin/ldconfig

%files
%license COPYINGv2
%{_bindir}/*

%files -n libnettle6
%{_libdir}/libnettle*.so.*

%files -n libhogweed4
%{_libdir}/libhogweed*.so.*

%files -n libnettle-devel
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/hogweed.pc
%{_libdir}/pkgconfig/nettle.pc
%endif

%if !(0%{?suse_version} > 1500) && !(0%{?sle_version} > 150000)
%package -n nettle-devel
Summary: Files for development of applications which will use nettle
Requires: nettle = %{epoch}:%{version}-%{release}
Requires: pkgconfig

%description -n nettle-devel
This package contains files for development of applications which will
use nettle.

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license COPYINGv2
%{_bindir}/*
%{_libdir}/*.so.*

%files -n nettle-devel
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/hogweed.pc
%{_libdir}/pkgconfig/nettle.pc
%endif

%changelog
