Summary:	XSL Formatter in Java
Summary(pl):	Formater XSL napisany w Javie
Name:		fop
Version:	0.92
%define	_snap	409208
Release:	0.%{_snap}.1
License:	Apache v1.1
Group:		Applications/Publishing/XML/Java
#Source0:	http://www.apache.org/dist/xml/fop/source/%{name}-%{version}-src.tar.bz2
# http://svn.apache.org/repos/asf/xmlgraphics/fop/branches/fop-0_92/
Source0:	%{name}-%{_snap}-svn.tar.bz2
# Source0-md5:	50ecf2fd3b474b83ca95f4489fd28b3c
Source1:	%{name}-font-install.sh
Source2:	%{name}.sh
URL:		http://xml.apache.org/fop/
BuildRequires:	batik
BuildRequires:	jce
BuildRequires:	jdk >= 1.3
BuildRequires:	junit
BuildRequires:	rpmbuild(macros) >= 1.300
BuildRequires:	xalan-j
BuildRequires:	xerces-j
BuildRequires:	xmlunit
BuildRequires:	avalon-framework
BuildRequires:	jeuclid
Requires:	batik
Requires:	freetype1
Requires:	jre >= 1.3
Requires:	xalan-j
Requires:	xerces-j
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

%description -l pl
FOP to pierwszy na ¶wiecie program formatuj±cy wydruki sterowany
obiektami formatuj±cymi XSL. To jest aplikacja Javy czytaj±ca drzewo
obiektów formatuj±cych i przekszta³caj±ca je w dokument PDF. Drzewo
obiektów formatuj±cych mo¿e byæ w formie dokumentu XML (wyj¶cia z
silnika XSLT takiego jak XT lub Xalan) lub byæ przekazane jako
dokument DOM lub (w przypadku XT) zdarzenia SAX.

%prep
%setup -q -n %{name}-svn

%build
required_jars='ant xml-commons-apis xercesImpl xalan batik junit xmlunit commons-io xmlgraphics-commons servlet jce'
CLASSPATH="%{_jvmlibdir}/java/lib/tools.jar"
export CLASSPATH="$CLASSPATH:`/usr/bin/build-classpath $required_jars`"
export JAVA_HOME=%{java_home}
export JAVAC=%{javac}
export JAVA=%{java}

%{ant}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_javadir},%{_fop_font_metrics},%{_bindir}} \
	$RPM_BUILD_ROOT%{_fontsdir}

install %{SOURCE1} $RPM_BUILD_ROOT%{_bindir}/fop-font-install
install %{SOURCE2} $RPM_BUILD_ROOT%{_bindir}/fop

# create empty config file
echo > $RPM_BUILD_ROOT%{_fontsdir}/fop-font.config

install lib/avalon-framework-cvs-20020806.jar build/fop.jar $RPM_BUILD_ROOT%{_javadir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{_bindir}/fop-font-install

%files
%defattr(644,root,root,755)
%doc CHANGES README STATUS
%dir %{_fop_font_metrics}
%attr(755,root,root) %{_bindir}/*
%{_javadir}/*
%{_fontsdir}/*.config
