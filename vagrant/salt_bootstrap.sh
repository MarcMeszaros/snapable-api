#!/bin/bash

echo ""
echo "+----------------+"
echo "| Bootstrap Salt |"
echo "+----------------+"
echo ""
salt-key -A -y
echo 'Updating the sls files...'
salt-run fileserver.update
echo 'Running salt.highstate... (may take several minutes)'
salt '*' state.highstate