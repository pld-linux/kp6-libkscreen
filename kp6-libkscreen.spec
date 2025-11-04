#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeplasmaver	6.5.2
%define		qtver		5.15.2
%define		kpname		libkscreen

Summary:	KDE screen management software
Name:		kp6-%{kpname}
Version:	6.5.2
Release:	1
License:	LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/plasma/%{kdeplasmaver}/%{kpname}-%{version}.tar.xz
# Source0-md5:	1f4450689ccc7a9aa20198ac8dc0a6cc
URL:		http://www.kde.org/
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	cmake >= 3.16.0
BuildRequires:	kf6-extra-cmake-modules
BuildRequires:	ninja
BuildRequires:	plasma-wayland-protocols-devel >= 1.16.0
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	xz
%requires_eq_to Qt6Core Qt6Core-devel
Obsoletes:	kp5-%{kpname} < 6
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		qt6dir		%{_libdir}/qt6

%description
KDE screen management software.

%package devel
Summary:	Header files for %{kpname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kpname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Obsoletes:	kp5-%{kpname}-devel < 6

%description devel
Header files for %{kpname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kpname}.

%prep
%setup -q -n %{kpname}-%{version}

%build
%cmake -B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	-DKDE_INSTALL_DOCBUNDLEDIR=%{_kdedocdir}
%ninja_build -C build

%if %{with tests}
ctest
%endif

%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%find_lang %{kpname}6_qt --all-name --with-qm

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f %{kpname}6_qt.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/kscreen-doctor
%attr(755,root,root) %{_prefix}/libexec/kf6/kscreen_backend_launcher
%dir %{_libdir}/qt6/plugins/kf6/kscreen
%{_libdir}/qt6/plugins/kf6/kscreen/KSC_Fake.so
%{_libdir}/qt6/plugins/kf6/kscreen/KSC_XRandR.so
%{_libdir}/qt6/plugins/kf6/kscreen/KSC_KWayland.so
%{_datadir}/dbus-1/services/org.kde.kscreen.service
%{_datadir}/qlogging-categories6/libkscreen.categories
%{systemduserunitdir}/plasma-kscreen.service
%{zsh_compdir}/_kscreen-doctor
%{_libdir}/libKF6Screen.so.*.*
%ghost %{_libdir}/libKF6Screen.so.8
%{_libdir}/libKF6ScreenDpms.so.*.*
%ghost %{_libdir}/libKF6ScreenDpms.so.8

%files devel
%defattr(644,root,root,755)
%{_libdir}/libKF6Screen.so
%{_libdir}/libKF6ScreenDpms.so
%{_includedir}/KF6/KScreen
%{_includedir}/KF6/kscreen_version.h
%{_libdir}/cmake/KF6Screen
%{_pkgconfigdir}/KF6Screen.pc
