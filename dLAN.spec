# TODO
# - about license: http://www.spinics.net/lists/linux-usb-devel/msg03600.html
#
# Conditional build:
%bcond_without	dist_kernel	# without kernel from distribution
%bcond_without	kernel		# don't build kernel modules
%bcond_without	userspace	# don't build userspace module
%bcond_with	verbose		# verbose build (V=1)
#
%if %{without kernel}
%undefine	with_dist_kernel
%endif
#
Summary:	dLAN drivers
Summary(de.UTF-8):	dLAN Treiber
Summary(pl.UTF-8):	Sterowniki dLAN
Name:		dLAN
Version:	3
Release:	0.1
License:	Devolo AG License, non-distributable
Group:		Applications
Source0:	http://download.devolo.net/webcms/0518732001164965747/%{name}-linux-package-v%{version}.tar.gz
# NoSource0-md5:	5ac30a52511a22571805519641a28e66
NoSource:	0
URL:		http://www.devolo.com/co_EN/produkte/dlan/dn-1-mldlanduo.html
%if %{with kernel}
%{?with_dist_kernel:BuildRequires:	kernel%{_alt_kernel}-module-build >= 3:2.6.20.2}
BuildRequires:	rpmbuild(macros) >= 1.379
%endif
%if %{with userspace}
BuildRequires:	libpcap-devel
%endif
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
dLAN drivers for Linux 2.4/2.6.

%description -l de.UTF-8
dLAN Treiber für Linux 2.4/2.6.

%description -l pl.UTF-8
Sterowniki dLAN dla Linuksa 2.4/2.6.

%package -n kernel-char-dLAN
Summary:	Linux kernel driver for dLAN
Summary(de.UTF-8):	Linux Kernel Treiber für dLAN
Summary(pl.UTF-8):	Sterownik jądra Linuksa dla dLAN
Release:	%{release}@%{_kernel_ver_str}
Group:		Base/Kernel
%if %{with dist_kernel}
%requires_releq_kernel
Requires(postun):	%releq_kernel
%endif
Requires(post,postun):	/sbin/depmod

%description -n kernel-char-dLAN
Linux kernel drivers for dLAN.

%description -n kernel-char-dLAN -l de.UTF-8
Linux Kernel Treiber für dLAN.

%description -n kernel-char-dLAN -l pl.UTF-8
Sterowniki jądra Linuksa dla dLAN.

%prep
%setup -q -n %{name}-linux-package-v%{version}

%build
%configure \
	%{?without_kernel:--disable-usbdriver}

%if %{with userspace}
%{__make} -C tool
%endif

%if %{with kernel}
%build_kernel_modules -C driver -m devolo_usb
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT

%if %{with userspace}
%{__make} -C tool install \
	DESTDIR=$RPM_BUILD_ROOT
%endif

%if %{with kernel}
%install_kernel_modules -m driver/devolo_usb -d misc
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post -n kernel-char-dLAN
%depmod %{_kernel_ver}

%postun -n kernel-char-dLAN
%depmod %{_kernel_ver}

%if %{with userspace}
%files
%defattr(644,root,root,755)
%doc %lang(de) LIESMICH
%doc %lang(es) LEAME
%doc %lang(fr) LISEZ-MOI
%doc %lang(it) LEGGIMI
%doc %lang(nl) LEESMIJ
%doc README
%attr(755,root,root) %{_sbindir}/dlanconfig
%attr(755,root,root) %{_sbindir}/dlanconfig_son
%{_mandir}/man8/dlanconfig.8*
%endif

%if %{with kernel}
%files -n kernel-char-dLAN
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/misc/devolo_usb.*o*
%endif
