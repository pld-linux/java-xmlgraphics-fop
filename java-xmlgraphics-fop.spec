
# TODO:
# - Tests are temporarily disabled, because even if all tests passes ant still
#   thinks that some tests failed.
# - package avalon. This package should not provide it.

%if "%{pld_release}" == "ti"
%bcond_without	java_sun	# build with gcj
%else
%bcond_with	java_sun	# build with java-sun
%endif

%bcond_with	tests		# perform tests, broken, see TODO

%include	/usr/lib/rpm/macros.java

Summary:	XSL Formatter in Java
Summary(pl.UTF-8):	Formater XSL napisany w Javie
Name:		fop
Version:	0.95
Release:	1
License:	Apache v1.1
Group:		Applications/Publishing/XML/Java
Source0:	http://www.apache.org/dist/xmlgraphics/fop/source/%{name}-%{version}-src.tar.gz
# Source0-md5:	58593e6c86be17d7dc03c829630fd152
Source1:	%{name}-font-install.sh
Source2:	%{name}.sh
URL:		http://xmlgrapics.apache.org/fop/
BuildRequires:	batik
BuildRequires:	glibc-localedb-all
%{!?with_java_sun:BuildRequires:	java-gcj-compat-devel}
%{?with_java_sun:BuildRequires:	java-sun}
BuildRequires:	jpackage-utils
%{?with_tests:BuildRequires:	java-junit}
%{?with_tests:BuildRequires:	java-xmlunit}
BuildRequires:	rpm >= 4.4.9-56
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.300
BuildRequires:	xalan-j
BuildRequires:	xerces-j
Requires:	batik
Requires:	freetype1
Requires:	jpackage-utils
Requires:	xalan-j
Requires:	xerces-j
Patch0:		fop-disableX11tests.patch
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_fop_font_metrics	/var/lib/fop

%description
FOP is the world's first print formatter driven by XSL formatting
objects. It is a Java application that reads a formatting object tree
and then turns it into a PDF document. The formatting object tree, can
be in the form of an XML document (output by an XSLT engine like XT or
Xalan) or can be passed in memory as a DOM Document or (in the case of
XT) SAX events.

%description -l pl.UTF-8
FOP to pierwszy na świecie program formatujący wydruki sterowany
obiektami formatującymi XSL. To jest aplikacja Javy czytająca drzewo
obiektów formatujących i przekształcająca je w dokument PDF. Drzewo
obiektów formatujących może być w formie dokumentu XML (wyjścia z
silnika XSLT takiego jak XT lub Xalan) lub być przekazane jako
dokument DOM lub (w przypadku XT) zdarzenia SAX.

%prep
%setup -q

%{?with_tests:%patch0 -p1}

%build
required_jars='ant xml-commons-apis xercesImpl xalan batik'
CLASSPATH="%{_jvmlibdir}/java/lib/tools.jar"
CLASSPATH="$CLASSPATH:$(/usr/bin/build-classpath $required_jars)"
export JAVA_HOME=%{java_home}
export JAVAC=%{javac}
export JAVA=%{java}

export LC_ALL=en_US # source code not US-ASCII

%ant package servlet transcoder-pkg

%if %{with tests}
required_jars='xmlunit junit'
CLASSPATH="$CLASSPATH:$(/usr/bin/build-classpath $required_jars)"
%ant -Dbuild.sysclasspath=first
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_javadir},%{_fop_font_metrics},%{_bindir}} \
	$RPM_BUILD_ROOT%{_fontsdir}

install %{SOURCE1} $RPM_BUILD_ROOT%{_bindir}/fop-font-install
install %{SOURCE2} $RPM_BUILD_ROOT%{_bindir}/fop

# create empty config file
echo > $RPM_BUILD_ROOT%{_fontsdir}/fop-font.config

# TODO ugly, ugly, ugly hack
install lib/avalon-framework-4.2.0.jar $RPM_BUILD_ROOT%{_javadir}

# jars
cp -a build/%{name}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
ln -s %{name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}.jar


%clean
rm -rf $RPM_BUILD_ROOT

%post
%{_bindir}/fop-font-install

%files
%defattr(644,root,root,755)
%doc KEYS README
%dir %{_fop_font_metrics}
%attr(755,root,root) %{_bindir}/*
%{_javadir}/*.jar
%{_fontsdir}/*.config
