PWD=`pwd`
cd ..
tar -cvzf $HOME/nextcloud/mediadc.tar.gz \
   mediadc/appinfo             mediadc/css            mediadc/main.py   mediadc/pyproject.toml \
    mediadc/stylelint.config.js \
    mediadc/babel.config.js     mediadc/img            mediadc/Makefile  mediadc/python \
    mediadc/templates mediadc/CHANGELOG.md      mediadc/krankerl.toml \
    mediadc/README.md     \
    mediadc/CODE_OF_CONDUCT.md  mediadc/l10n    mediadc/package.json   mediadc/requirements.txt \
    mediadc/vendor  mediadc/composer.json   mediadc/lib    mediadc/package-lock.json  mediadc/screenshots \
    mediadc/webpack.config.js mediadc/composer.lock       mediadc/LICENSE  mediadc/psalm.xml \
    mediadc/src mediadc/js


ls -lh mediadc.tar.gz

rsync mediadc.tar.gz -avz root@download.svc.bring.out.ba:/data/download/nextcloud/mediadc.tar.gz

cd $PWD
