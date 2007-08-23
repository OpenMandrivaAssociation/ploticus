%define name 	ploticus
%define version 2.30
%define release %mkrel 4

%define filever 230

Summary: 	Graph/plot generator
Name: 		%{name}
Version: 	%{version}
Release: 	%{release}
License: 	GPL
Group: 		Publishing
URL: 		http://ploticus.sourceforge.net/
Source0:	http://ploticus.sourceforge.net/download/pl%{filever}src.tar.bz2
Source1:	http://ploticus.sourceforge.net/download/pl%{filever}docs.tar.bz2
# http://ploticus.sourceforge.net/download/plsrc210_gd20gif.patch
Patch0:		plsrc230_gd20gif.diff.bz2
Requires: 	gd-utils
BuildRequires:	XFree86-devel
BuildRequires:	freetype-devel
BuildRequires:	gd-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
#BuildRequires:	ming-devel
BuildRequires:	xpm
BuildRequires:	zlib-devel
Conflicts:	swi-prolog
BuildRoot: 	%{_tmppath}/%{name}-%{version}-%{release}buildroot

%description
PLOTICUS is a popular command line utility for creating graphs and plots
that may be presented in Web pages, printed reports, slides, posters, or
interactively. It can produce pie, bar, line, boxplot, scatterplot,
sweep, and other types of plots. Colors and appearance details are very
configurable. PLOTICUS can handle date and time data in a variety of
formats in addition to numeric and alphanumeric data. It is suitable for
on-demand plotting, CGI, etc. It accepts ASCII or comma-spearated (.csv)
files and can output to GIF, PNG, SVG, JPEG, WBMP, PostScript, EPS, or
interactively via X11. Some statistical capabilities such as linear
regression and curve fitting are included.

NOTE: the executable name is: pl

%prep

%setup -q -n pl%{filever}src -a1
%patch0 -p1

# with ming:
#perl -pi -e "s|^NOSWFFLAG.* = -DNOSWF|#NOSWFFLAG = -DNOSWF|g" src/Makefile

%build
cd src
%make	CC="%{__cc} $RPM_OPT_FLAGS" \
	XLIBS="-L%{_prefix}/X11R6/%{_lib} -lX11" \
	XINCLUDEDIR="-I%{_prefix}/X11R6/include" \
	GD18LIBS="-lgd -lpng -lz -ljpeg -lfreetype" \
	GD18H="" \
	GDFREETYPE="-DGDFREETYPE" \
	ZFLAG="-DWZ" \
	PREFABS_DIR=%{_datadir}/%{name} \
	LOCALEOBJ=localef.o \
	LOCALE_FLAG="-DLOCALE" \
	plgd18

# it won't compile...
#    MING="-lming" \
#    MINGH="-I%{_includedir}" \

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{name}
install -m755 src/pl -D $RPM_BUILD_ROOT%{_bindir}/pl
cp prefabs/* $RPM_BUILD_ROOT%{_datadir}/%{name}

install -d %{buildroot}%{_mandir}/man1
#install -d %{buildroot}%{_mandir}/man3

install -m0644 pl%{filever}docs/man/man1/pl.1 %{buildroot}%{_mandir}/man1/
#install -m0644 pl%{sver}docs/man/man3/libploticus.3 %{buildroot}%{_mandir}/man3/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc README pl%{filever}docs/index.html pl%{filever}docs/doc
%{_bindir}/pl
%{_datadir}/%{name}
%{_mandir}/man1/pl.1*
#%{_mandir}/man3/libploticus.3*

