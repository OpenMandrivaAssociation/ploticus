%define name 	ploticus
%define version 2.33
%define upstream_version %(echo %{version} | sed -e 's/\\.//g')
%define release %mkrel 3

Summary: 	Graph/plot generator
Name: 		%{name}
Version: 	%{version}
Release: 	%{release}
License: 	GPL
Group: 		Publishing
URL: 		http://ploticus.sourceforge.net/
Source0:	http://ploticus.sourceforge.net/download/pl%{upstream_version}src.tar.gz
Source1:	http://ploticus.sourceforge.net/download/pl%{upstream_version}docs.tar.gz
Patch0:		ploticus-2.33-gd20gif.patch
Requires: 	gd-utils
BuildRequires:	X11-devel
BuildRequires:	freetype-devel
BuildRequires:	gd-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	zlib-devel
Conflicts:	swi-prolog
BuildRoot: 	%{_tmppath}/%{name}-%{version}

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
%setup -q -n pl%{upstream_version}src -a1
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
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_datadir}/%{name}
install -m755 src/pl -D %{buildroot}%{_bindir}/pl
cp prefabs/* %{buildroot}%{_datadir}/%{name}

install -d %{buildroot}%{_mandir}/man1
#install -d %{buildroot}%{_mandir}/man3

install -m0644 pl%{upstream_version}docs/man/man1/pl.1 %{buildroot}%{_mandir}/man1/
#install -m0644 pl%{sver}docs/man/man3/libploticus.3 %{buildroot}%{_mandir}/man3/

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README pl%{upstream_version}docs/index.html pl%{upstream_version}docs/doc
%{_bindir}/pl
%{_datadir}/%{name}
%{_mandir}/man1/pl.1*
#%{_mandir}/man3/libploticus.3*

