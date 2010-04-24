
# TODO:
# - Tests are temporarily disabled, because even if all tests passes ant still
#   thinks that some tests failed.
# - I'm not able to produce correct UTF-8 character in PDF/PNG output (-awt
#   output works perfectly)
# - fop-font-install.sh: generate config for other types of fonts (at least
#   PFM fonts are supported)

%bcond_with	tests		# perform tests, broken, see TODO

%include	/usr/lib/rpm/macros.java

%define		srcname	xmlgraphics-fop
Summary:	XSL Formatter in Java
Summary(pl.UTF-8):	Formater XSL napisany w Javie
Name:		java-xmlgraphics-fop
Version:	0.95
Release:	3
License:	Apache v2.0
Group:		Libraries/Java
Source0:	http://www.apache.org/dist/xmlgraphics/fop/source/fop-%{version}-src.tar.gz
# Source0-md5:	58593e6c86be17d7dc03c829630fd152
Source1:	fop-font-install.sh
Source2:	fop.sh
URL:		http://xmlgrapics.apache.org/fop/
BuildRequires:	glibc-localedb-all
%{?with_tests:BuildRequires:	java-junit}
BuildRequires:	java-xalan
BuildRequires:	java-xerces
BuildRequires:	java-xmlgraphics-batik
%{?with_tests:BuildRequires:	java-xmlunit}
BuildRequires:	jdk
BuildRequires:	jpackage-utils
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.300
Requires:	freetype1
Requires:	java-avalon-framework
Requires:	java-commons-io
Requires:	java-xalan
Requires:	java-xerces
Requires:	java-xmlgraphics-batik
Requires:	java-xmlgraphics-commons
Requires:	jpackage-utils
Requires:	jre-X11
Requires:	ttmkfdir
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

%package -n fop
Summary:	fop commandline utility
Group:		Applications/Publishing/XML/Java
Requires:	%{name} = %{version}-%{release}

%description -n fop
Shell script that allows to use java-xmlgraphics-fop as standalone
application.

%prep
%setup -q -n fop-%{version}

%{?with_tests:%patch0 -p1}

%build
required_jars='ant xml-commons-apis xercesImpl xalan xmlgraphics-batik'
CLASSPATH="%{_jvmlibdir}/java/lib/tools.jar"
CLASSPATH="$CLASSPATH:$(%{_bindir}/build-classpath $required_jars)"
export JAVA_HOME=%{java_home}
export JAVAC=%{javac}
export JAVA=%{java}

export LC_ALL=en_US # source code not US-ASCII

%ant package servlet transcoder-pkg

%if %{with tests}
required_jars='xmlunit junit'
CLASSPATH="$CLASSPATH:$(%{_bindir}/build-classpath $required_jars)"
%ant -Dbuild.sysclasspath=first
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_javadir},%{_fop_font_metrics},%{_bindir}} \
	$RPM_BUILD_ROOT%{_fontsdir}

install %{SOURCE1} $RPM_BUILD_ROOT%{_bindir}/fop-font-install
install %{SOURCE2} $RPM_BUILD_ROOT%{_bindir}/fop

# jars
cp -a build/fop.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}-%{version}.jar
ln -s %{srcname}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}.jar

touch $RPM_BUILD_ROOT%{_fop_font_metrics}/fop-font.config

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{_bindir}/fop-font-install

%files
%defattr(644,root,root,755)
%doc KEYS README
%dir %{_fop_font_metrics}
%ghost %{_fop_font_metrics}/fop-font.config
%{_javadir}/%{srcname}.jar
%{_javadir}/%{srcname}-%{version}.jar
%attr(755,root,root) %{_bindir}/fop-font-install

%files -n fop
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/fop
