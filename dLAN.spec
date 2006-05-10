# TODO: optflags for userspace
#
# Conditional build:
%bcond_without  dist_kernel     # without kernel from distribution
%bcond_without  kernel          # don't build kernel modules
%bcond_without  smp             # don't build SMP module
%bcond_without  userspace       # don't build userspace module
%bcond_with     verbose         # verbose build (V=1)
#
Summary:	dLAN drivers
Summary(de):	dLAN Treiber
Summary(pl):	Sterowniki dLAN
Name:		dLAN
Version:	2.0
Release:	1
License:	Devolo AG License, non-distributable
Group:		Applications
Source0:	http://download.devolo.net/webcms/0599755001130248395/%{name}-linux-package-%{version}.tar.gz
# NoSource0-md5:	419b5e551a7e8eb7e2f609b252287712
NoSource:	0
Patch0:		%{name}-usbkill.patch
URL:		http://www.devolo.de/de_DE/index.html
%if %{with kernel}
BuildRequires:	%{kgcc_package}
%{?with_dist_kernel:BuildRequires:      kernel-module-build}
%endif
%if %{with userspace}
BuildRequires:	libpcap-devel
%endif
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
MicroLink dLAN drivers for Linux 2.4/2.6.

%description -l de
MicroLink dLAN Treiber für Linux 2.4/2.6.

%description -l pl
Sterowniki MicroLink dLAN dla Linuksa 2.4/2.6.

%package -n kernel-char-dLAN
Summary:	Linux kernel driver for MicroLink dLAN
Summary(de):	Linux Kernel Treiber für MicroLink dLAN
Summary(pl):	Sterownik j±dra Linuksa dla dLAN MicroLinka
Release:	%{release}@%{_kernel_ver_str}
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel_up}
Requires(post,postun):	/sbin/depmod

%description -n kernel-char-dLAN
Linux kernel drivers for MicroLink dLAN.

%description -n kernel-char-dLAN -l de
Linux Kernel Treiber für MicroLink dLAN.

%description -n kernel-char-dLAN -l pl
Sterowniki j±dra Linuksa dla dLAN MicroLinka.

%package -n kernel-smp-char-dLAN
Summary:	Linux SMP kernel driver for MicroLink dLAN
Summary(de):	Linux SMP Kernel Treiber für MicroLink dLAN
Summary(pl):	Sterownik j±dra SMP Linuksa dla dLAN MicroLinka
Release:	%{release}@%{_kernel_ver_str}
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel_up}
Requires(post,postun):	/sbin/depmod

%description -n kernel-smp-char-dLAN
Linux SMP kernel drivers for MicroLink dLAN.

%description -n kernel-smp-char-dLAN -l de
Linux SMP Kernel Treiber für MicroLink dLAN.

%description -n kernel-smp-char-dLAN -l pl
Sterowniki j±dra SMP Linuksa dla dLAN MicroLinka.

%prep
%setup -q -n %{name}-linux-package-%{version}
%patch0 -p1

%build
%configure
%if %{with userspace}
%{__make} cfgtool \
	CC="%{__cc}"
%endif

%if %{with kernel}
# kernel module(s)
cd driver
for cfg in %{?with_dist_kernel:%{?with_smp:smp} up}%{!?with_dist_kernel:nondist}; do
	if [ ! -r "%{_kernelsrcdir}/config-$cfg" ]; then
		exit 1
	fi
	install -d o/include/linux
	ln -sf %{_kernelsrcdir}/config-$cfg o/.config
	ln -sf %{_kernelsrcdir}/Module.symvers-$cfg o/Module.symvers
	ln -sf %{_kernelsrcdir}/include/linux/autoconf-$cfg.h o/include/linux/autoconf.h
	%{__make} -C %{_kernelsrcdir} O=$PWD/o prepare scripts
	%{__make} -C %{_kernelsrcdir} clean \
		RCS_FIND_IGNORE="-name '*.ko' -o" \
		M=$PWD O=$PWD/o \
		%{?with_verbose:V=1}
	%{__make} -C %{_kernelsrcdir} modules \
%if "%{_target_base_arch}" != "%{_arch}"
		ARCH=%{_target_base_arch} \
		CROSS_COMPILE=%{_target_base_cpu}-pld-linux- \
%endif
		HOSTCC="%{__cc}" \
		CPP="%{__cpp}" \
		M=$PWD O=$PWD/o \
		%{?with_verbose:V=1}
	mv devolo_usb{,-$cfg}.ko
done
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT

%if %{with userspace}
%{__make} install-cfgtool \
	DESTDIR=$RPM_BUILD_ROOT
%endif

%if %{with kernel}
install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}{,smp}/misc
install driver/devolo_usb-%{?with_dist_kernel:up}%{!?with_dist_kernel:nondist}.ko \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc/devolo_usb.ko
%if %{with smp} && %{with dist_kernel}
install driver/devolo_usb-smp.ko \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/misc/devolo_usb.ko
%endif
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
%doc LEAME LEESMIJ LEGGIMI LIESMICH LISEZ-MOI README
%attr(755,root,root) %{_sbindir}/dlanconfig
%attr(755,root,root) %{_sbindir}/dlanconfig_son
%{_mandir}/man8/dlanconfig.8*
%endif

%if %{with kernel}
%files -n kernel-char-dLAN
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/misc/devolo_usb.*o*

%if %{with smp}
%files -n kernel-smp-char-dLAN
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}smp/misc/devolo_usb.*o*
%endif
%endif
