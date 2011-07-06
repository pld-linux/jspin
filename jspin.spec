#
# TODO:
#	- desktop file?
#	- pl description
#
Summary:	Tools for Teaching Concurrency with Spin
Summary(pl.UTF-8):	Narzędzia do nauki współbieżności przy użyciu Spin
Name:		jspin
Version:	5.0
Release:	0.1
License:	GPLv2
Group:		Development/Tools
Source0:	http://jspin.googlecode.com/files/%{name}-5-0.zip
# Source0-md5:	a4cd4e338a4172004a0c6b5d79cbffc5
Patch0:		%{name}-config.patch
URL:		http://stwww.weizmann.ac.il/g-cs/benari/jspin/
BuildRequires:	jar
BuildRequires:	jdk
BuildRequires:	unzip
Requires:	jre-X11
Requires:	spin
Requires:	graphviz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
jSpin is a graphical user interface for the Spin model checker
that is used for verifying concurrent and distributed programs.
It is an alternative to the XSpin GUI and was developed primarily
for pedagogical purposes. jSpin is written in Java, because
the Java platform is both portable and widely in computer science
education. The user interface of jSpin is simple and consists
of a single window with menus, a toolbar and three adjustable
text areas. Spin option strings are automatically supplied and
the Spin output is filtered and presented in a tabular form.
All aspects of jSpin are configurable: some at compile time,
some at initialization through a configuration file and some at
runtime.

#%description -l pl.UTF-8

%prep
%setup -q -c
%patch0 -p1

%build
sed -i -e "s|@@BINDIR@@|%{_bindir}|g" \
	-e "s|@@EXAMPLESDIR@@|%{_examplesdir}/%{name}-%{version}|g" \
	jspin/Config.java config.cfg 

javac -target 1.5 jspin/*.java
javac -target 1.5 spinSpider/*.java
javac -target 1.5 filterSpin/*.java
jar cfm jSpin.jar \
	jspin/MANIFEST.MF \
	jspin/*.class \
	spinSpider/*.class \
	filterSpin/*.class

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_datadir}/%{name},%{_examplesdir}/%{name}-%{version}}

cp -a jspin-examples $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -a spider-examples $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

install jSpin.jar $RPM_BUILD_ROOT%{_datadir}/%{name}
install config.cfg $RPM_BUILD_ROOT%{_datadir}/%{name}
install txt/help.txt txt/copyright.txt $RPM_BUILD_ROOT%{_datadir}/%{name}

echo -e "#!/bin/sh\n\njava -jar %{_datadir}/%{name}/jSpin.jar $@" \
	>$RPM_BUILD_ROOT%{_bindir}/jspin
echo -e "#!/bin/sh\n\njava -cp %{_datadir}/%{name}/jSpin.jar filterSpin.FilterSpin $@" \
	>$RPM_BUILD_ROOT%{_bindir}/jspin-filter
echo -e "#!/bin/sh\n\njava -cp %{_datadir}/%{name}/jSpin.jar spinSpider.SpinSpider $@" \
	>$RPM_BUILD_ROOT%{_bindir}/jspin-spider

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc docs/*.pdf
%attr(755,root,root) %{_bindir}/*
%{_datadir}/%{name}
%{_examplesdir}/%{name}-%{version}
