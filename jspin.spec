#
# TODO:
#	- desktop file?
#	- pl description
#
Summary:	Tools for Teaching Concurrency with Spin
Summary(pl.UTF-8):	Narzędzia do nauki współbieżności przy użyciu Spin
Name:		jspin
Version:	4.6
Release:	1
License:	GPLv2
Group:		Development/Tools
Source0:	http://stwww.weizmann.ac.il/g-cs/benari/jspin/%{name}-4-6.zip
# Source0-md5:	0b2866e1eb3709b994ad6ff47c05be0e
URL:		http://stwww.weizmann.ac.il/g-cs/benari/jspin/
BuildRequires:	jar
BuildRequires:	jdk
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

%build
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

cp -a jspin-examples $RPM_BUILD_ROOT%{_datadir}/%{name}
cp -a spider-examples $RPM_BUILD_ROOT%{_datadir}/%{name}

echo -e "#!/bin/sh\n\njavaws -jar %{_datadir}/%{name}/jSpin.jar $@" \
	>$RPM_BUILD_ROOT%{_bindir}/jspin
echo -e "#!/bin/sh\n\njava -cp %{_datadir}/%{name}/jSpin.jar filterSpin.FilterSpin $@" \
	>$RPM_BUILD_ROOT%{_bindir}/jspin-filter
echo -e "#!/bin/sh\n\njavaws -cp %{_datadir}/%{name}/jSpin.jar spinSpider.SpinSpider $@" \
	>$RPM_BUILD_ROOT%{_bindir}/jspin-spider

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc docs/*.pdf txt/help.txt
%attr(755,root,root) %{_bindir}/*
%{_datadir}/%{name}
%{_examplesdir}/%{name}-%{version}
