#!/bin/bash

VERSION_LEVEL=$1

if [ -z "$VERSION_LEVEL" ]; then
    echo "Usage: $0 <VERSION_LEVEL>"
    echo "  VERSION_LEVEL: The level of the version to bump. One of: patch, minor, major"
    exit 1
fi

# Bump the version and save poetry output to string
ret=$(poetry version $VERSION_LEVEL)
echo $ret
FROM=$(echo $ret | awk '{ print $4; }')
TO=$(echo $ret | awk '{ print $6; }')

# commit the changes
git add pyproject.toml
git commit -m "Increment version from $FROM to $TO"

# create a tag
git tag -a "v$TO" -m "Version $TO"

echo "Bump to version $TO complete. Remember to run 'git push' and 'git push --tags' to push the changes."
