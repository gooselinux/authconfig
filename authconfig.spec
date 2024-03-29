Summary: Command line tool for setting up authentication from network services
Name: authconfig
Version: 6.1.4
Release: 6%{?dist}
License: GPLv2+
ExclusiveOS: Linux
Group: System Environment/Base
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
URL: https://fedorahosted.org/authconfig
Source: https://fedorahosted.org/releases/a/u/%{name}/%{name}-%{version}.tar.bz2
Patch1: authconfig-6.1.3-no-freeipa.patch
Patch2: authconfig-6.1.4-backports.patch
Patch3: authconfig-6.1.4-update.patch
Patch4: authconfig-6.1.4-ldap-packages.patch
Patch5: authconfig-6.1.4-nis-startup.patch
Requires: newt-python, pam >= 0.99.10.0, python
Conflicts: pam_krb5 < 1.49, samba-common < 3.0, samba-client < 3.0
Conflicts: nss_ldap < 254, sssd < 0.99.1
BuildRequires: glib2-devel, python >= 2.6, python-devel
BuildRequires: desktop-file-utils, intltool, gettext, perl-XML-Parser

%description 
Authconfig is a command line utility which can configure a workstation
to use shadow (more secure) passwords.  Authconfig can also configure a
system to be a client for certain networked user information and
authentication schemes.

%package gtk
Summary: Graphical tool for setting up authentication from network services
Group: System Environment/Base
Requires: %{name} = %{version}-%{release}, pygtk2-libglade >= 2.14.0
Requires: usermode-gtk, hicolor-icon-theme

%description gtk
Authconfig-gtk is a GUI program which can configure a workstation
to use shadow (more secure) passwords.  Authconfig-gtk can also configure
a system to be a client for certain networked user information and
authentication schemes.

%prep
%setup -q -n %{name}-%{version}
%patch1 -p1 -b .no-freeipa
%patch2 -p1 -b .backports
%patch3 -p1 -b .update
%patch4 -p1 -b .ldap-packages
%patch5 -p1 -b .nis-startup

%build
CFLAGS="$RPM_OPT_FLAGS -fPIC"; export CFLAGS
%configure
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT/%{_libdir}/python*/site-packages/acutilmodule.a
rm $RPM_BUILD_ROOT/%{_libdir}/python*/site-packages/acutilmodule.la
rm $RPM_BUILD_ROOT/%{_datadir}/%{name}/authconfig-tui.py
ln -s authconfig.py $RPM_BUILD_ROOT/%{_datadir}/%{name}/authconfig-tui.py

%find_lang %{name}
find $RPM_BUILD_ROOT%{_datadir} -name "*.mo" | xargs ./utf8ify-mo

%clean
rm -rf $RPM_BUILD_ROOT

%triggerin -- authconfig <= 5.4.9
authconfig --update --nostart >/dev/null 2>&1 || :

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc COPYING NOTES TODO README.samba3
%ghost %config(noreplace) %{_sysconfdir}/sysconfig/authconfig
%ghost %config(noreplace) %{_sysconfdir}/pam.d/system-auth-ac
%ghost %config(noreplace) %{_sysconfdir}/pam.d/password-auth-ac
%ghost %config(noreplace) %{_sysconfdir}/pam.d/fingerprint-auth-ac
%ghost %config(noreplace) %{_sysconfdir}/pam.d/smartcard-auth-ac
%{_sbindir}/cacertdir_rehash
%{_sbindir}/authconfig
%{_sbindir}/authconfig-tui
%exclude %{_mandir}/man8/system-config-authentication.*
%exclude %{_mandir}/man8/authconfig-gtk.*
%{_mandir}/man8/*
%{_mandir}/man5/*
%{_libdir}/python*/site-packages/acutilmodule.so
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/authconfig.py*
%{_datadir}/%{name}/authconfig-tui.py*
%{_datadir}/%{name}/authinfo.py*
%{_datadir}/%{name}/shvfile.py*
%{_datadir}/%{name}/dnsclient.py*
%{_datadir}/%{name}/msgarea.py*
%attr(700,root,root) %dir %{_localstatedir}/lib/%{name}

