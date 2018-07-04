# Conditional build:
%bcond_without	tests	# do not perform "make test"
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define		module		jaraco
%define		egg_name	jaraco.packaging
%define		pypi_name	jaraco.packaging
Summary:	Tools for packaging
Summary(pl.UTF-8):	-
Name:		python-%{pypi_name}
Version:	5.1.1
Release:	1
License:	MIT
Group:		Libraries/Python
Source0:	https://pypi.debian.net/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
# Source0-md5:	490cb330f6654fcb46aa27c123f2ef84
URL:		https://pypi.org/project/jaraco.packaging
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with python2}
BuildRequires:	python-modules
BuildRequires:	python-setuptools
%endif
%if %{with python3}
BuildRequires:	python3-modules
BuildRequires:	python3-setuptools
%endif
Requires:	python-modules
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A distutils command for reporting the dependency tree as resolved by
setuptools. Use after installing a package.

%package -n python3-%{pypi_name}
Summary:	Tools for packaging
Group:		Libraries/Python
Requires:	python3-modules

%description -n python3-%{pypi_name}
A distutils command for reporting the dependency tree as resolved by
setuptools. Use after installing a package.

%prep
%setup -q -n %{pypi_name}-%{version}

%build
%if %{with python2}
%py_build %{?with_tests:test}
%endif

%if %{with python3}
%py3_build %{?with_tests:test}
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

# when files are installed in other way that standard 'setup.py
# they need to be (re-)compiled
# change %{py_sitedir} to %{py_sitescriptdir} for 'noarch' packages!
%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
%py_comp $RPM_BUILD_ROOT%{py_sitedir}

%py_postclean
%endif

%if %{with python3}
%py3_install
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc CHANGES.rst README.rst
%{py_sitescriptdir}/%{module}
%{py_sitescriptdir}/%{egg_name}-%{version}-py*.egg-info
%{py_sitescriptdir}/%{egg_name}-%{version}-py*-nspkg.pth
%endif

%if %{with python3}
%files -n python3-%{pypi_name}
%defattr(644,root,root,755)
%doc CHANGES.rst README.rst
%attr(755,root,root) %{_bindir}/dependency-tree
%attr(755,root,root) %{_bindir}/upload-package
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/%{egg_name}-%{version}-py*.egg-info
%{py3_sitescriptdir}/%{egg_name}-%{version}-py*-nspkg.pth
%endif
