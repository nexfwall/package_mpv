%global         _zshdir %{_datadir}/zsh/site-functions

Name:           mpv
Version:        0.14.0
Release:        1%{?dist}
Epoch:          1
Summary:        A free, open source, and cross-platform media player

License:        GPLv2+
URL:            https://mpv.io/
Source0:        https://github.com/%{name}-player/%{name}/archive/v%{version}.tar.gz
# Fix rpmlint incorrect-fsf-address
Patch0:         %{name}-incorrect-fsf-address.patch
# Install symbolic icon
Patch1:         %{name}-symbolic.svg.patch

BuildRequires:  pkgconfig(alsa)
BuildRequires:  pkgconfig(caca)
BuildRequires:  desktop-file-utils
BuildRequires:  pkgconfig(dvdnav)
BuildRequires:  pkgconfig(dvdread)
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(enca)
BuildRequires:  ffmpeg-devel
BuildRequires:  pkgconfig(gbm)
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(jack)
BuildRequires:  pkgconfig(lcms2)
BuildRequires:  pkgconfig(libarchive)
BuildRequires:  pkgconfig(libass)
BuildRequires:  pkgconfig(libbluray)
BuildRequires:  pkgconfig(libcdio)
BuildRequires:  pkgconfig(libcdio_paranoia)
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(libguess)
BuildRequires:  libjpeg-turbo-devel
BuildRequires:  pkgconfig(libpulse)
BuildRequires:  pkgconfig(libv4l2)
BuildRequires:  pkgconfig(libva)
BuildRequires:  pkgconfig(luajit)
BuildRequires:  pkgconfig(openal)
BuildRequires:  pkgconfig(rubberband)
BuildRequires:  pkgconfig(smbclient)
BuildRequires:  pkgconfig(uchardet)
BuildRequires:  pkgconfig(vdpau)
BuildRequires:  waf >= 1.8.16
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-cursor)
BuildRequires:  pkgconfig(wayland-egl)
BuildRequires:  pkgconfig(wayland-scanner)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xext)
BuildRequires:  pkgconfig(xinerama)
BuildRequires:  pkgconfig(xrandr)
BuildRequires:  pkgconfig(xscrnsaver)
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  pkgconfig(xv)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  perl(Math::BigInt)
BuildRequires:  perl(Math::BigRat)
BuildRequires:  python-docutils

Requires:       hicolor-icon-theme

%description
Mpv is a fork of mplayer2 and MPlayer. It shares some features with the former
projects while introducing many more.

%package        libs
Summary:        Shared library for MPV
Obsoletes:      libmpv

%description    libs
MPV shared library.

%package        libs-devel
Summary:        Headers for MPV library
Requires:       %{name}-libs%{?_isa} = %{epoch}:%{version}-%{release}

%description    libs-devel
Headers for MPV library.

%package        zsh
Summary:        MPV zsh completion support
BuildArch:      noarch
Requires:       %{name} = %{epoch}:%{version}-%{release}
Requires:       zsh

%description    zsh
This package provides zsh completion script of MPV.

%prep
%autosetup -p1

echo '#!/bin/bash' > configure
chmod +x configure

%build
%configure
waf configure \
          --prefix=%{_prefix} \
          --bindir=%{_bindir} \
          --libdir=%{_libdir} \
          --confdir=%{_sysconfdir}/%{name} \
          --incdir=%{_includedir} \
          --datadir=%{_datadir} \
          --mandir=%{_mandir} \
          --docdir=%{_docdir}/%{name} \
          --zshdir=%{_zshdir} \
          --disable-build-date \
          --disable-debug-build \
          --enable-alsa \
          --enable-audio-input \
          --enable-caca \
          --enable-cdda \
          --enable-dvbin \
          --enable-dvdnav \
          --enable-dvdread \
          --enable-drm \
          --enable-egl-drm \
          --enable-egl-x11 \
          --enable-enca \
          --enable-encoding \
          --enable-gbm \
          --enable-gl \
          --enable-gl-wayland \
          --enable-gl-x11 \
          --enable-iconv \
          --enable-jack \
          --enable-jpeg \
          --enable-lcms2 \
          --enable-libass \
          --enable-libass-osd \
          --enable-libarchive \
          --enable-libavdevice \
          --enable-libavfilter \
          --enable-libbluray \
          --enable-libguess \
          --enable-libmpv-shared \
          --enable-libsmbclient \
          --enable-libswresample \
          --enable-libv4l2 \
          --enable-lua \
          --enable-manpage-build \
          --enable-openal \
          --enable-oss-audio \
          --enable-pulse \
          --enable-rubberband \
          --enable-shm \
          --enable-termios \
          --enable-tv \
          --enable-tv-v4l2 \
          --enable-uchardet \
          --enable-vaapi \
          --enable-vaapi-glx \
          --enable-vaapi-hwaccel \
          --enable-vaapi-wayland \
          --enable-vaapi-x-egl \
          --enable-vaapi-x11 \
          --enable-vdpau \
          --enable-vdpau-gl-x11 \
          --enable-vdpau-hwaccel \
          --enable-wayland \
          --enable-x11 \
          --enable-xext \
          --enable-xinerama \
          --enable-xrandr \
          --enable-xss \
          --enable-xv \
          --enable-zsh-comp

