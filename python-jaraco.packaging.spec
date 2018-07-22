#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define		egg_name	jaraco.packaging
%define		pypi_name	jaraco.packaging
Summary:	Tools to supplement packaging Python releases
Summary(pl.UTF-8):	Narzędzia wspierające pakietowanie wydań modułów Pythona
Name:		python-%{pypi_name}
Version:	5.1.1
Release:	1
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/jaraco-packaging/
Source0:	https://files.pythonhosted.org/packages/source/j/jaraco.packaging/%{pypi_name}-%{version}.tar.gz
# Source0-md5:	490cb330f6654fcb46aa27c123f2ef84
URL:		https://pypi.org/project/jaraco.packaging/
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with python2}
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-setuptools
BuildRequires:	python-setuptools_scm >= 1.15
%if %{with tests}
BuildRequires:	python-pytest >= 3.5
BuildRequires:	python-pytest-flake8
BuildRequires:	python-six >= 1.4
%endif
%endif
%if %{with python3}
BuildRequires:	python3-modules
BuildRequires:	python3-setuptools
BuildRequires:	python3-setuptools_scm >= 1.15
%if %{with tests}
BuildRequires:	python3-pytest >= 3.5
BuildRequires:	python3-pytest-flake8
BuildRequires:	python3-six >= 1.4
%endif
%endif
%if %{with doc}
BuildRequires:	python3-rst.linker >= 1.9
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python-jaraco
Requires:	python-modules >= 1:2.7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A few tools to supplement packaging Python releases.

%description -l pl.UTF-8
Kilka narzędzi wspierających pakietowanie wydań modułów Pythona.

%package -n python3-%{pypi_name}
Summary:	Tools to supplement packaging Python releases
Summary(pl.UTF-8):	Narzędzia wspierające pakietowanie wydań modułów Pythona
Group:		Libraries/Python
Requires:	python3-jaraco
Requires:	python3-modules

%description -n python3-%{pypi_name}
A few tools to supplement packaging Python releases.

%description -n python3-%{pypi_name} -l pl.UTF-8
Kilka narzędzi wspierających pakietowanie wydań modułów Pythona.

%prep
%setup -q -n %{pypi_name}-%{version}

%build
%if %{with python2}
%py_build %{?with_tests:test}
%endif

%if %{with python3}
%py3_build %{?with_tests:test}
%endif

%if %{with doc}
# no Makefile
cd docs
PYTHONPATH=$(pwd)/.. \
sphinx-build-3 -b html . _build/html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

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
%doc CHANGES.rst LICENSE README.rst
%{py_sitescriptdir}/jaraco/packaging
%{py_sitescriptdir}/%{egg_name}-%{version}-py*.egg-info
%{py_sitescriptdir}/%{egg_name}-%{version}-py*-nspkg.pth
%endif

%if %{with python3}
%files -n python3-%{pypi_name}
%defattr(644,root,root,755)
%doc CHANGES.rst LICENSE README.rst
%attr(755,root,root) %{_bindir}/dependency-tree
%attr(755,root,root) %{_bindir}/upload-package
%{py3_sitescriptdir}/jaraco/packaging
%{py3_sitescriptdir}/%{egg_name}-%{version}-py*.egg-info
%{py3_sitescriptdir}/%{egg_name}-%{version}-py*-nspkg.pth
%endif
