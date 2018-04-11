%define _use_internal_dependency_generator 0
%define __find_requires %{nil}
%global debug_package %{nil}
%global __spec_install_post /usr/lib/rpm/check-rpaths   /usr/lib/rpm/check-buildroot  \
  /usr/lib/rpm/brp-compress

Name:       cronsun
Version:    0.1.1
Release:    1%{?dist}
Summary:    A distributed job system, similar with distributed crontab


Group:      System Environment/Daemons
License:    Apache License Version 2.0
URL:        https://github.com/zhangchunsheng/cronsun
Source0:    %{name}-%{version}.tgz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires:  golang >= 1.7.4

%description
A distributed job system, similar with distributed crontab.

%package node
Summary:    A distributed job system, similar with distributed crontab
Requires:   %{name}
%description node
A distributed job system, similar with distributed crontab.

%package web
Summary:    A distributed job system, similar with distributed crontab
Requires:   %{name}
%description web
A distributed job system, similar with distributed crontab.


%prep
%setup -q


%build
export GOPATH=$HOME/go
bash ./build.sh

%install
%{__mkdir_p} ${RPM_BUILD_ROOT}%{_sysconfdir}/cronsun
%{__mkdir_p} ${RPM_BUILD_ROOT}%{_datadir}/cronsun
%{__mkdir_p} ${RPM_BUILD_ROOT}%{_sbindir}
%{__mkdir_p} ${RPM_BUILD_ROOT}%{_sysconfdir}/rc.d/init.d/
%{__mkdir_p} ${RPM_BUILD_ROOT}%{_prefix}/lib/systemd/system/

%{__cp} dist/conf/*.json ${RPM_BUILD_ROOT}%{_sysconfdir}/cronsun/
sed -i -e 's/"ui"/"\/usr\/share\/cronsun\/ui"/' ${RPM_BUILD_ROOT}%{_sysconfdir}/cronsun/web.json
%{__cp} -r dist/ui ${RPM_BUILD_ROOT}%{_datadir}/cronsun/
%{__install} -m0755 dist/cronnode ${RPM_BUILD_ROOT}%{_sbindir}/
%{__install} -m0755 dist/cronweb ${RPM_BUILD_ROOT}%{_sbindir}/

%if %{?rhel} == 6
%{__install} -pm 0755 rpms/cronnode.init ${RPM_BUILD_ROOT}%{_sysconfdir}/rc.d/init.d/cronnode
%{__install} -pm 0755 rpms/cronweb.init ${RPM_BUILD_ROOT}%{_sysconfdir}/rc.d/init.d/cronweb
%endif

%if %{?rhel} == 7
%{__install} -m 0644 rpms/cronnode.service ${RPM_BUILD_ROOT}%{_prefix}/lib/systemd/system/
%{__install} -m 0644 rpms/cronweb.service ${RPM_BUILD_ROOT}%{_prefix}/lib/systemd/system/
%endif

%files 
%config(noreplace) %{_sysconfdir}/cronsun/

%files node
%{_sbindir}/cronnode
%if %{?rhel} == 6
%{_sysconfdir}/rc.d/init.d/cronnode
%endif
%if %{?rhel} == 7
%{_prefix}/lib/systemd/system/cronnode.service
%endif

%files web
%{_sbindir}/cronweb
%{_datadir}/cronsun/
%if %{?rhel} == 6
%{_sysconfdir}/rc.d/init.d/cronweb
%endif
%if %{?rhel} == 7
%{_prefix}/lib/systemd/system/cronweb.service
%endif

%post web
%if %{?rhel} == 6
chkconfig cronweb on
%else
systemctl enable cronweb
%endif

%post node
%if %{?rhel} == 6
chkconfig cronnode on
%else
systemctl enable cronnode
%endif

%preun web
%if %{?rhel} == 6
chkconfig cronweb off
%else
systemctl disable cronweb
%endif

%preun node
%if %{?rhel} == 6
chkconfig cronnode off
%else
systemctl disable cronnode
%endif



%changelog

* Wed Apr 11 2018 - zhangchunsheng423@gmail.com 0.1.1
- upgrade

* Mon Apr 09 2018 - zhangchunsheng423@gmail.com 0.1.0
- init version
