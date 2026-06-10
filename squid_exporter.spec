%global debug_package %{nil}
%global user prometheus
%global group prometheus

Name:    squid_exporter
Version: 1.13.0
Release: 1%{?dist}
Summary: Prometheus Squid proxy metric exporter
License: MIT
URL:     https://github.com/boynux/squid-exporter

Source0: https://github.com/boynux/squid-exporter/releases/download/v%{version}/squid-exporter-linux-amd64
Source1: autogen_%{name}.unit
Source2: autogen_%{name}.default

%{?systemd_requires}
Requires(pre): shadow-utils

%description
Exports Squid proxy metrics in Prometheus format

%prep

%build
/bin/true

%install
mkdir -vp %{buildroot}%{_sharedstatedir}/prometheus
install -D -m 755 %{SOURCE0} %{buildroot}%{_bindir}/%{name}
install -D -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/default/%{name}
install -D -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service

%pre
getent group prometheus >/dev/null || groupadd -r prometheus
getent passwd prometheus >/dev/null || \
useradd -r -g prometheus -d %{_sharedstatedir}/prometheus -s /sbin/nologin -c "Prometheus services" prometheus
exit 0

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun %{name}.service

%files
%defattr(-,root,root,-)
%caps(cap_dac_read_search=ep) %{_bindir}/%{name}
%config(noreplace) %{_sysconfdir}/default/%{name}
%dir %attr(755, %{user}, %{group}) %{_sharedstatedir}/prometheus
%{_unitdir}/%{name}.service

%changelog
* Wed Jun 10 2026 Ivan Garcia <igarcia@cloudox.org> - 1.13.0
- Initial packaging for the 1.13.0 branch
