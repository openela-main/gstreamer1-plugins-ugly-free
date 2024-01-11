%global         majorminor 1.0

#global gitrel     140
#global gitcommit  4ca3a22b6b33ad8be4383063e76f79c4d346535d
#global shortcommit %(c=%{gitcommit}; echo ${c:0:5})

# Only build mpeg2dec on Fedora
%if 0%{?fedora}
%bcond_without mpeg2
%else
%bcond_with mpeg2
%endif

Name:           gstreamer1-plugins-ugly-free
Version:        1.16.1
Release:        1%{?dist}
Summary:        GStreamer streaming media framework "ugly" plugins

License:        LGPLv2+ and LGPLv2
URL:            http://gstreamer.freedesktop.org/
%if 0%{?gitrel}
# git clone git://anongit.freedesktop.org/gstreamer/gst-plugins-ugly
# cd gst-plugins-ugly; git reset --hard %{gitcommit}; ./autogen.sh; make; make distcheck
# modified with gst-p-ugly-cleanup.sh from SOURCE1
%else
# The source is:
# http://gstreamer.freedesktop.org/src/gst-plugins-ugly/gst-plugins-ugly-%{version}.tar.xz
# modified with gst-p-ugly-cleanup.sh from SOURCE1
%endif
Source0:        gst-plugins-ugly-free-%{version}.tar.xz
Source1:        gst-p-ugly-cleanup.sh

BuildRequires:  gstreamer1-devel >= %{version}
BuildRequires:  gstreamer1-plugins-base-devel >= %{version}

BuildRequires:  check
BuildRequires:  gettext-devel
BuildRequires:  gtk-doc
BuildRequires:  automake autoconf libtool

BuildRequires:  liba52-devel
BuildRequires:  libcdio-devel
BuildRequires:  libdvdread-devel
BuildRequires:  python3-devel

%if %{with mpeg2}
BuildRequires:  libmpeg2-devel
%endif

# when mpeg2dec was moved here from -ugly
Conflicts: gstreamer1-plugins-ugly < 1.16.0-2

%description
GStreamer is a streaming media framework, based on graphs of elements which
operate on media data.

This package contains plug-ins whose license is not fully compatible with LGPL.

%package devel
Summary:        Development files for the GStreamer media framework "ugly" plug-ins
Requires:       %{name} = %{version}-%{release}
Requires:       gstreamer1-plugins-base-devel


%description devel
GStreamer is a streaming media framework, based on graphs of elements which
operate on media data.

This package contains the development files for the plug-ins whose license
is not fully compatible with LGPL.


%prep
%setup -q -n gst-plugins-ugly-%{version}


%build
# libsidplay was removed as obsolete, not forbidden
%configure --disable-silent-rules --disable-fatal-warnings \
    --with-package-name="Fedora GStreamer-plugins-ugly package" \
    --with-package-origin="http://download.fedoraproject.org" \
    --enable-debug --disable-static --enable-gtk-doc --enable-experimental \
%if %{with mpeg2}
    --enable-mpeg2dec \
%else
    --disable-mpeg2dec \
%endif
    --disable-amrnb --disable-amrwb --disable-sidplay --disable-x264
make %{?_smp_mflags}


%install
make install DESTDIR=$RPM_BUILD_ROOT

# Register as an AppStream component to be visible in the software center
#
# NOTE: It would be *awesome* if this file was maintained by the upstream
# project, translated and installed into the right place during `make install`.
#
# See http://www.freedesktop.org/software/appstream/docs/ for more details.
#
mkdir -p $RPM_BUILD_ROOT%{_datadir}/appdata
cat > $RPM_BUILD_ROOT%{_datadir}/appdata/gstreamer-ugly-free.appdata.xml <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!-- Copyright 2013 Richard Hughes <richard@hughsie.com> -->
<component type="codec">
  <id>gstreamer-ugly-free</id>
  <metadata_license>CC0-1.0</metadata_license>
  <name>GStreamer Multimedia Codecs - Extra</name>
  <summary>Multimedia playback for CD, DVD, and MP3</summary>
  <description>
    <p>
      This addon includes several additional codecs that have good quality and
      correct functionality, but whose license is not fully compatible with LGPL.
    </p>
    <p>
      These codecs can be used to encode and decode media files where the
      format is not patent encumbered.
    </p>
    <p>
      A codec decodes audio and video for for playback or editing and is also
      used for transmission or storage.
      Different codecs are used in video-conferencing, streaming media and
      video editing applications.
    </p>
  </description>
  <keywords>
    <keyword>CD</keyword>
    <keyword>DVD</keyword>
    <keyword>MP3</keyword>
  </keywords>
  <url type="homepage">http://gstreamer.freedesktop.org/</url>
  <url type="bugtracker">https://bugzilla.gnome.org/enter_bug.cgi?product=GStreamer</url>
  <url type="help">http://gstreamer.freedesktop.org/documentation/</url>
  <url type="donation">http://www.gnome.org/friends/</url>
  <update_contact><!-- upstream-contact_at_email.com --></update_contact>
