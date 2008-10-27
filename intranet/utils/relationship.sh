echo 'from intranet.photologue.models import Gallery'
for i in */album.dat; do
#for i in aktivizem/album.dat; do
    parent=`tr -d '\r' < $i | tr -d '\n' | ssed -R 's/.*parentAlbumName.*?:"(.*?)".*/\1/'` 
    me="${i%/*}"
    if [[ $parent == 'clicks' ]]; then
        printf "me = Gallery.objects.get(album_name='$me')\nme.parent = None\nme.save()\n"
    else
        printf "me = Gallery.objects.get(album_name='$me')\nme.parent = Gallery.objects.get(album_name='$parent')\nme.save()\n"
    fi
done
