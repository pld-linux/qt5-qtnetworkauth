#
# Conditional build:
%bcond_with	bootstrap	# disable features to able to build without installed qt5
%bcond_without	doc		# documentation

%if %{with bootstrap}
%undefine	with_doc
%endif

%define		orgname		qtnetworkauth
%define		qtbase_ver		%{version}
%define		qtdeclarative_ver	%{version}
%define		qttools_ver		5.9
Summary:	The Qt5 Network Auth library
Summary(pl.UTF-8):	Biblioteka Qt5 Network Auth
Name:		qt5-%{orgname}
Version:	5.15.13
Release:	1
License:	GPL v3 or commercial
Group:		X11/Libraries
Source0:	https://download.qt.io/official_releases/qt/5.15/%{version}/submodules/%{orgname}-everywhere-opensource-src-%{version}.tar.xz
# Source0-md5:	61f17b78977b3de00a648cead98586e5
URL:		https://www.qt.io/
BuildRequires:	Qt5Core-devel >= %{qtbase_ver}
BuildRequires:	Qt5Network-devel >= %{qtbase_ver}
%if %{with doc}
BuildRequires:	qt5-assistant >= %{qttools_ver}
%endif
BuildRequires:	qt5-build >= %{qtbase_ver}
BuildRequires:	qt5-qmake >= %{qtbase_ver}
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 2.016
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		specflags	-fno-strict-aliasing
%define		qt5dir		%{_libdir}/qt5

%description
Qt is a cross-platform application and UI framework. Using Qt, you can
write web-enabled applications once and deploy them across desktop,
mobile and embedded systems without rewriting the source code.

This package contains Qt5 Network Auth library.

%description -l pl.UTF-8
Qt to wieloplatformowy szkielet aplikacji i interfejsów użytkownika.
Przy użyciu Qt można pisać aplikacje powiązane z WWW i wdrażać je w
systemach biurkowych, przenośnych i wbudowanych bez przepisywania kodu
źródłowego.

Ten pakiet zawiera bibliotekę Qt5 Network Auth.

%package -n Qt5NetworkAuth
Summary:	The Qt5 Network Auth library
Summary(pl.UTF-8):	Biblioteka Qt5 Network Auth
Group:		Libraries
%requires_eq_to	Qt5Core Qt5Core-devel
Requires:	Qt5Network >= %{qtbase_ver}

%description -n Qt5NetworkAuth
Qt5 Network Auth library provides classes for network authentication.

%description -n Qt5NetworkAuth -l pl.UTF-8
Biblioteka Qt5 Network Auth dostarcza klasy do uwierzytelniania w
sieci.

%package -n Qt5NetworkAuth-devel
Summary:	Qt5 Network Auth library - development files
Summary(pl.UTF-8):	Biblioteka Qt5 Network Auth - pliki programistyczne
Group:		Development/Libraries
Requires:	Qt5Core-devel >= %{qtbase_ver}
Requires:	Qt5Network-devel >= %{qtbase_ver}
Requires:	Qt5NetworkAuth = %{version}-%{release}

%description -n Qt5NetworkAuth-devel
Qt5 Network Auth library - development files.

%description -n Qt5NetworkAuth-devel -l pl.UTF-8
Biblioteka Qt5 NetworkAuth - pliki programistyczne.

%package doc
Summary:	Qt5 Network Auth documentation in HTML format
Summary(pl.UTF-8):	Dokumentacja do biblioteki Qt5 Network Auth w formacie HTML
License:	FDL v1.3
Group:		Documentation
Requires:	qt5-doc-common >= %{qtbase_ver}
BuildArch:	noarch

%description doc
Qt5 Network Auth documentation in HTML format.

%description doc -l pl.UTF-8
Dokumentacja do biblioteki Qt5 Netwok Auth w formacie HTML.

%package doc-qch
Summary:	Qt5 Network Auth documentation in QCH format
Summary(pl.UTF-8):	Dokumentacja do biblioteki Qt5 Network Auth w formacie QCH
License:	FDL v1.3
Group:		Documentation
Requires:	qt5-doc-common >= %{qtbase_ver}
BuildArch:	noarch

%description doc-qch
Qt5 Network Auth documentation in QCH format.

%description doc-qch -l pl.UTF-8
Dokumentacja do biblioteki Qt5 Network Auth w formacie QCH.

%package examples
Summary:	Qt5 Network Auth examples
Summary(pl.UTF-8):	Przykłady do biblioteki Qt5 Network Auth
License:	BSD or commercial
Group:		X11/Development/Libraries
BuildArch:	noarch

%description examples
Qt5 Network Auth examples.

%description examples -l pl.UTF-8
Przykłady do biblioteki Qt5 Network Auth.

%prep
%setup -q -n %{orgname}-everywhere-src-%{version}

%build
%{qmake_qt5}
%{__make}

%{?with_doc:%{__make} docs}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT

%if %{with doc}
%{__make} install_docs \
	INSTALL_ROOT=$RPM_BUILD_ROOT
%endif

# useless symlinks
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libQt5*.so.5.??
# actually drop *.la, follow policy of not packaging them when *.pc exist
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libQt5*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n Qt5NetworkAuth -p /sbin/ldconfig
%postun	-n Qt5NetworkAuth -p /sbin/ldconfig

%files -n Qt5NetworkAuth
%defattr(644,root,root,755)
%doc LICENSE.GPL3-EXCEPT dist/changes-*
%attr(755,root,root) %{_libdir}/libQt5NetworkAuth.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt5NetworkAuth.so.5

%files -n Qt5NetworkAuth-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt5NetworkAuth.so
%{_libdir}/libQt5NetworkAuth.prl
%{_includedir}/qt5/QtNetworkAuth
%{_libdir}/cmake/Qt5NetworkAuth
%{_pkgconfigdir}/Qt5NetworkAuth.pc
%{_libdir}/qt5/mkspecs/modules/qt_lib_networkauth.pri
%{_libdir}/qt5/mkspecs/modules/qt_lib_networkauth_private.pri

%if %{with doc}
%files doc
%defattr(644,root,root,755)
%{_docdir}/qt5-doc/qtnetworkauth

%files doc-qch
%defattr(644,root,root,755)
%{_docdir}/qt5-doc/qtnetworkauth.qch
%endif

%files examples
%defattr(644,root,root,755)
# XXX: dir shared with qt5-qtbase-examples
%dir %{_examplesdir}/qt5
%{_examplesdir}/qt5/oauth
