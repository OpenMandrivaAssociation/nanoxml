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

%define gcj_support 0
%define section free

Name:           nanoxml
Version:        2.2.3
Release:        4.1.6
Epoch:          0
Summary:        Small XML parser for Java
License:        BSD-style
URL:            http://nanoxml.cyberelf.be/
Source0:        http://nanoxml.cyberelf.be/downloads/NanoXML-2.2.3.tar.bz2
Source1:        %{name}-java-1.4.2-package-list
Patch0:         %{name}-build.patch
BuildRequires:  java-rpmbuild >= 0:1.6
#BuildRequires:  java-javadoc
Group:          Development/Java
%if %{gcj_support}
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
find . -name "*.jar" | xargs -t rm
%{__perl} -pi -e 's|javac |%{javac} -source 1.3 |;' -e 's|jar |%{jar} |g;' -e 's|javadoc |%{javadoc} -source 1.3 |;' ./build.sh

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
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name}

%{gcj_compile}

%clean
rm -rf $RPM_BUILD_ROOT

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

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
%doc %{_javadocdir}/%{name}


%changelog
* Sat Dec 11 2010 Oden Eriksson <oeriksson@mandriva.com> 0:2.2.3-4.1.5mdv2011.0
+ Revision: 620476
- the mass rebuild of 2010.0 packages

* Fri Sep 04 2009 Thierry Vignaud <tv@mandriva.org> 0:2.2.3-4.1.4mdv2010.0
+ Revision: 430154
- rebuild

* Fri Sep 19 2008 Alexander Kurtakov <akurtakov@mandriva.org> 0:2.2.3-4.1.3mdv2009.0
+ Revision: 285841
- fix build

  + Thierry Vignaud <tv@mandriva.org>
    - fix "foobar is blabla" summary (=> "blabla") so that it looks nice in rpmdrake
    - kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Anssi Hannula <anssi@mandriva.org>
    - buildrequire java-rpmbuild, i.e. build with icedtea on x86(_64)

* Sat Sep 15 2007 Anssi Hannula <anssi@mandriva.org> 0:2.2.3-4.1.1mdv2008.0
+ Revision: 87264
- rebuild to filter out autorequires of GCJ AOT objects
- remove unnecessary Requires(post) on java-gcj-compat

* Wed Aug 29 2007 David Walluck <walluck@mandriva.org> 0:2.2.3-4.1.0mdv2008.0
+ Revision: 74734
- fix javadoc build
- change license to BSD-style
- add gcj scriptlets
- remove javadoc scriptlets
- Import nanoxml




* Wed Aug 09 2006 David Walluck <walluck@mandriva.org> 0:2.2.3-4.1mdv2007.0
- release

* Thu Jul 20 2006 Ralph Apel <r.apel@r-apel.de> - 0:2.2.3-4jpp
- First JPP-1.7 release
- Drop BR java-javadoc, add package-list as Source instead

* Mon Aug 23 2004 Fernando Nasser <fnasser@redhat.com> - 0:2.2.3-3jpp
- Updated URL
- Pro-forma rebuild with Ant 1.6.2 present

* Sat Jan 10 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:2.2.3-2jpp
- Add Epoch.
- Change group to Text Processing/Markup/XML.
- Add unversioned javadoc dir symlinks, mark javadoc as %%doc.
- Install manual as normal %%doc, not into %%{_javadocdir}.
- BuildRequires java-devel (not ant).
- Don't use bundled SAX jar.

* Sat Dec 27 2003 Thomas Leonard <tle@sirius.sued.tremium.de> - 2.2.3-1
- Initial build.
