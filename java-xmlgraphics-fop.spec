
Summary:	XSL Formatter in Java
Summary(pl):	Formater XSL napisany w Javie
Name:		fop
%define arname	xml-%{name}
%define snapshot 20010427102823
Version:	0.19
Release:	0.%{snapshot}
Vendor:		xml.apache.org
License:	Apache Software License (BSD-like)
Group:		Applications/Publishing/XML
Group(de):	Applikationen/Publizieren/XML
Group(pl):	Aplikacje/Publikowanie/XML
Source0:	http://xml.apache.org/from-cvs/xml-fop/%{arname}_%{snapshot}.tar.gz
Source1:	%{name}-font-install.sh
Source2:	%{name}.sh
URL:		http://xml.apache.org/fop/
BuildRequires:	java1.3sdk
Requires:	freetype1
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_javaclassdir		%{_datadir}/java/classes
%define		_fop_font_metrics	/var/lib/fop

%description 
FOP is the world's first print formatter driven by XSL formatting
objects. It is a Java application that reads a formatting object tree
and then turns it into a PDF document. The formatting object tree, can
be in the form of an XML document (output by an XSLT engine like XT or
Xalan) or can be passed in memory as a DOM Document or (in the case of
XT) SAX events.

%prep
%setup -q -n %{arname}

%build
JAVA_HOME=/usr/lib/java-sdk
export JAVA_HOME
./build.sh

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_javaclassdir},%{_fop_font_metrics},%{_bindir}} \
	$RPM_BUILD_ROOT%{_fontsdir}

install %{SOURCE1} $RPM_BUILD_ROOT%{_bindir}/fop-font-install
install %{SOURCE2} $RPM_BUILD_ROOT%{_bindir}/fop

# create empty config file
echo > $RPM_BUILD_ROOT%{_fontsdir}/fop-font.config

install lib/{jimi-1.0,w3c,xalan-2.0.0,xerces-1.2.3}.jar build/fop.jar \
	$RPM_BUILD_ROOT%{_javaclassdir}

gzip -9nf LICENSE README STATUS

%post
%{_bindir}/fop-font-install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc *.gz docs/html-docs
%dir %{_fop_font_metrics}
%attr(755,root,root) %{_bindir}/*
%{_javaclassdir}/*
%{_fontsdir}/*.config
