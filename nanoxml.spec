# Copyright (c) 2000-2005, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

%define gcj_support 1
%define section free

Name:           nanoxml
Version:        2.2.3
Release:        %mkrel 4.1
Epoch:          0
Summary:        NanoXML is a small XML parser for Java
License:        zlib License
URL:            http://nanoxml.cyberelf.be/
Source0:        http://nanoxml.cyberelf.be/downloads/NanoXML-2.2.3.tar.bz2
Source1:        %{name}-java-1.4.2-package-list
Patch0:         %{name}-build.patch
BuildRequires:  jpackage-utils >= 0:1.6
#BuildRequires:  java-javadoc
Group:          Development/Java
%if %{gcj_support}
Requires(post): java-gcj-compat
Requires(postun): java-gcj-compat
BuildRequires:  java-gcj-compat-devel
%else
BuildRequires: java-devel >= 0:1.4.2
BuildArch:      noarch
%endif
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot
#Vendor:         JPackage Project
#Distribution:   JPackage

%description
The intent of NanoXML is to be a small parser which is easy to use.
Although many features were added to NanoXML, it is very small.
The full parser with builder fits in a JAR file of about 32K.

%package        lite
Summary:        Lite version of %{name}
Group:          Development/Java

%description    lite
Lite version of %{name}.

%package        manual
Summary:        Manual for %{name}
Group:          Development/Java

%description    manual
Documentation for %{name}.

%package        manual-lite
Summary:        Manual for the lite version of %{name}
Group:          Development/Java

%description    manual-lite
Documentation for the lite version of %{name}.

%package        javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java

%description    javadoc
Javadoc for %{name}.


%prep
%setup -q -n NanoXML-%{version}
%patch0
cp %{SOURCE1} package-list
find . -name "*.jar" | xargs -r rm -f


%build
sh ./build.sh


%install
rm -rf $RPM_BUILD_ROOT

# jars
install -dm 755 $RPM_BUILD_ROOT%{_javadir}
install -pm 644 Output/%{name}-lite.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}-lite-%{version}.jar
install -pm 644 Output/%{name}-sax.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}-sax-%{version}.jar
install -pm 644 Output/%{name}.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar
(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}*; do ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`; done)

# javadoc
install -dm 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr Documentation/JavaDoc/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name} # ghost symlink

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean
rm -rf $RPM_BUILD_ROOT


%post javadoc
rm -f %{_javadocdir}/%{name}
ln -s %{name}-%{version} %{_javadocdir}/%{name}

%postun javadoc
if [ "$1" = "0" ]; then
    rm -f %{_javadocdir}/%{name}
fi


%files
%defattr(-,root,root,-)
%{_javadir}/%{name}-%{version}.jar
%{_javadir}/%{name}.jar
%{_javadir}/%{name}-sax-%{version}.jar
%{_javadir}/%{name}-sax.jar
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/%{name}-%{version}.jar.*
%attr(-,root,root) %{_libdir}/gcj/%{name}/%{name}-sax-%{version}.jar.*
%endif

%files lite
%defattr(-,root,root,-)
%{_javadir}/%{name}-lite-%{version}.jar
%{_javadir}/%{name}-lite.jar
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/%{name}-lite-%{version}.jar.*
%endif

%files manual
%defattr(0644,root,root,0755)
%doc Documentation/NanoXML-Java/*

%files manual-lite
%defattr(0644,root,root,0755)
%doc Documentation/NanoXML-Lite/*

%files javadoc
%defattr(0644,root,root,0755)
%doc %{_javadocdir}/%{name}-%{version}
%ghost %doc %{_javadocdir}/%{name}
