Summary:	XSL Formatter in Java
Summary(pl):	Formater XSL napisany w Javie
Name:		Fop
Version:	0.20.3rc
Release:	3
Vendor:		http://xml.apache.org/
License:	Apache
Group:		Applications/Publishing/XML/Java
Source0:	http://xml.apache.org/dist/fop/%{name}-%{version}-src.tar.gz
Source1:	fop-font-install.sh
Source2:	fop.sh
Patch0:		fop-build.patch
URL:		http://xml.apache.org/fop/
BuildRequires:	batik
BuildRequires:	jdk >= 1.3
BuildRequires:	xalan-j
BuildRequires:	xerces-j
Requires:	batik
Requires:	freetype1
Requires:	jre >= 1.3
Requires:	xalan-j
Requires:	xerces-j
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_javaclassdir		%{_libdir}/java
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
%setup -q
%patch0 -p1

%build
JAVA_HOME=%{_libdir}/java
export JAVA_HOME

sh build.sh

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_javaclassdir},%{_fop_font_metrics},%{_bindir}} \
	$RPM_BUILD_ROOT%{_fontsdir}

install %{SOURCE1} $RPM_BUILD_ROOT%{_bindir}/fop-font-install
install %{SOURCE2} $RPM_BUILD_ROOT%{_bindir}/fop

# create empty config file
echo > $RPM_BUILD_ROOT%{_fontsdir}/fop-font.config

install lib/{jimi-1.0.jar,logkit-1.0b4.jar,avalon-framework-4.0.jar} build/fop.jar $RPM_BUILD_ROOT%{_javaclassdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{_bindir}/fop-font-install

%files
%defattr(644,root,root,755)
%doc LICENSE README STATUS lib/jimi-License.txt docs/html-docs
%dir %{_fop_font_metrics}
%attr(755,root,root) %{_bindir}/*
%{_javaclassdir}/*
%{_fontsdir}/*.config