waf build %{?_smp_mflags} -v

%install
waf install --destdir=%{buildroot}

%{__rm} -r %{buildroot}%{_docdir}/%{name}

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop

%post
/usr/bin/update-desktop-database &> /dev/null || :
/bin/touch --no-create %{_datadir}/icons/hicolor &> /dev/null || :

%postun
/usr/bin/update-desktop-database &> /dev/null || :
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &> /dev/null || :
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null || :

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files
%license LICENSE Copyright
%doc README.md etc/input.conf etc/example.conf
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%{_datadir}/icons/hicolor/*/apps/%{name}.svg
%{_datadir}/icons/hicolor/*/apps/%{name}-symbolic.svg
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/encoding-profiles.conf
%{_mandir}/man1/%{name}.1.*

%files libs
%license LICENSE Copyright
%doc README.md
%{_libdir}/lib%{name}.so.*

%files libs-devel
%{_includedir}/%{name}
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/%{name}.pc

%files zsh
%{_zshdir}/_%{name}

%changelog
* Mon Dec 14 2015 Maxim Orlov <murmansksity@gmail.com> - 1:0.14.0-1.R
- Update to 0.14.0

* Fri Nov 13 2015 Vasiliy N. Glazov <vascom2@gmail.com> - 0.13.0-2.R
- Clean spec
- Use fedora gcc flags

* Thu Nov 12 2015 Vasiliy N. Glazov <vascom2@gmail.com> - 0.13.0-1.R
- update to 0.13.0

* Wed Nov 11 2015 Arkady L. Shane <ashejn@russianfedora.pro> - 0.11.0-0.1.R
- update to 0.11.0

* Tue May 05 2015 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.9.1-3
- Revert patch for reject lua 5.3

* Tue May 05 2015 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.9.1-2
- Disable SDL2 backend
- Apply patch to fix osc bar

* Mon May 04 2015 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.9.1-1
- Update to 0.9.1
- Enable SDL2 backend

* Tue Apr 28 2015 Miro Hrončok <mhroncok@redhat.com> - 0.8.3-3
- Conditionalize old waf patch

* Tue Apr 28 2015 Miro Hrončok <mhroncok@redhat.com> - 0.8.3-2
- Rebuilt

* Mon Apr 13 2015 Miro Hrončok <mhroncok@redhat.com> - 0.8.3-1
- Updated

* Wed Jan 28 2015 Miro Hrončok <mhroncok@redhat.com> - 0.7.3-1
- Updated

* Mon Dec 22 2014 Miro Hrončok <mhroncok@redhat.com> - 0.7.1-3
- Slightly change the waf patch

* Mon Dec 22 2014 Miro Hrončok <mhroncok@redhat.com> - 0.7.1-2
- Add patch to allow waf 1.7

