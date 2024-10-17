%define upstream_version %(echo %{version} | sed -e 's/\\.//g')
%define docs_version 2.4.1
%define docs_upstream_version %(echo %{docs_version} | sed -e 's/\\.//g')

Summary: 	Graph/plot generator
Name: 		ploticus
Version: 	2.42
Release: 	1
License: 	GPLv2
Group: 		Publishing
URL: 		https://ploticus.sourceforge.net/
#http://downloads.sourceforge.net/ploticus/2.4.2/ploticus242_src.tar.gz
#http://downloads.sourceforge.net/ploticus/2.4.1/pl241docs.tar.gz
Source0:	http://downloads.sourceforge.net/ploticus/%{version}/ploticus%{upstream_version}_src.tar.gz
Source1:	http://downloads.sourceforge.net/ploticus/%{docs_version}/pl%{docs_upstream_version}docs.tar.gz
Requires: 	gd-utils 
BuildRequires:	gd-devel pkgconfig(zlib)
Conflicts:	swi-prolog

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
%setup -q -n ploticus%{upstream_version} -a1

%build
cd src
%make	CC="%{__cc} %{optflags} %ldflags" \
	XLIBS="-L%{_libdir} -lX11" \
	XINCLUDEDIR="-I%{_includedir}" \
	GD18LIBS="-lgd" \
	GD18H="" \
	GDFREETYPE="-DGDFREETYPE" \
	ZFLAG="" \
	PREFABS_DIR=%{_datadir}/%{name} \
	LOCALEOBJ=localef.o \
	LOCALE_FLAG="-DLOCALE" \
	plgd18 -lz

%install
mkdir -p %{buildroot}%{_datadir}/%{name}
install -m755 src/pl -D %{buildroot}%{_bindir}/pl
cp prefabs/* %{buildroot}%{_datadir}/%{name}

install -d %{buildroot}%{_mandir}/man1

install -m0644 pl%{docs_upstream_version}docs/man/man1/pl.1 %{buildroot}%{_mandir}/man1/

%clean

%files
%doc pl%{docs_upstream_version}docs/index.html pl%{docs_upstream_version}docs/doc
%{_bindir}/pl
%{_datadir}/%{name}
%{_mandir}/man1/pl.1*
#%{_mandir}/man3/libploticus.3*

