git add .
git update-index --chmod=+x actions/release-checker/entrypoint.sh
git commit -m "Created Release Checker Action v1"
git tag -a -m "Release Checker Action First Release" rc-v1
git push --follow-tags