</component>
EOF

%find_lang gst-plugins-ugly-%{majorminor}
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'


%files -f gst-plugins-ugly-%{majorminor}.lang
%license COPYING
%doc AUTHORS README REQUIREMENTS

%{_datadir}/appdata/*.appdata.xml

# Plugins without external dependencies
%{_libdir}/gstreamer-%{majorminor}/libgstxingmux.so

# Plugins with external dependencies
%{_libdir}/gstreamer-%{majorminor}/libgsta52dec.so
%{_libdir}/gstreamer-%{majorminor}/libgstcdio.so
%{_libdir}/gstreamer-%{majorminor}/libgstdvdread.so
%if %{with mpeg2}
%{_libdir}/gstreamer-%{majorminor}/libgstmpeg2dec.so
%endif

%files devel
%doc %{_datadir}/gtk-doc/html/gst-plugins-ugly-plugins-%{majorminor}


%changelog
* Thu Nov 14 2019 Wim Taymans <wtaymans@redhat.com> - 1.16.1-1
- Update to 1.16.1
- Only enable mpeg2dec on Fedora
- Resolves: rhbz#1756299

* Mon May 20 2019 Rex Dieter <rdieter@fedoraproject.org> - 1.16.0-3
- Conflicts: gstreamer1-plugins-ugly < 1.16.0-2

* Mon May 13 2019 Yaakov Selkowitz <yselkowi@redhat.com> - 1.16.0-2
- Enable mpeg2dec plugin (#1709470)

* Mon Aug 13 2018 Troy Dawson <tdawson@redhat.com> - 1.14.0-2
- Add BuildRequest python3-devel

* Tue Mar 20 2018 Wim Taymans <wtaymans@redhat.com> - 1.14.0-1
- Update to 1.14.0

* Wed Mar 14 2018 Wim Taymans <wtaymans@redhat.com> - 1.13.91-1
- Update to 1.13.91

* Mon Mar 05 2018 Wim Taymans <wtaymans@redhat.com> - 1.13.90-1
- Update to 1.13.90

* Tue Feb 27 2018 Rex Dieter <rdieter@fedoraproject.org> - 1.13.1-2
- drop Obsoletes/Provides: -mpg123 (moved to -good)

* Thu Feb 22 2018 Wim Taymans <wtaymans@redhat.com> - 1.13.1-1
- Update to 1.13.1
- mp3 plugins moved to -good

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jan 25 2018 Adrian Reber <adrian@lisas.de> - 1.12.4-3
- Rebuilt for new libcdio (2.0.0)

* Sun Jan 14 2018 Yaakov Selkowitz <yselkowi@redhat.com> - 1.12.4-2
- Enable twolame plugin (#1534289)

* Mon Dec 11 2017 Wim Taymans <wtaymans@redhat.com> - 1.12.4-1
- Update to 1.12.4
- Add autoconf and friends to BuildRequires

* Tue Sep 19 2017 Wim Taymans <wtaymans@redhat.com> - 1.12.3-1
- Update to 1.12.3

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jul 17 2017 Wim Taymans <wtaymans@redhat.com> - 1.12.2-1
- Update to 1.12.2

* Tue Jun 20 2017 Wim Taymans <wtaymans@redhat.com> - 1.12.1-1
- Update to 1.12.1

* Thu May 11 2017 Yaakov Selkowitz <yselkowi@redhat.com> - 1.12.0-3
- Enable LAME plugin (#1450108)

* Thu May 11 2017 Yaakov Selkowitz <yselkowi@redhat.com> - 1.12.0-2
- Update to 1.12.0

* Thu May 11 2017 Yaakov Selkowitz <yselkowi@redhat.com> - 1.10.4-2
- Initial Fedora spec file
