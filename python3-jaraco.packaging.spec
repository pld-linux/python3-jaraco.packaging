#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_with	tests	# unit tests (no tests in sources)
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define		egg_name	jaraco.packaging
%define		pypi_name	jaraco.packaging
Summary:	Tools to supplement packaging Python releases
Summary(pl.UTF-8):	Narzędzia wspierające pakietowanie wydań modułów Pythona
Name:		python3-%{pypi_name}
Version:	8.2.0
Release:	1
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/jaraco-packaging/
Source0:	https://files.pythonhosted.org/packages/source/j/jaraco.packaging/%{pypi_name}-%{version}.tar.gz
# Source0-md5:	3a587b8210aaf4ce5433bc57f570883a
URL:		https://pypi.org/project/jaraco.packaging/
BuildRequires:	python3-modules >= 1:3.6
BuildRequires:	python3-setuptools >= 1:31.0.1
BuildRequires:	python3-setuptools_scm >= 3.4.1
BuildRequires:	python3-toml
%if %{with tests}
%if "%{py3_ver}" < "3.8"
BuildRequires:	python3-importlib_metadata
%endif
BuildRequires:	python3-jaraco.test
BuildRequires:	python3-pytest >= 3.5
BuildRequires:	python3-pytest-cov
BuildRequires:	python3-pytest-black >= 0.3.7
BuildRequires:	python3-pytest-flake8
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	python3-rst.linker >= 1.9
BuildRequires:	sphinx-pdg-3
%endif
Requires:	python3-jaraco
Requires:	python3-modules >= 1:3.6
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A few tools to supplement packaging Python releases.

%description -l pl.UTF-8
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
%py3_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
%{__python3} -m pytest 
%endif

%if %{with doc}
# no Makefile
PYTHONPATH=$(pwd) \
sphinx-build-3 -b html docs docs/_build/html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

# packaged in python3-jaraco.spec
%{__rm} $RPM_BUILD_ROOT%{py3_sitescriptdir}/jaraco/__init__.py
%{__rm} $RPM_BUILD_ROOT%{py3_sitescriptdir}/jaraco/__pycache__/__init__.*

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES.rst LICENSE README.rst
%attr(755,root,root) %{_bindir}/dependency-tree
%{py3_sitescriptdir}/jaraco/packaging
%{py3_sitescriptdir}/%{egg_name}-%{version}-py*.egg-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_static,*.html,*.js}
%endif
