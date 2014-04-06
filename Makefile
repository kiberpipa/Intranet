all: develop


nix:
	@type nix-shell >/dev/null || curl -L https://nixos.org/nix/install | bash
	@type nix-shell >/dev/null || source ~/.nix-profile/etc/profile.d/nix.sh

develop: nix
	@nix-shell --command 'eval "$$shellHook"' 

test:
	@django-admin.py test intranet.org intranet.www
