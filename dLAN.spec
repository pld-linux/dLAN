%bcond_without  dist_kernel     # without kernel from distribution
%bcond_without  kernel          # don't build kernel modules
%bcond_without  smp             # don't build SMP module
%bcond_without  userspace       # don't build userspace module
%bcond_with     verbose         # verbose build (V=1)

Summary:	dLAN drivers
Summary(de):	dLAN Treiber
Summary(pl):	Sterowniki dLAN
Name:		dLAN
Version:	2.0
Release:	1
License:	Devolo AG License
Group:		Applications
Source0:	http://download.devolo.net/webcms/0599755001130248395/%{name}-linux-package-%{version}.tar.gz
# Source0-md5:	419b5e551a7e8eb7e2f609b252287712
Patch0:		%{name}-usbkill.patch
URL:		http://www.devolo.de/de_DE/index.html
BuildRequires:	%{kgcc_package}
%{?with_dist_kernel:BuildRequires:      kernel-module-build}
BuildRequires:	libpcap-devel
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
MicroLink dLAN drivers for Linux 2.4/2.6.

%description -l de
MicroLink dLAN Treiber für Linux 2.4/2.6.

%description -l pl
Sterowniki MicroLink dLAN dla linuksa 2.4/2.6.

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
%{__make} cfgtool
%endif

%if %{with kernel}
# kernel module(s)
cd driver
for cfg in %{?with_dist_kernel:%{?with_smp:smp} up}%{!?with_dist_kernel:nondist}; do
        if [ ! -r "%{_kernelsrcdir}/config-$cfg" ]; then
                exit 1
        fi
        rm -rf include
        install -d include/{linux,config}
        ln -sf %{_kernelsrcdir}/config-$cfg .config
        ln -sf %{_kernelsrcdir}/include/linux/autoconf-$cfg.h include/linux/autoconf.h
        ln -sf %{_kernelsrcdir}/include/asm-%{_target_base_arch} include/asm
        ln -sf %{_kernelsrcdir}/Module.symvers-$cfg Module.symvers
        touch include/config/MARKER

	%{__make} -C %{_kernelsrcdir} modules
                CC="%{__cc}" CPP="%{__cpp}" \
                M=$PWD O=$PWD \
                %{?with_verbose:V=1}
        for mod in *.ko; do
                mod=$(echo "$mod" | sed -e 's#\.ko##g')
                mv $mod.ko ../$mod-$cfg.ko
        done
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
%if %{without dist_kernel}
for mod in *-nondist.ko; do
        nmod=$(echo "$mod" | sed -e 's#-nondist##g')
        install $mod $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc/$nmod
done
%else
for mod in *-up.ko; do
        nmod=$(echo "$mod" | sed -e 's#-up##g')
        install $mod $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/misc/$nmod
done
%if %{with smp}
for mod in *-smp.ko; do
        nmod=$(echo "$mod" | sed -e 's#-smp##g')
        install $mod $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/misc/$nmod
done
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
