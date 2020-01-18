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
Version:	6.2
Release:	3
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/jaraco-packaging/
Source0:	https://files.pythonhosted.org/packages/source/j/jaraco.packaging/%{pypi_name}-%{version}.tar.gz
# Source0-md5:	ac36cfb217276af107bcbcb60bced1ec
URL:		https://pypi.org/project/jaraco.packaging/
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with python2}
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-setuptools >= 1:31.0.1
BuildRequires:	python-setuptools_scm >= 1.15
%if %{with tests}
BuildRequires:	python-importlib_metadata
BuildRequires:	python-pytest >= 3.5
BuildRequires:	python-six >= 1.4
%endif
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.2
BuildRequires:	python3-setuptools >= 1:31.0.1
BuildRequires:	python3-setuptools_scm >= 1.15
%if %{with tests}
%if "%{py3_ver}" < "3.8"
BuildRequires:	python3-importlib_metadata
%endif
BuildRequires:	python3-pytest >= 3.5
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
Requires:	python3-modules >= 1:3.2

%description -n python3-%{pypi_name}
A few tools to supplement packaging Python releases.

%description -n python3-%{pypi_name} -l pl.UTF-8
Kilka narzędzi wspierających pakietowanie wydań modułów Pythona.

%package apidocs
Summary:	API documentation for Python jaraco.packaging module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona jaraco.packaging
Group:		Documentation

%description apidocs
API documentation for Python jaraco.packaging module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona jaraco.packaging.

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

# packaged in python-jaraco.spec
%{__rm} $RPM_BUILD_ROOT%{py_sitescriptdir}/jaraco/__init__.py*
%endif

%if %{with python3}
%py3_install

# packaged in python-jaraco.spec
%{__rm} $RPM_BUILD_ROOT%{py3_sitescriptdir}/jaraco/__init__.py
%{__rm} $RPM_BUILD_ROOT%{py3_sitescriptdir}/jaraco/__pycache__/__init__.*
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc CHANGES.rst LICENSE README.rst
%{py_sitescriptdir}/jaraco/packaging
%{py_sitescriptdir}/%{egg_name}-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-%{pypi_name}
%defattr(644,root,root,755)
%doc CHANGES.rst LICENSE README.rst
%attr(755,root,root) %{_bindir}/dependency-tree
%attr(755,root,root) %{_bindir}/upload-package
%{py3_sitescriptdir}/jaraco/packaging
%{py3_sitescriptdir}/%{egg_name}-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_static,*.html,*.js}
%endif
