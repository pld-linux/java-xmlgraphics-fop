Summary:	XSL Formatter in Java
Summary(pl):	Formater XSL napisany w Javie
Name:		fop
%define	major	0
%define	minor	16
%define micro	0
Version:	%{major}.%{minor}.%{micro}
%define arname	%{name}-%{major}_%{minor}_%{micro}
Release:	1
Vendor:		xml.apache.org
License:	Apache Software License (BSD-like)
Group:		Applications/Publishing/XML
Group(de):	Applikationen/Publizieren/XML
Group(pl):	Aplikacje/Publikowanie/XML
Source0:	http://xml.apache.org/dist/fop/%{arname}.tar.gz
URL:		http://xml.apache.org/fop/
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define	_javaclassdir	%{_datadir}/java/classes

%description 
FOP is the world's first print formatter driven by XSL formatting
objects. It is a Java application that reads a formatting object tree
and then turns it into a PDF document. The formatting object tree, can
be in the form of an XML document (output by an XSLT engine like XT or
Xalan) or can be passed in memory as a DOM Document or (in the case of
XT) SAX events.

%prep
%setup -q -n %{arname}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_javaclassdir}

install *.jar lib/w3c.jar $RPM_BUILD_ROOT%{_javaclassdir}

gzip -9nf LICENSE README STATUS

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc *.gz docs/html-docs
%{_javaclassdir}/*
