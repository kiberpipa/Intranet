{ }:

with import <nixpkgs> {};

let
  akismet = pythonPackages.buildPythonPackage rec {
      name = "akismet-0.2.0";
  
      propagatedBuildInputs = [  ];
  
      src = fetchurl {
        url = "https://pypi.python.org/packages/source/a/akismet/akismet-0.2.0.tar.gz";
        md5 = "bd4b471d88aadad00a6fd70dea97e718";
      };
  
      meta = with stdenv.lib; {
        description = "`Akismet <http://www.akismet.com>`_ is a web service for recognising spam";
        homepage = http://www.voidspace.org.uk/python/modules.shtml;
      };
    };
  
  django-coverage = pythonPackages.buildPythonPackage rec {
    name = "django-coverage-1.2.4";
  
    propagatedBuildInputs = [ pythonPackages.coverage ];
  
    src = fetchurl {
      url = "https://pypi.python.org/packages/source/d/django-coverage/django-coverage-1.2.4.tar.gz";
      md5 = "20c853910783e56e544775c61cf64ef6";
    };
  
    meta = with stdenv.lib; {
      description = "A test coverage reporting tool that utilizes Ned Batchelder's excellent coverage.py to show how much of your code is exercised with your tests";
      homepage = https://bitbucket.org/kmike/django-coverage/;
      license = licenses.asl2;
    };
  };
  
  django-reversion = pythonPackages.buildPythonPackage rec {
    name = "django-reversion-1.8.0";

    propagatedBuildInputs = [  ];

    src = fetchurl {
      url = "https://pypi.python.org/packages/source/d/django-reversion/django-reversion-1.8.0.tar.gz";
      md5 = "8238f97228f2d97c8580f3be3694b1fe";
    };

    meta = {
      description = "UNKNOWN";
      homepage = http://github.com/etianen/django-reversion;
      #license = unknown;
    };
  };
  
  django-honeypot = pythonPackages.buildPythonPackage rec {
    name = "django-honeypot-0.4.0";

    propagatedBuildInputs = [ pythonPackages.setuptools pythonPackages.six ];

    src = fetchgit {
      url = "https://github.com/iElectric/django-honeypot.git";
      rev = "99e423e7f2687bf10156d8fe1c948971d94d7ff5";
      sha256 = "0dfjwbqd4jfb48dbsl4ca5rvakfby2pr45rd41wrdygcw2c8glpx";
    };

    meta = with stdenv.lib; {
      description = "";
      homepage = http://github.com/sunlightlabs/django-honeypot/;
      #license = unknown;
    };
  };
  
  django-haystack = pythonPackages.buildPythonPackage rec {
    name = "django-haystack-2.1.0";

    propagatedBuildInputs = [  ];

    src = fetchurl {
      url = "https://pypi.python.org/packages/source/d/django-haystack/django-haystack-2.1.0.tar.gz";
      md5 = "0bc74c0d71c30169ddb796c20655fe98";
    };

    meta = with stdenv.lib; {
      homepage = http://haystacksearch.org/;
    };
  };
  
  icalendar = pythonPackages.buildPythonPackage rec {
    name = "icalendar-3.6.2";

    propagatedBuildInputs = [ pythonPackages.setuptools pythonPackages.dateutil pythonPackages.pytz ];

    src = fetchurl {
      url = "https://pypi.python.org/packages/source/i/icalendar/icalendar-3.6.2.zip";
      md5 = "e815c0bbef1097713555925235af0630";
    };

    meta = with stdenv.lib; {
      homepage = https://github.com/collective/icalendar;
    };
  };
  
  py-bcrypt = pythonPackages.buildPythonPackage rec {
    name = "py-bcrypt-0.4";

    propagatedBuildInputs = [  ];

    src = fetchurl {
      url = "https://pypi.python.org/packages/source/p/py-bcrypt/py-bcrypt-0.4.tar.gz";
      md5 = "dd8b367d6b716a2ea2e72392525f4e36";
    };

    meta = with stdenv.lib; {
      description = "py-bcrypt is an implementation the OpenBSD Blowfish password hashing";
      homepage = https://code.google.com/p/py-bcrypt;
    };
  };


  passlib = pythonPackages.buildPythonPackage rec {
    name = "passlib-1.6.2";

    propagatedBuildInputs = with pythonPackages; [ nose py-bcrypt ];

    src = fetchurl {
      url = "https://pypi.python.org/packages/source/p/passlib/passlib-1.6.2.tar.gz";
      md5 = "2f872ae7c72ca338634c618f2cff5863";
    };

    meta = with stdenv.lib; {
      description = "Passlib is a password hashing library for Python 2 & 3, which provides";
      homepage = http://passlib.googlecode.com;
    };
  };
  
  flickrapi = pythonPackages.buildPythonPackage rec {
    name = "flickrapi-1.4.2";

    propagatedBuildInputs = [  ];

    src = fetchurl {
      url = "https://pypi.python.org/packages/source/f/flickrapi/flickrapi-1.4.2.zip";
      md5 = "90dca08a45968b18da0894887f3e59b3";
    };
    
    preBuild = ''
      sed -i '/use_setuptools/d' setup.py
    '';
    
    # tests require networking
    doCheck = false;

    meta = with stdenv.lib; {
      description = "The easiest to use, most complete, and most actively developed Python interface to the Flickr API.It includes support for authorized and non-authorized access, uploading and replacing photos, and all Flickr API functions";
      homepage = http://stuvel.eu/projects/flickrapi;
    };
  };
  
  pysolr = pythonPackages.buildPythonPackage rec {
    name = "pysolr-3.2.0";

    propagatedBuildInputs = [ pythonPackages.requests2 ];

    src = fetchurl {
      url = "https://pypi.python.org/packages/source/p/pysolr/pysolr-3.2.0.tar.gz";
      md5 = "abed75a1a61edc42714b37f13b231453";
    };
  
    meta = with stdenv.lib; {
      homepage = http://github.com/toastdriven/pysolr/;
    };
  };
  
  html2text = pythonPackages.buildPythonPackage rec {
    name = "html2text-2014.4.5";

    propagatedBuildInputs = [  ];

    src = fetchurl {
      url = "https://pypi.python.org/packages/source/h/html2text/html2text-2014.4.5.tar.gz";
      md5 = "24ebaaea74c03d331ded5445c8c1b763";
    };

    meta = with stdenv.lib; {
      homepage = https://github.com/Alir3z4/html2text/;
    };
  };

  django-chosen = pythonPackages.buildPythonPackage rec {
    name = "django-chosen-0.1";

    propagatedBuildInputs = [  ];

    src = fetchurl {
      url = "https://pypi.python.org/packages/source/d/django-chosen/django-chosen-0.1.tar.gz";
      md5 = "83130171a8573c5b711c3fa45a9b67ba";
    };

    meta = with stdenv.lib; {
      homepage = https://github.com/theatlantic/django-chosen;
    };
  };

  django-gravatar2 = pythonPackages.buildPythonPackage rec {
    name = "django-gravatar2-1.1.4";

    propagatedBuildInputs = [  ];

    src = fetchurl {
      url = "https://pypi.python.org/packages/source/d/django-gravatar2/django-gravatar2-1.1.4.tar.gz";
      md5 = "487e4fc3da0d7bd3904744ef4fd40773";
    };

    meta = with stdenv.lib; {
      homepage = https://github.com/twaddington/django-gravatar;
    };
  };

  django-grappelli = pythonPackages.buildPythonPackage rec {
    name = "django-grappelli-2.5.2";

    propagatedBuildInputs = [  ];

    src = fetchurl {
      url = "https://pypi.python.org/packages/source/d/django-grappelli/django-grappelli-2.5.2.tar.gz";
      md5 = "dd1d57f2958fbcaee1da0f5d72b6c639";
    };

    meta = with stdenv.lib; {
      homepage = http://django-grappelli.readthedocs.org;
    };
  };
  
  South = pythonPackages.buildPythonPackage rec {
    name = "South-0.8.4";

    propagatedBuildInputs = [  ];

    src = fetchurl {
      url = "https://pypi.python.org/packages/source/S/South/South-0.8.4.tar.gz";
      md5 = "ccd6ebadd3e2c8c6ef16d771632f7840";
    };

    meta = with stdenv.lib; {
      description = "South is an intelligent database migrations library for the Django web framework. It is database-independent and DVCS-friendly, as well as a whole host of other features";
      homepage = http://south.aeracode.org/;
    };
  };
 
  django-tinymce = pythonPackages.buildPythonPackage rec {
    name = "django-tinymce-1.5.2";

    propagatedBuildInputs = [  ];

    src = fetchurl {
      url = "https://pypi.python.org/packages/source/d/django-tinymce/django-tinymce-1.5.2.tar.gz";
      md5 = "f7d0118f801673734d232274c4fe17d0";
    };

    meta = with stdenv.lib; {
      description = "django-tinymce";
      homepage = https://github.com/aljosa/django-tinymce;
    };
  };
  
  django-akismet-comments = pythonPackages.buildPythonPackage rec {
    name = "django-akismet-comments-0.1";

    propagatedBuildInputs = with pythonPackages; [ setuptools akismet ];

    src = fetchurl {
      url = "https://pypi.python.org/packages/source/d/django-akismet-comments/django-akismet-comments-0.1.zip";
      md5 = "c43898ee4b2c1ab5eed376bfcb287bc6";
    };

    meta = with stdenv.lib; {
      description = "Django moderator for checking django.contrib.comments spam against akismet service";
    };
  };

  django-activelink = pythonPackages.buildPythonPackage rec {
    name = "django-activelink-0.4";

    propagatedBuildInputs = [  ];

    src = fetchurl {
      url = "https://pypi.python.org/packages/source/d/django-activelink/django-activelink-0.4.tar.gz";
      md5 = "287b53d2e69bf7ddb2001edc22c21d67";
    };

    meta = with stdenv.lib; {
      homepage = http://github.com/j4mie/django-activelink/;
    };
  };
  
  Feedjack = pythonPackages.buildPythonPackage rec {
    name = "Feedjack-0.9.20";

    propagatedBuildInputs = with pythonPackages; [ feedparser django_1_6 ];

    src = fetchurl {
      url = "https://pypi.python.org/packages/source/F/Feedjack/Feedjack-0.9.20.tar.gz";
      md5 = "30f32fef946171bf0536aec7dca7eb22";
    };

    meta = with stdenv.lib; {
      homepage = http://www.feedjack.org/;
    };
  };
  
  django-mailman = pythonPackages.buildPythonPackage rec {
    name = "django-mailman-0.4";

    propagatedBuildInputs = [  ];

    src = fetchurl {
      url = "https://pypi.python.org/packages/source/d/django-mailman/django-mailman-0.4.tar.gz";
      md5 = "9a9855c3e6811633c9f8821dafe68374";
    };

    meta = with stdenv.lib; {
      description = "django-mailman is a simple way to manage one or more mailman mailing lists which are not installed on your server";
      homepage = https://bitbucket.org/albertoconnor/django-mailman;
    };
  };

  python-twitter = pythonPackages.buildPythonPackage rec {
    name = "python-twitter-1.3.1";

    propagatedBuildInputs = with pythonPackages; [ setuptools simplejson requests requests_oauthlib ];

    src = fetchurl {
      url = "https://pypi.python.org/packages/source/p/python-twitter/python-twitter-1.3.1.tar.gz";
      md5 = "84a1076388187196b4d83a6a658d722a";
    };
    
    doCheck = false;

    meta = with stdenv.lib; {
      description = "# Python Twitter";
      homepage = https://github.com/bear/python-twitter;
      license = unknown;
    };
  };
  
  django-debug-toolbar = pythonPackages.buildPythonPackage rec {
    name = "django-debug-toolbar-1.0.1";

    propagatedBuildInputs = with pythonPackages; [ sqlparse django_1_6 ];

    src = fetchurl {
      url = "https://pypi.python.org/packages/source/d/django-debug-toolbar/django-debug-toolbar-1.0.1.tar.gz";
      md5 = "ef346e11ad80d25469110ee9dbdf92c2";
    };

    meta = with stdenv.lib; {
      homepage = https://github.com/django-debug-toolbar/django-debug-toolbar;
    };
  };

  sqlparse = pythonPackages.buildPythonPackage rec {
    name = "sqlparse-0.1.11";

    propagatedBuildInputs = with pythonPackages; [  ];

    src = fetchurl {
      url = "https://pypi.python.org/packages/source/s/sqlparse/sqlparse-0.1.11.tar.gz";
      md5 = "abc3315f4970e7ff0f6758d693dc8a45";
    };

    meta = with stdenv.lib; {
      description = "``sqlparse`` is a non-validating SQL parser module";
      homepage = https://github.com/andialbrecht/sqlparse;
    };
  };


