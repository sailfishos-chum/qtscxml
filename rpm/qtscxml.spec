%global qt_version 5.15.8

Summary: Qt5 - ScXml component
Name:    opt-qt5-qtscxml
Version: 5.15.8
Release: 1%{?dist}

# See LGPL_EXCEPTIONS.txt, LICENSE.GPL3, respectively, for exception details
License: LGPL-3.0-only OR GPL-3.0-only WITH Qt-GPL-exception-1.0
Url:     http://www.qt.io
%global majmin %(echo %{version} | cut -d. -f1-2)
Source0: %{name}-%{version}.tar.bz2

BuildRequires: make
BuildRequires: opt-qt5-qtbase-devel >= %{qt_version}
BuildRequires: opt-qt5-qtbase-private-devel
%{?_opt_qt5:Requires: %{_opt_qt5}%{?_isa} = %{_opt_qt5_version}}
BuildRequires: opt-qt5-qtdeclarative-devel >= %{qt_version}

%description
The Qt SCXML module provides functionality to create state machines from SCXML files.
This includes both dynamically creating state machines loading the SCXML file and instantiating states and transitions)
and generating a C++ file that has a class implementing the state machine.
It also contains functionality to support data models and executable content.

%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: opt-qt5-qtbase-devel%{?_isa}
Requires: opt-qt5-qtdeclarative-devel%{?_isa}
%description devel
%{summary}.

%prep
%autosetup -n %{name}-%{version}/upstream


%build
export QTDIR=%{_opt_qt5_prefix}
touch .git
%{opt_qmake_qt5}

# have to restart build several times due to bug in sb2
%make_build -k || chmod -R ugo+r . || true
%make_build
chmod -R ugo+r .

%install
make install INSTALL_ROOT=%{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license LICENSE.*
%{_opt_qt5_libdir}/libQt5Scxml.so.5*
%{_opt_qt5_bindir}/qscxmlc
%{_opt_qt5_qmldir}/QtScxml/

%files devel
%{_opt_qt5_headerdir}/QtScxml/
%{_opt_qt5_libdir}/libQt5Scxml.so
%{_opt_qt5_libdir}/libQt5Scxml.prl
%{_opt_qt5_libdir}/pkgconfig/Qt5Scxml.pc
%{_opt_qt5_libdir}/cmake/Qt5Scxml
%{_opt_qt5_archdatadir}/mkspecs/features/qscxmlc.prf
%{_opt_qt5_archdatadir}/mkspecs/modules/*
%exclude %{_opt_qt5_libdir}/libQt5Scxml.la
