#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_with	tests	# unit tests (no tests in sources)

%define		pypi_name	jaraco.packaging
Summary:	Tools to supplement packaging Python releases
Summary(pl.UTF-8):	Narzędzia wspierające pakietowanie wydań modułów Pythona
Name:		python3-%{pypi_name}
Version:	10.2.3
Release:	1
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/jaraco-packaging/
Source0:	https://files.pythonhosted.org/packages/source/j/jaraco_packaging/jaraco_packaging-%{version}.tar.gz
# Source0-md5:	7d4621f007cc2d0e646c26194c6e5f12
Patch0:		no-isolated-env.patch
URL:		https://pypi.org/project/jaraco.packaging/
BuildRequires:	python3-build
BuildRequires:	python3-installer
BuildRequires:	python3-modules >= 1:3.8
BuildRequires:	python3-setuptools >= 1:31.0.1
BuildRequires:	python3-setuptools_scm >= 3.4.1
BuildRequires:	python3-toml
%if %{with tests}
BuildRequires:	python3-domdf-python-tools
%if "%{py3_ver}" < "3.8"
BuildRequires:	python3-importlib_metadata
%endif
BuildRequires:	python3-jaraco.test
BuildRequires:	python3-pytest >= 6
BuildRequires:	python3-pytest-black >= 0.3.7
# lint only?
#BuildRequires:	python3-pytest-checkdocs >= 2.4
BuildRequires:	python3-pytest-cov
#BuildRequires:	python3-pytest-enabler >= 2.2
#BuildRequires:	python3-pytest-mypy >= 0.9.1
#BuildRequires:	python3-ruff
#BuildRequires:	python3-types-docutils
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 2.044
%if %{with doc}
BuildRequires:	python3-furo
BuildRequires:	python3-jaraco.context
BuildRequires:	python3-rst.linker >= 1.9
#BuildRequires:	python3-sphinx-lint
BuildRequires:	sphinx-pdg-3 >= 3.5
%endif
Requires:	python3-jaraco
Requires:	python3-modules >= 1:3.8
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
%setup -q -n jaraco_packaging-%{version}
%patch -P0 -p1

%build
%py3_build_pyproject

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

%py3_install_pyproject

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc LICENSE NEWS.rst README.rst
%{py3_sitescriptdir}/jaraco/packaging
%{py3_sitescriptdir}/jaraco_packaging-%{version}.dist-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_static,*.html,*.js}
%endif