* Sat Dec 13 2014 Miro Hrončok <mhroncok@redhat.com> - 0.7.1-1
- New version 0.7.1
- Rebuilt new lirc (#3450)

* Tue Nov 04 2014 Nicolas Chauvet <kwizart@gmail.com> - 0.6.0-3
- Rebuilt for vaapi 0.36

* Mon Oct 20 2014 Sérgio Basto <sergio@serjux.com> - 0.6.0-2
- Rebuilt for FFmpeg 2.4.3

* Sun Oct 12 2014 Miro Hrončok <mhroncok@redhat.com> - 0.6.0-1
- New version 0.6.0

* Fri Sep 26 2014 Nicolas Chauvet <kwizart@gmail.com> - 0.5.1-2
- Rebuilt for FFmpeg 2.4.x

* Wed Sep 03 2014 Miro Hrončok <mhroncok@redhat.com> - 0.5.1-1
- New version 0.5.1
- Add BR ncurses-devel (#3233)

* Thu Aug 07 2014 Sérgio Basto <sergio@serjux.com> - 0.4.0-2
- Rebuilt for ffmpeg-2.3

* Tue Jul 08 2014 Miro Hrončok <mhroncok@redhat.com> - 0.4.0-1
- New version 0.4.0

* Tue Jun 24 2014 Miro Hrončok <mhroncok@redhat.com> - 0.3.11-1
- New version 0.3.11

* Tue Mar 25 2014 Miro Hrončok <mhroncok@redhat.com> - 0.3.6-2
- Rebuilt for new libcdio and libass

* Thu Mar 20 2014 Miro Hrončok <mhroncok@redhat.com> - 0.3.6-1
- New version 0.3.6

* Fri Feb 28 2014 Miro Hrončok <mhroncok@redhat.com> - 0.3.5-2
- Rebuilt for mistake

* Fri Feb 28 2014 Miro Hrončok <mhroncok@redhat.com> - 0.3.5-1
- New version 0.3.5

* Sat Jan 25 2014 Miro Hrončok <mhroncok@redhat.com> - 0.3.3-1
- New version 0.3.3

* Wed Jan 01 2014 Miro Hrončok <mhroncok@redhat.com> - 0.3.0-2
- Use upstream .desktop file

* Wed Jan 01 2014 Miro Hrončok <mhroncok@redhat.com> - 0.3.0-1
- New version 0.3.0
- Switch to waf
- Add some tricks from openSUSE
- Removed already included patch

* Sun Dec 22 2013 Miro Hrončok <mhroncok@redhat.com> - 0.2.4-8
- Added patch for https://fedoraproject.org/wiki/Changes/FormatSecurity

* Sun Dec 22 2013 Miro Hrončok <mhroncok@redhat.com> - 0.2.4-7
- Support wayland

* Sun Dec 22 2013 Miro Hrončok <mhroncok@redhat.com> - 0.2.4-6
- Rebuilt

* Sun Dec 22 2013 Miro Hrončok <mhroncok@redhat.com> - 0.2.4-5
- Fixed wrong license tag (see upstream a5507312)

* Sun Dec 15 2013 Miro Hrončok <mhroncok@redhat.com> - 0.2.4-4
- Added libva (#3065)

* Sun Dec 15 2013 Miro Hrončok <mhroncok@redhat.com> - 0.2.4-3
- Added lua and libquvi (#3025)

* Sun Dec 15 2013 Miro Hrončok <mhroncok@redhat.com> - 0.2.4-2
- Rebuilt for mistakes

* Sun Dec 15 2013 Miro Hrončok <mhroncok@redhat.com> - 0.2.4-1
- New version 0.2.4

* Mon Nov 11 2013 Miro Hrončok <mhroncok@redhat.com> - 0.2.3-4
- There's no longer AUTHORS file in %%doc
- Install icons

* Mon Nov 11 2013 Miro Hrončok <mhroncok@redhat.com> - 0.2.3-3
- Rebased config patch

* Mon Nov 11 2013 Miro Hrončok <mhroncok@redhat.com> - 0.2.3-2
- Proper sources for all branches

* Mon Nov 11 2013 Miro Hrončok <mhroncok@redhat.com> - 0.2.3-1
- New upstream version

* Sat Oct 12 2013 Miro Hrončok <mhroncok@redhat.com> - 0.1.7-4
- Fixing cvs errors

* Sat Oct 12 2013 Miro Hrončok <mhroncok@redhat.com> - 0.1.7-3
- Add desktop file

* Sat Oct 12 2013 Miro Hrončok <mhroncok@redhat.com> - 0.1.7-2
- Do not use xv as default vo

* Sat Oct 12 2013 Miro Hrončok <mhroncok@redhat.com> - 0.1.7-1
- New upstream release

* Mon Sep 30 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.1.2-4
- Rebuilt

* Mon Sep 09 2013 Miro Hrončok <mhroncok@redhat.com> - 0.1.2-3
- Added BR ffmpeg-libs

* Tue Aug 27 2013 Miro Hrončok <mhroncok@redhat.com> - 0.1.2-2
- Reduced BRs a lot (removed support for various stuff)
- Make smbclient realized
- Changed the description to the text from manual page

* Mon Aug 19 2013 Miro Hrončok <mhroncok@redhat.com> - 0.1.2-1
- Initial spec
- Inspired a lot in mplayer.spec

