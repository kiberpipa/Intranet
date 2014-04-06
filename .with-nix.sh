#!/bin/bash
source ~/.nix-profile/etc/profile.d/nix.sh 2>/dev/null
exec nix-shell "$@"
