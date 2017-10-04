#!/usr/bin/env bash

# bump semver of module

set -e
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo 'bump to new version'

version=`cat ${DIR}/../version.txt`
versions=`git tag --list`

echo 'current version' ${version}

#increase patch

target_version=$1

version_array=( ${version//./ } )
major_version=${version_array[0]}
minor_version=${version_array[1]}
patch_version=${version_array[2]}

# major, minor, patch
case ${target_version} in
    major)
    new_major_version=$((major_version + 1))
    new_minor_version=0
    new_patch_version=0
    echo "major update"
    shift
    ;;
    minor)
    new_major_version=${major_version}
    new_minor_version=$((minor_version + 1))
    new_patch_version=0
    echo "minor update"
    shift
    ;;
    *)
    new_major_version=${major_version}
    new_minor_version=${minor_version}
    new_patch_version=$((patch_version + 1))
    target_version=patch
    echo "patch"
    ;;
esac

next_version="${new_major_version}.${new_minor_version}.${new_patch_version}"

echo "next version ${next_version}"

echo ${next_version} > ${DIR}/../version.txt
echo 'updated version.txt'


if [[ ${versions} == *${next_version}* ]]; then
   echo 'already has this version'
   exit 1
fi

# TODO: update CHANGELOG
# github_changelog_generator

# don't need to deploy yet
# ${DIR}/deploy.sh

git commit -am "bump to ${next_version}"
git tag ${next_version}
git push
git push --tag
