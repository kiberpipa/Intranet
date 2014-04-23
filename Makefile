SHELL=bash

all: develop

nix:
	@type nix-shell 2>/dev/null || [[ -e ~/.nix-profile/etc/profile.d/nix.sh ]] || curl -L https://nixos.org/nix/install | bash

develop: nix
	./.with-nix.sh --command 'return' 

exec: nix
	./.with-nix.sh --command '$(COMMAND);exit' --pure

test: COMMAND=django-admin.py test intranet.org intranet.www
test: nix exec
