#
# Conditional build:
%bcond_without	static_libs	# static library
#
Summary:	Apple Lossless Audio Codec library
Summary(pl.UTF-8):	Biblioteka kodeka ALAC (Apple Lossless Audio Codec)
Name:		alac
Version:	0.0.7
Release:	1
License:	Apache v2.0
Group:		Libraries
# original project: https://github.com/macosforge/alac (last commit 2016)
# here is maintained (last commit 2022) fork with autotools support
#Source0Download: https://github.com/mikebrady/alac/tags
Source0:	https://github.com/mikebrady/alac/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	782f2752e9a8ef99d4c4a913e850e741
# https://github.com/mikebrady/alac/commit/5d6d836ee5b025a5e538cfa62c88bc5bced506ed
Patch0:		%{name}-unbreak-conversion-utility.patch
URL:		https://github.com/mikebrady/alac
BuildRequires:	autoconf >= 2.68
BuildRequires:	automake
BuildRequires:	libstdc++-devel
BuildRequires:	libtool >= 2:2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Apple Lossless Audio Codec library.

%description -l pl.UTF-8
Biblioteka kodeka ALAC (Apple Lossless Audio Codec).

%package devel
Summary:	Header files for ALAC library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki ALAC
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for ALAC library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki ALAC.

%package static
Summary:	Static ALAC library
Summary(pl.UTF-8):	Statyczna biblioteka ALAC
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static ALAC library.

%description static -l pl.UTF-8
Statyczna biblioteka ALAC.

%prep
%setup -q
%patch -P0 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--enable-example \
	%{!?with_static_libs:--disable-static}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libalac.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc ReadMe.txt codec/APPLE_LICENSE.txt
%attr(755,root,root) %{_bindir}/alacconvert
%attr(755,root,root) %{_libdir}/libalac.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libalac.so.0

%files devel
%defattr(644,root,root,755)
%doc ALACMagicCookieDescription.txt
%attr(755,root,root) %{_libdir}/libalac.so
%{_includedir}/alac
%{_pkgconfigdir}/alac.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libalac.a
%endif
