./build-catalog.sh
cp gamelist.pdf ~/perso/felleg.gitlab.io/static/files
cd ~/perso/felleg.gitlab.io
git add static/files/gamelist.pdf
git commit -m "update gamelist.pdf"
git push origin master
