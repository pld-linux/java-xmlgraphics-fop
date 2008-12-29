# TODO:
# - Some test fails. Reason of some failures is obvious:
#   [junit] No X11 DISPLAY variable was set, but this program performed an operation which requires it.
# - Where should we %%install fop.war file?
# - is freetype really required?
#
# Conditional build:
%bcond_without  tests           # build without tests
#
Summary:	XSL Formatter in Java
Summary(pl.UTF-8):	Formater XSL napisany w Javie
Name:		fop
Version:	0.95
Release:	0.1
License:	Apache v1.1
Group:		Applications/Publishing/XML/Java
Source0:	http://archive.apache.org/dist/xmlgraphics/fop/source/%{name}-%{version}-src.zip
# Source0-md5:	adeb416f81125d8554a621050f319632
Source1:	%{name}-font-install.sh
Source2:	%{name}.sh
Patch0:		%{name}-nojunit.patch
URL:		http://xmlgrapics.apache.org/fop/
BuildRequires:	batik
BuildRequires:	jakarta-servletapi5
BuildRequires:	java-commons-io
BuildRequires:	java-commons-logging
BuildRequires:	jdk >= 1.3
BuildRequires:	jpackage-utils
%{?with_tests:BuildRequires:	junit}
BuildRequires:	rpmbuild(macros) >= 1.300
BuildRequires:	xalan-j
BuildRequires:	xerces-j
BuildRequires:	xmlgraphics-commons
%{?with_tests:BuildRequires:	xmlunit}
Requires(post):	xorg-app-mkfontdir
Requires(post):	awk
Requires:	batik
Requires:	freetype
Requires:	jakarta-servletapi5
Requires:	java-commons-io
Requires:	java-commons-logging
Requires:	jpackage-utils
Requires:	jre
Requires:	xalan-j
Requires:	xerces-j
Requires:	xmlgraphics-commons
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

%if %{without tests}
%patch0 -p1
%endif

# We do want to use system libs
# br_jars='commons-io commons-logging avalon-framework-api serializer servlet xmlgraphics-commons xml-apis-ext xercesImpl xalan batik batik/*'
rm lib/*
# for jar in $br_jars; do
#   ln -s $(find-jar $jar) lib
# done

%build
# required_jars='ant'
# CLASSPATH="%{_jvmlibdir}/java/lib/tools.jar"
# export CLASSPATH="$CLASSPATH:`%{_bindir}/build-classpath $required_jars`"
# export JAVA_HOME=%{java_home}
# export JAVAC=%{javac}
# export JAVA=%{java}

br_jars='commons-io commons-logging avalon-framework-api serializer servlet xmlgraphics-commons xml-apis-ext xercesImpl xalan batik'
export CLASSPATH=$(build-classpath $br_jars):$(build-classpath-directory %{_javadir}/batik)
%ant \
%if %{without tests}
	-Djunit.present=false \
	-Dxmlunit.present=false
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_javadir},%{_fop_font_metrics},%{_bindir}} \
	$RPM_BUILD_ROOT%{_fontsdir}

install %{SOURCE1} $RPM_BUILD_ROOT%{_bindir}/fop-font-install
install %{SOURCE2} $RPM_BUILD_ROOT%{_bindir}/fop

# create empty config file
echo > $RPM_BUILD_ROOT%{_fontsdir}/fop-font.config

cd build
for jar in fop*.jar; do
  base=$(basename $jar .jar)
  install $jar $RPM_BUILD_ROOT%{_javadir}/$base-%{version}.jar
  ln -s $base-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/$base.jar
done

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{_bindir}/fop-font-install

%files
%defattr(644,root,root,755)
%doc KEYS NOTICE README known-issues.xml
%dir %{_fop_font_metrics}
%attr(755,root,root) %{_bindir}/fop
%attr(755,root,root) %{_bindir}/fop-font-install
%{_javadir}/fop*.jar
%{_fontsdir}/fop-font.config
