SHELL=/bin/bash

all: develop

nix:
	@type nix-shell 2>/dev/null || [[ -e ~/.nix-profile/etc/profile.d/nix.sh ]] || curl -L https://nixos.org/nix/install | bash

develop: nix
	./.with-nix.sh --command 'eval "$$shellHook"' 

test:
	@django-admin.py test intranet.org intranet.www
