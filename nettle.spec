# Just a hack because rpmlint rejects build with unstripped libs
#% define _enable_debug_packages %{nil}
#% define debug_package %{nil}

%bcond_with bootstrap

%define major 4
%define hogweedmajor 2
%define libname %mklibname nettle %{major}
%define libhogweed %mklibname hogweed %{hogweedmajor}
%define devname %mklibname -d nettle

Summary:	Old version of the Nettle cryptographic library
Name:		nettle2
Epoch:		1
Version:	2.7.1
Release:	10
License:	LGPLv2+
Group:		System/Libraries
Url:		https://www.lysator.liu.se/~nisse/nettle/
Source0:	http://www.lysator.liu.se/~nisse/archive/nettle-%{version}.tar.gz
Patch0:		nettle-aarch64.patch
Patch1:		nettle-2.7.1-remove-ecc-testsuite.patch
Patch2:		nettle-2.7.1-tmpalloc.patch
BuildRequires:	recode
BuildRequires:	texinfo
BuildRequires:	gmp-devel
%if %{with bootstrap}
BuildRequires:	pkgconfig(openssl)
%endif

%description
Nettle is a cryptographic library that is designed to fit easily in more or
less any context:
In crypto toolkits for object-oriented languages (C++, Python, Pike, ...),
in applications like LSH or GNUPG, or even in kernel space.

#----------------------------------------------------------------------------

%package -n %{libname}
Summary:	Old version of the Nettle shared library
Group:		System/Libraries

%description -n %{libname}
This is the shared library part of the Nettle library.

%files -n %{libname}
%{_libdir}/libnettle.so.%{major}*

#----------------------------------------------------------------------------

%if !%{with bootstrap}
%package -n %{libhogweed}
Summary:	Old version of the Hogweed shared library
Group:		System/Libraries

%description -n %{libhogweed}
This is the shared library part of the Hogweed library.

%files -n %{libhogweed}
%{_libdir}/libhogweed.so.%{hogweedmajor}*
%endif

#----------------------------------------------------------------------------

%prep
%setup -qn nettle-%{version}
%autopatch -p1
# Disable -ggdb3 which makes debugedit unhappy
sed s/ggdb3/g/ -i configure
sed 's/ecc-192.c//g' -i Makefile.in
sed 's/ecc-224.c//g' -i Makefile.in

%build
%configure \
	--enable-static \
	--enable-shared

%make

%check
%make check

%install
%makeinstall_std
recode ISO-8859-1..UTF-8 ChangeLog

# No -devel files for compat packages...
rm -rf %{buildroot}%{_libdir}/*.so \
	%{buildroot}%{_libdir}/*.a \
	%{buildroot}%{_includedir} \
	%{buildroot}%{_libdir}/pkgconfig \
	%{buildroot}%{_infodir}

# No tools either, use 3.x
rm -rf %{buildroot}%{_bindir}