in buildPythonPackage rec {
  name = "kiberpipa-intranet";

  src = ./.;
  
  # TODO: systemd for gunicorn
  # TODO: staging, production
  # TODO: configure solr
  # TODO: remove dependency on SOLR for development

  propagatedBuildInputs = with python27Packages; [
    pytz
    pysolr
    passlib
    html2text
    django_1_6
    beautifulsoup
    python-twitter
    pillow
    psycopg2
    requests
    pygments
    ldap
    dateutil
    gunicorn
    raven
    nose
    bpython
    icalendar
    Feedjack
    django_tagging
    django-gravatar2
    django-activelink
    django-grappelli
    django-chosen
    django-tinymce
    django-debug-toolbar
    django-mailman
    django-reversion
    django-honeypot
    django-akismet-comments
    django-haystack
    South
    flickrapi
    python.modules.sqlite3
  ];
  
  shellHook = ''
    mkdir -p /tmp/$name/lib/${python.libPrefix}/site-packages
    export PATH="/tmp/$name/bin:$PATH"
    export PYTHONPATH="/tmp/$name/lib/${python.libPrefix}/site-packages:$PYTHONPATH"
    python setup.py develop --prefix /tmp/$name
  '';
  
  # maybe enable it with sqlite3
  doCheck = false;
  
  DJANGO_SETTINGS_MODULE = "intranet.settings.local";
}