%files gtk
%defattr(-,root,root,-)
%{_bindir}/authconfig
%{_bindir}/authconfig-tui
%{_bindir}/authconfig-gtk
%{_bindir}/system-config-authentication
%{_sbindir}/authconfig-gtk
%{_sbindir}/system-config-authentication
%{_mandir}/man8/system-config-authentication.*
%{_mandir}/man8/authconfig-gtk.*
%{_datadir}/%{name}/authconfig.glade
%{_datadir}/%{name}/authconfig-gtk.py*
%config(noreplace) %{_sysconfdir}/pam.d/authconfig-gtk
%config(noreplace) %{_sysconfdir}/pam.d/system-config-authentication
%config(noreplace) %{_sysconfdir}/security/console.apps/authconfig-gtk
%config(noreplace) %{_sysconfdir}/security/console.apps/system-config-authentication
%config(noreplace) %{_sysconfdir}/pam.d/authconfig
%config(noreplace) %{_sysconfdir}/pam.d/authconfig-tui
%config(noreplace) %{_sysconfdir}/security/console.apps/authconfig
%config(noreplace) %{_sysconfdir}/security/console.apps/authconfig-tui
%{_datadir}/applications/*
%{_datadir}/icons/hicolor/16x16/apps/system-config-authentication.*
%{_datadir}/icons/hicolor/22x22/apps/system-config-authentication.*
%{_datadir}/icons/hicolor/24x24/apps/system-config-authentication.*
%{_datadir}/icons/hicolor/32x32/apps/system-config-authentication.*
%{_datadir}/icons/hicolor/48x48/apps/system-config-authentication.*

%changelog
* Thu Jul 15 2010 Tomas Mraz <tmraz@redhat.com> - 6.1.4-6
- fix startup of NIS (#614856)

* Mon Jul 12 2010 Tomas Mraz <tmraz@redhat.com> - 6.1.4-5
- use current ldap packages in the warnings

* Thu Jun 10 2010 Tomas Mraz <tmraz@redhat.com> - 6.1.4-4
- remove superfluous space in nsswitch.conf (#595265)
- always write to 'default' domain in sssd.conf only (#598558)

* Fri May 21 2010 Tomas Mraz <tmraz@redhat.com> - 6.1.4-3
- update pam and nsswitch config only when needed

* Wed May 19 2010 Tomas Mraz <tmraz@redhat.com> - 6.1.4-2
- disable the krb5 inputs if using dns discovery (#591716)
- add pam_sss to password-auth password stack (#592872)

* Tue May  4 2010 Tomas Mraz <tmraz@redhat.com> - 6.1.4-1
- set the new icon also for the windows (#583330)
- updated translations
- disable non-smartcard PAM stacks if require smart card for authentication
- remove pam_pkcs11 from the password PAM stack
- set smartcard action also in gconf
- properly set the options for pam_pkcs11
- do not write pam_password option to nslcd.conf (#585953)

* Wed Apr 14 2010 Tomas Mraz <tmraz@redhat.com> - 6.1.3-3
- write pam_password setting only to appropriate files (#582246)

* Thu Apr  8 2010 Tomas Mraz <tmraz@redhat.com> - 6.1.3-2
- drop FreeIPA choice from the GUI

* Wed Apr  7 2010 Tomas Mraz <tmraz@redhat.com> - 6.1.3-1
- manual page improvements (#578258, #526164)
- use ldap instead of sss for nsswitch maps unsupported by sssd (#578325)
- call cacertdir_rehash also in case ldaps: server uri is used (#578219)
- ldap_uri must be comma separated (#579881)
- updated translations
- new icon (#540249)

* Mon Mar 29 2010 Tomas Mraz <tmraz@redhat.com> - 6.1.2-1
- fix SSSD provider change (#577263)
- drop LDAP authentication from FreeIPA choice
- updated translations
- use pam_oddjob_mkhomedir if the appropriate package is installed (#552485)

* Fri Mar 19 2010 Tomas Mraz <tmraz@redhat.com> - 6.1.1-1
- added credential caching enablement for SSSD
- added msgarea for LDAP authentication requirements
- fix spurious missing modules warnings and other minor changes

* Thu Mar 18 2010 Tomas Mraz <tmraz@redhat.com> - 6.1.0-1
- new very much simplified GUI
- use SSSD instead of legacy ldap/krb5 if the configuration is
  supported
- drop krb4 config file write (#569612)
- handle exception when running with insufficient priviledges (#572534)
- support RFC2307bis LDAP schema

* Tue Feb  2 2010 Tomas Mraz <tmraz@redhat.com> - 6.0.2-1
- fix regression from the nss_ldap/pam_ldap nslcd split

* Thu Jan 14 2010 Tomas Mraz <tmraz@redhat.com> - 6.0.1-1
- do not try to write smartcard settings if pam_pkcs11 is not
  installed (#528458)
- make position of sss in nsswitch consistent with position in
  system-auth (#552501)
- support nss_ldap/pam_ldap split and nslcd

* Thu Dec 10 2009 Tomas Mraz <tmraz@redhat.com> - 6.0.0-1
- support for SSSD enabling/disabling and basic support for
  SSSD domain setup
- safe atomic overwrites of the config files

* Wed Nov 11 2009 Tomas Mraz <tmraz@redhat.com> - 5.4.14-1
- fixed missing truncation in the backup restores (#533881)

* Fri Sep 25 2009 Tomas Mraz <tmraz@redhat.com> - 5.4.13-1
- updated translations

* Thu Sep 17 2009 Tomas Mraz <tmraz@redhat.com> - 5.4.12-1
- fixed indentation error (#523534)

* Mon Sep 14 2009 Tomas Mraz <tmraz@redhat.com> - 5.4.11-1
- updated translations (#522444)
- silence failures when restarting services (#500385)

* Thu Apr 23 2009 Tomas Mraz <tmraz@redhat.com> - 5.4.10-1
- update PAM configuration when updating from old authconfig versions (#495924)

* Fri Apr 10 2009 Tomas Mraz <tmraz@redhat.com> - 5.4.9-1
- add support for multiple PAM auth stacks (by Ray Strode) (#494874)

* Thu Apr  2 2009 Tomas Mraz <tmraz@redhat.com> - 5.4.8-1
- fix regression in authconfig-tui (#493576)

* Mon Jan 26 2009 Tomas Mraz <tmraz@redhat.com> - 5.4.7-1
- move the consolehelper symlinks to the gtk subpackage to remove
  the dependency on usermode in the base package (#480014)
- return nonzero exit codes on some more possible errors (#440461)

* Fri Dec 19 2008 Tomas Mraz <tmraz@redhat.com> - 5.4.6-1
- fix typo in the fingerprint reader patch (#477080)

* Thu Nov 27 2008 Tomas Mraz <tmraz@redhat.com> - 5.4.5-1
- improved cacertdir_rehash to be more robust
- add fingerprint reader support (original patch by Bastien Nocera) (#469418)
- remove pam_smb support from GUI and TUI
- fix nscd pid file path (#471642)

* Tue Aug  5 2008 Tomas Mraz <tmraz@redhat.com> - 5.4.4-1
- do not call domainname when run with --nostart (#457697)

* Fri Jun  6 2008 Tomas Mraz <tmraz@redhat.com> - 5.4.3-1
- remove the --enableldapssl alias and add some help to GUI tooltips
  to clear up some confusion (#220973)
- add option --enablepreferdns to prefer DNS over NIS or WINS in
  hostname resolution

* Tue Apr  8 2008 Tomas Mraz <tmraz@redhat.com> - 5.4.2-1
- read wins setting from nsswitch.conf correctly (#440459)
- do not ignore --enablemd5/--disablemd5 options

* Tue Mar 11 2008 Tomas Mraz <tmraz@redhat.com> - 5.4.1-1
- fixed backup directory in Makefile and spec (#437040)

* Mon Mar 10 2008 Tomas Mraz <tmraz@redhat.com> - 5.4.0-1
- include config-util in console.apps files
- add support for saving/restoring backups of configuration
  files affected by authconfig (#433776)
- improve the authconfig manual page (#432023, #432938)

* Tue Jan 29 2008 Tomas Mraz <tmraz@redhat.com> - 5.3.21-1
- correct the fix for bug #237956

* Fri Jan 18 2008 Tomas Mraz <tmraz@redhat.com> - 5.3.20-1
- update translations

* Wed Jan  9 2008 Tomas Mraz <tmraz@redhat.com> - 5.3.19-1
- support new sha256 and sha512 password hash algorithms
- add support for pam_mkhomedir (#212790)
- do not crash in authconfig --help (#237956) - thanks to Andy Shevchenko for
  the idea how to fix that
- setup password hash algorithm in /etc/login.defs (#218652)
- update translations

* Tue Sep 25 2007 Tomas Mraz <tmraz@redhat.com> - 5.3.18-1
- improve krb5.conf handling (#238766)

* Fri Aug 24 2007 Tomas Mraz <tmraz@redhat.com> - 5.3.17-1
- remove obsolete pam_krb5afs support (#250704)
- add support for pam_access (#251360)
- update translations

* Tue Aug 21 2007 Tomas Mraz <tmraz@redhat.com> - 5.3.16-3
- license tag fix

* Thu Aug  9 2007 Tomas Mraz <tmraz@redhat.com> - 5.3.16-2
- require newt-python (#251359)

* Wed Jul 25 2007 Tomas Mraz <tmraz@redhat.com> - 5.3.16-1
- add support for winbind offline login (#232955)

* Wed Jul 18 2007 Tomas Mraz <tmraz@redhat.com> - 5.3.15-1
- dnsclient fixes by Simo Sorce
- add Categories to .desktop file (#245868)
- fixed traceback when calling joinDomain (#245374)
- disable smart card action setting when gnome-screensaver
  not installed (#209643)
- do not change protocols and services in nsswitch.conf (#236669)

* Tue Jun 12 2007 Tomas Mraz <tmraz@redhat.com> - 5.3.14-1
- authconfig.8 synopsis fixed (patch by Eric Raymond) (#220574)
- drop explicit requirement on python version as it is now 
  generated automatically
- improve writing /etc/samba/smb.conf (based on patch by
  Simo Sorce)
- merge changes upstream
  
* Fri May  4 2007 Tomas Mraz <tmraz@redhat.com> - 5.3.13-4
- local nis domain is obtained from sysconfig/network (#235927)
- set "local authorization is sufficient" on by default

* Thu Apr  5 2007 Tomas Mraz <tmraz@redhat.com> - 5.3.13-3
- minor changes and cleanups for merge review (#225293)

* Mon Mar 19 2007 Tomas Mraz <tmraz@redhat.com> - 5.3.13-2
- nss_ldap is now in /usr/lib (#232975)

* Tue Dec 12 2006 Tomas Mraz <tmraz@redhat.com> - 5.3.13-1
- another traceback in --probe and other fixes (#218874)
- make smbRealm a default realm when appropriate (#219300)
- added missing languages in LINGUAS

* Wed Nov 29 2006 Tomas Mraz <tmraz@redhat.com> - 5.3.12-1
- when pam_krb5 auth fails with smartcard login don't enforce it
  in the account stack (#214931)
- updated translations (#216570)
- winbind should be added only to user tables (#216862)

* Fri Oct 20 2006 Tomas Mraz <tmraz@redhat.com> - 5.3.11-1
- fixed --smartcardaction command line option (#211552)

* Fri Oct  6 2006 Tomas Mraz <tmraz@redhat.com> - 5.3.10-1
- fixed passwd PAM stack when PKCS11 enabled (#195960)
- make authconfig --probe work again (#209676)

* Mon Oct  2 2006 Tomas Mraz <tmraz@redhat.com> - 5.3.9-1
- updated translations (#207095)
- correctly write pam_smb.conf with only one server specified (#208365)

* Thu Sep 21 2006 Tomas Mraz <tmraz@redhat.com> - 5.3.8-1
- move options to another tab to fit on 800x600 screen (#207357)

* Tue Sep 19 2006 Tomas Mraz <tmraz@redhat.com> - 5.3.7-1
- improve PAM setup for smart card login
- support smart card login with kerberos (PKINIT)
- add pam_pkcs11 to password PAM stack

* Mon Sep  4 2006 Tomas Mraz <tmraz@redhat.com> - 5.3.6-1
- skip pam_unix for session for crond service
- fixed a bug in saving when smartcard settings changed (#204838)
- removed allow_ypbind setsebool as it is now handled in ypbind

* Tue Aug 29 2006 Tomas Mraz <tmraz@redhat.com> - 5.3.5-1
- improve smart card related UI strings
- removed possibility to set smart card type from authconfig-gtk
  as only coolkey will be supported for now

* Thu Aug 24 2006 Tomas Mraz <tmraz@redhat.com> - 5.3.4-1
- pass options given to authconfig-gtk to authconfig (#203955)

* Sun Jul 23 2006 Ray Strode <rstrode@redhat.com> - 5.3.3-2
- write out new "wait_for_card" config option if we're
  forcing smart card authentication
- add "use_uid" option to smart card pam_succeed_if line to
  work around bug where pam_succeed_if checks user information
  even in cases where the conditional doesn't depend on it.
- remove unimplemented "logout" smart card removal action from
  settings
- remove unnecessary "card_only" argument

* Fri Jul 21 2006 Tomas Mraz <tmraz@redhat.com> - 5.3.3-1
- don't start sceventd when smartcard login is enabled
- improve pam config for smartcard login

* Tue Jul 18 2006 Tomas Mraz <tmraz@redhat.com> - 5.3.2-1
- don't require pam_pkcs11 to run

* Tue Jul 18 2006 Tomas Mraz <tmraz@redhat.com> - 5.3.1-1
- screensavers should be authenticated by smartcard too
- add feature to download a CA certificate for LDAP from 
  an URL (#197103)
- add pam_keyinit session module to the PAM configuration (#198638)

* Fri Jul  7 2006 Tomas Mraz <tmraz@redhat.com> - 5.3.0-1
- added support for smartcard authentication
- fixed parsing kerberos realms

* Thu May 18 2006 Tomas Mraz <tmraz@redhat.com> - 5.2.5-1
- write ldap servers as URIs and not HOSTs (#191842)
- fix a typo in --test output
- updated summary, converted changelog to UTF-8

* Fri May 12 2006 Tomas Mraz <tmraz@redhat.com> - 5.2.4-1
- added crond to the services restarted after firstboot (#187334)
- when checking nscd status redirect output to /dev/null (#188555)

* Tue Mar 21 2006 Tomas Mraz <tmraz@redhat.com> - 5.2.3-1
- make smb.conf and krb5.conf loading more robust (#185766)

* Mon Feb 27 2006 Tomas Mraz <tmraz@redhat.com> - 5.2.2-1
- add try_first_pass option to pam_unix for better integration
  with individual service configurations (#182350)
- updated translations

* Mon Feb 20 2006 Tomas Mraz <tmraz@redhat.com> - 5.2.1-1
- don't crash in TUI when some options aren't set (#182151)

* Fri Feb  3 2006 Tomas Mraz <tmraz@redhat.com> - 5.2.0-1
- redesigned GUI (#178112)
- added man page for system-config-ac (#179584)
- disable authentication of system accounts by network services
  by default, added option for changing that (#179009)
- updated translations, new languages

* Mon Jan  9 2006 Tomas Mraz <tmraz@redhat.com> - 5.1.2-1
- fixed regression when saving nsswitch.conf

* Fri Jan  6 2006 Tomas Mraz <tmraz@redhat.com> - 5.1.1-1
- print warning if PAM module is missing when the PAM configuration
  is saved (#168880)

* Fri Dec 23 2005 Tomas Mraz <tmraz@redhat.com>
- make child dialog preset code more robust (#176462)

* Sat Dec 17 2005 Tomas Mraz <tmraz@redhat.com> - 5.1.0-1
- update only configuration files which settings were modified (#72290)

* Mon Dec  5 2005 Tomas Mraz <tmraz@redhat.com> - 5.0.4-1
- don't ignore krb5realm command line option (#174838)
- read dns_lookup_realm and dns_lookup_kdc values correctly
- the PAM configuration is now written in system-auth-ac file
  which is then symlinked from system-auth, the symlink is not
  overwritten so local PAM configuration is now possible (#165342)

* Mon Nov  7 2005 Tomas Mraz <tmraz@redhat.com> - 5.0.3-1
- add symlinks to python scripts in sbindir
- don't override nullok setting from system-auth (#96996)

* Fri Oct 14 2005 Tomas Mraz <tmraz@redhat.com> - 5.0.2-1
- authinfo-tui.py is now symlink
- reword the CA certificate message (#154317)
- use include instead of pam_stack in pam config
- don't break yp.conf with multiple domains (#127306)

* Mon Sep  5 2005 Tomas Mraz <tmraz@redhat.com> - 5.0.1-1
- fixed a few errors catched by pychecker

* Sat Sep  3 2005 Tomas Mraz <tmraz@redhat.com> - 5.0.0-1
- C code completely rewritten in Python
- some bugs fixed in the process (and no doubt new introduced)
- TUI deprecated, opens only when run as authconfig-tui

* Mon Jun 20 2005 Tomas Mraz <tmraz@redhat.com> - 4.6.13-1
- set domain and ypserver option correctly when multiple servers
  specified in kickstart (#159214)

* Tue Apr 12 2005 Tomas Mraz <tmraz@redhat.com> - 4.6.12-1
- replaced deprecated gtk.TRUE/FALSE (#153034)
- updated translations

* Fri Mar 14 2005 Tomas Mraz <tmraz@redhat.com>
- propagate the --enablewinbindauth option to the configuration (#151018)

* Fri Mar  4 2005 Tomas Mraz <tmraz@redhat.com> - 4.6.11-1
- changed version propagation

* Thu Mar  3 2005 Tomas Mraz <tmraz@redhat.com>
- updated translations
- fixed build on gcc4

* Wed Feb 23 2005 Tomas Mraz <tmraz@redhat.com> - 4.6.10-1
- updated translations

* Thu Feb 10 2005 Tomas Mraz <tmraz@redhat.com> - 4.6.9-1
- improved the code that writes tls_cacertdir to ldap.conf

* Tue Jan 25 2005 Tomas Mraz <tmraz@redhat.com>
- renamed functions in authconfigmodule to be more clear
- implemented cacertdir for LDAP with TLS

* Mon Jan 24 2005 Tomas Mraz <tmraz@redhat.com>
- fixed a bug in authinfo_differs when called from python

* Wed Dec 17 2004 Tomas Mraz <tmraz@redhat.com> - 4.6.8-1
- add option for making local authorization sufficient for local users
  this is attempt to 'solve/workaround' the problem with blocking local logins by
  pulling out network cable (#115181)

* Wed Dec 15 2004 Tomas Mraz <tmraz@redhat.com>
- remove dependency on nscd
- don't show warning messages when switching options off

* Mon Dec  6 2004 Tomas Mraz <tmraz@redhat.com> - 4.6.7-1
- updated translations
- winbind in authconfig-gtk.py was setting the nsswitch.conf on the auth tab
- use GtkComboBox instead of deprecated GtkOptionMenu
- disable options with not installed binaries, remove unnecessary deps of
  authconfig-gtk

* Thu Nov 18 2004 Tomas Mraz <tmraz@redhat.com> - 4.6.6-1
- merged patches from dist
- fix versioning

* Mon Nov  8 2004 Jeremy Katz <katzj@redhat.com> - 4.6.5-6
- rebuild against python 2.4

* Thu Oct 28 2004 Dan Walsh <dwalsh@redhat.com>
- Fix setsebool patch to turn off boolean

* Thu Oct 28 2004 Dan Walsh <dwalsh@redhat.com>
- Add setsebool for NIS

* Fri Oct 15 2004 Tomas Mraz <tmraz@redhat.com>
- force broken_shadow option on network auth (#136760)

* Fri Oct 15 2004 Tomas Mraz <tmraz@redhat.com>
- force restart of autofs on firstboot call when using NIS (#133035, #124498)

* Thu Oct 07 2004 Tomas Mraz <tmraz@redhat.com>
- require python to install (#134654)

* Mon Oct 04 2004 Jindrich Novy <jnovy@redhat.com> 4.6.5-1
- updated translations from upstream
- autogeneration of build stripts in prep phase

* Fri Sep 30 2004 Jindrich Novy <jnovy@redhat.com>
- fixed man page
- added dependency on nscd

* Wed Sep 29 2004 Jindrich Novy <jnovy@redhat.com> 4.6.4-6
- regenerated build scripts

* Wed Sep 29 2004 Jindrich Novy <jnovy@redhat.com> 4.6.4-5
- fixed all po files to translate correctly messages with modified accelerators (#133742)
- added translations for Arabic, Bulgarian and other languages (#133716, #133158)

* Wed Sep 22 2004 Jindrich Novy <jnovy@redhat.com> 4.6.4-4
- added "quiet" option to pam_success_if PAM module in sytem-auth (#133179)

* Mon Sep 13 2004 Jindrich Novy <jnovy@redhat.com> 4.6.4-3
- corrected package dependencies #132411
- regenerated glade.strings.h #132369

* Wed Aug 25 2004 Jindrich Novy <jnovy@redhat.com> 4.6.4-2
- modified authconfig-gtk interface to fit lower resolution screens (#127175)
- modified accelerators in authconfig-gtk (#125797)
- updated package dependencies (#125306)

* Tue Aug 24 2004 Jindrich Novy <jnovy@redhat.com>
- updated configure scripts
- warnfixes and minor hacks

* Mon Jun  7 2004 Nalin Dahyabhai <nalin@redhat.com> 4.6.4-1
- tweak account management to fix #55193 correctly
- require anything we might want to run in the gui subpackage because it
  doesn't warn about missing things and you don't have a terminal to see
  error messages about missing commands
- properly display the domain in the GUI join dialog (#124621)

* Tue May 11 2004 Nalin Dahyabhai <nalin@redhat.com> 4.6.3-1
- omit the "ads" or "rpc" when calling "net join", Samba's smarter now (#122802)
- properly warn about missing "net" (samba-client) and libnss_winbind and
  pam_winbind (samba-common) in text mode (#122802)

* Wed Apr 21 2004 Nalin Dahyabhai <nalin@redhat.com> 4.6.2-1
- learn all about pam_passwdqc
- preserve arguments to pam_cracklib and pam_passwdqc
- short-circuit PAM authorization checks for users with UID < 100
- remove redhat-config-authentication as a way to invoke the GUI tool (#115977)

* Fri Feb  6 2004 Nalin Dahyabhai <nalin@redhat.com> 4.6.1-1
- fix man page: --enableldapssl should be --enableldaptls
- make --enableldapssl an alias for --enableldaptls

* Thu Jan  8 2004 Nalin Dahyabhai <nalin@redhat.com> 4.6-1
- authconfig-gtk.py: require rhpl, which is required by the script (#104209)
- both: require usermode (authconfig-gtk transitively), else leave a dangling
  symlink (#104209)
- the great redhat-config-authentication/system-config-authentication renaming,
  as was foretold in the fedora-config-list archives

* Wed Jan  7 2004 Nalin Dahyabhai <nalin@redhat.com>
- preserve "compat" if it's used in /etc/nsswitch.conf

* Tue Nov 18 2003 Nalin Dahyabhai <nalin@redhat.com> 4.4-1
- add options for toggling krb5's use of DNS

* Mon Nov 17 2003 Nalin Dahyabhai <nalin@redhat.com>
- rework tui to include winbind options. there wasn't enough room in the old
  dialog to include the important options, so the whole thing's been reworked

* Thu Nov 13 2003 Nalin Dahyabhai <nalin@redhat.com>
- conflict with older versions of samba which expect different configuration

* Mon Nov 10 2003 Nalin Dahyabhai <nalin@redhat.com>
- initial support for configuring winbind

* Tue Oct 28 2003 Nalin Dahyabhai <nalin@redhat.com>
- make pam_cracklib requisite instead of required in generated PAM configs

* Wed Oct 22 2003 Bill Nottingham <notting@redhat.com> 4.3.8-1
- rebuild with current translations

* Thu Aug 21 2003 Nalin Dahyabhai <nalin@redhat.com> 4.3.7-2
- make the tarball name include the release number

* Thu Aug 21 2003 Nalin Dahyabhai <nalin@redhat.com> 4.3.7-1
- authconfig-gtk: condrestart certain additional services if invoked with
  the --firstboot flag (half of #91268, needs cooperating firstboot)
- translation updates

* Mon Jul  7 2003 Nalin Dahyabhai <nalin@redhat.com> 4.3.6-1
- translation updates

* Mon Jun 30 2003 Nalin Dahyabhai <nalin@redhat.com>
- add 'redhat-config-authentication' as an alias for authconfig-gtk
- make authconfig-gtk exec authconfig if gui startup fails and it looks like
  we're connected to a tty

* Thu Jun 05 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon May  5 2003 Nalin Dahyabhai <nalin@redhat.com> 4.3.5-1
- translation updates
- close unusable file descriptors if locking fails

* Tue Feb 18 2003 Nalin Dahyabhai <nalin@redhat.com> 4.3.4-1
- learn how to toggle defaults/crypt_style in /etc/libuser.conf (#79337)

* Fri Feb  7 2003 Nalin Dahyabhai <nalin@redhat.com> 4.3.3-1
- look in /lib64 for modules for nsswitch and PAM by default on
  x86_64, ppc64, and s390x (#83049)

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt
 
* Mon Nov  4 2002 Nalin Dahyabhai <nalin@redhat.com> 4.3.2-1
- update translations
- update copyright strings (only took 10 months!)

* Wed Oct 23 2002 Nalin Dahyabhai <nalin@redhat.com> 4.3.1-1
- require a version of PAM (0.75-43) which supports $ISA
- use $ISA in our own PAM config files

* Tue Oct 22 2002 Nalin Dahyabhai <nalin@redhat.com>
- add $ISA to the name of the directory in which we expect PAMs to be stored

* Fri Sep 20 2002 Nalin Dahyabhai <nalin@redhat.com> 4.3-1
- build with -fPIC, necessary on some arches

* Tue Sep  3 2002 Nalin Dahyabhai <nalin@redhat.com> 4.2.11-3
- update translations

* Thu Aug 29 2002 Trond Eivind Glomsrød <teg@redhat.com> 4.2.12-2
- Update translations

* Fri Aug 23 2002 Nalin Dahyabhai <nalin@redhat.com> 4.2.11-1
- modify spacing and layout in authconfig-gtk

* Thu Aug 15 2002 Nalin Dahyabhai <nalin@redhat.com> 4.2.10-4
- translation updates
- rebuild to pick up dependency changes

* Mon Jul 29 2002 Nalin Dahyabhai <nalin@redhat.com> 4.2.10-3
- include the userhelper configuration file
- require sufficiently-new pam package in the gui subpackage

* Fri Jul 26 2002 Nalin Dahyabhai <nalin@redhat.com> 4.2.10-2
- actually include the icon in the package
- translation updates

* Tue Jul 23 2002 Nalin Dahyabhai <nalin@redhat.com> 4.2.10-1
- use desktop-file-install (#69376)
- include an icon for the menu item (#68577)

* Wed Jul 17 2002 Nalin Dahyabhai <nalin@redhat.com> 4.2.9-2
- own the pkgdatadir
- pull in translation updates

* Mon Jun  3 2002 Nalin Dahyabhai <nalin@redhat.com> 4.2.9-1
- add --enable-experimental to enable some of that experimental code
- add --enable-local to enable local policies
- update translations

* Thu May 30 2002 Nalin Dahyabhai <nalin@redhat.com> 4.2.8-7
- use the current revision of python by default
- get the intltool/gettext situation sorted out

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Fri May  3 2002 Nalin Dahyabhai <nalin@redhat.com> 4.2.8-5
- remove bogus buildrequires left over from when authconfig-gtk was C code
- buildrequires python-devel in addition to python (to build the python module,
  but we still need python to byte-compile the python script)

* Thu Apr 18 2002 Nalin Dahyabhai <nalin@redhat.com> 4.2.8-4
- add missing translations back in
- convert .mo files at install-time

* Mon Apr 15 2002 Nalin Dahyabhai <nalin@redhat.com> 4.2.8-3
- refresh translations

* Wed Apr 10 2002 Nalin Dahyabhai <nalin@redhat.com> 4.2.8-2
- actually add the .desktop files

* Tue Apr  9 2002 Nalin Dahyabhai <nalin@redhat.com> 4.2.8-1
- refresh translations
- destroy the python object correctly

* Tue Mar 26 2002 Nalin Dahyabhai <nalin@redhat.com> 4.2.7-2
- add the .desktop file

* Mon Mar 25 2002 Nalin Dahyabhai <nalin@redhat.com> 4.2.7-1
- rework the auth stack logic to require all applicable auth modules

* Fri Mar  1 2002 Nalin Dahyabhai <nalin@redhat.com> 4.2.6-1
- allow pam_krb5afs to be used for account management, too

* Mon Feb 25 2002 Nalin Dahyabhai <nalin@redhat.com> 4.2.5-3
- refresh translations

* Fri Feb 22 2002 Nalin Dahyabhai <nalin@redhat.com> 4.2.5-2
- refresh translations

* Tue Feb 12 2002 Nalin Dahyabhai <nalin@redhat.com> 4.2.5-1
- actually free authInfo structures when asked to
- use pam_krb5's account management facilities
- conflict with versions of pam_krb5 which don't offer account management

* Mon Feb  4 2002 Nalin Dahyabhai <nalin@redhat.com> 4.2.4-1
- add python bindings for the back-end
- redo the gui so that it exercises the python bindings
- take a shot at getting authconfig to work in a firstboot container

* Thu Jan 31 2002 Nalin Dahyabhai <nalin@redhat.com> 4.2.3-4
- rebuild again

* Wed Jan 30 2002 Tim Powers <timp@redhat.com> 4.2.3-3
- rebuilt against new glib

* Wed Jan 23 2002 Nalin Dahyabhai <nalin@redhat.com> 4.2.3-2
- rebuild in new environment

* Thu Jan 10 2002 Nalin Dahyabhai <nalin@redhat.com> 4.2.3-1
- add some more experimental options
- clean up the glade files a bit
- don't destroy a garbage pointer on main cancel, destroy the main dialog

* Thu Jan  3 2002 Nalin Dahyabhai <nalin@redhat.com> 4.2.2-2
- bump release and rebuild

* Thu Dec 20 2001 Nalin Dahyabhai <nalin@redhat.com> 4.2.2-1
- make setting of experimental options only possible through
  /etc/sysconfig/authconfig, to keep accidents from happening
- add some more support for experimental stuff

* Tue Dec 11 2001 Nalin Dahyabhai <nalin@redhat.com> 4.2.1-1
- fix setting of LDAP TLS option in authconfig-gtk
- change Apply to Ok, Close to Cancel, because that's how they work

* Tue Dec 11 2001 Nalin Dahyabhai <nalin@redhat.com> 4.2-2
- add the glade XML file to the -gtk subpackage (fix from katzj)

* Mon Dec 10 2001 Nalin Dahyabhai <nalin@redhat.com> 4.2-1
- port to glib2
- move post code to the back-end
- add a libglade GUI in a -gtk subpackage
- set up to use userhelper
